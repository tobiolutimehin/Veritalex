#!/usr/bin/env python3
"""Build the dependency-free Veritalex design package from screens.json.

Run from any directory: python3 .stitch/scripts/build_package.py [--check]
No Android files, network requests, browser state or real account data are touched.
"""
from __future__ import annotations

import argparse
import base64
import html
import json
import re
import subprocess
from collections import Counter, deque
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "screens.json").read_text())
SCREENS = {s["id"]: s for s in MANIFEST["screens"]}
NUMBER = {key: index + 1 for index, key in enumerate(SCREENS)}
CATALOGUE = MANIFEST["catalogue"]


def esc(value):
    return html.escape(str(value), quote=True)


def payload(value):
    # JSON is data inside a script element; prevent an embedded closing tag.
    return json.dumps(value, ensure_ascii=False).replace("<", "\\u003c")


PATHS = {
    "back": '<path d="m15 18-6-6 6-6M9 12h12"/>',
    "chevron": '<path d="m9 6 6 6-6 6"/>',
    "home": '<path d="m3 10 9-7 9 7v11h-6v-7H9v7H3Z"/>',
    "book": '<path d="M3 4h7l2 2 2-2h7v16h-7l-2 2-2-2H3ZM12 6v16"/>',
    "explore": '<circle cx="12" cy="12" r="9"/><path d="m16 8-2 6-6 2 2-6Z"/>',
    "library": '<path d="M3 4h4v17H3ZM10 4h4v17h-4ZM16 5l4-1 4 16-4 1Z"/>',
    "settings": '<path d="m9 3-.6 3-2 .9-2.7-1.1-3 5.2 2.4 1.9v2.2L.7 17l3 5.2L6.4 21l2 .9L9 25h6l.6-3.1 2-.9 2.7 1.2 3-5.2-2.4-1.9v-2.2l2.4-1.9-3-5.2-2.7 1.1-2-.9L15 3Z" transform="translate(2 -2) scale(.85)"/><circle cx="12" cy="12" r="3"/>',
    "search": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
    "close": '<path d="m6 6 12 12M6 18 18 6"/>',
    "check": '<path d="m5 12 4 4L20 5"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "filter": '<path d="M3 6h18M6 12h12M9 18h6"/>',
    "more": '<circle cx="5" cy="12" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/>',
    "download": '<path d="M12 3v12m-5-5 5 5 5-5M4 16v5h16v-5"/>',
    "cloud-off": '<path d="m3 3 18 18M5 16a5 5 0 0 1 1-10m4-1a6 6 0 0 1 10 4 4 4 0 0 1 0 8H9"/>',
    "sync": '<path d="M3 11a9 9 0 0 1 16-5l2 3M21 3v6h-6M21 13a9 9 0 0 1-16 5l-2-3M3 21v-6h6"/>',
    "device": '<rect x="6" y="2" width="12" height="20" rx="2"/><path d="M10 18h4"/>',
    "warning": '<path d="m12 3 10 18H2ZM12 9v5m0 3h.01"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v6m0-10h.01"/>',
    "journal": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 7h8M8 11h8M8 15h5"/>',
    "shelf": '<path d="M3 20h18M4 4h4v13H4ZM10 4h4v13h-4ZM16 5l3-1 3 12-3 1Z"/>',
    "star": '<path d="m12 3 3 6 7 1-5 5 1 7-6-3-6 3 1-7-5-5 7-1Z"/>',
    "delete": '<path d="M3 6h18M9 6V3h6v3M6 6l1 15h10l1-15M10 10v7m4-7v7"/>',
    "edit": '<path d="m16 3 5 5-12 12-6 1 1-6ZM13 6l5 5"/>',
    "person": '<circle cx="12" cy="7" r="4"/><path d="M4 21v-2a8 8 0 0 1 16 0v2"/>',
    "logout": '<path d="M9 3H3v18h6M9 12h13m-5-5 5 5-5 5"/>',
    "appearance": '<circle cx="12" cy="12" r="9"/><path d="M12 3v18"/>',
    "text": '<path d="M3 5h18M12 5v16M8 21h8"/>',
    "bookmark": '<path d="M6 3h12v19l-6-4-6 4Z"/>',
}


def icon(name, cls=""):
    return f'<svg class="icon {esc(cls)}" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{PATHS.get(name, PATHS["chevron"])}</svg>'


APP_CSS = """
*{box-sizing:border-box}html{color-scheme:light}body{margin:0;font-family:Arial,Helvetica,sans-serif;color:#242424;background:#ececec}a{color:inherit}button,input,textarea,select{font:inherit}button,a,input,textarea,select{-webkit-tap-highlight-color:transparent}button,a{touch-action:manipulation}a:focus-visible,button:focus-visible,input:focus-visible,textarea:focus-visible,select:focus-visible{outline:3px solid #111;outline-offset:3px}button{cursor:pointer}a{text-decoration:none}.icon{width:24px;height:24px;flex:none;vertical-align:middle}.phone{--paper:#fff;--panel:#eee;--tonal:#e3e3e3;--ink:#222;--muted:#5b5b5b;--line:#c3c3c3;--accent:#333;--onaccent:#fff;position:relative;background:var(--paper);color:var(--ink);width:412px;height:915px;border:1px solid #888;border-radius:24px;overflow:hidden;flex:none;display:flex;flex-direction:column;box-shadow:0 4px 14px #0000000d}.statusbar{height:32px;flex:none;padding:8px 20px 0;display:flex;justify-content:space-between;font-size:12px;font-weight:600;letter-spacing:.02em}.status-icons{display:flex;gap:5px;align-items:center}.status-icons svg{width:13px;height:13px}.topbar{min-height:64px;display:flex;align-items:center;padding:4px 12px;gap:4px;flex:none}.topbar h1{font-size:24px;line-height:32px;font-weight:500;margin:0;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.topbar .small-title{font-size:19px}.topbar.no-back h1{padding-left:8px}.iconbutton{width:48px;height:48px;display:inline-flex;align-items:center;justify-content:center;border:0;border-radius:50%;background:transparent;color:inherit;flex:none}.app-main{padding:4px 20px 24px;flex:1;min-height:0;overflow:auto;scrollbar-width:thin;display:flex;flex-direction:column;gap:16px;overscroll-behavior:contain}.app-main>*{flex:none}.app-main h2,.app-main h3,.dialog-body h2{font-size:20px;line-height:28px;font-weight:500;margin:0 0 6px}.app-main p,.dialog-body p{font-size:15px;line-height:23px;margin:0;color:var(--muted);white-space:pre-line}.text-block{padding:2px 0}.text-block:empty{display:none}.brand{padding:30px 0 18px;text-align:center}.brand .brand-mark{display:inline-flex;border:1.5px solid var(--ink);border-radius:17px;padding:14px;margin-bottom:14px}.brand .brand-mark .icon{width:40px;height:40px}.brand strong{display:block;font-size:25px;line-height:32px;font-weight:500}.brand span{font-size:14px;color:var(--muted)}.button{min-height:48px;padding:12px 20px;border-radius:28px;display:flex;align-items:center;justify-content:center;gap:8px;border:1px solid transparent;font-size:14px;font-weight:600;text-align:center;background:var(--accent);color:var(--onaccent);width:100%;line-height:22px}.button.tonal{background:var(--tonal);color:var(--ink)}.button.text{background:transparent;color:var(--ink)}.button:hover,.row-link:hover,.iconbutton:hover{filter:brightness(.95)}.button:active{transform:translateY(1px)}.notice{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px 16px}.notice strong{display:block;font-size:14px;line-height:20px;margin-bottom:3px;font-weight:600}.notice p{font-size:14px;line-height:20px}.notice.error{border-style:dashed;border-color:var(--ink)}.empty{text-align:center;padding:30px 8px 20px}.empty>.icon{width:44px;height:44px;margin-bottom:18px}.empty h2{font-size:22px;line-height:30px;margin:0 0 10px}.empty p{max-width:320px;margin:auto}.row,.row-link{display:flex;align-items:center;gap:14px;min-height:60px;padding:10px 0;border-bottom:1px solid var(--line);width:100%;background:transparent}.row .rowcopy,.row-link .rowcopy{flex:1;min-width:0}.row strong,.row-link strong{display:block;font-size:16px;line-height:24px;font-weight:500}.row small,.row-link small{display:block;color:var(--muted);font-size:14px;line-height:20px;margin-top:2px}.row .leading,.row-link .leading{color:var(--muted)}.row-link>.trailing{width:20px}.book{display:flex;align-items:center;gap:16px;min-width:0}.book.large{flex-direction:column;text-align:center;gap:16px;padding:10px 0 8px}.cover{width:70px;aspect-ratio:2/3;border:1px solid #969696;border-radius:3px;background:#e3e3e3;color:#333;display:flex;flex-direction:column;align-items:center;justify-content:space-between;text-align:center;padding:12px 5px;flex:none;box-shadow:inset 4px 0 #00000012}.cover-title{font-size:10px;line-height:13px;font-weight:600;max-width:100%;overflow-wrap:anywhere}.cover-author{font-size:8px;line-height:10px}.cover-rule{height:1px;background:currentColor;width:28px;opacity:.6}.book-copy{min-width:0}.book-copy h2{font-size:17px;line-height:24px;margin:0 0 3px}.book-copy p{font-size:14px;line-height:20px}.book-copy small{display:block;font-size:13px;line-height:20px;margin-top:7px;color:var(--muted)}.book.large .cover{width:112px;padding:20px 9px}.book.large .cover-title{font-size:15px;line-height:19px}.book.large .cover-author{font-size:10px;line-height:14px}.book.large .book-copy h2{font-size:23px;line-height:30px}.book-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px 16px}.grid-book{display:flex;flex-direction:column;align-items:flex-start;min-width:0}.grid-book .cover{width:100%;max-width:122px;padding:21px 10px;align-self:center}.grid-book .cover-title{font-size:14px;line-height:18px}.grid-book .cover-author{font-size:10px;line-height:13px}.grid-book h3{font-size:15px;line-height:21px;margin:10px 0 2px;font-weight:500}.grid-book p{font-size:13px;line-height:18px}.chips{display:flex;flex-wrap:wrap;gap:8px}.chip{display:inline-flex;min-height:36px;align-items:center;padding:6px 12px;border:1px solid var(--line);border-radius:9px;font-size:13px;line-height:20px;background:transparent;color:var(--ink)}button.chip{cursor:pointer}.chip.selected{background:var(--tonal);border-color:var(--tonal);font-weight:600}.chip.selected:before{content:'✓';padding-right:6px}.tabs{display:flex;position:sticky;top:-4px;z-index:1;background:var(--paper);margin:0 -20px;padding:0 16px;border-bottom:1px solid var(--line)}.tab{flex:1;text-align:center;min-height:48px;font-size:14px;padding:14px 4px;position:relative}.tab.selected{font-weight:600}.tab.selected:after{content:'';position:absolute;bottom:0;left:25%;width:50%;height:3px;background:var(--accent);border-radius:4px 4px 0 0}.bottomnav{min-height:80px;display:flex;justify-content:space-around;padding:8px 8px 5px;background:var(--panel);flex:none;border-top:1px solid var(--line)}.navitem{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;min-width:80px;font-size:12px;line-height:18px}.navitem>span{display:flex;align-items:center;justify-content:center;width:64px;height:32px;border-radius:20px}.navitem.selected>span{background:var(--tonal)}.navitem.selected{font-weight:600}.gesture{height:24px;flex:none;display:flex;justify-content:center;align-items:center;background:var(--paper)}.gesture:after{content:'';display:block;width:108px;height:4px;border-radius:4px;background:var(--ink)}.phone:has(.bottomnav) .gesture{background:var(--panel)}.search{display:flex;align-items:center;gap:12px;border-radius:28px;padding:14px 16px;min-height:56px;background:var(--panel);font-size:15px;color:var(--muted)}.subjects{display:grid;grid-template-columns:1fr 1fr;gap:10px}.subject{padding:18px 12px;border:1px solid var(--line);border-radius:12px;font-size:14px;font-weight:500;min-height:58px}.continue{border:1px solid var(--line);border-radius:16px;padding:18px;background:var(--panel);display:flex;flex-direction:column;gap:14px}.continue .eyebrow{font-size:13px;font-weight:600}.progress-copy{display:flex;justify-content:space-between;margin-bottom:8px;gap:8px;font-size:14px;line-height:20px;color:var(--muted)}.progress-track{height:4px;background:var(--tonal);overflow:hidden;border-radius:6px}.progress-track span{display:block;height:100%;background:var(--accent)}.progress-track.indeterminate span{width:40%;margin-left:20%}.progress-wrap{padding:4px 0}.skeleton{display:flex;gap:15px;padding:8px 0}.skeleton-cover{width:60px;height:90px;background:#e1e1e1}.skeleton-lines{flex:1;padding-top:12px}.skeleton-lines i{height:10px;background:#e4e4e4;display:block;margin:0 0 14px}.skeleton-lines i:nth-child(2){width:65%}.field{display:flex;flex-direction:column;gap:7px}.field label{font-size:13px;line-height:18px;font-weight:600}.field input,.field textarea{width:100%;min-height:56px;padding:15px;border:1px solid var(--line);border-radius:5px;background:var(--paper);color:var(--ink);font-size:16px;line-height:24px}.field textarea{height:148px;resize:vertical}.field .field-error{font-size:13px;line-height:18px;color:var(--ink);font-weight:600}.field.invalid input{border:2px dashed var(--ink)}.choice-group{display:flex;flex-direction:column;gap:4px;border:0;padding:0;margin:0}.choice{min-height:48px;display:flex;align-items:center;gap:13px;font-size:15px;line-height:22px}.choice input{appearance:auto;width:20px;height:20px;accent-color:var(--accent);margin:0;flex:none}.slider{display:flex;flex-direction:column;gap:10px;font-size:14px;line-height:20px;padding:4px 0}.slider input{width:100%;min-height:28px;accent-color:var(--accent)}.rating{display:flex;justify-content:space-between;gap:3px;padding:16px 0}.rating button{background:transparent;border:0;padding:9px;color:var(--muted);border-radius:50%}.rating .icon{width:32px;height:32px}.rating .rated .icon{fill:var(--tonal);color:var(--ink)}.entry{border-bottom:1px solid var(--line);padding:6px 0 18px}.entry h2{font-size:19px;line-height:26px}.entry .entry-meta{font-size:13px;line-height:20px;margin-bottom:12px}.quote{border-left:3px solid var(--accent);padding:10px 0 10px 16px;margin:4px 0}.quote p{font-family:Georgia,serif;font-size:19px;line-height:29px;color:var(--ink)}.quote small{font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:18px;color:var(--muted);display:block;margin-top:8px}.quote a{font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:24px;text-decoration:underline;display:inline-block;margin-top:10px}.reader-content{font-family:Georgia,'Times New Roman',serif;font-size:19px;line-height:32px;padding:8px 0}.reader-content h2{font-family:Georgia,serif;font-size:26px;line-height:34px;font-weight:400;margin:18px 0 28px}.reader-content p{font-family:inherit;font-size:inherit;line-height:inherit;color:var(--ink);margin:0 0 22px}.reader-content mark{background:var(--tonal);color:inherit;border-radius:2px;padding:2px 0}.reader-actions{display:flex;justify-content:space-around;margin:0 -12px;padding:4px 0;border-bottom:1px solid var(--line)}.reader-position{font-family:Arial,Helvetica,sans-serif;font-size:12px;color:var(--muted);display:flex;justify-content:space-between;gap:10px;margin-top:12px}.reader-tap{display:block}.reader-immersive .topbar{display:none}.reader-immersive .app-main{padding-top:30px}.reader-immersive .reader-content h2{margin-top:24px}.reader-immersive .reader-position{margin-top:20px}.selection-bar{display:flex;gap:4px;justify-content:center;background:var(--panel);border:1px solid var(--line);padding:4px;border-radius:12px}.selection-bar a{padding:10px 12px;font-size:14px;line-height:20px;min-height:44px}.paged-nav{display:flex;justify-content:space-between;gap:12px;margin-top:8px}.paged-nav a{min-height:48px;padding:12px 14px;border:1px solid var(--line);border-radius:24px;font-size:14px}.mini-prose{font-family:Georgia,serif;font-size:19px;line-height:30px;padding:18px;border:1px solid var(--line);border-radius:12px;background:var(--panel)}.app-dialog{position:absolute;inset:auto 16px 25px;margin:0;max-width:none;width:calc(100% - 32px);max-height:calc(100% - 70px);padding:0;border:1px solid var(--line);border-radius:28px;background:var(--paper);color:var(--ink);overflow:auto;z-index:3;box-shadow:0 12px 30px #0002}.app-dialog:modal{position:fixed;left:16px;right:16px;bottom:24px;top:auto;margin:0 auto;width:calc(100% - 32px);max-width:380px;max-height:calc(100dvh - 60px);overscroll-behavior:contain}.app-dialog::backdrop{background:#0005;overflow:hidden;overscroll-behavior:contain}.app-dialog:not(:modal)+.modal-dim{position:absolute;inset:0;background:#0004;z-index:2;pointer-events:none}.dialog-header{display:flex;align-items:center;padding:12px 12px 0 20px;gap:4px}.dialog-header h2{font-size:23px;line-height:31px;font-weight:500;flex:1;margin:0}.dialog-body{padding:16px 24px 24px;display:flex;flex-direction:column;gap:16px}.dialog-handle{width:32px;height:4px;background:var(--line);border-radius:4px;margin:12px auto 0}.modal-background{display:contents}.modal-background .app-main{pointer-events:none}.screen-page{display:grid;grid-template-columns:minmax(0,412px) minmax(250px,400px);gap:36px;justify-content:center;padding:32px;align-items:start}.screen-notes{padding:4px 0 24px}.eyebrow{font-size:12px;line-height:18px;font-weight:600;letter-spacing:.07em;text-transform:uppercase}.screen-notes h1{font-size:28px;line-height:36px;font-weight:500;margin:10px 0}.screen-notes p,.screen-notes li{font-size:14px;line-height:22px;color:#555}.screen-notes ul{padding-left:20px}.screen-notes .note{border-top:1px solid #bbb;padding:14px 0}.transition-list{padding:0;list-style:none;display:flex;flex-direction:column;gap:8px}.transition-list a{display:flex;align-items:flex-start;gap:9px;padding:9px 10px;background:#fff;border:1px solid #c3c3c3;border-radius:7px;font-size:13px;line-height:20px}.transition-number{font-size:11px;border:1px solid #777;border-radius:4px;min-width:26px;text-align:center;line-height:20px;flex:none}.transition-list a small{display:block;color:#666;overflow-wrap:anywhere}.notes-links{display:flex;flex-wrap:wrap;gap:16px;font-size:14px;text-decoration:underline;margin-bottom:24px}.screen-notes .prototype-notice{background:#ddd;border-radius:8px;padding:12px;color:#333}.embed-page{background:#fff}.embed-page .screen-page{display:block;padding:0}.embed-page .screen-notes{display:none}.embed-page .phone{width:100%;max-width:none;height:100dvh;min-height:0;border:0;border-radius:0;box-shadow:none}.styled .phone{--paper:#fff8f3;--panel:#fcf1e8;--tonal:#ffdcbd;--ink:#241a14;--muted:#55483d;--line:#d7c3b4;--accent:#895021;--onaccent:#fff}.styled .cover{background:#e3d3bf;border-color:#ad977e;color:#50381f}.styled .reader-content mark{background:#f6e5a8}.styled .reader-sepia{--paper:#f4e9d4;--panel:#eee0c7}.board-page{padding:40px;background:#eee;min-width:1860px}.board-header{max-width:1776px;margin:0 0 28px;display:flex;align-items:end;justify-content:space-between;gap:40px}.board-header h1{font-size:32px;line-height:40px;font-weight:500;margin:7px 0 8px}.board-header p{font-size:15px;line-height:24px;margin:0;max-width:1150px;color:#555}.board-grid{display:grid;grid-template-columns:repeat(4,412px);gap:36px 32px;align-items:start}.board-frame h2{font-size:18px;line-height:25px;margin:0 0 8px;font-weight:600}.board-frame .stable-id{font-size:12px;line-height:18px;margin:0 0 12px;color:#555}.board-frame .phone{box-shadow:none}.board-frame .board-links{font-size:12px;line-height:19px;margin-top:12px;max-width:412px}.board-links a{display:inline-block;margin:0 8px 5px 0;border:1px solid #aaa;border-radius:4px;padding:2px 6px;background:#fff}.board-frame .board-note{font-size:12px;line-height:18px;color:#555;margin:6px 0 0}.board-footer{font-size:14px;line-height:22px;max-width:1500px;border-top:1px solid #aaa;padding-top:20px;margin-top:36px;color:#555}.board-page .app-dialog{pointer-events:none}.board-page a{pointer-events:none}@media(max-width:760px){.screen-page{display:flex;flex-direction:column;padding:16px;align-items:center;gap:24px}.screen-page .phone{width:min(412px,100%)}.screen-notes{width:min(412px,100%)}.screen-notes h1{font-size:24px}.phone .app-main{padding-left:16px;padding-right:16px}.phone .tabs{margin-left:-16px;margin-right:-16px}.topbar h1{font-size:22px}}@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important;animation:none!important}}
"""


