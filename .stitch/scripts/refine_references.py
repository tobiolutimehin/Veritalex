#!/usr/bin/env python3
"""Bake approved Stitch DOM edits into the downloaded reference source files.

Uses lxml from the bundled document runtime. The original cloud resources remain
recorded separately; the refined HTML and rendered PNGs are published as Final.
"""
import json
from pathlib import Path
from lxml import html

root = Path(__file__).resolve().parents[1]
record = root / "raw" / "reference-refinements.json"
changes = json.loads(record.read_text()) if record.exists() else {}
for slug in ["home", "sync-conflict", "reader", "dark-reader"]:
    file = root / "designs" / (slug + ".html")
    tree = html.fromstring(file.read_text())
    if slug == "home":
        for count in ["54k", "48k", "42k"]:
            for node in tree.xpath("//*[normalize-space(text())=$value]", value=count):
                containers = node.xpath("ancestor::div[contains(concat(' ',normalize-space(@class),' '),' mt-1 ')]")
                if not containers:
                    raise ValueError("Could not locate the download count row")
                containers[-1].getparent().remove(containers[-1])
        changes[slug] = "Removed invented catalogue download counts using the approved Stitch DOM operation."
    elif slug == "sync-conflict":
        for node in tree.xpath("//*[@data-icon='format_quote']"):
            node.getparent().getparent().remove(node.getparent())
        for node in tree.xpath("//body//*[contains(text(),'Chapter 20')]"):
            if node.text:
                node.text = node.text.replace("Chapter 20", "Chapter 19")
        changes[slug] = "Removed illustrative quotes and matched the account position to Chapter 19 / 31%."
    else:
        for node in tree.xpath("//*[contains(concat(' ',normalize-space(@class),' '),' text-justify ')]"):
            node.set("class", node.get("class").replace("text-justify", "text-left"))
            node.set("style", "text-align:left;word-spacing:normal")
        for node in tree.xpath("//span[normalize-space(text())='Book I' or normalize-space(text())='BOOK I']"):
            header = node.getparent()
            for child in list(header):
                if child.tag != "h2":
                    header.remove(child)
            header.set("class", "")
            header.set("style", "padding:8px 0 20px;text-align:left")
            for title in header.xpath("./h2"):
                title.set("style", "font-family:Literata,Georgia,serif;font-size:26px;line-height:34px;font-weight:500")
        changes[slug] = "Left-aligned prose with natural spacing and a compact chapter introduction."
    title = tree.find("head/title")
    if title is not None:
        title.text = "Veritalex - " + slug.replace("-", " ").title()
    file.write_text("<!DOCTYPE html>\n" + html.tostring(tree, encoding="unicode", method="html"))
for file in (root / "designs").glob("*.html"):
    text = file.read_text()
    if "Veritalex Archives" in text:
        file.write_text(text.replace("Veritalex Archives", "Project Gutenberg"))
        changes[file.stem] = changes.get(file.stem, "") + " Corrected catalogue attribution to Project Gutenberg."
record.write_text(json.dumps(changes, indent=2))
print(json.dumps({"refined": list(changes)}))
