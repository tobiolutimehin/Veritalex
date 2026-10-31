#!/usr/bin/env python3
"""Publish reviewed board images or self-contained HTML, resuming saved receipts."""
import argparse
import hashlib
import json
from pathlib import Path
from stitch_io import ROOT, upload

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("kind", choices=["images", "html", "docs", "references-images", "references-html", "missing-references"])
parser.add_argument("--revision", choices=["final", "clarity"], default="final", help="Name the reviewed reference revision on the Stitch canvas.")
args = parser.parse_args()
saved = set()
for receipt in (ROOT / "transfers").glob("*.json"):
    transfer = json.loads(receipt.read_text()).get("transfer", {})
    for name, digest in transfer.get("sha256", {}).items():
        saved.add((name, digest, transfer.get("prefix", "")))

groups = [("boards", "WF / "), ("polished-boards", "UI / ")]
if args.kind == "docs":
    groups = [("", "Handoff / ")]
elif args.kind == "missing-references":
    groups = [("designs", "Reference / ")]
elif args.kind.startswith("references-"):
    label = "Clarity" if args.revision == "clarity" else "Final"
    groups = [("designs", label + " / " if args.kind.endswith("images") else "Source / " + label + " / ")]
for folder, prefix in groups:
    if args.kind == "docs":
        paths = [ROOT / name for name in ["HANDOFF.md", "WIREFLOW.md", "DESIGN.md", "DESIGN-DARK.md"]]
    elif args.kind == "missing-references":
        meta = json.loads((ROOT / "metadata.json").read_text())
        project = json.loads((ROOT / "raw/project-final.json").read_text())
        present = {item.get("sourceScreen") for item in project["screenInstances"]}
        final_files = {name for name, _, saved_prefix in saved if saved_prefix == "Final / "}
        paths = [ROOT / item["screenshot"] for item in meta["stitchScreens"] if item["name"] not in present and item["screenshot"] not in final_files]
    elif args.kind.startswith("references-"):
        suffix = "png" if args.kind.endswith("images") else "html"
        refinements = json.loads((ROOT / "raw/reference-refinements.json").read_text())
        paths = [ROOT / "designs" / (slug + "." + suffix) for slug in refinements]
    else:
        suffix = "png" if args.kind == "images" else "html"
        paths = sorted((ROOT / folder).glob("*." + suffix))
        if args.kind == "html":
            prefix = "Source / " + prefix
    pending = [p for p in paths if (str(p.relative_to(ROOT)), hashlib.sha256(p.read_bytes()).hexdigest(), prefix) not in saved]
    for index in range(0, len(pending), 4):
        upload([str(p) for p in pending[index:index + 4]], prefix)
    print(json.dumps({"group": prefix, "published": len(pending), "already_saved": len(paths) - len(pending)}))