def action(screen, key):
    return next((a for a in screen["transitions"] if a["id"] == key), None)


def link(screen, key, text=None, cls="", *, prefix="", attrs=""):
    a = action(screen, key)
    if not a:
        raise ValueError(f"Missing action {screen['id']}:{key}")
    book = key.removeprefix("book-") if key.startswith("book-") else ""
    query = f"?book={book}" if book else ""
    data_book = f' data-book-id="{esc(book)}"' if book else ""
    return f'<a class="{esc(cls)}" href="{prefix}{esc(a["to"])}.html{query}" data-to="{esc(a["to"])}" data-action="{esc(key)}"{data_book} {attrs}>{text if text is not None else esc(a["label"])}</a>'


def cover(book_id, *, dynamic=False):
    b = CATALOGUE[book_id]
    d = ' data-dynamic-cover="true"' if dynamic else ""
    return f'<div class="cover" role="img" aria-label="Typeset cover: {esc(b["title"])} by {esc(b["author"])}"{d}><span class="cover-rule"></span><span class="cover-title">{esc(b["title"])}</span><span class="cover-author">{esc(b["author"])}</span></div>'


def book_block(b, screen):
    dynamic = (screen["area"] == "Book" or screen["id"] in ("library-actions", "library-rating", "library-remove", "journal-book", "journal-book-empty", "shelf-membership")) and b["book_id"] == "1342"
    attrs = ' data-dynamic-book="true"' if dynamic else ""
    inner = cover(b["book_id"], dynamic=dynamic) + f'<div class="book-copy"{attrs}><h2>{esc(b["title"])}</h2><p>{esc(b["author"])}</p>'
    if b.get("detail"):
        inner += f'<small>{esc(b["detail"])}</small>'
    inner += "</div>"
    cls = "book large" if b.get("large") else "book"
    return link(screen, b["action"], inner, cls) if b.get("action") else f'<section class="{cls}">{inner}</section>'


PROSE = [
    "Till Elizabeth entered the drawing-room at Netherfield, and looked in vain for Mr. Wickham among the cluster of red coats there assembled, a doubt of his being present had never occurred to her.",
    "The two first dances, however, brought a return of distress: they were dances of mortification. Mr. Collins, awkward and solemn, apologizing instead of attending, and often moving wrong without being aware of it, gave her all the shame and misery which a disagreeable partner for a couple of dances can give.",
    "The moment of her release from him was ecstasy.",
]


def reader(b, screen):
    mode = b["mode"]
    out = ""
    if mode != "immersive" and mode not in ("selection",):
        controls = [("contents", "book", "Contents"), ("appearance", "text", "Appearance"), ("search", "search", "Search"), ("journal", "journal", "Journal")]
        out += '<nav class="reader-actions" aria-label="Reading controls">'
        for key, ico, label in controls:
            a = action(screen, key)
            if a:
                content = icon(ico) + f'<span>{label}</span>'
                out += link(screen, key, content, "reader-tool", attrs=f'aria-label="{esc(a["label"])}"')
        out += "</nav>"
    out += '<article class="reader-content"><h2>Chapter 18</h2>'
    if mode in ("selection", "highlight"):
        paras = [f"<p>{esc(PROSE[1])}</p>", f"<p><mark>{esc(PROSE[2])}</mark></p>"]
    else:
        paras = [f"<p>{esc(p)}</p>" for p in PROSE[:2]]
    content = "".join(paras)
    tap = "controls" if mode == "immersive" else "immersive"
    if action(screen, tap):
        out += link(screen, tap, content, "reader-tap", attrs=f'aria-label="{esc(action(screen,tap)["label"])}"')
    else:
        out += content
    out += '</article><div class="reader-position"><span>Chapter 18</span><span>28%</span></div>'
    if mode == "paged":
        out += '<nav class="paged-nav" aria-label="Page navigation">' + link(screen, "previous", "← Previous") + link(screen, "next", "Next →") + "</nav>"
    if action(screen, "select"):
        # Gives keyboard users the same route as a touch text-selection gesture.
        out += link(screen, "select", "Select a passage", "button text")
    return out


def render_block(b, screen, n):
    kind = b["type"]
    if kind == "brand":
        return f'<div class="brand"><span class="brand-mark">{icon("book")}</span><strong>Veritalex</strong><span>A personal place to read</span></div>'
    if kind == "text":
        title, text = b.get("title", ""), b.get("text", "")
        d = ' data-book-about="true"' if title == "About this book" else ""
        return f'<section class="text-block"{d}>' + (f'<h2>{esc(title)}</h2>' if title else "") + (f'<p>{esc(text)}</p>' if text else "") + "</section>"
    if kind == "notice":
        return f'<aside class="notice {esc(b["kind"])}"><strong>{esc(b["title"])}</strong><p>{esc(b["text"])}</p></aside>'
    if kind == "button":
        attrs = 'data-require-selection="true" aria-disabled="true"' if b.get("requires_selection") else ""
        return link(screen, b["action"], cls="button " + b["style"], attrs=attrs)
    if kind == "book":
        return book_block(b, screen)
    if kind == "row":
        ico = b.get("icon", "chevron")
        before = icon(ico, "leading") if ico != "chevron" else ""
        inner = before + f'<span class="rowcopy"><strong>{esc(b["label"])}</strong>' + (f'<small>{esc(b["detail"])}</small>' if b.get("detail") else "") + "</span>"
        inner += icon("chevron", "trailing") if b.get("action") else ""
        return link(screen, b["action"], inner, "row-link") if b.get("action") else f'<div class="row">{inner}</div>'
    if kind == "empty":
        return f'<section class="empty">{icon(b["icon"])}<h2>{esc(b["title"])}</h2><p>{esc(b["text"])}</p></section>'
    if kind == "grid":
        cards = []
        for book_id in b["books"]:
            book = CATALOGUE[book_id]
            content = cover(book_id) + f'<h3>{esc(book["title"])}</h3><p>{esc(book["author"])}</p>'
            cards.append(link(screen, "book-" + book_id, content, "grid-book"))
        return '<section class="book-grid" aria-label="Books">' + "".join(cards) + "</section>"
    if kind == "chips":
        chips = []
        filters = {"All": "filters", "Want to read": "want", "Reading": "reading", "Finished": "finished", "Downloaded": "downloaded"}
        for item in b["items"]:
            cls = "chip" + (" selected" if item == b.get("selected") else "")
            key = filters.get(item) if screen["id"].startswith("library-") and b.get("action") in ("filters", "status") else b.get("action")
            if screen["id"] == "reader-appearance" and item == "Scroll":
                key = "done"
            a = action(screen, key) if key else None
            if a:
                chips.append(link(screen, key, esc(item), cls, attrs='aria-current="true"' if item == b.get("selected") else ""))
            elif b.get("action"):
                chips.append(link(screen, b["action"], esc(item), cls))
            elif screen["area"] == "Book" and not b.get("setting"):
                chips.append(f'<span class="chip">{esc(item)}</span>')
            else:
                chips.append(f'<button type="button" class="{cls}" aria-pressed="{str(item == b.get("selected")).lower()}" data-choice="{n}">{esc(item)}</button>')
        setting = f' data-setting="{esc(b["setting"])}"' if b.get("setting") else ""
        return '<div class="chips" aria-label="Choices"' + setting + '>' + "".join(chips) + "</div>"
    if kind == "tabs":
        return '<nav class="tabs" aria-label="Library sections">' + "".join(link(screen, "tab-" + item.lower(), esc(item), "tab" + (" selected" if item == b["selected"] else ""), attrs='aria-current="page"' if item == b["selected"] else "") for item in b["items"]) + "</nav>"
    if kind == "search":
        return link(screen, b["action"], icon("search") + f'<span>{esc(b.get("value") or b.get("placeholder", "Search"))}</span>', "search")
    if kind == "subjects":
        return '<div class="subjects">' + "".join(link(screen, b["action"], esc(item), "subject") for item in b["items"]) + "</div>"
    if kind == "continue":
        return '<section class="continue">' + book_block({"book_id": "1342", "title": "Pride and Prejudice", "author": "Jane Austen", "detail": "Chapter 18 · 28%"}, screen) + '<div class="progress-track"><span style="width:28%"></span></div>' + link(screen, b["action"], "Continue reading", "button") + "</section>"
    if kind == "progress":
        value = b["value"]
        pct = f'<span>{value}%</span>' if value is not None else ""
        attrs = f'aria-valuenow="{value}"' if value is not None else ""
        return f'<div class="progress-wrap"><div class="progress-copy"><span>{esc(b["label"])}</span>{pct}</div><div class="progress-track {"indeterminate" if value is None else ""}" role="progressbar" aria-label="{esc(b["label"])}" aria-valuemin="0" aria-valuemax="100" {attrs}><span style="width:{value if value is not None else 40}%"></span></div></div>'
    if kind == "skeleton":
        return '<div aria-hidden="true">' + '<div class="skeleton"><div class="skeleton-cover"></div><div class="skeleton-lines"><i></i><i></i><i></i></div></div>' * b["count"] + "</div>"
    if kind == "field":
        uid = f'{screen["id"]}-field-{n}'
        invalid = ' aria-invalid="true" aria-describedby="' + uid + '-error"' if b.get("error") else ""
        field = f'<textarea id="{uid}"{invalid}>{esc(b["value"])}</textarea>' if b.get("multiline") else f'<input id="{uid}" type="text" value="{esc(b["value"])}" placeholder="{esc(b.get("placeholder", ""))}"{invalid}>'
        error = f'<span class="field-error" id="{uid}-error">{esc(b["error"])}</span>' if b.get("error") else ""
        return f'<div class="field {"invalid" if b.get("error") else ""}"><label for="{uid}">{esc(b["label"])}</label>{field}{error}</div>'
    if kind in ("checks", "radios"):
        items = b["items"]
        rendered = []
        for index, item in enumerate(items):
            label = item["label"] if isinstance(item, dict) else item
            checked = item.get("checked", False) if isinstance(item, dict) else item == b.get("selected")
            typ = "checkbox" if kind == "checks" else "radio"
            value = item.get("value", label) if isinstance(item, dict) else label
            rendered.append(f'<label class="choice"><input type="{typ}" name="{screen["id"]}-choice-{n}" value="{esc(value)}" {"checked" if checked else ""}><span>{esc(label)}</span></label>')
        return '<fieldset class="choice-group"><legend class="sr-only">' + ("Shelf membership" if kind == "checks" else "Choose one option") + '</legend>' + "".join(rendered) + "</fieldset>"
    if kind == "slider":
        return f'<label class="slider">{esc(b["label"])}<input type="range" min="0" max="100" value="{b["value"]}" aria-label="{esc(b["label"])}"></label>'
    if kind == "rating":
        return '<div class="rating" role="group" aria-label="Private rating">' + "".join(f'<button type="button" class="{"rated" if i <= b["value"] else ""}" aria-label="{i} stars" aria-pressed="{str(i == b["value"]).lower()}" data-rating="{i}">{icon("star")}</button>' for i in range(1, 6)) + "</div>"
    if kind == "entry":
        content = f'<h2>{esc(b["title"])}</h2><p class="entry-meta">{esc(b["book"])} · {esc(b["reference"])}</p><div class="quote"><p>{esc(b["quote"])}</p></div><p>{esc(b["text"])}</p>'
        return link(screen, b["action"], content, "entry")
    if kind == "quote":
        out = f'<blockquote class="quote"><p>{esc(b["text"])}</p><small>{esc(b["reference"])}</small>'
        if b.get("action"):
            out += link(screen, b["action"], "Return to passage")
        return out + "</blockquote>"
    if kind == "reader":
        return reader(b, screen)
    if kind == "mini-prose":
        return '<div class="mini-prose">' + esc(PROSE[2]) + "</div>"
    if kind == "selection":
        return '<nav class="selection-bar" aria-label="Selected text">' + "".join(link(screen, key) for key in b["actions"]) + "</nav>"
    raise ValueError(f"Unknown block {kind}")


def statusbar():
    return '<div class="statusbar" aria-hidden="true"><span>9:41</span><span class="status-icons"><svg viewBox="0 0 16 16"><path d="M1 12h2V9H1Zm4 0h2V6H5Zm4 0h2V3H9Zm4 0h2V1h-2Z" fill="currentColor"/></svg><svg viewBox="0 0 16 16"><path d="M1 5a11 11 0 0 1 14 0L8 13Z" fill="currentColor"/></svg><svg viewBox="0 0 18 16"><rect x="1" y="4" width="14" height="8" rx="1" fill="none" stroke="currentColor"/><path d="M16 6h1v4h-1Z" fill="currentColor"/><rect x="3" y="6" width="10" height="4" fill="currentColor"/></svg></span></div>'


def core(screen):
    back = action(screen, "back")
    reader_view = screen["area"] == "Reader" and screen["id"] in ("reader-scroll", "reader-immersive", "reader-paged", "reader-bookmark", "reader-selection", "reader-highlight")
    title = "Pride and Prejudice" if reader_view else screen["title"]
    bar = f'<header class="topbar {"" if back else "no-back"}">'
    if back:
        bar += link(screen, "back", icon("back"), "iconbutton", attrs='aria-label="Back"')
    bar += f'<h1 class="{"small-title" if reader_view else ""}">{esc(title)}</h1>'
    if reader_view and screen["id"] not in ("reader-immersive", "reader-selection"):
        key = "remove" if screen["id"] == "reader-bookmark" else "bookmark"
        bookmark = action(screen, key)
        if bookmark:
            bar += f'<button type="button" class="iconbutton" data-bookmark-control="true" data-to="{esc(bookmark["to"])}" data-action="{key}" aria-label="{esc(bookmark["label"])}" aria-pressed="{str(screen["id"] == "reader-bookmark").lower()}">{icon("bookmark")}</button>'
    if action(screen, "settings"):
        bar += link(screen, "settings", icon("settings"), "iconbutton", attrs='aria-label="Settings"')
    if screen["id"] in ("shelf-detail", "shelf-detail-empty"):
        bar += '<details class="overflow"><summary class="iconbutton" aria-label="Shelf options">' + icon("more") + '</summary><nav class="overflow-actions" aria-label="Shelf actions">' + link(screen, "rename") + link(screen, "delete") + '</nav></details>'
    bar += '</header><main class="app-main">'
    bar += "".join(render_block(b, screen, n) for n, b in enumerate(screen["blocks"])) + "</main>"
    if screen.get("nav"):
        bar += '<nav class="bottomnav" aria-label="Primary navigation">'
        for label in MANIFEST["navigation"]["primary"]:
            current = label == screen["nav"]
            bar += link(screen, "nav-" + label.lower(), f'<span>{icon(label.lower())}</span>{esc(label)}', "navitem" + (" selected" if current else ""), attrs='aria-current="page"' if current else "")
        bar += "</nav>"
    return bar


