"""Build only the eleven bespoke dark/tablet clarity references."""

from base64 import b64encode
from html import escape
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
FONT = {
    name: b64encode((ROOT / "assets" / file).read_bytes()).decode()
    for name, file in [("Roboto Flex", "roboto-flex.woff2"), ("Literata", "literata.woff2")]
}

ICONS = {
    "back": '<path d="m12 5-7 7 7 7M5 12h14"/>',
    "home": '<path d="m3 10 9-7 9 7v10H7V10m3 10v-7h4v7"/>',
    "explore": '<circle cx="12" cy="12" r="9"/><path d="m16 8-2.5 5.5L8 16l2.5-5.5Z"/>',
    "library": '<path d="M4 4v16M8 4v16M12 4v16m4-15 5 14"/>',
    "settings": '<path d="m9 3-1 3-3 1-2 3 2 2v3l3 1 1 3h4l1-3 3-1 1-3 2-2-2-3-3-1-1-3Z"/><circle cx="11" cy="11" r="3"/>',
    "cloud": '<path d="M6 18a4 4 0 0 1-.5-8A6.5 6.5 0 0 1 18 9a4.5 4.5 0 0 1 0 9H6Z"/><path d="m9 13 2 2 4-4"/>',
    "book": '<path d="M3 4h6a3 3 0 0 1 3 3 3 3 0 0 1 3-3h6v15h-6a3 3 0 0 0-3 2 3 3 0 0 0-3-2H3ZM12 7v14"/>',
    "addbook": '<path d="M4 4h12v16H4Zm15 4v8m-4-4h8"/>',
    "download": '<path d="M12 3v12m-5-5 5 5 5-5M4 17v4h16v-4"/>',
    "check": '<path d="m5 12 4 4L19 6"/>',
    "chevron": '<path d="m9 5 7 7-7 7"/>',
    "search": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
    "more": '<circle cx="12" cy="5" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="12" cy="19" r="1"/>',
    "shelf": '<path d="M3 20h18M4 4v12h4V4Zm7 0v12h4V4Zm6 1 3-1 3 11-3 1Z"/>',
    "journal": '<path d="M4 3h15v18H4Zm3 5h8m-8 4h8m-8 4h5"/>',
    "plus": '<path d="M12 4v16M4 12h16"/>',
    "bookmark": '<path d="M6 3h12v18l-6-4-6 4Z"/>',
    "type": '<path d="m4 19 6-14 6 14M6 14h8m3-4h6m-3 0v9"/>',
    "contents": '<path d="M8 6h13M8 12h13M8 18h13M3 6h.1M3 12h.1M3 18h.1"/>',
    "hide": '<path d="m3 3 18 18M10 5h2c5 0 9 7 9 7a19 19 0 0 1-4 4M6 6a20 20 0 0 0-4 6s4 7 10 7c2 0 4-1 5-2M9 9a4 4 0 0 0 6 6"/>',
    "show": '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>',
    "palette": '<path d="M12 3a9 9 0 1 0 0 18h2a2 2 0 0 0 0-4h-1a1 1 0 0 1 0-2h3a5 5 0 0 0 5-5c0-4-4-7-9-7Z"/><path d="M7 9h.1M10 6h.1M15 7h.1M6 14h.1"/>',
    "phone": '<rect x="6" y="2" width="12" height="20" rx="2"/><path d="M10 18h4"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v6m0-10v.1"/>',
    "logout": '<path d="M9 4H4v16h5m5-13 5 5-5 5M8 12h11"/>',
    "edit": '<path d="m4 16-1 5 5-1L20 8l-4-4Z"/>',
    "star": '<path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1.1 6.2-5.6-3-5.6 3 1.1-6.2L3 9.6l6.2-.9Z"/>',
}


def icon(name, cls=""):
    return f'<svg class="icon {cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'


def link(state, text, cls="", name=None, book=None, shelf=None, subject=None, workspace=None):
    label = f' aria-label="{escape(name, quote=True)}"' if name else ""
    params = {key: value for key, value in [("book", book), ("shelf", shelf), ("subject", subject), ("workspace", workspace)] if value}
    query = "?" + urlencode(params) if params else ""
    return f'<a href="../prototype.html{query}#{state}" class="{cls}"{label}>{text}</a>'


def action(state, text, sym=None, cls="primary"):
    return link(state, (icon(sym) if sym else "") + f'<span>{text}</span>', f"button {cls}")


def tool(state, sym, name, workspace=None):
    return link(state, icon(sym), "icon-button", name, workspace=workspace)


BOOKS = [
    ("1342", "Pride and Prejudice", "Jane Austen", "#4A2228", "#F6DED8"),
    ("84", "Frankenstein", "Mary Shelley", "#263E33", "#E0E9D9"),
    ("11", "Alice’s Adventures in Wonderland", "Lewis Carroll", "#24354F", "#E5E9F5"),
    ("1260", "Jane Eyre", "Charlotte Brontë", "#473629", "#F5E6CC"),
]


def cover(index=0, cls=""):
    ident, title, author, bg, ink = BOOKS[index]
    return f'<div class="cover {cls}" style="--cover:{bg};--cover-ink:{ink}" aria-hidden="true"><span class="cover-id">GUTENBERG {ident}</span><span class="cover-title">{title}</span><span class="cover-author">{author}</span></div>'


def statusbar(tablet=False):
    return '<div class="system-bar" aria-hidden="true"><span>' + ("10:42" if tablet else "9:41") + '</span><span class="system-icons">▴ ≋ ▰</span></div>'


def nav(selected="Home", rail=False):
    dests = [("Home", "home-returning", "home"), ("Explore", "explore-browse", "explore"), ("Library", "library-books", "library")]
    items = []
    for title, state, sym in dests:
        selected_attr = ' aria-current="page"' if selected == title else ""
        items.append(f'<a href="../prototype.html#{state}"{selected_attr}>{icon(sym)}<span>{title}</span></a>')
    if rail:
        return f'<aside class="rail"><div class="rail-brand" aria-label="Veritalex">{icon("book")}<span>Veritalex</span></div><nav aria-label="Main navigation">{"".join(items)}</nav>{link("settings-main", icon("settings") + "<span>Settings</span>", "rail-settings")}</aside>'
    return '<nav class="bottom-nav" aria-label="Main navigation">' + "".join(items) + '</nav><div class="gesture" aria-hidden="true"></div>'


