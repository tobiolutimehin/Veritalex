#!/usr/bin/env python3
"""Rebuild the reference and board index from saved resource records and receipts."""
import json
import struct
import hashlib
from pathlib import Path

root = Path(__file__).resolve().parents[1]
slugs = ["home", "book-details", "reader", "library", "explore", "shelves", "journal", "welcome", "guest-import", "settings", "account-sync", "reader-appearance", "downloads", "sync-conflict", "tablet-home", "tablet-library", "tablet-journal", "tablet-reader", "dark-home", "dark-explore", "dark-library", "dark-book-details", "dark-reader", "dark-settings", "dark-account-sync"]
states = {"home": "home-returning", "book-details": "book-new", "reader": "reader-scroll", "library": "library-books", "explore": "explore-browse", "shelves": "shelves-list", "journal": "journal-all", "welcome": "auth-welcome", "guest-import": "auth-import-preview", "settings": "settings-main", "account-sync": "account-details", "reader-appearance": "reader-appearance", "downloads": "settings-storage", "sync-conflict": "sync-conflict"}
metadata = json.loads((root / "metadata.json").read_text())
refinements_path = root / "raw" / "reference-refinements.json"
refinements = json.loads(refinements_path.read_text()) if refinements_path.exists() else {}
metadata["stitchScreens"] = []
for slug in slugs:
    source = json.loads((root / "raw" / (slug + "-screen.json")).read_text())
    source.update(slug=slug, variant="dark" if slug.startswith("dark-") else "tablet" if slug.startswith("tablet-") else "light", html="designs/"+slug+".html", screenshot="designs/"+slug+".png", source="Stitch")
    state = states.get(slug.removeprefix("dark-").removeprefix("tablet-"))
    source["screenIds"] = [state] if state else []
    if slug in refinements:
        source["refinement"] = refinements[slug]
        source["source"] = "Stitch with approved final content and typography edits"
    png = root / source["screenshot"]
    if png.exists() and png.read_bytes()[:8] == b'\x89PNG\r\n\x1a\n':
        width, height = struct.unpack('>II', png.read_bytes()[16:24])
        source["exportDimensions"] = {"width": width, "height": height}
    metadata["stitchScreens"].append(source)
boards = {}
for path in sorted((root / "transfers").glob("*.json")):
    data = json.loads(path.read_text())
    transfer = data.get("transfer", {})
    if transfer.get("prefix") not in ["WF / ", "UI / ", "Source / WF / ", "Source / UI / "]:
        continue
    for file, instance in zip(transfer.get("files", []), data.get("screenInstances", [])):
        boards[file] = {"file": file, "prefix": transfer["prefix"], "instanceId": instance.get("id"), "sourceScreen": instance.get("sourceScreen"), "receipt": str(path.relative_to(root))}
metadata["boardExports"] = list(boards.values())
canvas = {item["slug"]: {"slug": item["slug"], "sourceScreen": item["name"], "kind": "Stitch design"} for item in metadata["stitchScreens"]}
for path in sorted((root / "transfers").glob("*.json"), key=lambda p: p.stat().st_mtime):
    data = json.loads(path.read_text())
    transfer = data.get("transfer", {})
    if transfer.get("prefix") not in ["Final / ", "Reference / ", "Clarity / "]:
        continue
    for file, instance in zip(transfer.get("files", []), data.get("screenInstances", [])):
        local = root / file
        if local.suffix != ".png" or local.stem not in canvas or not local.exists():
            continue
        if transfer.get("sha256", {}).get(file) != hashlib.sha256(local.read_bytes()).hexdigest():
            continue
        canvas[local.stem] = {"slug": local.stem, "sourceScreen": instance["sourceScreen"], "kind": transfer["prefix"].strip(" /"), "receipt": str(path.relative_to(root))}
metadata["canvasReferences"] = list(canvas.values())
reference_sources = {}
for path in sorted((root / "transfers").glob("*.json"), key=lambda p: p.stat().st_mtime):
    data = json.loads(path.read_text())
    transfer = data.get("transfer", {})
    if transfer.get("prefix") not in ["Source / Final / ", "Source / Clarity / "]:
        continue
    for file, instance in zip(transfer.get("files", []), data.get("screenInstances", [])):
        local = root / file
        if local.suffix != ".html" or local.stem not in canvas or not local.exists():
            continue
        if transfer.get("sha256", {}).get(file) != hashlib.sha256(local.read_bytes()).hexdigest():
            continue
        reference_sources[local.stem] = {"slug": local.stem, "file": file, "sourceScreen": instance["sourceScreen"], "instanceId": instance.get("id"), "receipt": str(path.relative_to(root))}
metadata["referenceSourceExports"] = list(reference_sources.values())
metadata["designSystems"]["dark"] = "assets/1cf14a0733a54b90a61f9744d7e53b3c"
(root / "metadata.json").write_text(json.dumps(metadata, indent=2))
print(json.dumps({"references": len(metadata["stitchScreens"]), "uploaded_board_assets": len(boards)}))