def phone(screen):
    modal = screen["variant"] in ("dialog", "sheet")
    cls = "phone reader-" + screen["variant"] if screen["area"] == "Reader" else "phone"
    out = f'<section class="{cls}" data-screen-id="{esc(screen["id"])}" aria-label="{esc(screen["title"])}">' + statusbar()
    if modal:
        back = action(screen, "back")
        base = SCREENS[back["to"]] if back else SCREENS["home-returning"]
        if base["variant"] in ("dialog", "sheet"):
            base = SCREENS["library-books"]
        out += '<div class="modal-background">' + core(base) + '</div><div class="gesture" aria-hidden="true"></div>'
        uid = screen["id"] + "-dialog-title"
        out += f'<dialog open class="app-dialog" aria-labelledby="{uid}"><div class="dialog-handle" aria-hidden="true"></div><header class="dialog-header"><h2 id="{uid}">{esc(screen["title"])}</h2>'
        if back:
            out += link(screen, "back", icon("close"), "iconbutton", attrs='aria-label="Close"')
        out += '</header><div class="dialog-body">' + "".join(render_block(b, screen, n) for n, b in enumerate(screen["blocks"])) + '</div></dialog><div class="modal-dim" aria-hidden="true"></div>'
    else:
        out += core(screen) + '<div class="gesture" aria-hidden="true"></div>'
    out += "</section>"
    # Each board repeats parent contexts behind overlays. Scope form/ARIA IDs
    # to the owning phone so labels never point into a neighboring frame.
    return re.sub(r' (id|for|aria-labelledby|aria-describedby)="([^"]+)"', lambda m: ' ' + m[1] + '="' + ' '.join(screen["id"] + '--' + token for token in m[2].split()) + '"', out)


def transitions(screen, *, prefix="", compact=False):
    out = []
    for a in screen["transitions"]:
        target = SCREENS[a["to"]]
        number = NUMBER[a["to"]]
        if compact:
            if a["role"] in ("navigation", "toolbar", "tab"):
                continue
            out.append(f'<a href="{prefix}{a["to"]}.html">{esc(a["label"])} → {number:02d}</a>')
        else:
            role = "Simulated event" if a["role"] == "event" else a["role"].capitalize()
            out.append(f'<li><a href="{prefix}{a["to"]}.html" data-to="{a["to"]}" data-action="{esc(a["id"])}"><span class="transition-number">{number:02d}</span><span>{esc(a["label"])}<small>{esc(role)} → {esc(target["id"])}</small></span></a></li>')
    return "".join(out) if compact else '<ul class="transition-list">' + "".join(out) + "</ul>"


CHILD_JS = r"""
(()=>{
  const params=new URLSearchParams(location.search),embedded=params.has('embed');
  const sid=document.querySelector('[data-screen-id]').dataset.screenId;
  const catalog=JSON.parse(document.querySelector('#catalogue').textContent);
  const $=s=>document.querySelector(s),all=s=>[...document.querySelectorAll(s)];
  const escape=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let state=null,currentBook=params.get('book')||'1342';
  if(embedded)document.body.classList.add('embed-page');
  if(params.get('mode')==='styled')document.body.classList.add('styled');
  const foreground=()=>$('.dialog-body')||$('.app-main');
  const row=(bid,target,detailOverride)=>{const b=catalog[bid],w=state?.workspaceData,position=w?.positions[bid],detail=detailOverride??(sid.startsWith('explore-')?b.language:(w?.statuses[bid]||'Want to read')+(position?' · '+position.percent+'%':'')+(w?.downloaded.includes(bid)?' · Downloaded':''));return '<a class="book" href="'+target+'.html" data-to="'+target+'" data-action="book-'+bid+'" data-book-id="'+bid+'"><div class="cover" role="img" aria-label="Typeset cover: '+escape(b.title)+'"><span class="cover-rule"></span><span class="cover-title">'+escape(b.title)+'</span><span class="cover-author">'+escape(b.author)+'</span></div><div class="book-copy"><h2>'+escape(b.title)+'</h2><p>'+escape(b.author)+'</p><small>'+escape(detail)+'</small></div></a>'};
  const fields=()=>Object.fromEntries(all('.field').map(el=>[el.querySelector('label').textContent,el.querySelector('input,textarea').value]));
  function snapshot(){return {fields:fields(),checks:all('.dialog-body input[type=checkbox],.app-main input[type=checkbox]').filter(el=>el.checked).map(el=>el.value),radios:all('input[type=radio]:checked').map(el=>el.value),settings:Object.fromEntries(all('[data-setting]').map(el=>[el.dataset.setting,el.querySelector('[aria-pressed=true]')?.textContent.trim()])),ranges:all('input[type=range]').map(el=>({label:el.getAttribute('aria-label'),value:Number(el.value)})),rating:Number($('.rating [aria-pressed=true]')?.dataset.rating||0)}}
  function go(to,action,label,book,entry){if(embedded)parent.postMessage({type:'veritalex:navigate',source:sid,to,action,label,book:book||currentBook,entry,form:snapshot()},'*');else location.href=to+'.html'+(book||currentBook?'?book='+encodeURIComponent(book||currentBook):'')}
  function dynamicBook(bid){const b=catalog[bid];if(!b)return;currentBook=bid;
    all('[data-dynamic-cover]').forEach(el=>{el.querySelector('.cover-title').textContent=b.title;el.querySelector('.cover-author').textContent=b.author;el.setAttribute('aria-label','Typeset cover: '+b.title+' by '+b.author)});
    all('[data-dynamic-book]').forEach(el=>{el.querySelector('h2').textContent=b.title;el.querySelector('p').textContent=b.author});
    const about=$('[data-book-about]');if(about)about.querySelector('p').textContent=b.summary;
    if(sid.startsWith('book-')){const chips=foreground().querySelector('.chips');if(chips)chips.innerHTML=[b.language,...b.subjects].map(x=>'<span class="chip">'+escape(x)+'</span>').join('')}
  }
  function setField(label,value){all('.field').forEach(el=>{if(el.querySelector('label').textContent===label)el.querySelector('input,textarea').value=value??''})}
  function replaceBooks(ids,targetFor,main=foreground()){[...main.children].filter(el=>el.classList.contains('book')||el.classList.contains('empty')).forEach(el=>el.remove());const container=document.createElement('section');container.dataset.liveBooks='true';container.style.cssText='display:flex;flex-direction:column;gap:20px';main.querySelector('[data-live-books]')?.remove();container.innerHTML=ids.length?ids.map(bid=>row(bid,targetFor(bid))).join(''):'<section class="empty"><h2>No books here yet</h2><p>Saved books and their reading status will appear here.</p></section>';const button=main.querySelector('.button');main.insertBefore(container,button||null)}
  function hydrate(s){state=s;currentBook=s.book;const w=s.workspaceData,main=foreground();dynamicBook(s.book);
    if(['library-books','library-want','library-reading','library-finished','library-downloaded','library-after-removal','library-empty','journal-book-picker'].includes(sid)){
      const filter={'library-want':'Want to read','library-reading':'Reading','library-finished':'Finished'}[sid];let ids=w.books.filter(b=>!filter||w.statuses[b]===filter);if(sid==='library-downloaded')ids=ids.filter(b=>w.downloaded.includes(b));replaceBooks(ids,b=>sid==='journal-book-picker'?'journal-create':w.statuses[b]==='Reading'?'book-reading':w.downloaded.includes(b)?'book-downloaded':'book-saved');
      if(sid==='journal-book-picker'&&!ids.length){main.querySelector('.empty p').textContent='Save a book from Explore before writing a journal entry.';const a=document.createElement('a');a.className='button';a.href='explore-browse.html';a.dataset.to='explore-browse';a.dataset.action='explore';a.textContent='Explore books';main.append(a)}
    }
    if(['shelf-detail','shelf-detail-empty'].includes(sid)){const shelf=w.shelves[s.shelf];if(shelf){$('.topbar h1').textContent=shelf.name;replaceBooks(shelf.books,b=>w.statuses[b]==='Reading'?'book-reading':'book-saved');const empty=main.querySelector('.empty');if(empty){empty.querySelector('h2').textContent='This shelf has room';empty.querySelector('p').textContent='Add books from your library.'}}}
    if(['shelves-list','shelves-empty','shelves-after-delete'].includes(sid)){
      [...main.children].filter(el=>el.classList.contains('row-link')||el.classList.contains('empty')).forEach(el=>el.remove());main.querySelector('[data-live-shelves]')?.remove();const section=document.createElement('section');section.dataset.liveShelves='true';section.innerHTML=Object.entries(w.shelves).map(([id,sh])=>'<a class="row-link" href="shelf-detail.html" data-to="shelf-detail" data-action="shelf-'+escape(id)+'"><span class="rowcopy"><strong>'+escape(sh.name)+'</strong><small>'+sh.books.length+' books</small></span></a>').join('')||'<section class="empty"><h2>Make a shelf of your own</h2><p>Group your saved books in a way that feels right.</p></section>';main.append(section);if(!main.querySelector('[data-action=create]')){const a=document.createElement('a');a.className='button';a.dataset.to='shelf-create';a.dataset.action='create';a.href='shelf-create.html';a.textContent='New shelf';main.append(a)}
    }
    if(sid==='shelf-add-books'){const group=main.querySelector('fieldset');group.innerHTML='<legend class="sr-only">Choose Library books</legend>'+w.books.map(b=>'<label class="choice"><input type="checkbox" value="'+b+'" '+(w.shelves[s.shelf]?.books.includes(b)?'checked':'')+'><span>'+escape(catalog[b].title)+'</span></label>').join('');const title=main.querySelector('.text-block h2');if(title)title.textContent='Add to '+(w.shelves[s.shelf]?.name||'shelf')}
    if(sid==='shelf-membership'){main.querySelector('fieldset').innerHTML='<legend class="sr-only">Choose shelves</legend>'+Object.entries(w.shelves).map(([id,sh])=>'<label class="choice"><input type="checkbox" value="'+escape(id)+'" '+(sh.books.includes(s.book)?'checked':'')+'><span>'+escape(sh.name)+'</span></label>').join('')}
    if(['shelf-create','shelf-rename','shelf-name-error'].includes(sid)){setField('Shelf name',s.shelfDraft??(sid==='shelf-rename'?w.shelves[s.shelf]?.name:''));if(s.shelfError){let error=main.querySelector('.field-error');if(!error){error=document.createElement('span');error.className='field-error';main.querySelector('.field').append(error)}error.textContent=s.shelfError;main.querySelector('.field input').setAttribute('aria-invalid','true')}}
    if(sid==='shelf-delete'){const background=$('.modal-background .app-main');if(background){$('.modal-background .topbar h1').textContent=w.shelves[s.shelf]?.name||'Shelf';replaceBooks(w.shelves[s.shelf]?.books||[],b=>w.statuses[b]==='Reading'?'book-reading':'book-saved',background)}const text=main.querySelector('.text-block');if(text&&w.shelves[s.shelf]){text.querySelector('h2').textContent=w.shelves[s.shelf].name;text.querySelector('p').textContent=w.shelves[s.shelf].books.length+' books'}}
    if(['journal-create','journal-edit'].includes(sid)&&s.draft){setField('Title',s.draft.title);setField('Your thought',s.draft.text);all('.row .rowcopy small,.row-link .rowcopy small').forEach(el=>{if(el.previousElementSibling?.textContent==='Book')el.textContent=catalog[s.draft.book].title});const quote=main.querySelector('.quote');if(quote&&!s.draft.quote)quote.remove();else if(quote)quote.querySelector('p').textContent=s.draft.quote}
    if(['journal-all','journal-empty','journal-book','journal-book-empty'].includes(sid)){main.querySelectorAll('.entry,.empty').forEach(el=>el.remove());let entries=w.entries;if(sid==='journal-book'||sid==='journal-book-empty')entries=entries.filter(e=>e.book===s.book);const section=document.createElement('section');section.innerHTML=entries.map(e=>'<a class="entry" style="display:block" href="journal-view.html" data-to="journal-view" data-action="entry" data-entry-id="'+escape(e.id)+'"><h2>'+escape(e.title||'Untitled entry')+'</h2><p class="entry-meta">'+escape(catalog[e.book].title)+(e.reference?' · '+escape(e.reference):'')+'</p>'+(e.quote?'<div class="quote"><p>'+escape(e.quote)+'</p></div>':'')+'<p>'+escape(e.text)+'</p></a>').join('')||'<section class="empty"><h2>A place for what stays with you</h2><p>Write a thought about a saved book.</p></section>';main.append(section)}
    if(sid==='journal-view'){const e=w.entries.find(e=>e.id===s.entryId)||w.entries[0];if(e){const text=main.querySelectorAll('.text-block');text[0].querySelector('h2').textContent=e.title||'Untitled entry';text[0].querySelector('p').textContent=catalog[e.book].title+' · '+catalog[e.book].author;text[1].querySelector('p').textContent=e.text;const q=main.querySelector('.quote');if(q){const locator=e.locator&&Number.isFinite(e.locator.chapter)&&Number.isFinite(e.locator.percent);q.querySelector('p').textContent=e.quote||'';q.querySelector('p').hidden=!e.quote;if(locator)q.querySelector('small').textContent=e.reference||'Saved passage';else{q.querySelector('a')?.remove();q.querySelector('small')?.remove()}if(!e.quote&&!locator)q.remove()}}}
    if(sid==='journal-delete'){const e=w.entries.find(e=>e.id===s.entryId);if(e)main.querySelector('.text-block h2').textContent=e.title||'Untitled entry'}
    if(sid==='book-saved'){const status=main.querySelector('.notice p'),pos=w.positions[s.book];if(status)status.textContent=(w.statuses[s.book]||'Want to read')+(pos?' · Chapter '+pos.chapter+' · '+pos.percent+'%':'')}
    if(sid==='book-downloaded'){const pos=w.positions[s.book],read=main.querySelector('[data-action=read]');if(read)read.textContent=pos?'Continue reading':'Start reading';const organize=main.querySelector('[data-action=actions] small');if(organize)organize.textContent=(w.statuses[s.book]||'Want to read')+' · In your library'}
    if(sid==='library-rating'){const score=w.ratings[s.book]||0;all('[data-rating]').forEach(b=>{b.classList.toggle('rated',Number(b.dataset.rating)<=score);b.setAttribute('aria-pressed',String(Number(b.dataset.rating)===score))})}
    if(sid==='library-actions'){const selected=w.statuses[s.book]||'Want to read';all('.chips a').forEach(a=>{a.classList.toggle('selected',a.textContent.trim()===selected)});const rating=main.querySelector('[data-action=rating] small');if(rating)rating.textContent=w.ratings[s.book]?w.ratings[s.book]+' out of 5 · Private':'Not rated · Private'}
    if(sid==='settings-main'){const appearance=main.querySelector('[data-action=appearance] small');if(appearance)appearance.textContent=s.appAppearance.theme+' · '+s.appAppearance.colors;const account=main.querySelector('[data-action=account] small');if(account)account.textContent=s.workspace==='account'?'Google account · '+s.syncStatus:'Guest · Saved on device';const storage=main.querySelector('[data-action=storage] small');if(storage)storage.textContent=w.downloaded.length+' on this device';const reader=main.querySelector('[data-action=reader] small');if(reader)reader.textContent=s.appearance.mode+' · '+s.appearance.font+' · '+s.appearance.size+' sp'}
    if(sid==='home-first'||sid==='home-returning'){const sync=main.querySelector('[data-action=sync]');if(sync){sync.querySelector('strong').textContent=s.workspace==='account'?s.syncStatus:'Saved on device';sync.querySelector('small').textContent=s.workspace==='account'?(s.pending?s.pending+' changes pending':'Just now'):'Guest'}const guest=main.querySelector('.notice');if(guest&&s.workspace==='account'){guest.querySelector('strong').textContent=s.syncStatus;guest.querySelector('p').textContent='Your account library is available on this device.'}}
    if(sid==='account-details'&&!s.deleteStatus){const sync=main.querySelector('[data-action=sync]');if(sync){sync.querySelector('strong').textContent=s.syncStatus;sync.querySelector('small').textContent=s.pending?s.pending+' changes pending':'Just now'}}
    if(sid==='account-details'&&s.deleteStatus){main.querySelector('[data-deletion-notice]')?.remove();const notice=document.createElement('aside');notice.className='notice';notice.dataset.deletionNotice='true';notice.innerHTML='<strong>'+escape(s.deleteStatus==='deleting'?'Account deletion in progress':'Deletion wasn’t confirmed')+'</strong><p>Review deletion status before making further account changes.</p>';main.prepend(notice);const sync=main.querySelector('[data-action=sync]');if(sync)sync.querySelector('strong').textContent=s.deleteStatus==='deleting'?'Deletion in progress':'Deletion needs attention'}
    if(sid==='settings-appearance'){all('input[type=radio]').forEach(el=>el.checked=[s.appAppearance.theme,s.appAppearance.colors].includes(el.value))}
    if(sid==='account-signout-pending'){const title=main.querySelector('.notice strong');if(title)title.textContent=s.pending+' changes are waiting to sync'}
    if(sid==='sync-failed'&&s.pendingOperation!=='sync'){main.querySelector('.empty h2').textContent=s.pendingOperation==='import'?'Guest reading wasn’t fully added':'Library restoration interrupted';main.querySelector('.empty p').textContent='Your local reading is safe. Try again to continue this operation without duplicating records.'}
    if(sid==='book-saved'&&s.resumeAfterDownload){const notice=main.querySelector('.notice p');if(notice)notice.textContent='Download the book text to return to your saved passage. Your journal reference is kept.'}
    if(sid==='shelf-name-error'&&s.shelfEditMode==='rename')$('.topbar h1').textContent='Rename shelf';
    if(sid==='auth-import-preview'){const newBooks=s.guestData.books.filter(b=>!s.accountData.books.includes(b)),matched=s.guestData.books.length-newBooks.length;const summaryRow=[...main.querySelectorAll('.rowcopy')].find(el=>el.querySelector('strong')?.textContent.endsWith('guest books'));if(summaryRow){summaryRow.querySelector('strong').textContent=s.guestData.books.length+' guest books';summaryRow.querySelector('small').textContent=newBooks.length+' new · '+matched+' already saved'}main.querySelectorAll('.book').forEach(el=>el.remove());const list=document.createElement('section');list.style.cssText='display:flex;flex-direction:column;gap:16px';list.innerHTML=s.guestData.books.map(b=>row(b,'book-saved',s.accountData.books.includes(b)?'Already in account':'New to account')).join('');main.insertBefore(list,main.querySelector('.notice'));const reading=[...main.querySelectorAll('.notice')].find(el=>el.querySelector('strong')?.textContent==='Your reading stays intact');if(reading){const g=s.guestData;reading.querySelector('p').textContent=g.entries.length+' journal '+(g.entries.length===1?'entry':'entries')+' · '+g.highlights.length+' '+(g.highlights.length===1?'highlight':'highlights')+' · '+Object.keys(g.shelves).length+' shelves · '+Object.keys(g.ratings).length+' private '+(Object.keys(g.ratings).length===1?'rating':'ratings')+'\nExisting account writing stays. Duplicate books and entries are matched.'}}
    if(sid==='auth-import-complete'&&s.importSummary)main.querySelector('.empty p').textContent=s.importSummary.newBooks+' new books added. '+s.importSummary.matched+' existing books matched. '+s.importSummary.notes+' journal '+(s.importSummary.notes===1?'entry':'entries')+' and '+s.importSummary.highlights+' '+(s.importSummary.highlights===1?'highlight':'highlights')+' preserved.';
    if(sid==='library-after-removal'&&s.removedBook)main.querySelector('.notice p').textContent=catalog[s.removedBook].title+' left Library. Your notes and highlights are kept in Journal.';
    if(sid==='shelves-after-delete'&&s.deletedShelfName)main.querySelector('.notice p').textContent=s.deletedShelfName+' was removed. All its books remain in Library.';
    if(sid==='book-reading'){const pos=w.positions[s.book];const progress=main.querySelector('.progress-wrap');if(progress){if(pos){progress.querySelector('.progress-copy').innerHTML='<span>Reading · Chapter '+pos.chapter+'</span><span>'+pos.percent+'%</span>';progress.querySelector('.progress-track span').style.width=pos.percent+'%';progress.querySelector('[role=progressbar]').setAttribute('aria-valuenow',String(pos.percent))}else progress.innerHTML='<p>Reading · No saved position yet</p>'}const journal=main.querySelector('[data-action=journal] small');if(journal)journal.textContent=w.entries.filter(e=>e.book===s.book).length+' entries for this book';const organize=main.querySelector('[data-action=actions] small');if(organize)organize.textContent=(w.statuses[s.book]||'Want to read')+' · '+Object.values(w.shelves).filter(sh=>sh.books.includes(s.book)).map(sh=>sh.name).join(', ')}
    if(['home-returning','home-first'].includes(sid)&&sid==='home-returning'){if(!w.positions['1342']||!w.books.includes('1342'))main.querySelector('.continue')?.remove();const card=main.querySelector('.continue'),pos=w.positions['1342'];if(card&&pos){card.querySelector('small').textContent='Chapter '+pos.chapter+' · '+pos.percent+'%';card.querySelector('.progress-track span').style.width=pos.percent+'%';card.querySelector('[data-action=continue]').textContent=w.downloaded.includes('1342')?'Continue reading':'Download to read'}const grid=main.querySelector('.book-grid');if(grid)grid.innerHTML=w.books.filter(b=>b!=='1342'||!main.querySelector('.continue')).map(b=>row(b,w.statuses[b]==='Reading'?'book-reading':'book-saved')).join('')}
    if(sid==='settings-storage'){replaceBooks(w.downloaded,b=>'book-downloaded');const text=main.querySelector('.notice p');if(text)text.textContent=w.downloaded.length+' books available offline on this device.'}
    if(sid==='explore-results'){const q=s.search.toLowerCase(),subject=s.subject;let ids=Object.keys(catalog).filter(b=>(!q||(catalog[b].title+' '+catalog[b].author).toLowerCase().includes(q))&&(!subject||catalog[b].subjects.includes(subject)));replaceBooks(ids,()=> 'book-new');const search=main.querySelector('.search span');if(search)search.textContent=s.search||s.subject||'All books';const count=main.querySelector('.rowcopy strong');if(count)count.textContent=ids.length+' titles'}
    if(sid==='explore-search')setField('Title or author',s.search);
    if(sid==='reader-search')setField('Word or phrase',s.readerQuery);
    if(sid==='reader-search-empty'||sid==='reader-search-results'){const input=main.querySelector('.search span');if(input)input.textContent=s.readerQuery;if(sid==='reader-search-results'){main.querySelectorAll('[data-action=result]').forEach(el=>el.remove());const results=document.createElement('section');results.innerHTML=s.readerResults.map(r=>'<a class="row-link" href="reader-scroll.html" data-to="reader-scroll" data-action="result" data-entry-id="'+r.passage+'"><span class="rowcopy"><strong>'+escape(r.text)+'</strong><small>Chapter 18</small></span></a>').join('');main.insertBefore(results,main.querySelector('.notice'))}}
    if(s.appAppearance.theme==='Dark'){Object.entries({'--paper':'#19120d','--panel':'#231a14','--ink':'#f0dfd6','--muted':'#d6c3b7','--tonal':'#6d3a0d','--accent':'#ffb77f','--onaccent':'#4e2600','--line':'#9f8d83'}).forEach(([k,v])=>$('.phone').style.setProperty(k,v))}
    const bookmarkControl=$('.topbar [data-bookmark-control]');if(bookmarkControl){const pos=w.positions['1342'],saved=w.bookmarks.some(b=>b.book==='1342'&&b.chapter===pos?.chapter&&(b.passage||0)===(pos?.passage||0));bookmarkControl.setAttribute('aria-pressed',String(saved));bookmarkControl.setAttribute('aria-label',saved?'Remove bookmark':'Add bookmark');bookmarkControl.classList.toggle('bookmarked',saved)}
    if(sid==='reader-contents'){const bookmark=main.querySelector('[data-action=bookmark]');if(bookmark){if(!w.bookmarks.length)bookmark.remove();else{const saved=w.bookmarks[0];bookmark.querySelector('strong').textContent='Chapter '+saved.chapter+' · '+saved.percent+'%'}}const label=[...main.querySelectorAll('.text-block h2')].find(el=>el.textContent==='Saved bookmark');if(label&&!w.bookmarks.length)label.textContent='No bookmarks yet'}
    if(sid==='reader-highlight'&&!w.highlights.some(h=>h.book==='1342')){main.querySelectorAll('mark').forEach(el=>el.replaceWith(document.createTextNode(el.textContent)));main.querySelector('.notice')?.remove()}
    if(sid.startsWith('reader-')){const pos=w.positions['1342']||{chapter:18,percent:28},appearance=s.appearance;all('[data-setting]').forEach(el=>{el.querySelectorAll('button').forEach(b=>{const selected=b.textContent.trim()===appearance[el.dataset.setting];b.classList.toggle('selected',selected);b.setAttribute('aria-pressed',String(selected))})});const prose=main.querySelector('.reader-content');if(prose){prose.style.fontFamily=appearance.font==='Roboto Flex'?"'Roboto Flex',Arial,sans-serif":"Literata,Georgia,serif";prose.style.fontSize=appearance.size+'px';prose.style.lineHeight=appearance.line+'px';prose.querySelector('h2').textContent='Chapter '+pos.chapter;prose.querySelectorAll('p').forEach(p=>{p.style.fontSize='inherit';p.style.lineHeight='inherit'});if(pos.chapter===19)prose.innerHTML='<h2>Chapter 19</h2><p>'+(sid==='reader-selection'||sid==='reader-highlight'?'<mark>The next day opened a new scene at Longbourn.</mark>':'The next day opened a new scene at Longbourn.')+' Mr. Collins made his declaration in form.</p>';else if(pos.passage===1)prose.innerHTML='<h2>Chapter 18</h2><p>The moment of her release from him was ecstasy.</p>';const margin={Narrow:16,Comfortable:24,Wide:32}[appearance.margins];main.style.paddingLeft=margin+'px';main.style.paddingRight=margin+'px'}all('.reader-position').forEach(el=>el.innerHTML='<span>Chapter '+pos.chapter+'</span><span>'+pos.percent+'%</span>');const palettes={Light:{'--paper':'#fff8f3','--panel':'#fcf1e8','--ink':'#241a14','--muted':'#55483d','--tonal':'#ffdcbd','--line':'#d7c3b4','--accent':'#895021','--onaccent':'#fff'},Sepia:{'--paper':'#f4e9d4','--panel':'#eee0c7','--ink':'#332519','--muted':'#654d36','--tonal':'#e7d7b8','--line':'#c9b38a','--accent':'#895021','--onaccent':'#fff'},Dark:{'--paper':'#19120d','--panel':'#231a14','--ink':'#f0dfd6','--muted':'#d6c3b7','--tonal':'#6d3a0d','--line':'#9f8d83','--accent':'#ffb77f','--onaccent':'#4e2600'}};Object.entries(palettes[appearance.paper]||palettes.Light).forEach(([k,v])=>$('.phone').style.setProperty(k,v))}
    if(sid==='reader-appearance'||sid==='settings-reader-defaults'){const a=s.appearance;all('[data-setting]').forEach(el=>el.querySelectorAll('button').forEach(b=>{const selected=b.textContent.trim()===a[el.dataset.setting];b.classList.toggle('selected',selected);b.setAttribute('aria-pressed',String(selected))}));all('input[type=range]').forEach(el=>{if(el.getAttribute('aria-label').includes('size'))el.value=(a.size-14)/.12;else el.value=(a.line-24)/.13})}
    const required=$('[data-require-selection]');if(required)required.setAttribute('aria-disabled',String(!all('input[type=checkbox]:checked').length));
  }
  document.addEventListener('click',event=>{
    const a=event.target.closest('a[data-to],button[data-to]');if(a){event.preventDefault();if(a.getAttribute('aria-disabled')==='true')return;go(a.dataset.to,a.dataset.action,a.textContent.trim(),a.dataset.bookId,a.dataset.entryId);return}
    const chip=event.target.closest('button[data-choice]');if(chip){chip.parentElement.querySelectorAll('button').forEach(b=>{b.classList.remove('selected');b.setAttribute('aria-pressed','false')});chip.classList.add('selected');chip.setAttribute('aria-pressed','true')}
    const rating=event.target.closest('[data-rating]');if(rating){const score=Number(rating.dataset.rating);rating.parentElement.querySelectorAll('button').forEach(b=>{b.classList.toggle('rated',Number(b.dataset.rating)<=score);b.setAttribute('aria-pressed',String(Number(b.dataset.rating)===score))})}
  });
  document.addEventListener('keydown',event=>{if(event.key==='Escape'){const menu=$('.overflow[open]');if(menu){event.preventDefault();menu.open=false;menu.querySelector('summary').focus();return}}if(event.key!=='Enter'||event.isComposing||event.target.tagName!=='INPUT')return;const key=sid==='explore-search'?'submit':sid==='reader-search'?'search':null;if(key){const submit=$('[data-action='+key+']');if(submit){event.preventDefault();go(submit.dataset.to,key,submit.textContent)}}});
  document.addEventListener('click',event=>{all('.overflow[open]').forEach(menu=>{if(!menu.contains(event.target))menu.open=false})});
  all('.overflow').forEach(menu=>menu.addEventListener('focusout',event=>{if(event.relatedTarget&&!menu.contains(event.relatedTarget))menu.open=false}));
  document.addEventListener('change',()=>{const required=$('[data-require-selection]');if(required)required.setAttribute('aria-disabled',String(!all('input[type=checkbox]:checked').length))});
  window.addEventListener('message',event=>{if(event.source===parent&&event.data?.type==='veritalex:hydrate')hydrate(event.data.state)});
  const dialog=$('dialog');if(dialog&&params.get('embed')==='1'){dialog.removeAttribute('open');dialog.showModal();dialog.addEventListener('cancel',event=>{event.preventDefault();const back=dialog.querySelector('[data-action=back]');if(back)go(back.dataset.to,'back','Back')});const safe=dialog.querySelector('[data-action=cancel],[data-action=keep]');if(safe)safe.focus()}
  dynamicBook(currentBook);if(embedded)parent.postMessage({type:'veritalex:ready'},'*');
})();
"""