def appbar(title, back=None, sync=False, settings=True, workspace=None):
    start = tool(back, "back", "Back", workspace=workspace) if back else ""
    end = (link("account-details", icon("cloud") + '<span>Up to date</span>', "sync-status", "Up to date", workspace=workspace) if sync else "")
    if settings:
        end += tool("settings-main", "settings", "Settings", workspace=workspace)
    return f'<header class="app-bar"><div class="app-title">{start}<h1>{title}</h1></div><div class="app-actions">{end}</div></header>'


def tabs(selected="Books"):
    values = [("Books", "library-books"), ("Shelves", "shelves-list"), ("Journal", "journal-all")]
    return '<nav class="tabs" aria-label="Library sections">' + ''.join(f'<a href="../prototype.html#{state}"' + (' aria-current="page"' if name == selected else '') + f'>{name}</a>' for name, state in values) + '</nav>'


def filters():
    return '<nav class="chips" aria-label="Filter books">' + ''.join(link(s, (icon("check") if t == "All" else "") + t, "chip" + (" selected" if t == "All" else "")) for t, s in [("All", "library-books"), ("Want to read", "library-want"), ("Reading", "library-reading"), ("Finished", "library-finished"), ("Downloaded", "library-downloaded")]) + '</nav>'


def progress(value=28):
    return f'<div class="progress" role="progressbar" aria-label="Reading progress" aria-valuemin="0" aria-valuemax="100" aria-valuenow="{value}"><span style="width:{value}%"></span></div>'


def current_book():
    return f'<section class="current-book"><div class="current-identity">{cover()}<div><h2>Pride and Prejudice</h2><p class="muted">Jane Austen</p><p class="position">Chapter 18 · 28% read</p>{progress()}<p class="availability">{icon("download")}Downloaded on this device</p></div></div>{action("reader-scroll", "Continue reading", "book")}</section>'


def saved_books():
    cards = []
    for i, state, detail in [(1, "book-saved", "Want to read"), (2, "book-downloaded", "Finished · Downloaded")]:
        _, title, author, _, _ = BOOKS[i]
        cards.append(link(state, cover(i) + f'<h3>{title}</h3><p class="muted">{author}</p><p class="book-state">{detail}</p>', "saved-book", book=BOOKS[i][0]))
    return '<section class="saved-section"><div class="section-head"><h2>Your books</h2>' + link("library-books", "See all", "text-action") + '</div><div class="saved-grid">' + ''.join(cards) + '</div></section>'


def home(tablet=False):
    feed = current_book() + saved_books()
    if not tablet:
        return phone("Veritalex", '<div class="page home-page">' + feed + '</div>', "Home", sync=True)
    shelves = '<aside class="home-shelves"><div class="section-head"><h2>Your shelves</h2>' + link("shelves-list", "See all", "text-action") + '</div>'
    for title, count, shelf_id in [("Classics", 2, "classics"), ("Reading next", 1, "reading-next")]:
        shelves += link("shelf-detail", icon("shelf") + f'<span><strong>{title}</strong><small>{count} {"book" if count == 1 else "books"}</small></span>' + icon("chevron"), "shelf-row", shelf=shelf_id)
    shelves += '</aside>'
    return tablet_shell("Home", '<main class="tablet-home"><div class="home-feed">' + feed + '</div>' + shelves + '</main>', "Home")


def book_row(i, selected=False, tablet=False):
    _, title, author, _, _ = BOOKS[i]
    states = ["book-reading", "book-saved", "book-downloaded", "book-saved"]
    status = ["Reading · 28%", "Want to read", "Finished", "Want to read"]
    available = ['Downloaded', '', 'Downloaded', '']
    body = cover(i, "mini") + f'<span class="row-meta"><strong>{title}</strong><span class="muted">{author}</span><span class="row-state">{status[i]}</span>'
    if i == 0:
        body += progress(28)
    if available[i]:
        body += f'<span class="availability">{icon("download")}{available[i]}</span>'
    body += '</span>' + icon("chevron")
    return link(states[i], body, "book-row" + (" selected-row" if selected else ""), book=BOOKS[i][0])


def library(tablet=False):
    rows = ''.join(book_row(i, tablet and i == 0, tablet) for i in range(3))
    if not tablet:
        return phone("Library", tabs() + filters() + '<main class="page library-page"><p class="list-count">3 books</p>' + rows + '<p class="source-note">Books from Project Gutenberg</p></main>', "Library", sync=True)
    detail = '<section class="book-detail-pane"><div class="detail-identity">' + cover(0, "large") + '<div><h1>Pride and Prejudice</h1><p class="author muted">Jane Austen</p><p class="subjects">English · Fiction · Romance</p><div class="reading-state"><p>Chapter 18 · 28% read</p>' + progress() + '<p class="availability">' + icon("download") + 'Downloaded on this device</p></div>' + action("reader-scroll", "Continue reading", "book") + '</div></div>'
    detail += '<section class="organization"><h2>In your library</h2><div class="organization-row"><span>Reading status</span>' + link("library-actions", 'Reading' + icon("chevron"), "text-action") + '</div><div class="organization-row"><span>Shelves</span>' + link("shelf-membership", 'Add to shelves' + icon("chevron"), "text-action") + '</div><div class="organization-row"><span>Your private rating</span>' + link("library-rating", icon("star", "filled") * 4 + icon("star") + '<span class="sr-only">4 out of 5 stars. Change rating</span>', "rating-link") + '</div></section>'
    detail += '<section class="about"><h2>About</h2><p>A novel of manners, family, and marriage in nineteenth-century England, following the turbulent relationship between Elizabeth Bennet and Fitzwilliam Darcy.</p><p class="source-note">Project Gutenberg · Book 1342</p></section>'
    detail += '<section class="book-journal"><div class="section-head"><h2>Journal</h2>' + link("journal-book", "View entry", "text-action") + '</div><p class="muted">Chapter 18</p><blockquote>“The moment of her release from him was ecstasy.”</blockquote><p>Elizabeth&#39;s relief says more than her politeness ever could.</p></section></section>'
    return tablet_shell("Library", tabs() + '<main class="library-split"><section class="library-list">' + filters() + '<p class="list-count">3 books</p>' + rows + '</section>' + detail + '</main>', "Library")


