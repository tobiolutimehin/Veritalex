#!/usr/bin/env python3
"""Verify reviewed export hashes and their attachment to the Stitch project."""
import hashlib
import json
from stitch_io import ROOT, API, PROJECT_ID, request_json

meta = json.loads((ROOT / "metadata.json").read_text())
project = request_json(f"{API}/v1/projects/{PROJECT_ID}")
(ROOT / "raw/project-final.json").write_text(json.dumps(project, indent=2))
present = {s.get("sourceScreen") for s in project.get("screenInstances", [])}
missing_refs, missing_sources, missing_boards, changed = [], [], [], []


def check_hash(item, file):
    receipt_path = item.get("receipt")
    if not receipt_path:
        changed.append(file)
        return
    receipt = json.loads((ROOT / receipt_path).read_text())
    expected = receipt.get("transfer", {}).get("sha256", {}).get(file)
    local = ROOT / file
    if not local.exists() or hashlib.sha256(local.read_bytes()).hexdigest() != expected:
        changed.append(file)


for item in meta["canvasReferences"]:
    if item["sourceScreen"] not in present:
        missing_refs.append(item["slug"])
    check_hash(item, "designs/" + item["slug"] + ".png")
for item in meta.get("referenceSourceExports", []):
    if item["sourceScreen"] not in present:
        missing_sources.append(item["file"])
    check_hash(item, item["file"])
for item in meta["boardExports"]:
    if item["sourceScreen"] not in present:
        missing_boards.append(item["file"])
    check_hash(item, item["file"])

counts = (len(meta["canvasReferences"]), len(meta.get("referenceSourceExports", [])), len(meta["boardExports"]))
report = {
    "revision": "clarity-v1",
    "references_on_canvas": counts[0] - len(missing_refs),
    "reference_html_on_canvas": counts[1] - len(missing_sources),
    "board_assets_on_canvas": counts[2] - len(missing_boards),
    "missing_references": missing_refs,
    "missing_reference_html": missing_sources,
    "missing_boards": missing_boards,
    "changed_local_files": changed,
    "passed": counts == (25, 25, 48) and not (missing_refs or missing_sources or missing_boards or changed),
}
(ROOT / "qa/cloud-inventory.json").write_text(json.dumps(report, indent=2))
print(json.dumps(report))
raise SystemExit(0 if report["passed"] else 1)