def head(title, css=APP_CSS):
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>' + esc(title) + '</title><style>' + css + '.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap;border:0}</style></head>'


def font_css():
    rules = []
    for filename, family, weight in [("roboto-flex.woff2", "Roboto Flex", "100 1000"), ("literata.woff2", "Literata", "200 900")]:
        path = ROOT / "assets" / filename
        if not path.exists():
            continue
        encoded = base64.b64encode(path.read_bytes()).decode("ascii")
        rules.append(f"@font-face{{font-family:'{family}';font-style:normal;font-weight:{weight};font-display:swap;src:url(data:font/woff2;base64,{encoded}) format('woff2')}}")
    return "".join(rules)


POLISHED_CSS = """
.styled .phone{font-family:'Roboto Flex',Arial,sans-serif;--paper:#fff8f3;--panel:#fcf1e8;--tonal:#ffdcbd;--ink:#241a14;--muted:#55483d;--line:#d7c3b4;--accent:#895021;--onaccent:#fff}.styled .phone input,.styled .phone textarea,.styled .phone button{font-family:inherit}.styled .reader-content,.styled .reader-content h2,.styled .reader-content p,.styled .quote p,.styled .mini-prose{font-family:Literata,Georgia,serif}.styled .reader-position,.styled .quote small,.styled .quote a{font-family:'Roboto Flex',Arial,sans-serif}.styled .notice{border:0;background:#f5e9df;border-radius:16px}.styled .notice.error{background:#ffdad6;color:#410002}.styled .notice.error p{color:#410002}.styled .cover{background:#e6d8c6;border-color:#a88f70;color:#503c27;box-shadow:inset 4px 0 #503c2715}.styled .book-grid .grid-book:nth-child(2n) .cover{background:#dce0cf;color:#3e4530;border-color:#8d957a}.styled .book-grid .grid-book:nth-child(3n) .cover{background:#edd7c9;color:#684838;border-color:#b79984}.styled .cover-rule{opacity:.5}.styled .bottomnav{background:#f5e9df;border:0}.styled .chip{border-color:#857468}.styled .chip.selected{background:#f9ddc5;border-color:#f9ddc5}.styled .subject{background:#fcf1e8;border:0;border-radius:16px}.styled .search{background:#f5e9df}.styled .progress-track{background:#f9ddc5}.styled .reader-content mark{background:#f6e5a8}.styled .button{font-weight:600}.styled .app-dialog{border:0}.styled .button.text{color:#895021}.styled .book.large{padding-top:14px}.styled .row,.styled .row-link,.styled .entry{border-color:#e1d3c7}.styled .topbar h1{font-weight:500}.styled .tabs{border-color:#d7c3b4}.styled .empty>.icon{color:#895021}.styled .brand-mark{background:#ffdcbd;border:0;color:#895021}.styled .reader-sepia{--paper:#f4e9d4;--panel:#eee0c7}.styled .quote{border-color:#895021}.styled .field input,.styled .field textarea{border-color:#857468}.styled .choice input,.styled .slider input{accent-color:#895021}
"""
APP_CSS += ".phone .chip{min-height:48px;min-width:48px;justify-content:center}.phone .slider input{min-height:48px}.phone .quote a{min-height:48px;display:flex;align-items:center}.phone .selection-bar a{min-height:48px}.phone .app-main p{font-size:16px;line-height:24px}.phone .notice p,.phone .book-copy p{font-size:14px;line-height:20px}.phone .reader-content p{font-size:19px;line-height:32px}.phone .quote p{font-size:19px;line-height:29px}.phone .grid-book p{font-size:13px;line-height:18px}.phone a[aria-disabled=true]{opacity:.45;cursor:default}"
APP_CSS += ".phone .book.large{flex-direction:row;text-align:left;align-items:center;padding:8px 0;gap:16px}.phone .book.large .cover{width:80px;padding:14px 6px}.phone .book.large .cover-title{font-size:11px;line-height:15px}.phone .book.large .cover-author{font-size:9px;line-height:12px}.phone .book.large .book-copy{flex:1}.phone .book.large .book-copy h2{font-size:22px;line-height:29px}.phone .subjects{gap:8px}.phone .subject{min-height:48px;padding:13px 12px}.phone .entry{display:block}.reader-tool{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px;min-height:64px;min-width:0;flex:1;padding:8px 2px;font-size:12px;line-height:16px;background:transparent;color:inherit;border:0;border-radius:12px}.reader-tool span{min-width:0;max-width:100%;overflow-wrap:anywhere}.iconbutton[data-bookmark-control][aria-pressed=true]{background:var(--tonal)}.iconbutton[data-bookmark-control][aria-pressed=true] .icon{fill:currentColor}.overflow{position:relative;flex:none}.overflow summary{list-style:none;cursor:pointer}.overflow summary::-webkit-details-marker{display:none}.overflow summary:focus-visible{outline:3px solid var(--accent);outline-offset:2px}.overflow-actions{position:absolute;right:0;top:52px;min-width:184px;padding:8px;background:var(--paper);border:1px solid var(--line);border-radius:12px;box-shadow:0 6px 18px #0002;z-index:5}.overflow-actions a{display:flex;align-items:center;min-height:48px;padding:12px;border-radius:8px;font-size:15px;line-height:24px}.overflow-actions a:hover{background:var(--panel)}"