def book_details():
    body = '<main class="page new-book"><section class="new-book-identity">' + cover(0, "large") + '<h2>Pride and Prejudice</h2><p class="author muted">Jane Austen</p><p class="subjects">English · Fiction · Romance</p></section><section class="book-actions">' + action("book-downloading", "Download to read", "download") + action("book-saved", "Want to read", "addbook", "tonal") + '</section><section class="about"><h2>About</h2><p>A novel of manners, family, and marriage in nineteenth-century England, following the turbulent relationship between Elizabeth Bennet and Fitzwilliam Darcy.</p><p class="source-note">Project Gutenberg · Book 1342</p></section></main>'
    return phone("Book details", body, None, back="explore-browse", settings=False)


def explore():
    search = link("explore-search", icon("search") + '<span>Search books or authors</span>', "search-field")
    subjects = '<section><h2>Subjects</h2><div class="subject-grid">' + ''.join(link("explore-results", s, "subject-chip", subject=s) for s in ["Fiction", "Romance", "Gothic fiction", "Adventure"]) + '</div></section>'
    rows = ''
    for i in [0, 1, 2, 3]:
        _, title, author, _, _ = BOOKS[i]
        rows += link("book-new", cover(i, "mini") + f'<span class="row-meta"><strong>{title}</strong><span class="muted">{author}</span></span>' + icon("chevron"), "book-row catalogue-row", book=BOOKS[i][0])
    return phone("Explore", '<main class="page explore-page">' + search + subjects + '<section><h2>Books</h2>' + rows + '<p class="source-note">Public domain books from Project Gutenberg</p></section></main>', "Explore")


def setting_row(state, sym, title, value=None, workspace=None):
    text = f'<span><strong>{title}</strong>' + (f'<small>{value}</small>' if value else '') + '</span>'
    return link(state, icon(sym) + text + icon("chevron"), "setting-row", workspace=workspace)


def settings():
    body = '<main class="page settings-page"><section><h2>Account</h2><div class="identity"><span class="avatar">R</span><span><strong>Reader</strong><small>reader@example.com</small></span></div>' + setting_row("account-details", "cloud", "Account & sync", "Up to date", workspace="account") + '</section>'
    body += '<section><h2>Appearance</h2>' + setting_row("settings-appearance", "palette", "App theme", "Dark", workspace="account") + '<label class="setting-row switch-row">' + icon("palette") + '<strong>Use wallpaper colors</strong><input type="checkbox" checked aria-label="Use wallpaper colors"><span class="switch" aria-hidden="true"></span></label></section>'
    body += '<section><h2>Reading</h2>' + setting_row("settings-reader-defaults", "book", "Reader defaults", "Scroll · Literata", workspace="account") + '<label class="setting-row switch-row">' + icon("phone") + '<strong>Keep screen awake</strong><input type="checkbox" aria-label="Keep screen awake while reading"><span class="switch" aria-hidden="true"></span></label></section>'
    body += '<section><h2>Storage</h2>' + setting_row("settings-storage", "download", "Downloads", "2 books on this device", workspace="account") + '</section><section><h2>About</h2>' + setting_row("settings-about", "info", "Veritalex", "Version 1.0.4", workspace="account") + setting_row("settings-about", "library", "Content sources", "Project Gutenberg", workspace="account") + setting_row("settings-about", "info", "Privacy", workspace="account") + '</section></main>'
    return phone("Settings", body, None, back="home-returning", settings=False, workspace="account")


def account():
    body = '<main class="page account-page"><div class="identity"><span class="avatar">R</span><span><strong>Reader</strong><small>reader@example.com</small></span><span class="provider">Google</span></div><section class="account-status">' + icon("cloud") + '<span><strong>Up to date</strong><small>Just now</small></span></section><p class="muted device-note">Downloaded book text stays on each device.</p><div class="account-destinations">' + setting_row("library-books", "library", "Library", workspace="account") + setting_row("shelves-list", "shelf", "Shelves", workspace="account") + setting_row("journal-all", "journal", "Journal", workspace="account") + '</div><div class="account-actions">' + action("account-signout-pending", "Sign out", "logout", "outline") + link("account-delete-confirm", "Delete account", "danger-action") + '</div></main>'
    return phone("Account & sync", body, None, back="settings-main", settings=False, workspace="account")


P1 = "When the dancing recommenced, however, and Darcy approached to claim her hand, Charlotte could not help cautioning her in a whisper, not to be a simpleton, and allow her fancy for Wickham to make her appear unpleasant in the eyes of a man of ten times his consequence. Elizabeth made no answer, and took her place in the set, amazed at the dignity to which she was arrived in being allowed to stand opposite to Mr. Darcy, and reading in her neighbours' looks their equal amazement in beholding it."
P2 = 'They stood for some time without speaking a word; and she began to imagine that their silence was to last through the two dances, and, at first, was resolved not to break it; till suddenly fancying that it would be the greater punishment to her partner to oblige him to talk, she made some slight observation on the dance. He replied, and was again silent. After a pause of some minutes, she addressed him a second time, with--'


def reader_tools():
    return '<nav class="reader-tools" aria-label="Reading tools">' + ''.join(link(state, icon(sym) + f'<span>{label}</span>', "reader-tool") for state, sym, label in [("reader-contents", "contents", "Contents"), ("reader-appearance", "type", "Appearance"), ("reader-search", "search", "Search"), ("journal-book", "journal", "Journal")]) + '</nav>'