def screen_page(screen, polished=False):
    n = NUMBER[screen["id"]]
    notes = "".join(f'<p class="note">{esc(note)}</p>' for note in screen["annotations"])
    label = "Light state design" if polished else "Wireframe"
    header = f'<nav class="notes-links" aria-label="Package navigation"><a href="../index.html#{screen["id"]}">All screens</a><a href="../prototype.html#{screen["id"]}">Open prototype</a></nav><div class="eyebrow">{label} {n:02d} / {len(SCREENS)} · {esc(screen["area"])}</div><h1>{esc(screen["title"])}</h1><p><code>{esc(screen["id"])}</code> · {esc(screen["variant"])} · 412 × 915</p><p class="prototype-notice">{esc(MANIFEST["prototype_notice"])}</p>{notes}<h2>Transitions</h2>'
    css = APP_CSS + (font_css() + POLISHED_CSS if polished else "")
    return head(f'{n:02d} · {screen["title"]} · Veritalex {label.lower()}', css) + ('<body class="styled">' if polished else '<body>') + '<div class="screen-page">' + phone(screen) + '<aside class="screen-notes">' + header + transitions(screen) + '</aside></div><script id="catalogue" type="application/json">' + payload(CATALOGUE) + '</script><script>' + CHILD_JS + '</script></body></html>'


PACKAGE_CSS = """
*{box-sizing:border-box}html{color-scheme:light;scroll-behavior:smooth}body{margin:0;background:#f2f0ec;color:#282521;font-family:Arial,Helvetica,sans-serif}button,input,select{font:inherit}a{color:inherit}a,button{touch-action:manipulation}button,a,input,select{border-radius:6px}a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid #895021;outline-offset:3px}.shell{max-width:1440px;margin:auto;padding:36px clamp(20px,4vw,64px)}.shell h1{font-size:clamp(1.8rem,3vw,2.8rem);line-height:1.2;font-weight:500;margin:10px 0 14px}.shell h2{font-size:23px;line-height:31px;font-weight:500;margin:0 0 14px}.shell p{line-height:1.65}.eyebrow{font-size:12px;line-height:18px;letter-spacing:.08em;text-transform:uppercase;font-weight:600}.intro{max-width:850px;color:#605a52;margin-bottom:26px}.shellnav{display:flex;gap:12px;flex-wrap:wrap;margin:24px 0}.shellnav a,.shellbutton{background:#fff;border:1px solid #ccc3b9;min-height:44px;padding:11px 15px;text-decoration:none;display:inline-flex;align-items:center;justify-content:center;font-size:14px;cursor:pointer;color:inherit}.shellnav .primary{background:#493a2d;border-color:#493a2d;color:#fff}.summary{display:flex;gap:24px;flex-wrap:wrap;border-top:1px solid #d4cdc3;border-bottom:1px solid #d4cdc3;padding:16px 0;margin-bottom:28px;font-size:14px}.filterbar{display:grid;grid-template-columns:minmax(180px,1fr) 180px 180px;gap:16px;max-width:930px;margin:24px 0}.filterbar label,.control{display:flex;flex-direction:column;gap:7px;font-size:13px}.filterbar input,.filterbar select,.control select{background:#fff;border:1px solid #c8beb2;padding:12px;min-height:46px;width:100%;color:#282521}.result-count{font-size:13px;line-height:22px;color:#665d53;margin-bottom:18px}.screen-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,250px),1fr));gap:24px}.screen-card{background:#fff;border:1px solid #d8d0c6;border-radius:12px;overflow:hidden;min-width:0}.screen-card[hidden]{display:none}.card-preview{height:300px;overflow:hidden;background:#e8e5e0;position:relative;display:block;border-bottom:1px solid #ddd6ce}.card-preview iframe{border:0;width:412px;height:915px;pointer-events:none;transform:scale(.68);transform-origin:top left;position:absolute;left:50%;margin-left:-140px}.card-copy{padding:17px}.card-copy .eyebrow{font-size:10px}.card-copy h3{font-size:18px;line-height:25px;margin:7px 0 6px;font-weight:500}.card-copy code{font-size:11px;overflow-wrap:anywhere;color:#766c61}.card-links{display:flex;gap:13px;flex-wrap:wrap;font-size:13px;line-height:21px;margin-top:17px}.card-links a{min-height:28px;text-underline-offset:3px}.export-badge{position:absolute;top:10px;left:10px;background:#fff;border:1px solid #c8b8a5;padding:4px 7px;font-size:10px;z-index:1;border-radius:4px}.export-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,250px),1fr));gap:20px}.export-card{background:#fff;padding:16px;border:1px solid #d8d0c6;border-radius:10px}.export-card img{display:block;max-width:100%;height:260px;object-fit:contain;margin:auto;background:#eee}.export-card h3{font-size:17px;line-height:24px}.export-card p{font-size:13px;color:#6a6056}.export-links{display:flex;flex-wrap:wrap;gap:14px;font-size:13px}.section{margin-top:44px}.boards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,290px),1fr));gap:14px}.board-link{border:1px solid #d0c5b8;border-radius:9px;padding:18px;background:#fff;text-decoration:none}.board-link strong{display:block;font-size:16px;line-height:23px;font-weight:500;margin-bottom:6px}.board-link span{font-size:12px;color:#786b5e}.footer{font-size:12px;color:#73695e;border-top:1px solid #d4cdc3;margin-top:44px;padding-top:18px;line-height:20px}.prototype-shell{max-width:1230px;margin:auto;padding:24px;display:grid;grid-template-columns:minmax(260px,1fr) 414px minmax(210px,.8fr);gap:28px;align-items:start}.prototype-sidebar{position:sticky;top:24px}.prototype-sidebar h1{font-size:27px;line-height:35px;font-weight:500;margin:8px 0 12px}.prototype-sidebar p{font-size:14px;line-height:22px;color:#6b6157}.prototype-sidebar .control{margin:20px 0}.mode-switch{display:flex;border:1px solid #bbac9b;border-radius:8px;padding:3px;background:#e9e2d9;gap:3px}.mode-switch button{border:0;padding:10px 8px;background:transparent;flex:1;font-size:12px;cursor:pointer;min-height:42px}.mode-switch button[aria-pressed=true]{background:#fff;box-shadow:0 1px 3px #0002}.prototype-device{border:1px solid #8c8377;border-radius:25px;overflow:hidden;background:#fff;width:414px;height:917px;box-shadow:0 8px 28px #00000012}.prototype-device iframe{width:100%;height:100%;display:block;border:0}.prototype-inspector{padding-top:2px}.prototype-inspector h2{font-size:18px;line-height:26px;font-weight:500;margin-top:0}.prototype-inspector p{font-size:13px;line-height:21px;color:#6b6157}.prototype-inspector ul{list-style:none;padding:0;display:flex;flex-direction:column;gap:8px}.prototype-inspector li a{display:block;border:1px solid #d2c6b7;background:#fff;padding:10px;font-size:13px;line-height:19px;text-decoration:none}.prototype-inspector small{display:block;color:#807163;font-size:11px;line-height:18px}.state-counter{font-size:12px;line-height:20px;color:#77695a;margin-bottom:18px}.prototype-footer{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px}.prototype-footer button{min-height:44px;border:1px solid #c8b9a7;background:#fff;padding:8px 12px;cursor:pointer}.inline-status{font-size:12px;line-height:20px;color:#766658;margin-top:15px}.no-results{padding:32px;background:#fff;border:1px solid #d8d0c6;border-radius:8px}.no-results[hidden]{display:none}@media(max-width:1050px){.prototype-shell{grid-template-columns:minmax(220px,1fr) 414px}.prototype-inspector{grid-column:1/-1;position:static}.prototype-inspector ul{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}.prototype-sidebar{position:static}}@media(max-width:720px){.shell{padding:24px 18px}.filterbar{grid-template-columns:1fr 1fr}.filterbar label:first-child{grid-column:1/-1}.prototype-shell{display:flex;flex-direction:column;padding:16px;gap:20px;align-items:center}.prototype-sidebar,.prototype-inspector{width:min(414px,100%)}.prototype-device{width:min(414px,100%);height:915px}.prototype-sidebar h1{font-size:23px;line-height:30px}.prototype-sidebar .intro-copy{display:none}.prototype-sidebar .control{margin:12px 0}.screen-grid{grid-template-columns:repeat(auto-fill,minmax(min(100%,230px),1fr))}.summary{gap:14px}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
"""


PACKAGE_JS = """
(()=>{'use strict';const data=JSON.parse(document.querySelector('#package-data').textContent);const byId=new Map(data.screens.map(s=>[s.id,s]));const count=data.screens.length;const $=s=>document.querySelector(s);const escapeHTML=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
if(document.body.dataset.page==='gallery'){const search=$('#screen-search'),area=$('#area-filter'),state=$('#state-filter'),cards=[...document.querySelectorAll('.screen-card')];const update=()=>{const q=search.value.toLowerCase().trim();let visible=0;cards.forEach(card=>{const show=(!q||card.dataset.search.includes(q))&&(!area.value||card.dataset.area===area.value)&&(!state.value||card.dataset.variant===state.value);card.hidden=!show;if(show)visible++});$('#result-count').textContent=visible+' of '+count+' screen states';$('#no-results').hidden=visible!==0};[search,area,state].forEach(el=>el.addEventListener('input',update));update();if(location.hash){const id=decodeURIComponent(location.hash.slice(1));const card=document.getElementById(id);if(card){card.scrollIntoView({block:'start'});card.querySelector('a').focus({preventScroll:true})}}}
if(document.body.dataset.page==='prototype'){window.startVeritalexPrototype(data)}
})();
"""

PACKAGE_JS += """
(()=>{if(document.body.dataset.page!=='gallery')return;const button=document.querySelector('#refresh-references'),status=document.querySelector('#reference-status'),grid=document.querySelector('#stitch-export-grid');const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));const safe=p=>typeof p==='string'&&!p.startsWith('/')&&!p.includes('..')&&!p.includes(':')&&/^[a-zA-Z0-9_./-]+$/.test(p);const exists=async path=>{if(!safe(path))return false;try{return(await fetch(path,{method:'HEAD',cache:'no-store'})).ok}catch{return false}};const refresh=async()=>{button.disabled=true;status.textContent='Checking available local Stitch exports…';try{const response=await fetch('metadata.json',{cache:'no-store'});if(!response.ok)throw Error('No metadata');const metadata=await response.json();const available=await Promise.all((metadata.stitchScreens||[]).map(async item=>({...item,hasImage:await exists(item.screenshot),hasHTML:await exists(item.html)})));const items=available.filter(x=>x.hasImage||x.hasHTML);grid.innerHTML=items.map(item=>'<article class="export-card">'+(item.hasImage?'<a href="'+escape(item.screenshot)+'"><img loading="lazy" src="'+escape(item.screenshot)+'" alt="'+escape(item.title||item.slug||'Stitch reference')+'"></a>':'')+'<h3>'+escape(item.title||item.slug||'Stitch reference')+'</h3><p>'+escape(item.variant||'design')+' · '+escape(item.deviceType||'phone')+'</p><div class="export-links">'+(item.hasImage?'<a href="'+escape(item.screenshot)+'">Screenshot</a>':'')+(item.hasHTML?'<a href="'+escape(item.html)+'">Stitch HTML</a>':'')+'</div></article>').join('');document.querySelector('#reference-count').textContent=items.length+' available Stitch references';status.textContent='References refreshed. Only files present in this package are linked.';document.querySelectorAll('.screen-card').forEach(card=>{card.querySelectorAll('[data-live-reference]').forEach(a=>a.remove());items.filter(item=>(item.screenIds||[]).includes(card.id)).slice(0,2).forEach(item=>{const a=document.createElement('a');a.dataset.liveReference='true';a.href=item.hasImage?item.screenshot:item.html;a.textContent='Stitch · '+(item.variant||'design');card.querySelector('.card-links').append(a)})})}catch{status.textContent='Showing the references bundled at build time. Serve this folder over localhost to refresh metadata.'}finally{button.disabled=false}};button.addEventListener('click',refresh);if(location.protocol==='http:'||location.protocol==='https:')refresh()})();
"""


PROTOTYPE_JS = r"""
window.startVeritalexPrototype=function(data){
  const byId=new Map(data.screens.map(s=>[s.id,s])),frame=document.querySelector('#prototype-frame'),select=document.querySelector('#screen-select');
  const $=s=>document.querySelector(s),clone=x=>JSON.parse(JSON.stringify(x));
  const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const sample={id:'entry-1',book:'1342',title:'First impressions',text:'How quickly a first impression becomes a certainty. I want to notice when Elizabeth changes her mind.',quote:'“The moment of her release from him was ecstasy.”',reference:'Chapter 18 · 28%',locator:{chapter:18,percent:28,passage:0}};
  function library(empty=false){return {books:empty?[]:['1342','84','11'],statuses:empty?{}:{'1342':'Reading','84':'Want to read','11':'Finished'},downloaded:empty?[]:['1342','11'],ratings:empty?{}:{'1342':4},positions:empty?{}:{'1342':{chapter:18,percent:28,passage:0}},shelves:empty?{}:{classics:{name:'Classics',books:['1342','84']},'reading-next':{name:'Reading next',books:['84']}},entries:empty?[]:[clone(sample)],bookmarks:[],highlights:[]}}
  function fixture(id,selectedBook='1342',bookDemo=true){const first=['auth-welcome','home-first','library-empty','shelves-empty','journal-empty'].includes(id);const guest=library(first),account=library();if(bookDemo&&selectedBook==='1342'&&['book-new','book-saved','book-downloaded','book-downloading','book-download-failed'].includes(id)){delete guest.positions['1342'];guest.downloaded=guest.downloaded.filter(b=>b!=='1342');guest.statuses['1342']='Want to read';if(id==='book-downloaded')guest.downloaded.push('1342');if(id==='book-new'){guest.books=guest.books.filter(b=>b!=='1342');delete guest.statuses['1342'];Object.values(guest.shelves).forEach(sh=>sh.books=sh.books.filter(b=>b!=='1342'))}}guest.entries.forEach(e=>e.id='guest-'+e.id);guest.highlights=first?[]:[{id:'guest-highlight-1',book:'1342',reference:'Chapter 18',locator:{chapter:18,percent:28,passage:0},text:sample.quote}];account.entries[0].id='account-entry-1';account.positions['1342']={chapter:19,percent:31,passage:0};if(id==='account-deleted'){account.books=[];account.statuses={};account.downloaded=[];account.ratings={};account.positions={};account.shelves={};account.entries=[];account.highlights=[];account.bookmarks=[]}if(id==='library-after-removal'){guest.books=guest.books.filter(b=>b!=='1342');guest.downloaded=guest.downloaded.filter(b=>b!=='1342');Object.values(guest.shelves).forEach(sh=>sh.books=sh.books.filter(b=>b!=='1342'))}if(id==='shelves-after-delete')delete guest.shelves.classics;if(id==='journal-book-empty')guest.entries=[];if(id==='shelf-detail-empty')guest.shelves.classics.books=[];if(id==='settings-storage-empty')guest.downloaded=[];const signed=id.startsWith('account-')||id.startsWith('auth-import')||id.startsWith('sync-')&&id!=='sync-local';const s={workspace:signed&&id!=='account-deleted'?'account':'guest',guest,account,book:'1342',shelf:'classics',shelfDraft:null,shelfError:'',shelfEditMode:id==='shelf-rename'?'rename':'create',entryId:signed?'account-entry-1':'guest-entry-1',draft:null,draftOrigin:'journal-create',appAppearance:{theme:'Follow system',colors:'Veritalex brand'},appearance:{font:'Literata',margins:'Comfortable',paper:'Light',mode:'Scroll',size:19,line:32},readerQuery:'Elizabeth',readerResults:[{text:'Till Elizabeth entered the drawing-room at Netherfield',passage:0}],search:first?'':'Austen',subject:'',syncStatus:'Up to date',nextShelf:1,pending:0,pendingOperation:'sync',signoutAfterSync:false,deleteStatus:null,readerMode:'reader-scroll',settingsReturn:'home-returning',bookReturn:'library-books',journalReturn:'journal-all',importSummary:null};if(id==='reader-search-empty'){s.readerQuery='no matching phrase';s.readerResults=[]}if(id==='account-signout-pending'||['sync-waiting','sync-failed','sync-syncing','sync-expired'].includes(id))s.pending=2;if(id==='sync-restoring')s.pendingOperation='restore';if(id==='auth-importing')s.pendingOperation='import';if(id==='account-deleting')s.deleteStatus='deleting';if(id==='account-delete-error')s.deleteStatus='failed';if(id==='reader-paged')s.readerMode='reader-paged';if(['journal-create','journal-edit','journal-discard'].includes(id)){s.draft=id==='journal-edit'?clone(s[s.workspace].entries[0]):{...clone(sample),id:null};s.entryId=s.draft.id||s.entryId;s.draftOrigin=id==='journal-edit'?'journal-edit':'journal-create'}s.pendingByWorkspace={guest:0,account:signed?s.pending:0};if(s.pending&&signed)s.syncStatus='Waiting to sync';if(id==='reader-bookmark'||id==='reader-contents')s[s.workspace].bookmarks=[{id:'bookmark-1342-18-0',book:'1342',chapter:18,percent:28,passage:0}];return s}
  const entryParams=new URLSearchParams(location.search),requestedBook=entryParams.get('book'),requestedWorkspace=entryParams.get('workspace');
  let current=byId.has(location.hash.slice(1))?location.hash.slice(1):'auth-welcome';
  const contentWorkspace=['Home','Explore','Book','Library','Shelves','Journal','Reader','Settings'].includes(byId.get(current).area)&&['account','guest'].includes(requestedWorkspace)?requestedWorkspace:null;
  let state=fixture(current,Object.prototype.hasOwnProperty.call(data.catalogue,requestedBook)?requestedBook:'1342',contentWorkspace!=='account'),history=[],mode='wireframe';
  if(contentWorkspace){state.workspace=contentWorkspace;state.pending=state.pendingByWorkspace[contentWorkspace]}
  const workspace=()=>state[state.workspace];
  const bookDestination=(w,book)=>!w.books.includes(book)?'book-new':!w.downloaded.includes(book)?'book-saved':w.statuses[book]==='Reading'?'book-reading':'book-downloaded';
  if(contentWorkspace){
    if(['book-new','book-saved','book-reading','book-downloaded'].includes(current))current=bookDestination(workspace(),state.book);
    if(['home-first','home-returning'].includes(current))current=workspace().books.length?'home-returning':'home-first';
    if(['library-books','library-empty'].includes(current))current=workspace().books.length?'library-books':'library-empty';
    if(['shelves-list','shelves-empty'].includes(current))current=Object.keys(workspace().shelves).length?'shelves-list':'shelves-empty';
    if(['journal-all','journal-empty'].includes(current))current=workspace().entries.length?'journal-all':'journal-empty';
  }
  if(requestedBook&&Object.prototype.hasOwnProperty.call(data.catalogue,requestedBook)){
    state.book=requestedBook;
    if(['book-new','book-saved','book-reading','book-downloaded'].includes(current))current=bookDestination(workspace(),requestedBook);
    if(['journal-book','journal-book-empty'].includes(current))current=workspace().entries.some(e=>e.book===requestedBook)?'journal-book':'journal-book-empty';
  }
  const requestedShelf=entryParams.get('shelf');
  if(['shelf-detail','shelf-detail-empty','shelf-rename','shelf-delete'].includes(current)&&requestedShelf&&Object.prototype.hasOwnProperty.call(workspace().shelves,requestedShelf)){
    state.shelf=requestedShelf;
    if(['shelf-detail','shelf-detail-empty'].includes(current))current=workspace().shelves[requestedShelf].books.length?'shelf-detail':'shelf-detail-empty';
  }
  const requestedPosition=entryParams.get('position');
  if(current==='reader-scroll'&&state.book==='1342'&&['account','device'].includes(requestedPosition)){
    workspace().positions['1342']=clone((requestedPosition==='account'?state.account:state.guest).positions['1342']);
  }
  const requestedSubject=entryParams.get('subject');
  if(['explore-results','explore-empty'].includes(current)&&['Fiction','Romance','Gothic fiction','Adventure'].includes(requestedSubject)){
    state.search='';state.subject=requestedSubject;
    current=Object.values(data.catalogue).some(book=>book.subjects.includes(requestedSubject))?'explore-results':'explore-empty';
  }
  function transport(){return {book:state.book,shelf:state.shelf,shelfDraft:state.shelfDraft,shelfError:state.shelfError,shelfEditMode:state.shelfEditMode,entryId:state.entryId,draft:state.draft,removedBook:state.removedBook,deletedShelfName:state.deletedShelfName,appearance:state.appearance,appAppearance:state.appAppearance,pending:state.pending,resumeAfterDownload:state.resumeAfterDownload,workspace:state.workspace,workspaceData:workspace(),guestData:state.guest,accountData:state.account,readerQuery:state.readerQuery,readerResults:state.readerResults,search:state.search,subject:state.subject,syncStatus:state.syncStatus,deleteStatus:state.deleteStatus,pendingOperation:state.pendingOperation,importSummary:state.importSummary}}
  function hydrate(){frame.contentWindow?.postMessage({type:'veritalex:hydrate',state:transport()},'*')}
  function render(id,push=true){if(!byId.has(id))return;if(push&&current!==id)history.push(current);if(id==='sync-syncing')state.syncStatus='Syncing';current=id;select.value=id;const screen=byId.get(id);frame.title=screen.title+' · '+screen.variant+' · design prototype';frame.src=(mode==='styled'?'polished/':'wireframes/')+id+'.html?embed=1&mode='+mode+'&book='+encodeURIComponent(state.book);$('#state-label').textContent=String(data.screens.indexOf(screen)+1).padStart(2,'0')+' / '+data.screens.length+' · '+id;$('#state-title').textContent=screen.title;$('#state-notes').textContent=screen.annotations.join(' ')||'Representative '+screen.variant+' state. Changes are kept only in this prototype session.';$('#state-transitions').innerHTML=screen.transitions.map(a=>'<li><a href="#'+escape(a.to)+'" data-target="'+escape(a.to)+'" data-prototype-action="'+escape(a.id)+'">'+escape(a.label)+'<small>'+escape(a.role==='event'?'Simulated event':a.role)+' → '+escape(a.to)+'</small></a></li>').join('');$('#open-wireframe').href='wireframes/'+id+'.html';$('#back-button').disabled=history.length===0;window.history.replaceState(null,'','#'+id);$('#prototype-status').textContent='Simulated '+state.workspace+' workspace · In-memory changes reset on reload. Reader passages use the Pride and Prejudice demo.'}
  function markPending(){state.pending++;state.pendingByWorkspace[state.workspace]=state.pending;if(state.workspace==='account')state.syncStatus='Waiting to sync'}
  function capture(source,form={}){if(['journal-create','journal-edit'].includes(source)){state.draft=state.draft||{id:null,book:state.book,title:'',text:'',quote:'',reference:''};state.draft.title=form.fields?.Title??state.draft.title;state.draft.text=form.fields?.['Your thought']??state.draft.text;state.draftOrigin=source}if(['reader-appearance','settings-reader-defaults'].includes(source)){Object.assign(state.appearance,form.settings||{});for(const range of form.ranges||[]){if(range.label.toLowerCase().includes('size'))state.appearance.size=14+Math.round(range.value*.12);else state.appearance.line=24+Math.round(range.value*.13)}}}
  function newDraft(book,quote=false){const position=workspace().positions['1342']||{chapter:18,percent:28,passage:0};state.draft={id:null,book,title:'',text:'',quote:quote?(position.chapter===19?'“The next day opened a new scene at Longbourn.”':sample.quote):'',reference:quote?'Chapter '+position.chapter+' · '+position.percent+'%':'',locator:quote?clone(position):null};state.draftOrigin='journal-create'}
  function signedOut(){state.pendingByWorkspace.account=state.pending;state.workspace='guest';state.signoutAfterSync=false;state.pending=state.pendingByWorkspace.guest;return state.guest.books.length?'home-returning':'home-first'}
  function route(source,key,to,form={},book,label='',entry){
    capture(source,form);if(book&&data.catalogue[book])state.book=book;let w=workspace();
    if(key==='settings'){state.settingsReturn=source;return 'settings-main'}
    if(key==='nav-home')return w.books.length?'home-returning':'home-first';
    if(key==='nav-library'||key==='tab-books')return w.books.length?'library-books':'library-empty';
    if(key==='tab-shelves')return Object.keys(w.shelves).length?'shelves-list':'shelves-empty';
    if(key==='tab-journal')return w.entries.length?'journal-all':'journal-empty';
    if(key==='back'){
      if(source==='settings-main')return state.settingsReturn;
      if(source==='journal-create'||source==='journal-edit')return 'journal-discard';
      if(source==='journal-discard')return state.draftOrigin;
      if(source==='journal-view')return state.journalReturn;
      if(['journal-book','journal-book-empty'].includes(source))return state.bookJournalReturn||bookDestination(w,state.book);
      if(['reader-selection','reader-highlight','reader-bookmark','reader-appearance','reader-contents','reader-search','reader-search-results','reader-search-empty'].includes(source))return state.readerMode;
      if(source.startsWith('book-'))return state.bookReturn;
      if(source==='shelf-name-error')return state.shelfEditMode==='rename'?'shelf-rename':'shelf-create';
      if(source==='library-actions')return w.statuses[state.book]==='Reading'?'book-reading':w.downloaded.includes(state.book)?'book-downloaded':'book-saved';
      if(source==='shelf-add-books')return w.shelves[state.shelf]?.books.length?'shelf-detail':'shelf-detail-empty';
    }
    if(key?.startsWith('book-')&&!source.startsWith('journal-')){state.bookReturn=source;if(['book-new','book-saved','book-reading','book-downloaded'].includes(to))return bookDestination(w,state.book)}
    if(['auth-welcome','auth-error','auth-cancelled'].includes(source)&&key==='guest')return state.workspace==='account'?signedOut():state.guest.books.length?'home-returning':'home-first';
    if(source==='account-details'&&key==='sync')return state.deleteStatus?(state.deleteStatus==='deleting'?'account-deleting':'account-delete-error'):state.pending?'sync-waiting':'sync-current';
    if(source==='settings-main'&&key==='account')return state.workspace==='account'?'account-details':'sync-local';
    if(source==='home-returning'&&key==='sync')return state.workspace==='account'?(state.pending?'sync-waiting':'sync-current'):'sync-local';
    if(source==='explore-browse'&&key==='subject'){state.subject=label;state.search='';return 'explore-results'}
    if(source==='reader-search'&&key==='search'){state.readerQuery=(form.fields?.['Word or phrase']||'').trim();const passages=[{text:'Till Elizabeth entered the drawing-room at Netherfield',passage:0},{text:'Mr. Collins, awkward and solemn, apologizing instead of attending',passage:0},{text:'The moment of her release from him was ecstasy.',passage:1}];state.readerResults=state.readerQuery?passages.filter(p=>p.text.toLowerCase().includes(state.readerQuery.toLowerCase())):[];return state.readerResults.length?'reader-search-results':'reader-search-empty'}
    if(source==='reader-search-results'&&key==='result'){w.positions['1342']={chapter:18,percent:28,passage:Number(entry)||0};return state.readerMode}
    if(source==='explore-search'&&key==='submit'){state.search=form.fields?.['Title or author']||'';state.subject='';return 'explore-loading'}
    if(source==='explore-filters'&&key==='apply'){state.subject=form.settings?.subject==='Any subject'?'':form.settings?.subject||'';return 'explore-results'}
    if(source==='explore-filters'&&key==='reset'){state.subject='';return 'explore-results'}
    if(source==='settings-appearance'&&key==='save'){state.appAppearance={theme:form.radios?.[0]||'Follow system',colors:form.radios?.[1]||'Veritalex brand'};return 'settings-main'}
    if(source==='explore-empty'&&key==='filters'){state.subject='';return 'explore-results'}
    if(source==='book-new'&&key==='save'){if(w.books.includes(state.book))return bookDestination(w,state.book);w.books.push(state.book);w.statuses[state.book]='Want to read';markPending();return 'book-saved'}
    if(source==='book-downloading'&&key==='cancel')return w.books.includes(state.book)?'book-saved':'book-new';
    if(source==='book-downloading'&&key==='success'){if(!w.books.includes(state.book))w.books.push(state.book);if(!w.downloaded.includes(state.book))w.downloaded.push(state.book);w.statuses[state.book]??='Want to read';if(state.resumeAfterDownload){w.positions['1342']=state.resumeAfterDownload.position;state.resumeAfterDownload=null;state.book='1342';return state.readerMode}return 'book-downloaded'}
    if(['book-downloaded','book-reading','home-returning'].includes(source)&&['read','continue'].includes(key)){if(source==='home-returning')state.book='1342';if(state.book!=='1342')state.book='1342';if(!w.downloaded.includes(state.book))return 'book-saved';if(!w.books.includes(state.book))w.books.push(state.book);w.statuses[state.book]='Reading';w.positions['1342']??={chapter:18,percent:28,passage:0};state.readerMode=state.appearance.mode==='Paged'?'reader-paged':'reader-scroll';return state.readerMode}
    if(source==='library-actions'&&['want','reading','finished'].includes(key)){w.statuses[state.book]={want:'Want to read',reading:'Reading',finished:'Finished'}[key];if(!w.books.includes(state.book))w.books.push(state.book);markPending();return to}
    if(source==='reader-finished'&&key==='finish'){w.statuses['1342']='Finished';if(!w.books.includes('1342'))w.books.push('1342');return 'library-finished'}
    if(source==='library-rating'&&['save','clear'].includes(key)){if(key==='clear')delete w.ratings[state.book];else w.ratings[state.book]=form.rating||null;markPending();return 'library-actions'}
    if(source==='library-remove'&&key==='remove'){state.removedBook=state.book;w.books=w.books.filter(b=>b!==state.book);w.downloaded=w.downloaded.filter(b=>b!==state.book);Object.values(w.shelves).forEach(sh=>sh.books=sh.books.filter(b=>b!==state.book));markPending();return 'library-after-removal'}
    if(source==='settings-storage-confirm'&&key==='remove'){w.downloaded=[];return 'settings-storage-empty'}
    if(key?.startsWith('shelf-')&&['shelves-list','shelves-after-delete','shelves-empty'].includes(source)){state.shelf=key.slice(6);return w.shelves[state.shelf]?.books.length?'shelf-detail':'shelf-detail-empty'}
    if(source==='shelf-detail'&&key==='rename'||source==='shelf-detail-empty'&&key==='rename'){state.shelfDraft=w.shelves[state.shelf]?.name||'';state.shelfError='';state.shelfEditMode='rename'}
    if(key==='create'&&['shelves-list','shelves-empty','shelves-after-delete','shelf-membership'].includes(source)){state.shelfDraft='';state.shelfError='';state.shelfEditMode='create';return 'shelf-create'}
    if(['shelf-create','shelf-rename','shelf-name-error'].includes(source)&&['create','save','rename'].includes(key)){
      const name=(form.fields?.['Shelf name']||'').trim();const duplicate=Object.entries(w.shelves).find(([id,sh])=>sh.name.toLowerCase()===name.toLowerCase()&&!(state.shelfEditMode==='rename'&&id===state.shelf));state.shelfDraft=name;state.duplicateShelf=duplicate?.[0]||null;
      if(!name||duplicate){state.shelfError=!name?'Enter a shelf name.':'A shelf with this name already exists.';return 'shelf-name-error'}
      state.shelfError='';if(state.shelfEditMode==='rename')w.shelves[state.shelf].name=name;else{state.shelf='new-'+state.nextShelf++;w.shelves[state.shelf]={name,books:[]}}markPending();return w.shelves[state.shelf].books.length?'shelf-detail':'shelf-detail-empty'}
    if(source==='shelf-name-error'&&key==='existing'){if(state.duplicateShelf)state.shelf=state.duplicateShelf;return w.shelves[state.shelf]?.books.length?'shelf-detail':'shelf-detail-empty'}
    if(source==='shelf-add-books'&&key==='add'){w.shelves[state.shelf].books=[...new Set(form.checks||[])];markPending();return w.shelves[state.shelf].books.length?'shelf-detail':'shelf-detail-empty'}
    if(source==='shelf-membership'&&key==='save'){Object.entries(w.shelves).forEach(([id,sh])=>{sh.books=sh.books.filter(b=>b!==state.book);if(form.checks?.includes(id))sh.books.push(state.book)});markPending();return w.statuses[state.book]==='Reading'?'book-reading':'book-saved'}
    if(source==='shelf-delete'&&key==='delete'){state.deletedShelfName=w.shelves[state.shelf]?.name;delete w.shelves[state.shelf];markPending();return 'shelves-after-delete'}
    if(key==='new'&&source.startsWith('journal-')){newDraft(state.book);if(source==='journal-book'||source==='journal-book-empty'){state.journalReturn=source;return 'journal-create'}state.journalReturn='journal-all';return 'journal-book-picker'}
    if(source==='journal-book-picker'&&key?.startsWith('book-')){if(!state.draft)newDraft(state.book);state.draft.book=state.book;state.draft.quote='';state.draft.reference='';return 'journal-create'}
    if(source.startsWith('reader-')&&key==='journal'){state.book='1342';state.bookJournalReturn=state.readerMode;return w.entries.some(e=>e.book==='1342')?'journal-book':'journal-book-empty'}
    if(source==='book-reading'&&key==='journal'){state.bookJournalReturn='book-reading';return w.entries.some(e=>e.book===state.book)?'journal-book':'journal-book-empty'}
    if(source.startsWith('reader-')&&key==='note'){state.book='1342';newDraft('1342',true);state.journalReturn=state.readerMode;return 'journal-create'}
    if(key==='entry'&&source.startsWith('journal-')){state.entryId=entry||w.entries.find(e=>source==='journal-book'?e.book===state.book:true)?.id;state.journalReturn=source;return 'journal-view'}
    if(source==='journal-view'&&key==='edit'){state.draft=clone(w.entries.find(e=>e.id===state.entryId)||sample);state.book=state.draft.book;state.draftOrigin='journal-edit';return 'journal-edit'}
    if(['journal-create','journal-edit'].includes(source)&&key==='save'){const draft=state.draft;if(!draft.text.trim()&&!draft.title.trim())return source;draft.id??='entry-'+Date.now();const index=w.entries.findIndex(e=>e.id===draft.id);if(index<0)w.entries.push(clone(draft));else w.entries[index]=clone(draft);state.entryId=draft.id;markPending();return 'journal-view'}
    if(source==='journal-discard'&&key==='keep')return state.draftOrigin;
    if(source==='journal-discard'&&key==='discard'){state.draft=null;return state.journalReturn}
    if(source==='journal-delete'&&key==='delete'){w.entries=w.entries.filter(e=>e.id!==state.entryId);markPending();return w.entries.length?'journal-all':'journal-empty'}
    if(source==='journal-view'&&key==='passage'){const e=w.entries.find(e=>e.id===state.entryId);if(!e?.locator||!Number.isFinite(e.locator.chapter)||!Number.isFinite(e.locator.percent))return 'journal-view';state.book=e.book;const position=clone(e.locator);if(!w.downloaded.includes(state.book)){state.resumeAfterDownload={book:state.book,position};return 'book-saved'}w.positions['1342']=position;const highlight=w.highlights.find(h=>h.book===state.book&&h.locator?.chapter===position.chapter&&(h.locator?.passage||0)===(position.passage||0));state.activeHighlightId=highlight?.id;return highlight?'reader-highlight':state.readerMode}
    if(source==='reader-contents'&&key==='bookmark'){const saved=w.bookmarks[0];if(saved){w.positions['1342']={chapter:saved.chapter,percent:saved.percent,passage:saved.passage||0};state.activeBookmarkId=saved.id}return 'reader-bookmark'}
    if(source.startsWith('reader-')&&key==='bookmark'){const p=w.positions['1342'],id='bookmark-1342-'+p.chapter+'-'+(p.passage||0);if(w.bookmarks.some(b=>b.id===id)){w.bookmarks=w.bookmarks.filter(b=>b.id!==id);markPending();return state.readerMode}w.bookmarks.push({id,book:'1342',chapter:p.chapter,percent:p.percent,passage:p.passage||0});state.activeBookmarkId=id;markPending();return 'reader-bookmark'}
    if(source==='reader-bookmark'&&key==='remove'){const position=w.positions['1342'];w.bookmarks=w.bookmarks.filter(b=>b.id!==(state.activeBookmarkId||'bookmark-1342-'+position.chapter+'-'+(position.passage||0)));markPending();return state.readerMode}
    if(source==='reader-selection'&&key==='highlight'){const position=w.positions['1342'],id='highlight-1342-'+position.chapter+'-'+(position.passage||0);if(!w.highlights.some(h=>h.id===id))w.highlights.push({id,book:'1342',reference:'Chapter '+position.chapter,locator:clone(position),text:position.chapter===19?'The next day opened a new scene at Longbourn.':sample.quote});state.activeHighlightId=id;markPending();return 'reader-highlight'}
    if(source==='reader-highlight'&&key==='remove'){const position=w.positions['1342'];const current=w.highlights.find(h=>h.locator?.chapter===position.chapter&&(h.locator?.passage||0)===(position.passage||0));w.highlights=w.highlights.filter(h=>h.id!==(state.activeHighlightId||current?.id));markPending();return state.readerMode}
    if(source==='reader-paged'&&['next','previous'].includes(key)){const pos=w.positions['1342'];pos.passage=key==='next'?1:0;markPending();return 'reader-paged'}
    if(['reader-scroll','reader-paged'].includes(source))state.readerMode=source;
    if(source==='reader-selection'&&key==='dismiss')return state.readerMode;
    if(source==='reader-appearance'&&key==='done'){state.readerMode=state.appearance.mode==='Paged'?'reader-paged':'reader-scroll';return state.readerMode}
    if(source==='settings-reader-defaults'&&key==='save'){state.readerMode=state.appearance.mode==='Paged'?'reader-paged':'reader-scroll';return 'settings-main'}
    if(source==='sync-conflict'&&key==='use'){const account=form.radios?.some(x=>x.startsWith('Account'));w.positions['1342']=account?clone(state.account.positions['1342']):clone(state.guest.positions['1342']);state.book='1342';markPending();return state.readerMode}
    if(source==='account-details'&&key==='signout')return state.pending?'account-signout-pending':signedOut();
    if(source==='account-details'&&key==='delete'&&state.deleteStatus)return state.deleteStatus==='deleting'?'account-deleting':'account-delete-error';
    if(source==='account-signout-pending'&&key==='signout')return signedOut();
    if(source==='account-signout-pending'&&key==='sync'){state.signoutAfterSync=true;state.pendingOperation='sync';return 'sync-syncing'}
    if(source==='account-reauth'&&key==='verify'){state.deleteStatus='deleting';return 'account-deleting'}
    if(source==='account-deleting'&&key==='success'){state.account=library(true);state.pendingByWorkspace.account=0;state.deleteStatus=null;state.workspace='guest';return 'account-deleted'}
    if(source==='account-deleting'&&key==='failure'){state.deleteStatus='failed';return 'account-delete-error'}
    if(source==='sync-expired'&&key==='signin'){state.reauth=true;return 'auth-loading'}
    if(source==='auth-loading'&&key==='success'){state.pendingByWorkspace[state.workspace]=state.pending;state.workspace='account';state.pending=state.pendingByWorkspace.account;if(state.reauth){state.reauth=false;return state.pendingOperation==='restore'?'sync-restoring':'sync-syncing'}return state.guest.books.length?'auth-import-preview':state.pending?'sync-syncing':'sync-restoring'}
    if(source==='auth-import-preview'&&key==='skip'){state.workspace='account';return state.pending?'sync-syncing':'home-returning'}
    if(source==='auth-import-preview'&&key==='import'){state.pendingOperation='import';return 'auth-importing'}
    if(source==='auth-importing'&&key==='success'){const g=state.guest,a=state.account,newBooks=g.books.filter(b=>!a.books.includes(b));state.importSummary={newBooks:newBooks.length,matched:g.books.length-newBooks.length,notes:g.entries.length,highlights:g.highlights.length};a.books=[...new Set([...a.books,...g.books])];for(const bid of newBooks)a.statuses[bid]=g.statuses[bid];a.entries=[...a.entries,...g.entries.filter(e=>!a.entries.some(x=>x.id===e.id))];a.highlights=[...a.highlights,...g.highlights.filter(e=>!a.highlights.some(x=>x.id===e.id))];for(const [id,rating] of Object.entries(g.ratings))if(a.ratings[id]==null)a.ratings[id]=rating;for(const [id,sh] of Object.entries(g.shelves)){const key='guest-'+id;if(!a.shelves[key])a.shelves[key]=clone(sh)}state.pendingOperation='sync';state.syncStatus='Up to date';return 'auth-import-complete'}
    if(['auth-importing','sync-restoring','sync-syncing'].includes(source)&&key==='failure'){state.pendingOperation=source==='auth-importing'?'import':source==='sync-restoring'?'restore':'sync';state.syncStatus='Couldn’t sync';return 'sync-failed'}
    if(source==='sync-failed'&&key==='retry')return {import:'auth-importing',restore:'sync-restoring',sync:'sync-syncing'}[state.pendingOperation];
    if(['sync-syncing','sync-restoring'].includes(source)&&key==='success'){state.pending=0;state.pendingByWorkspace[state.workspace]=0;state.syncStatus='Up to date';if(state.signoutAfterSync)return signedOut();return 'sync-current'}
    return to;
  }
  function navigate(message){if(!byId.has(message.to))return;const target=route(current,message.action,message.to,message.form,message.book,message.label,message.entry);render(target)}
  window.addEventListener('message',event=>{if(event.source!==frame.contentWindow)return;if(event.data?.type==='veritalex:ready')hydrate();if(event.data?.type==='veritalex:navigate')navigate(event.data)});
  document.addEventListener('click',event=>{const a=event.target.closest('[data-prototype-action]');if(a){event.preventDefault();navigate({to:a.dataset.target,action:a.dataset.prototypeAction,form:{},label:a.textContent})}});
  select.addEventListener('change',()=>{state=fixture(select.value);history=[];render(select.value,false)});
  document.querySelectorAll('[data-mode]').forEach(button=>button.addEventListener('click',()=>{mode=button.dataset.mode;document.querySelectorAll('[data-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));render(current,false)}));
  $('#back-button').addEventListener('click',()=>{if(history.length)render(history.pop(),false)});
  $('#restart-button').addEventListener('click',()=>{state=fixture('auth-welcome');history=[];render('auth-welcome',false)});
  window.addEventListener('hashchange',()=>{const id=location.hash.slice(1);if(byId.has(id))render(id)});
  window.__veritalexPrototype={getState:()=>clone(state),navigate,fixture};
  render(current,false);
};
"""