def reader(tablet=False):
    head = '<header class="reader-header reader-controls">' + tool("book-reading", "back", "Back to book") + '<div><h1>Pride and Prejudice</h1><p>Chapter 18</p></div><button type="button" class="icon-button bookmark-button" aria-pressed="true" aria-label="Remove bookmark">' + icon("bookmark", "filled") + '</button><button type="button" class="icon-button hide-controls" aria-label="Hide reading controls">' + icon("hide") + '</button></header>'
    prose = '<article class="reader-prose" aria-label="Chapter 18"><h2>Chapter 18</h2><p>' + P1 + '</p><p>' + P2 + '</p></article>'
    foot = '<footer class="reader-footer reader-controls"><div class="reader-position"><span>Chapter 18</span><span>28% read</span></div>' + progress() + reader_tools() + '</footer>'
    show = '<button type="button" class="icon-button show-controls" aria-label="Show reading controls" hidden>' + icon("show") + '</button>'
    if tablet:
        contents = '<aside class="contents-pane reader-controls"><div class="contents-tabs" aria-label="Contents panel"><button type="button" data-panel="contents-list" aria-pressed="true">Contents</button><button type="button" data-panel="bookmarks-list" aria-pressed="false">Bookmarks</button></div><div id="contents-list"><p class="pane-label">Pride and Prejudice</p>'
        for chapter in range(16, 22):
            contents += '<div class="chapter-row current" aria-current="location">' + icon("book") + f'<span>Chapter {chapter}</span></div>' if chapter == 18 else link("reader-contents", icon("book") + f'<span>Chapter {chapter}</span>', "chapter-row")
        contents += '</div><div id="bookmarks-list" hidden><div data-bookmark-saved><p class="pane-label">Saved passage</p>' + link("reader-bookmark", icon("bookmark", "filled") + '<span>Chapter 18<small>28% read</small></span>', "chapter-row current", book="1342") + '</div><p class="pane-label" data-bookmark-empty role="status" hidden>No bookmarks yet</p></div></aside>'
        return '<div class="tablet reader tablet-reader">' + statusbar(True) + head + '<main class="reader-split">' + contents + '<div class="reading-pane">' + prose + foot + '</div></main>' + show + '<div class="gesture" aria-hidden="true"></div></div>'
    return '<div class="phone reader">' + statusbar() + head + '<main class="reading-pane">' + prose + '</main>' + foot + show + '<div class="gesture" aria-hidden="true"></div></div>'


def journal():
    note = "Elizabeth's relief says more than her politeness ever could. Even in early nineteenth-century ballroom decorum, Austen captures physical dread transforming into sheer bodily freedom the instant an unwanted obligation concludes."
    entries = '<section class="journal-list"><div class="journal-list-head"><p>3 entries</p>' + action("journal-book-picker", "New entry", "plus") + '</div><nav class="chips" aria-label="Filter journal">' + link("journal-all", icon("check") + "All books", "chip selected") + link("journal-book", "Pride and Prejudice", "chip") + '</nav>'
    data = [("Pride and Prejudice", "Today · Chapter 18", '“The moment of her release from him was ecstasy.”', "Elizabeth's relief says more than her politeness ever could."), ("Frankenstein", "Yesterday · Vol. 2, Ch. 1", '', '"Who is responsible for what we create? Victor abandons his creature the second it fails to resemble his ideal imagination."'), ("Alice’s Adventures in Wonderland", "Oct 14 · Chapter 2", '“Curiouser and curiouser!” cried Alice (she was so much surprised, that for the moment she quite forgot how to speak good English).', '')]
    for i, (title, when, quote, text) in enumerate(data):
        content = f'<strong>{title}</strong><small>{when}</small>'
        if quote:
            content += f'<blockquote>{quote}</blockquote>'
        if text:
            content += f'<p>{text}</p>'
        entries += link("journal-view", content, "journal-entry selected-row") if i == 0 else '<article class="journal-entry">' + content + '</article>'
    entries += '</section>'
    detail = '<section class="journal-detail"><div class="section-head"><p class="muted">Today, 9:15 AM</p><div class="detail-tools">' + tool("journal-edit", "edit", "Edit entry") + '<details class="overflow"><summary class="icon-button" aria-label="Entry options">' + icon("more") + '</summary><div class="disclosure-actions">' + link("journal-delete", "Delete entry", "danger") + '</div></details></div></div><div class="journal-book-identity">' + cover(0, "mini") + '<div><h1>Pride and Prejudice</h1><p class="muted">Jane Austen</p><p class="entry-locator">Chapter 18</p></div></div><section class="entry-writing"><blockquote>“The moment of her release from him was ecstasy.”</blockquote><p>' + note + '</p></section>' + action("reader-scroll", "Return to passage", "book", "tonal") + '</section>'
    return tablet_shell("Library", tabs("Journal") + '<main class="journal-split">' + entries + detail + '</main>', "Library")


def phone(title, body, selected, back=None, sync=False, settings=True, workspace=None):
    return '<div class="phone">' + statusbar() + appbar(title, back, sync, settings, workspace) + body + (nav(selected) if selected else '<div class="gesture" aria-hidden="true"></div>') + '</div>'


def tablet_shell(title, body, selected):
    return '<div class="tablet">' + statusbar(True) + '<div class="tablet-work">' + nav(selected, True) + '<div class="tablet-canvas">' + appbar(title, sync=True, settings=False) + body + '</div></div><div class="gesture" aria-hidden="true"></div></div>'