def metadata():
    path = ROOT / "metadata.json"
    return json.loads(path.read_text()) if path.exists() else {}


def valid_local(path):
    if not path or urlsplit(path).scheme:
        return False
    resolved = (ROOT / path).resolve()
    return resolved.is_relative_to(ROOT) and resolved.is_file()


def exports():
    return [item for item in metadata().get("stitchScreens", []) if valid_local(item.get("html")) or valid_local(item.get("screenshot"))]


def shell_head(title):
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + esc(title) + '</title><link rel="stylesheet" href="package.css"></head>'


def data_scripts():
    return '<script id="package-data" type="application/json">' + payload(MANIFEST) + '</script><script src="package.js"></script>'


def gallery():
    areas = sorted({s["area"] for s in SCREENS.values()})
    variants = sorted({s["variant"] for s in SCREENS.values()})
    options = lambda xs: "".join(f'<option value="{esc(x)}">{esc(x)}</option>' for x in xs)
    exp = exports()
    total = sum(len(s["transitions"]) for s in SCREENS.values())
    out = shell_head("Veritalex · Design handoff") + '<body data-page="gallery"><main class="shell"><div class="eyebrow">Veritalex · Approved MVP design package</div><h1>A personal place to read.</h1><p class="intro">A complete state map, grayscale phone wireframes and a simulated walkthrough. Polished Stitch exports appear alongside the states they represent. This package contains design artifacts; it does not run real account, catalogue or sync services.</p><nav class="shellnav" aria-label="Package navigation"><a class="primary" href="prototype.html">Open design prototype</a><a href="#polished">Stitch exports</a><a href="#boards">Wireframe boards</a><a href="revisions/clarity-v1/index.html">Review clarity refinements</a><a href="HANDOFF.md">Handoff notes</a><a href="WIREFLOW.md">Transition map</a><a href="screens.json">State manifest</a></nav>'
    out += f'<div class="summary"><span>{len(SCREENS)} distinct screen states</span><span>{total} declared transitions</span><span>{len(MANIFEST["boards"])} related boards</span><span id="reference-count">{len(exp)} available Stitch references</span><span>412 dp · compact 360 dp</span></div>'
    out += '<section aria-labelledby="screen-heading"><h2 id="screen-heading">Browse every state</h2><div class="filterbar"><label>Search screens<input id="screen-search" type="search" placeholder="Try offline, journal, download…"></label><label>Area<select id="area-filter"><option value="">All areas</option>' + options(areas) + '</select></label><label>State<select id="state-filter"><option value="">All states</option>' + options(variants) + '</select></label></div><p id="result-count" class="result-count" aria-live="polite"></p><div class="screen-grid">'
    for screen in SCREENS.values():
        screen_exp = [x for x in exp if screen["id"] in x.get("screenIds", [])]
        search = " ".join([screen["id"], screen["title"], screen["area"], screen["variant"], *screen["annotations"]]).lower()
        out += f'<article class="screen-card" id="{esc(screen["id"])}" data-area="{esc(screen["area"])}" data-variant="{esc(screen["variant"])}" data-search="{esc(search)}"><a class="card-preview" href="wireframes/{screen["id"]}.html" aria-label="Open wireframe: {esc(screen["title"])}"><iframe loading="lazy" src="wireframes/{screen["id"]}.html?embed=preview" title="Preview of {esc(screen["id"])}" tabindex="-1" aria-hidden="true"></iframe>'
        if screen_exp:
            out += f'<span class="export-badge">Stitch export available</span>'
        out += f'</a><div class="card-copy"><div class="eyebrow">{NUMBER[screen["id"]]:02d} · {esc(screen["area"])} · {esc(screen["variant"])}</div><h3>{esc(screen["title"])}</h3><code>{esc(screen["id"])}</code><div class="card-links"><a href="wireframes/{screen["id"]}.html">Wireframe</a><a href="polished/{screen["id"]}.html">Light state design</a><a href="prototype.html#{screen["id"]}">Prototype</a>'
        for item in screen_exp[:2]:
            path = item.get("screenshot") if valid_local(item.get("screenshot")) else item["html"]
            out += f'<a data-live-reference="true" href="{esc(path)}">Stitch · {esc(item.get("variant", "design"))}</a>'
        out += "</div></div></article>"
    out += '</div><p class="no-results" id="no-results" hidden>No matching states. Clear the search or choose another area.</p></section><section id="polished" class="section"><h2>Bespoke Stitch reference screens</h2><p>These generated reference compositions are distinct from the complete manifest-based light state designs linked on every screen card.</p><button type="button" class="shellbutton" id="refresh-references">Refresh Stitch references</button><p class="result-count" id="reference-status" aria-live="polite">Showing files bundled at build time.</p>'
    if exp:
        out += '<div class="export-grid" id="stitch-export-grid">'
        for item in exp:
            image_path = item.get("screenshot")
            out += '<article class="export-card">'
            if valid_local(image_path):
                out += f'<a href="{esc(image_path)}"><img loading="lazy" src="{esc(image_path)}" alt="{esc(item.get("title", item.get("slug", "Stitch export")))} · {esc(item.get("variant", "design"))}"></a>'
            out += f'<h3>{esc(item.get("title", item.get("slug", "Stitch export")))}</h3><p>{esc(item.get("variant", "design"))} · {esc(item.get("deviceType", "phone"))}</p><div class="export-links">'
            for key, label in [("screenshot", "Screenshot"), ("html", "Stitch HTML")]:
                if valid_local(item.get(key)):
                    out += f'<a href="{esc(item[key])}">{label}</a>'
            out += '</div></article>'
        out += '</div>'
    else:
        out += '<div class="export-grid" id="stitch-export-grid"><p>Stitch exports have not been indexed yet. Rebuild this package after exports are recorded in <code>metadata.json</code>.</p></div>'
    out += '</section><section id="boards" class="section"><h2>Related wireframe boards</h2><p>Each board contains 6–8 complete phone frames, with numbered transitions outside the app. All CSS and SVG icons are inline for upload.</p><div class="boards">'
    for board in MANIFEST["boards"]:
        out += f'<article class="board-link"><strong>{esc(board["title"])}</strong><span>{len(board["screen_ids"])} phone states · {esc(board["id"])}</span><div class="card-links"><a href="boards/{board["id"]}.html">Grayscale board</a><a href="polished-boards/{board["id"]}.html">Light design board</a></div></article>'
    out += '</div></section><footer class="footer">Light state designs embed Roboto Flex for UI and Literata for book prose when the bundled font assets are present; grayscale wireframes use safe system fallbacks. Only Home, Explore and Library are primary destinations. Book text excerpt: <a href="' + esc(MANIFEST["content_source"]) + '">Project Gutenberg 1342, Chapter XVIII</a>. Private notes, guest data and sync behaviors are specified in the handoff.</footer></main>' + data_scripts() + '</body></html>'
    return out


def prototype():
    opts = "".join(f'<option value="{s["id"]}">{NUMBER[s["id"]]:02d} · {esc(s["area"])} · {esc(s["title"])} ({esc(s["variant"])})</option>' for s in SCREENS.values())
    return shell_head("Veritalex · Simulated design prototype") + '<body data-page="prototype"><main class="prototype-shell"><aside class="prototype-sidebar"><a href="index.html">← Design package</a><h1>Design prototype</h1><p class="intro-copy">Simulated interactions only. No real Google sign-in, network requests, storage, sync or deletion. Choose a screen or follow an app action.</p><label class="control">Screen state<select id="screen-select">' + opts + '</select></label><div class="control"><span>Preview mode</span><div class="mode-switch" role="group" aria-label="Preview mode"><button type="button" data-mode="wireframe" aria-pressed="true">Grayscale wireframe</button><button type="button" data-mode="styled" aria-pressed="false">Local color preview</button></div></div><p>The color preview uses the approved tokens and fallback fonts. Polished Stitch exports are in the gallery.</p><div class="prototype-footer"><button id="back-button" type="button">Previous state</button><button id="restart-button" type="button">Restart</button></div><p class="inline-status" id="prototype-status" aria-live="polite"></p><p><a id="open-wireframe" href="wireframes/auth-welcome.html">Open standalone wireframe</a></p></aside><div class="prototype-device"><iframe id="prototype-frame" src="wireframes/auth-welcome.html?embed=1" title="Veritalex design prototype"></iframe></div><aside class="prototype-inspector"><div class="state-counter" id="state-label"></div><h2 id="state-title"></h2><p id="state-notes"></p><h2>Mapped actions</h2><p>Loading outcomes and errors are explicit simulated events in this shell.</p><ul id="state-transitions"></ul></aside></main>' + data_scripts() + '</body></html>'


def board_page(board, polished=False):
    label = "Light state designs" if polished else "Grayscale wireframes"
    width = len(board["screen_ids"]) * 412 + (len(board["screen_ids"]) - 1) * 32 + 80
    css = APP_CSS + (font_css() + POLISHED_CSS if polished else "") + f'.board-page{{min-width:{width}px}}.board-grid{{grid-template-columns:repeat({len(board["screen_ids"])},412px)}}.board-header{{max-width:none}}'
    out = head(board["title"] + " · Veritalex " + label, css) + f'<body class="board-page {"styled" if polished else ""}"><header class="board-header"><div><div class="eyebrow">Veritalex · ' + label + ' · ' + esc(board["id"]) + '</div><h1>' + esc(board["title"]) + '</h1><p>412 × 915 dp phone baseline. Numbered routes below each phone refer to screen numbers across the complete package. Annotation and event controls remain outside the app. Standard navigation: Home / Explore / Library. Settings is a toolbar action.</p></div><div class="eyebrow">' + str(len(board["screen_ids"])) + ' states</div></header><main class="board-grid">'
    for sid in board["screen_ids"]:
        screen = SCREENS[sid]
        note = screen["annotations"][0] if screen["annotations"] else f'{screen["area"]} · {screen["variant"]} state'
        prefix = "../polished/" if polished else "../wireframes/"
        frame = phone(screen).replace('href="', 'href="' + prefix)
        out += f'<article class="board-frame"><h2>{NUMBER[sid]:02d} · {esc(screen["title"])}</h2><p class="stable-id">{esc(sid)} · {esc(screen["variant"])}</p>' + frame + '<div class="board-links">' + transitions(screen, prefix=prefix, compact=True) + '</div><p class="board-note">' + esc(note) + '</p></article>'
    return out + '</main><footer class="board-footer">Design prototype only. Google sign-in is optional; guest reading stays local. Shelves never own or delete books. Ratings and journals are private. Downloads, reading positions and sync states are separate. The Reader demonstration uses Pride and Prejudice, Chapter 18, 28%; passage text is verified against Project Gutenberg 1342. No page counts or community ratings are invented. Scrollable content uses Android-style internal content areas.</footer></body></html>'


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def build():
    for screen in SCREENS.values():
        write(ROOT / "wireframes" / (screen["id"] + ".html"), screen_page(screen))
        write(ROOT / "polished" / (screen["id"] + ".html"), screen_page(screen, polished=True))
    for board in MANIFEST["boards"]:
        write(ROOT / "boards" / (board["id"] + ".html"), board_page(board))
        write(ROOT / "polished-boards" / (board["id"] + ".html"), board_page(board, polished=True))
    write(ROOT / "index.html", gallery())
    write(ROOT / "prototype.html", prototype())
    write(ROOT / "package.css", PACKAGE_CSS)
    write(ROOT / "package.js", PROTOTYPE_JS + PACKAGE_JS)
    write(ROOT / "WIREFLOW.md", wireflow())