CSS = r'''
*{box-sizing:border-box}html,body{margin:0;min-height:100%;font-family:"Roboto Flex",sans-serif}body{background:var(--surface);color:var(--ink);font-size:16px;line-height:1.5}body{--surface:#FFF8F3;--low:#FCF1E8;--container:#F5E9DF;--high:#EEE1D5;--ink:#241A14;--muted:#55483D;--primary:#895021;--on-primary:#FFF;--tonal:#FFDCBF;--on-tonal:#2D1606;--line:#D7C3B4;--error:#BA1A1A}.dark body{--surface:#19120D;--low:#231A14;--container:#2D231C;--high:#382D25;--ink:#F0DFD6;--muted:#D6C3B7;--primary:#FFB77F;--on-primary:#4E2600;--tonal:#6D3A0D;--on-tonal:#FFDCBF;--line:#52443B;--error:#FFB4AB;color-scheme:dark}a{color:inherit;text-decoration:none}button,input{font:inherit}button{color:inherit;cursor:pointer}a,button,label,summary{-webkit-tap-highlight-color:transparent}a:focus-visible,button:focus-visible,summary:focus-visible,input:focus-visible{outline:3px solid var(--primary);outline-offset:3px}h1,h2,h3,p,blockquote{margin:0}h1{font-size:24px;line-height:32px;font-weight:500}h2{font-size:20px;line-height:28px;font-weight:500}h3,strong{font-size:16px;line-height:24px;font-weight:500}small{display:block;font-size:14px;line-height:20px;color:var(--muted)}.muted{color:var(--muted)}.icon{width:24px;height:24px;flex:none;vertical-align:middle}.icon.filled{fill:currentColor}.icon-button{width:48px;height:48px;min-width:48px;border:0;background:transparent;display:inline-flex;align-items:center;justify-content:center;border-radius:50%}.icon-button:hover{background:var(--container)}.button{min-height:48px;display:inline-flex;justify-content:center;align-items:center;gap:8px;padding:12px 20px;border-radius:100px;font-size:14px;line-height:20px;font-weight:500;border:1px solid transparent;text-align:center}.primary{background:var(--primary);color:var(--on-primary)}.tonal{background:var(--tonal);color:var(--on-tonal)}.outline{border-color:var(--line);background:transparent}.text-action{min-width:48px;min-height:48px;display:inline-flex;align-items:center;gap:4px;color:var(--primary);font-size:14px;font-weight:500;padding:8px 4px;flex:none}.text-action .icon{width:20px;height:20px}.system-bar{height:28px;flex:none;padding:4px 24px;display:flex;align-items:center;justify-content:space-between;font-size:12px;font-weight:500}.system-icons{letter-spacing:3px}.phone{width:min(100%,412px);height:100dvh;min-height:600px;margin:auto;display:flex;flex-direction:column;position:relative;overflow:hidden;background:var(--surface)}.app-bar{height:64px;flex:none;display:flex;align-items:center;justify-content:space-between;padding:0 12px 0 20px;gap:8px}.app-title,.app-actions{display:flex;align-items:center;min-width:0}.app-title h1{white-space:nowrap}.app-title .icon-button{margin-left:-12px;margin-right:4px}.sync-status{display:inline-flex;align-items:center;gap:6px;font-size:12px;line-height:18px;color:var(--muted);min-height:48px}.sync-status .icon{width:18px;height:18px}.phone .sync-status{width:48px;justify-content:center}.phone .sync-status span{display:none}.phone .sync-status .icon{width:22px;height:22px}.phone .app-actions{gap:8px}.page{flex:1;min-height:0;overflow-y:auto;padding:16px 20px 24px;scrollbar-width:none}.page::-webkit-scrollbar{display:none}.bottom-nav{height:76px;flex:none;display:flex;justify-content:space-around;background:var(--container);padding:8px}.bottom-nav a{width:96px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;font-size:12px;font-weight:500}.bottom-nav .icon{box-sizing:content-box;width:24px;height:24px;padding:4px 20px;border-radius:24px}.bottom-nav a[aria-current] .icon{background:var(--tonal);color:var(--on-tonal);fill:currentColor;fill-opacity:.15}.gesture{height:16px;flex:none;display:flex;align-items:center;justify-content:center;background:var(--container)}.gesture:after{content:"";height:4px;width:108px;border-radius:4px;background:var(--muted);opacity:.4}.phone>.gesture:only-child{background:var(--surface)}.current-book{padding:20px;background:var(--low);border-radius:16px}.current-identity{display:flex;gap:16px;align-items:center;margin-bottom:20px}.current-identity>div:last-child{min-width:0}.current-identity h2{font-size:20px;line-height:28px}.current-identity .muted{font-size:14px;margin-top:4px}.current-book .button{width:100%}.cover{width:96px;aspect-ratio:2/3;flex:none;background:var(--cover);color:var(--cover-ink);border-radius:4px;display:flex;flex-direction:column;justify-content:space-between;padding:12px 9px;text-align:center;position:relative;box-shadow:0 2px 5px #0002}.cover:before{content:"";position:absolute;inset:5px;border:1px solid currentColor;opacity:.25;pointer-events:none}.cover-id{font-size:6px;line-height:10px;letter-spacing:.7px;opacity:.75}.cover-title{font-family:Literata,serif;font-size:12px;line-height:17px;font-weight:500}.cover-author{font-family:Literata,serif;font-size:8px;line-height:12px;font-style:italic;opacity:.85}.cover.mini{width:58px;padding:8px 6px}.mini .cover-title{font-size:8px;line-height:11px}.mini .cover-id{font-size:4px;letter-spacing:.3px;line-height:7px}.mini .cover-author{font-size:6px;line-height:8px}.cover.large{width:144px;padding:18px 14px}.large .cover-title{font-size:18px;line-height:26px}.large .cover-id{font-size:8px;line-height:12px}.large .cover-author{font-size:11px;line-height:16px}.position{font-size:14px;margin:18px 0 8px;color:var(--muted)}.progress{height:4px;background:var(--line);border-radius:8px;overflow:hidden}.progress>span{display:block;height:100%;background:var(--primary);border-radius:8px}.availability{display:flex;align-items:center;gap:4px;color:var(--muted);font-size:12px;line-height:18px;margin-top:9px}.availability .icon{width:14px;height:14px}.saved-section{margin-top:24px}.section-head{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:12px}.saved-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.saved-book{min-width:0}.saved-book .cover{width:100%;max-width:136px}.saved-book h3{font-size:14px;line-height:20px;margin-top:10px}.saved-book .muted{font-size:12px;line-height:18px;margin-top:2px}.book-state{font-size:12px;line-height:18px;margin-top:8px;color:var(--muted)}.source-note{font-size:12px;line-height:18px;color:var(--muted);margin-top:20px}.tabs{display:flex;flex:none;min-height:48px;border-bottom:1px solid var(--line);padding:0 20px;gap:24px}.tabs a{min-width:48px;justify-content:center;position:relative;min-height:48px;display:flex;align-items:center;padding:8px 4px;font-size:14px;font-weight:500;color:var(--muted)}.tabs a[aria-current]{color:var(--primary)}.tabs a[aria-current]:after{content:"";height:3px;border-radius:3px 3px 0 0;position:absolute;bottom:0;left:0;right:0;background:var(--primary)}.chips{display:flex;gap:8px;overflow-x:auto;flex:none;padding:12px 20px;scrollbar-width:none}.chip{min-height:48px;display:inline-flex;align-items:center;gap:6px;white-space:nowrap;font-size:14px;border:1px solid var(--line);padding:8px 14px;border-radius:12px}.chip .icon{width:18px;height:18px}.chip.selected{background:var(--tonal);color:var(--on-tonal);border-color:transparent}.list-count{font-size:14px;color:var(--muted);margin-bottom:8px}.library-page{padding-top:0}.book-row{display:flex;align-items:center;gap:14px;padding:16px 0;border-bottom:1px solid var(--line);min-height:118px}.book-row>.icon{width:20px;height:20px;color:var(--muted)}.row-meta{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}.row-meta strong{font-size:16px;line-height:22px}.row-meta>.muted{font-size:14px;line-height:20px}.row-state{font-size:12px;line-height:18px;color:var(--primary);margin-top:8px}.row-meta .progress{margin-top:5px;max-width:260px}.row-meta .availability{margin-top:4px}.new-book-identity{display:flex;flex-direction:column;align-items:center;text-align:center;gap:8px}.new-book-identity .cover{margin-bottom:12px}.new-book-identity h2{font-size:24px;line-height:32px}.author{font-size:16px}.subjects{font-size:14px;line-height:20px;color:var(--muted);margin-top:6px}.book-actions{display:grid;gap:12px;margin-top:24px}.about{padding-top:24px;margin-top:24px;border-top:1px solid var(--line)}.about p{font-size:14px;line-height:22px;color:var(--muted);margin-top:12px}.about .source-note{font-size:12px}.search-field{display:flex;align-items:center;gap:14px;min-height:56px;border-radius:28px;background:var(--container);padding:12px 20px;color:var(--muted);margin-bottom:24px}.subject-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin:14px 0 28px}.subject-chip{display:flex;align-items:center;justify-content:center;min-height:48px;padding:8px;font-size:14px;background:var(--low);border:1px solid var(--line);border-radius:12px}.catalogue-row{min-height:118px}.settings-page{padding-top:4px}.settings-page section{padding:12px 0;border-bottom:1px solid var(--line)}.settings-page h2{font-size:12px;line-height:20px;color:var(--muted);margin:0 0 4px;font-weight:500}.setting-row{min-height:68px;display:flex;align-items:center;gap:16px;padding:10px 0}.setting-row>span:not(.switch){flex:1;min-width:0}.setting-row strong{font-size:16px;display:block;font-weight:400}.setting-row>.icon:last-child{width:20px;color:var(--muted)}.identity{display:flex;align-items:center;gap:12px;min-height:72px}.identity strong{display:block;font-weight:500}.avatar{display:flex;align-items:center;justify-content:center;background:var(--tonal);color:var(--on-tonal);font-size:20px;border-radius:50%;height:44px;width:44px;flex:none}.switch-row{position:relative;cursor:pointer}.switch-row strong{flex:1}.switch-row input{position:absolute;width:48px;height:48px;right:0;opacity:0;cursor:pointer}.switch{width:48px;height:30px;border-radius:30px;background:var(--high);border:2px solid var(--muted);display:block;position:relative;pointer-events:none}.switch:after{content:"";width:18px;height:18px;position:absolute;top:4px;left:4px;border-radius:50%;background:var(--muted)}.switch-row input:checked+.switch{background:var(--primary);border-color:var(--primary)}.switch-row input:checked+.switch:after{left:22px;background:var(--on-primary)}.switch-row input:focus-visible+.switch{outline:3px solid var(--primary);outline-offset:4px}.provider{margin-left:auto;border:1px solid var(--line);border-radius:20px;padding:5px 10px;font-size:12px}.account-page{display:flex;flex-direction:column}.account-status{display:flex;align-items:center;gap:14px;background:var(--low);border-radius:16px;padding:20px;margin-top:24px}.account-status strong{display:block}.account-status>.icon{color:var(--primary)}.device-note{font-size:14px;line-height:22px;margin:16px 0 24px}.account-destinations .setting-row{border-bottom:1px solid var(--line)}.account-actions{margin-top:auto;padding-top:36px;display:flex;flex-direction:column;gap:8px}.danger-action{color:var(--error);display:flex;align-items:center;justify-content:center;min-height:48px;font-size:14px;font-weight:500}.tablet{width:100%;height:100dvh;min-height:720px;display:flex;flex-direction:column;overflow:hidden}.tablet .system-bar{height:28px;background:var(--low)}.tablet-work{display:flex;flex:1;min-height:0}.rail{width:96px;flex:none;background:var(--low);border-right:1px solid var(--line);display:flex;flex-direction:column;align-items:center;padding:24px 8px 16px}.rail-brand{display:flex;flex-direction:column;align-items:center;gap:8px;font-size:11px}.rail-brand>.icon{box-sizing:content-box;padding:12px;background:var(--tonal);color:var(--on-tonal);border-radius:16px}.rail nav{display:flex;flex-direction:column;gap:20px;margin-top:64px;width:100%}.rail nav a,.rail-settings{display:flex;flex-direction:column;align-items:center;gap:4px;min-height:56px;font-size:14px;color:var(--muted)}.rail nav .icon{box-sizing:content-box;padding:6px 18px;border-radius:24px}.rail nav a[aria-current] .icon{background:var(--tonal);color:var(--on-tonal)}.rail-settings{margin-top:auto;padding-top:24px}.tablet-canvas{flex:1;min-width:0;min-height:0;display:flex;flex-direction:column}.tablet .app-bar{height:76px;padding:0 32px}.tablet .sync-status{font-size:14px}.tablet .gesture{background:var(--surface);height:12px}.tablet-home{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:32px;padding:24px 32px 36px;overflow-y:auto;flex:1;min-height:0}.home-feed{max-width:800px}.tablet .current-book{padding:28px}.tablet .current-identity{gap:24px}.tablet .current-identity>.cover{width:112px}.tablet .current-identity>div:last-child{flex:1}.tablet .current-identity h2{font-size:24px;line-height:32px}.tablet .current-book .button{width:auto;min-width:200px}.tablet .saved-section{margin-top:32px}.tablet .saved-grid{gap:24px}.tablet .saved-book .cover{max-width:168px}.tablet .saved-book h3{font-size:16px;line-height:24px}.tablet .saved-book .muted{font-size:14px;line-height:20px}.home-shelves{padding-left:24px;border-left:1px solid var(--line)}.home-shelves h2{font-size:20px}.shelf-row{display:flex;gap:14px;align-items:center;min-height:88px;border-bottom:1px solid var(--line)}.shelf-row>span{flex:1}.shelf-row strong{font-size:16px;line-height:24px}.shelf-row>.icon{color:var(--muted)}.library-split,.journal-split{display:grid;grid-template-columns:390px minmax(0,1fr);flex:1;min-height:0}.library-list,.journal-list{overflow-y:auto;min-width:0;border-right:1px solid var(--line);padding:16px 20px 28px}.library-list .chips{padding:0 0 16px;flex-wrap:wrap;gap:8px}.library-list .chip{font-size:12px;padding:8px 12px}.library-list .book-row{padding:16px 12px;margin:0 -8px;min-height:128px;border-bottom:0;border-radius:12px}.selected-row{background:var(--low);box-shadow:inset 3px 0 var(--primary)}.book-detail-pane{overflow-y:auto;min-width:0;padding:32px;max-width:900px}.detail-identity{display:flex;align-items:flex-start;gap:24px}.detail-identity>div:last-child{flex:1;min-width:0}.detail-identity h1{font-size:24px;line-height:32px}.detail-identity .author{margin-top:8px}.reading-state{margin:24px 0 20px}.reading-state>p:first-child{font-size:14px;color:var(--muted);margin-bottom:8px}.organization{margin-top:32px;padding-top:24px;border-top:1px solid var(--line)}.organization h2{font-size:20px}.organization-row{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:56px}.organization-row>span{font-size:14px;color:var(--muted)}.rating-link{min-height:48px;display:flex;gap:4px;align-items:center;color:var(--primary)}.rating-link .icon{width:20px;height:20px}.book-journal{margin-top:24px;padding-top:24px;border-top:1px solid var(--line)}.book-journal .section-head{margin-bottom:0}.book-journal p{font-size:14px;line-height:22px}.book-journal blockquote{font-family:Literata,serif;font-size:16px;line-height:26px;margin:12px 0;border-left:3px solid var(--primary);padding-left:16px}.journal-split{grid-template-columns:440px minmax(0,1fr)}.journal-list-head{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:0 0 16px}.journal-list-head p{font-size:14px;color:var(--muted)}.journal-list .chips{padding:0 0 20px}.journal-entry{display:block;padding:20px 16px;border-bottom:1px solid var(--line);border-radius:12px}.journal-entry>strong{display:block}.journal-entry>small{margin-top:4px}.journal-entry blockquote{font-family:Literata,serif;font-size:16px;line-height:26px;margin:16px 0 12px}.journal-entry p{font-size:14px;line-height:22px;color:var(--muted);margin-top:12px}.journal-detail{overflow-y:auto;padding:24px 32px 36px;min-width:0;max-width:820px}.detail-tools{display:flex;gap:4px}.journal-book-identity{display:flex;align-items:center;gap:20px;margin:20px 0 32px}.journal-book-identity h1{font-size:24px;line-height:32px}.journal-book-identity .muted{margin-top:4px}.entry-locator{font-size:14px;color:var(--muted);margin-top:10px}.entry-writing blockquote{font-family:Literata,serif;font-size:24px;line-height:38px;border-left:3px solid var(--primary);padding-left:24px;margin-bottom:32px}.entry-writing p{font-size:16px;line-height:28px}.journal-detail>.button{margin-top:32px}.overflow{position:relative}.overflow summary{list-style:none;cursor:pointer}.overflow summary::-webkit-details-marker{display:none}.disclosure-actions{position:absolute;right:0;top:52px;z-index:5;width:180px;background:var(--high);border-radius:12px;box-shadow:0 6px 20px #0003;padding:8px}.disclosure-actions a{min-height:48px;display:flex;align-items:center;padding:8px 16px;border-radius:8px;font-size:14px}.disclosure-actions a:hover{background:var(--container)}.danger{color:var(--error)}.reader-header{display:flex;align-items:center;gap:4px;padding:4px 8px;height:68px;flex:none;border-bottom:1px solid var(--line)}.reader-header>div{flex:1;text-align:center;min-width:0}.reader-header h1{font-size:16px;line-height:24px}.reader-header p{font-size:12px;color:var(--muted)}.bookmark-button{color:var(--primary)}.reading-pane{flex:1;min-width:0;min-height:0;overflow-y:auto;scrollbar-width:none}.reader-prose{padding:36px 24px 56px;cursor:default}.reader-prose h2{font-family:Literata,serif;font-size:26px;line-height:38px;text-align:center;margin:8px 0 32px;color:var(--primary);font-weight:500}.reader-prose p{font-family:Literata,serif;font-size:19px;line-height:32px;margin:0 0 24px}.reader-footer{flex:none;background:var(--low);border-top:1px solid var(--line);padding:14px 20px 4px}.reader-position{font-size:12px;display:flex;justify-content:space-between;color:var(--muted);margin-bottom:10px}.reader-position>span:last-child{color:var(--primary)}.reader-tools{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;padding-top:12px}.reader-tool{display:flex;flex-direction:column;justify-content:center;align-items:center;gap:6px;font-size:12px;min-height:56px}.reader-tool .icon{width:22px;height:22px}.reader>.gesture{background:var(--low)}.reader-split{display:flex;flex:1;min-height:0}.contents-pane{width:272px;flex:none;border-right:1px solid var(--line);padding:24px 16px;background:var(--low);overflow-y:auto}.contents-tabs{display:flex;gap:8px;margin-bottom:24px}.contents-tabs button{min-height:48px;padding:8px 12px;border:1px solid var(--line);background:transparent;border-radius:12px;font-size:14px;flex:1}.contents-tabs button[aria-pressed=true]{background:var(--tonal);color:var(--on-tonal);border-color:transparent}.pane-label{font-size:14px;color:var(--muted);margin:8px 12px 16px}.chapter-row{display:flex;align-items:center;gap:12px;min-height:56px;padding:12px;border-radius:12px;font-size:14px}.chapter-row .icon{width:20px;height:20px}.chapter-row.current{background:var(--tonal);color:var(--on-tonal)}.chapter-row small{color:inherit;font-size:12px}.tablet-reader .reader-header{height:76px;padding:8px 24px}.tablet-reader .reader-header>div{text-align:left;margin-left:12px}.tablet-reader .reader-header h1{font-size:20px;line-height:28px}.tablet-reader .reading-pane{display:flex;flex-direction:column}.tablet-reader .reader-prose{width:min(100%,700px);margin:auto;flex:1;padding:48px 56px 28px}.tablet-reader .reader-prose h2{margin-top:0}.tablet-reader .reader-prose p{font-size:19px;line-height:32px}.tablet-reader .reader-footer{width:min(calc(100% - 64px),700px);margin:0 auto 16px;border:1px solid var(--line);border-radius:16px;padding:14px 20px 8px}.tablet-reader .reader-tools{padding-top:8px}.show-controls{position:absolute;right:20px;top:44px;background:var(--tonal);color:var(--on-tonal);z-index:20}.controls-hidden .reader-controls{display:none}.controls-hidden .reader-prose{cursor:pointer}.controls-hidden .reading-pane{width:100%}[hidden]{display:none!important}.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}@media(max-width:380px){.page{padding-left:16px;padding-right:16px}.current-book{padding:16px}.current-identity{gap:12px}.current-identity>.cover{width:80px}.current-identity h2{font-size:18px;line-height:26px}.availability{font-size:11px}.saved-grid{gap:10px}.tabs{padding:0 16px}.chips{padding-left:16px;padding-right:16px}.reader-prose{padding-left:20px;padding-right:20px}}@media(max-width:1100px){.tablet-home{grid-template-columns:minmax(0,1fr) 248px;gap:24px;padding-left:24px;padding-right:24px}.library-split{grid-template-columns:340px minmax(0,1fr)}.book-detail-pane{padding:24px}.detail-identity{gap:18px}.detail-identity>.cover{width:112px}.journal-split{grid-template-columns:380px minmax(0,1fr)}.journal-detail{padding-left:24px;padding-right:24px}.contents-pane{width:240px}.tablet-reader .reader-prose{padding-left:40px;padding-right:40px}}@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}
'''