def wireflow():
    lines = ["# Veritalex MVP wireflow", "", "Stable IDs in [screens.json](screens.json) drive every state export. This is the base scenario transition map; the prototype resolves collection empties, selected identity, return context and operation recovery dynamically. Numbers match the boards. Home / Explore / Library are the primary destinations. Library contains Books / Shelves / Journal; Account & sync lives in Settings.", "", "Loading completion, network failure and provider outcomes are simulated events outside the app frame. Empty and first-use scenarios can be selected from the prototype shell.", "", "## Primary journeys", "", "1. Guest reading: `auth-welcome` → `home-first` → `explore-browse` → `explore-results` → `book-new` → `book-saved` → `book-downloading` → `book-downloaded` → `reader-scroll`.", "2. Reading and writing: `home-returning` → `reader-scroll` → `reader-selection` → `reader-highlight` → `journal-create` → `journal-view` → `reader-highlight`.", "3. Organize: `library-books` → `library-actions` → `shelf-membership` → `book-reading`; or `shelf-detail` → `shelf-add-books` → `shelf-detail`. Shelf deletion preserves the saved books.", "4. Optional account: `settings-main` → `sync-local` → `auth-loading` → `auth-import-preview` → `auth-importing` → `auth-import-complete` → `sync-conflict`.", "5. Recovery: `explore-offline` → `explore-loading`; `book-download-failed` → `book-downloading`; `sync-failed` → `sync-syncing`. Local reading stays available.", "6. Deletion: `account-details` → `account-delete-confirm` → `account-reauth` → `account-deleting` → `account-deleted`, with cancellation and failure routes.", "", "## Every state and transition", ""]
    for screen in SCREENS.values():
        sid = screen["id"]
        lines += [f'### {NUMBER[sid]:02d} · {screen["title"]} · `{sid}`', "", f'{screen["area"]} · {screen["variant"]}. [Wireframe](wireframes/{sid}.html) · [Light state design](polished/{sid}.html) · [Prototype](prototype.html#{sid})', ""]
        for a in screen["transitions"]:
            lines.append(f'- {a["label"]} ({a["role"]}) → {NUMBER[a["to"]]:02d} · `{a["to"]}`')
        for note in screen["annotations"]:
            lines.append("\nAnnotation: " + note)
        lines.append("")
    return "\n".join(lines) + "\n"


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.screen_ids = []
        self.tags = Counter()
        self.transitions = []
        self.external = []
        self.ids = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags[tag] += 1
        for attr in ("href", "src"):
            if attr in attrs:
                self.links.append(attrs[attr])
        if "data-screen-id" in attrs:
            self.screen_ids.append(attrs["data-screen-id"])
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if "data-to" in attrs:
            self.transitions.append(attrs["data-to"])
        if tag == "script" and attrs.get("src", "").startswith(("http:", "https:")):
            self.external.append(attrs["src"])


def audit():
    errors = []
    assert len(SCREENS) == len(MANIFEST["screens"]), "Duplicate screen IDs"
    ids = set(SCREENS)
    coverage = [sid for b in MANIFEST["boards"] for sid in b["screen_ids"]]
    if Counter(coverage) != Counter(ids):
        errors.append("Boards must include every state exactly once")
    for b in MANIFEST["boards"]:
        if not 6 <= len(b["screen_ids"]) <= 8:
            errors.append(f'{b["id"]}: expected 6–8 frames')
    for screen in SCREENS.values():
        keys = [a["id"] for a in screen["transitions"]]
        if len(keys) != len(set(keys)):
            errors.append(screen["id"] + ": duplicate transition keys")
        for a in screen["transitions"]:
            if a["to"] not in ids:
                errors.append(f'{screen["id"]}: unknown target {a["to"]}')
        path = ROOT / "wireframes" / (screen["id"] + ".html")
        if not path.exists():
            errors.append(f"Missing wireframe {path.name}")
            continue
        parser = Links()
        parser.feed(path.read_text())
        if parser.screen_ids != [screen["id"]]:
            errors.append(screen["id"] + ": stable ID mismatch")
        if parser.external:
            errors.append(screen["id"] + ": external script dependency")
        if set(a["to"] for a in screen["transitions"]) - set(parser.transitions):
            errors.append(screen["id"] + ": transition not represented")
    reached = {"auth-welcome"}
    queue = deque(reached)
    while queue:
        for a in SCREENS[queue.popleft()]["transitions"]:
            if a["to"] not in reached:
                reached.add(a["to"])
                queue.append(a["to"])
    # Some empty/filtered states are screen-picker scenarios rather than normal paths.
    scenario_only = sorted(ids - reached)
    files = [ROOT / "index.html", ROOT / "prototype.html", *(ROOT / "wireframes").glob("*.html"), *(ROOT / "polished").glob("*.html"), *(ROOT / "boards").glob("*.html"), *(ROOT / "polished-boards").glob("*.html")]
    for path in files:
        parser = Links()
        parser.feed(path.read_text())
        if len(parser.ids) != len(set(parser.ids)):
            errors.append(f"Duplicate HTML IDs in {path.relative_to(ROOT)}")
        if path.parent.name in ("boards", "polished-boards") and parser.tags["iframe"]:
            errors.append(f"Board must be self-contained without iframe: {path.name}")
        for ref in parser.links:
            parsed = urlsplit(ref)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (path.parent / unquote(parsed.path)).resolve()
            if not target.exists():
                errors.append(f"Broken local link {path.relative_to(ROOT)} → {ref}")
    generated_ids = {path.stem for path in (ROOT / "wireframes").glob("*.html")}
    if generated_ids != ids:
        errors.append("Wireframe directory differs from manifest coverage")
    if {p.stem for p in (ROOT / "polished").glob("*.html")} != ids:
        errors.append("Polished directory differs from manifest coverage")
    for board in MANIFEST["boards"]:
        for folder in ("boards", "polished-boards"):
            parser = Links()
            path = ROOT / folder / (board["id"] + ".html")
            parser.feed(path.read_text())
            if parser.screen_ids != board["screen_ids"]:
                errors.append(f"Board state coverage mismatch: {folder}/{path.name}")
    for filename in ("roboto-flex.woff2", "literata.woff2"):
        if not (ROOT / "assets" / filename).is_file():
            errors.append(f"Required embedded font missing: {filename}")
    for item in metadata().get("stitchScreens", []):
        for sid in item.get("screenIds", []):
            if sid not in ids:
                errors.append(f'Stitch export {item.get("slug")}: unknown screenId {sid}')
    if errors:
        raise SystemExit("AUDIT FAILED\n" + "\n".join(errors))
    print(f'PASS: {len(SCREENS)} states, {sum(len(s["transitions"]) for s in SCREENS.values())} transitions, {len(MANIFEST["boards"])} boards; all stable IDs and local links valid.')
    print(f'PASS: {len(exports())} available Stitch exports indexed; no external JS dependencies in wireframes.')
    print("Scenario-only states (open through the prototype picker): " + (", ".join(scenario_only) or "none"))


def test_prototype():
    """Focused regressions for identity, preserved writing and reader actions."""
    for sid in ("book-new", "book-saved", "book-reading", "book-downloaded"):
        content = core(SCREENS[sid])
        key = {"book-new": "download", "book-saved": "download", "book-reading": "continue", "book-downloaded": "read"}[sid]
        assert content.index(f'data-action="{key}"') < content.index('data-book-about'), sid
    for sid in ("shelf-detail", "shelf-detail-empty"):
        content = core(SCREENS[sid])
        assert '<details class="overflow">' in content and '<summary class="iconbutton" aria-label="Shelf options">' in content
        assert content.count('data-action="rename"') == content.count('data-action="delete"') == 1
    for sid in ("journal-all", "journal-book", "journal-empty", "journal-book-empty"):
        content = core(SCREENS[sid])
        assert content.count('data-action="new"') == 1 and 'data-action="passage"' not in content
    harness = r"""
const assert = require('node:assert/strict');
const vm = require('node:vm');
function scenario(initial, search = '') {
  const elements = new Map();
  const element = selector => {
    if (!elements.has(selector)) elements.set(selector, {
      value: '', listeners: {}, contentWindow: { postMessage() {} },
      addEventListener(name, handler) { this.listeners[name] = handler; }
    });
    return elements.get(selector);
  };
  const location = { hash: '#' + initial, search };
  const window = {
    addEventListener() {},
    history: { replaceState(_state, _unused, hash) { location.hash = hash; } }
  };
  const context = vm.createContext({
    window, location, URLSearchParams,
    document: { querySelector: element, querySelectorAll: () => [], addEventListener() {} }
  });
  vm.runInContext(PROTOTYPE_SOURCE, context);
  window.startVeritalexPrototype(MANIFEST_DATA);
  const model = window.__veritalexPrototype;
  return {
    state: model.getState,
    go(action, to, book, form = {}) { model.navigate({ action, to, book, form }); },
    screen() { return element('#prototype-frame').src.split('/').pop().split('.html')[0]; }
  };
}
const owned = scenario('library-books');
const newState = scenario('book-new').state().guest;
assert.equal(newState.books.includes('1342'), false);
assert.equal(newState.downloaded.includes('1342'), false);
const savedState = scenario('book-saved').state().guest;
assert.equal(savedState.statuses['1342'], 'Want to read');
assert.equal(savedState.downloaded.includes('1342'), false);
const downloadedState = scenario('book-downloaded').state().guest;
assert.equal(downloadedState.statuses['1342'], 'Want to read');
assert.equal(downloadedState.downloaded.includes('1342'), true);
assert.equal(downloadedState.positions['1342'], undefined);
assert.equal(scenario('book-saved', '?book=1342').screen(), 'book-saved');
const linkedBook = scenario('book-new', '?book=84');
assert.equal(linkedBook.state().book, '84');
assert.equal(linkedBook.screen(), 'book-saved');
assert.equal(JSON.stringify(linkedBook.state().guest), JSON.stringify(owned.state().guest));
assert.equal(scenario('book-saved', '?book=11').screen(), 'book-downloaded');
assert.equal(scenario('book-saved', '?book=1260').screen(), 'book-new');
assert.equal(scenario('book-saved', '?book=invalid').state().book, '1342');
assert.equal(scenario('book-saved', '?book=toString').state().book, '1342');
assert.equal(scenario('journal-book', '?book=84').screen(), 'journal-book-empty');
const linkedShelf = scenario('shelf-delete', '?shelf=reading-next');
assert.equal(linkedShelf.state().shelf, 'reading-next');
assert.equal(JSON.stringify(linkedShelf.state().guest), JSON.stringify(owned.state().guest));
assert.equal(scenario('shelf-rename', '?shelf=unknown').state().shelf, 'classics');
assert.equal(scenario('reader-scroll', '?book=1342&position=account').state().guest.positions['1342'].percent, 31);
assert.equal(scenario('reader-scroll', '?position=device').state().guest.positions['1342'].percent, 28);
assert.equal(scenario('reader-scroll', '?book=84&position=account').state().guest.positions['1342'].percent, 28);
assert.equal(scenario('reader-scroll', '?position=invalid').state().guest.positions['1342'].percent, 28);
const linkedSubject = scenario('explore-empty', '?subject=Gothic%20fiction');
assert.equal(linkedSubject.screen(), 'explore-results');
assert.equal(linkedSubject.state().subject, 'Gothic fiction');
assert.equal(linkedSubject.state().search, '');
assert.equal(JSON.stringify(linkedSubject.state().guest), JSON.stringify(owned.state().guest));
assert.equal(scenario('explore-results', '?subject=invalid').state().search, 'Austen');
const accountContent = scenario('home-returning', '?workspace=account');
assert.equal(accountContent.state().workspace, 'account');
assert.equal(JSON.stringify(accountContent.state().guest), JSON.stringify(owned.state().guest));
assert.equal(JSON.stringify(accountContent.state().account), JSON.stringify(scenario('account-details').state().account));
assert.equal(scenario('home-first', '?workspace=account').screen(), 'home-returning');
assert.equal(scenario('book-new', '?workspace=account').screen(), 'book-reading');
assert.equal(scenario('home-returning', '?workspace=invalid').state().workspace, 'guest');
assert.equal(scenario('auth-import-preview', '?workspace=guest').state().workspace, 'account');
const before = JSON.stringify(owned.state().guest);
owned.go('nav-explore', 'explore-browse');
owned.go('book-1342', 'book-new', '1342');
assert.equal(owned.screen(), 'book-reading');
assert.equal(owned.state().guest.statuses['1342'], 'Reading');
assert.equal(JSON.stringify(owned.state().guest), before);
assert.equal(owned.state().pending, 0);
owned.go('back', 'explore-results');
assert.equal(owned.screen(), 'explore-browse');
owned.go('book-84', 'book-new', '84');
assert.equal(owned.screen(), 'book-saved');
assert.equal(owned.state().guest.statuses['84'], 'Want to read');
owned.go('back', 'explore-results');
owned.go('book-11', 'book-new', '11');
assert.equal(owned.screen(), 'book-downloaded');
assert.equal(owned.state().guest.statuses['11'], 'Finished');
const staleNew = scenario('library-books');
staleNew.go('scenario', 'book-new');
staleNew.go('save', 'book-saved');
assert.equal(staleNew.screen(), 'book-reading');
assert.equal(staleNew.state().guest.statuses['1342'], 'Reading');
assert.equal(staleNew.state().guest.books.length, 3);
assert.equal(staleNew.state().pending, 0);
const account = scenario('account-details');
const guestBefore = JSON.stringify(account.state().guest);
account.go('nav-explore', 'explore-browse');
account.go('book-1342', 'book-new', '1342');
assert.equal(account.screen(), 'book-reading');
assert.equal(account.state().account.statuses['1342'], 'Reading');
assert.equal(JSON.stringify(account.state().guest), guestBefore);
const fresh = scenario('home-first');
fresh.go('nav-explore', 'explore-browse');
fresh.go('book-1260', 'book-new', '1260');
assert.equal(fresh.screen(), 'book-new');
fresh.go('save', 'book-saved');
assert.equal(fresh.state().guest.books.join(','), '1260');
assert.equal(fresh.state().guest.statuses['1260'], 'Want to read');
assert.equal(fresh.state().pending, 1);
const removedText = scenario('settings-storage-confirm');
removedText.go('remove', 'settings-storage-empty');
removedText.go('nav-explore', 'explore-browse');
removedText.go('book-1342', 'book-new', '1342');
assert.equal(removedText.screen(), 'book-saved');
assert.equal(removedText.state().guest.statuses['1342'], 'Reading');
assert.equal(removedText.state().guest.positions['1342'].percent, 28);
assert.equal(removedText.state().guest.entries.length, 1);
const duplicate = scenario('shelves-list');
const shelfCount = Object.keys(duplicate.state().guest.shelves).length;
duplicate.go('create', 'shelf-create');
duplicate.go('create', 'shelf-detail-empty', null, { fields: { 'Shelf name': '  Reading next  ' } });
assert.equal(duplicate.screen(), 'shelf-name-error');
duplicate.go('existing', 'shelf-detail');
assert.equal(duplicate.state().shelf, 'reading-next');
assert.equal(duplicate.screen(), 'shelf-detail');
assert.equal(Object.keys(duplicate.state().guest.shelves).length, shelfCount);
const bookmark = scenario('reader-scroll');
bookmark.go('bookmark', 'reader-bookmark');
assert.equal(bookmark.state().guest.bookmarks.length, 1);
bookmark.go('back', 'reader-scroll');
bookmark.go('bookmark', 'reader-bookmark');
assert.equal(bookmark.screen(), 'reader-scroll');
assert.equal(bookmark.state().guest.bookmarks.length, 0);
bookmark.go('journal', 'journal-book');
assert.equal(bookmark.screen(), 'journal-book');
bookmark.go('back', 'book-reading');
assert.equal(bookmark.screen(), 'reader-scroll');
const journal = scenario('journal-all');
journal.go('new', 'journal-book-picker');
journal.go('book-84', 'journal-create', '84');
journal.go('save', 'journal-view', null, { fields: { Title: 'No passage', 'Your thought': 'A note written from Journal.' } });
assert.equal(journal.screen(), 'journal-view');
const writing = JSON.stringify(journal.state().guest.entries);
journal.go('passage', 'reader-highlight');
assert.equal(journal.screen(), 'journal-view');
assert.equal(JSON.stringify(journal.state().guest.entries), writing);
const imported = scenario('auth-import-preview');
imported.go('import', 'auth-importing');
imported.go('success', 'auth-import-complete');
const added = JSON.stringify(imported.state().account);
imported.go('back', 'auth-import-preview');
imported.go('import', 'auth-importing');
imported.go('success', 'auth-import-complete');
assert.equal(JSON.stringify(imported.state().account), added);
console.log('PASS: owned-book routing preserves Reading/Want/Finished status, downloads and workspace; stale Save is idempotent; new additions still save once; duplicate shelf opens matching identity.');
console.log('PASS: book actions precede About; shelf overflow owns Rename/Delete; Journal has one New entry and no fabricated passage; bookmark toggles and retried import preserve records.');
"""
    source = "const PROTOTYPE_SOURCE=" + json.dumps(PROTOTYPE_JS) + ";\nconst MANIFEST_DATA=" + json.dumps(MANIFEST) + ";\n" + harness
    subprocess.run(["node", "-"], input=source, text=True, check=True, cwd=ROOT)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Audit existing files without rebuilding")
    parser.add_argument("--test-prototype", action="store_true", help="Run focused identity regressions in Node's VM")
    args = parser.parse_args()
    if not args.check:
        build()
    audit()
    if args.test_prototype:
        test_prototype()