JS = r'''
document.querySelectorAll('.bookmark-button').forEach(button=>{const reader=button.closest('.reader'),saved=reader.querySelector('[data-bookmark-saved]'),empty=reader.querySelector('[data-bookmark-empty]'),savedLink=saved?.querySelector('a'),savedHref=savedLink?.getAttribute('href');const update=selected=>{button.setAttribute('aria-pressed',String(selected));button.setAttribute('aria-label',selected?'Remove bookmark':'Add bookmark');button.querySelector('svg').classList.toggle('filled',selected);if(saved){saved.hidden=!selected;empty.hidden=selected;if(selected)savedLink.setAttribute('href',savedHref);else savedLink.removeAttribute('href')}};update(button.getAttribute('aria-pressed')==='true');button.addEventListener('click',()=>update(button.getAttribute('aria-pressed')!=='true'))});
document.querySelectorAll('[data-panel]').forEach(button=>button.addEventListener('click',()=>{document.querySelectorAll('[data-panel]').forEach(other=>{const selected=other===button;other.setAttribute('aria-pressed',String(selected));document.getElementById(other.dataset.panel).hidden=!selected})}));
const reader=document.querySelector('.reader');if(reader){const show=reader.querySelector('.show-controls');const setControls=hidden=>{reader.classList.toggle('controls-hidden',hidden);show.hidden=!hidden};reader.querySelector('.hide-controls').addEventListener('click',()=>{setControls(true);show.focus()});show.addEventListener('click',()=>{setControls(false);reader.querySelector('.hide-controls').focus()});reader.querySelector('.reader-prose').addEventListener('click',()=>setControls(!reader.classList.contains('controls-hidden')))}
'''


def document(slug, body):
    font_css = ''.join(f'@font-face{{font-family:"{name}";src:url(data:font/woff2;base64,{data}) format("woff2");font-weight:100 900;font-style:normal;font-display:swap}}' for name, data in FONT.items())
    is_dark = slug.startswith("dark-")
    return f'<!doctype html>\n<html lang="en"' + (' class="dark"' if is_dark else '') + f'><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Veritalex · {slug.replace("-", " ").title()}</title><style>{font_css}{CSS}</style></head><body>{body}<script>{JS}</script></body></html>\n'


def main():
    screens = {
        "dark-home": home(),
        "dark-library": library(),
        "dark-book-details": book_details(),
        "dark-explore": explore(),
        "dark-settings": settings(),
        "dark-account-sync": account(),
        "dark-reader": reader(),
        "tablet-home": home(True),
        "tablet-library": library(True),
        "tablet-journal": journal(),
        "tablet-reader": reader(True),
    }
    for slug, body in screens.items():
        assert 'href="#"' not in body
        assert not ('<button' in body and 'role="menu"' in body)
        (ROOT / "designs" / f"{slug}.html").write_text(document(slug, body))
    print(f"Refined {len(screens)} dark/tablet HTML references.")


if __name__ == "__main__":
    main()
