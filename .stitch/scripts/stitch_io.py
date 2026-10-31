#!/usr/bin/env python3
"""Transfer approved design artifacts using the configured Stitch connection.

Credentials are read in memory and never written to artifacts or printed.
Requires Python 3.11+. Run from the repository root.
"""
from __future__ import annotations

import argparse
import base64
import contextlib
from datetime import datetime, timezone
import importlib.util
import io
import hashlib
import json
from pathlib import Path
import ssl
import sys
import tomllib
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ID = "6233788376335662642"
API = "https://stitch.googleapis.com"
UPLOADER = Path.home() / ".codex/plugins/cache/stitch-skills/stitch-design/1.0.0/skills/upload-to-stitch/scripts/upload_to_stitch.py"


def key() -> str:
    config = tomllib.loads((Path.home() / ".codex/config.toml").read_text())
    return config["mcp_servers"]["stitch"]["http_headers"]["X-Goog-Api-Key"]


def request_json(url: str, payload: dict | None = None) -> dict:
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers={
        "Content-Type": "application/json", "X-Goog-Api-Key": key()
    }, method="GET" if data is None else "POST")
    with urllib.request.urlopen(req, timeout=120, context=ssl.create_default_context()) as response:
        return json.load(response)


def download(slug: str) -> None:
    screen = json.loads((ROOT / "raw" / f"{slug}-screen.json").read_text())
    destination = ROOT / "designs"
    destination.mkdir(exist_ok=True)
    for field, suffix in (("htmlCode", "html"), ("screenshot", "png")):
        name = screen.get(field, {}).get("name")
        if not name:
            continue
        data = request_json(f"{API}/v1/{name}:download")
        target = destination / f"{slug}.{suffix}"
        payload = data.get("file", data)
        raw = payload.get("dataString")
        encoded = payload.get("fileContentBase64") or payload.get("image") or raw
        if suffix == "html" and "html" in payload:
            target.write_text(payload["html"])
        elif suffix == "html" and isinstance(raw, str) and raw.lstrip().startswith("<"):
            target.write_text(raw)
        elif encoded:
            target.write_bytes(base64.b64decode(encoded))
        else:
            raise ValueError(f"Unrecognized download response fields: {list(data)}")
        print(json.dumps({"saved": str(target.relative_to(ROOT)), "bytes": target.stat().st_size}))


def upload(paths: list[str], prefix: str) -> None:
    spec = importlib.util.spec_from_file_location("stitch_upload", UPLOADER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    requests = []
    for raw_path in paths:
        file_path = Path(raw_path).resolve()
        if not file_path.is_relative_to(ROOT):
            raise ValueError("Only files inside the approved .stitch package may be uploaded")
        mime = module._MIME_TYPES[file_path.suffix.lower()]
        item = module.build_screen_request(mime, module.encode_file(file_path),
                                          title=f"{prefix}{file_path.stem}",
                                          generated_by="stitch::code-to-design")
        requests.append(item)
    # The bundled uploader prints response fragments; retain only structured metadata.
    log = io.StringIO()
    try:
        with contextlib.redirect_stdout(log):
            response = module.call_batch_create_screens(API, key(), PROJECT_ID, requests, create_screen_instances=True)
    except SystemExit as error:
        raise RuntimeError(log.getvalue()[-2500:]) from error
    transfer_dir = ROOT / "transfers"
    transfer_dir.mkdir(exist_ok=True)
    first = Path(paths[0])
    stem = first.parent.name + "-" + first.stem + "-" + first.suffix.lstrip(".")
    response["transfer"] = {"files": [str(Path(p).resolve().relative_to(ROOT)) for p in paths], "prefix": prefix,
        "sha256": {str(Path(p).resolve().relative_to(ROOT)): hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in paths}}
    receipt = f"upload-{stem}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')}.json"
    (transfer_dir / receipt).write_text(json.dumps(response, indent=2))
    screens = response.get("screens", response.get("screenInstances", []))
    print(json.dumps({"uploaded": len(paths), "screens": [
        {"name": s.get("name") or s.get("sourceScreen"), "id": s.get("id"), "title": s.get("title")} for s in screens
    ], "response": f"transfers/{receipt}"}))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    down = sub.add_parser("download")
    down.add_argument("slugs", nargs="+")
    fresh = sub.add_parser("refresh")
    fresh.add_argument("slugs", nargs="+")
    up = sub.add_parser("upload")
    up.add_argument("paths", nargs="+")
    up.add_argument("--prefix", default="")
    sub.add_parser("status")
    args = parser.parse_args()
    try:
        if args.action == "refresh":
            meta = json.loads((ROOT / "metadata.json").read_text())
            for slug in args.slugs:
                raw_path = ROOT / "raw" / f"{slug}-screen.json"
                old = json.loads(raw_path.read_text())
                data = request_json(f"{API}/v1/{old['name']}")
                data = data.get("screen", data)
                current = {k: data.get(k, old.get(k)) for k in ["id", "name", "title", "width", "height", "deviceType", "htmlCode", "screenshot"]}
                current["slug"] = slug
                raw_path.write_text(json.dumps(current, indent=2))
                for item in meta["stitchScreens"]:
                    if item["slug"] == slug:
                        for field in ["id", "name", "title", "width", "height", "deviceType", "htmlCode"]:
                            item[field] = current[field]
                download(slug)
            (ROOT / "metadata.json").write_text(json.dumps(meta, indent=2))
        elif args.action == "download":
            for slug in args.slugs:
                download(slug)
        elif args.action == "upload":
            upload(args.paths, args.prefix)
        else:
            data = request_json(f"{API}/v1/projects/{PROJECT_ID}")
            (ROOT / "raw" / "project-final.json").write_text(json.dumps(data, indent=2))
            listing = request_json(f"{API}/v1/projects/{PROJECT_ID}/screens")
            (ROOT / "raw" / "remote-screens.json").write_text(json.dumps(listing, indent=2))
            print(json.dumps({"name": data.get("name"), "title": data.get("title"), "instances": len(data.get("screenInstances", [])), "screens": [{"name": s.get("name"), "title": s.get("title")} for s in listing.get("screens", [])]}))
    except urllib.error.HTTPError as error:
        print(json.dumps({"error": "Stitch HTTP request failed", "status": error.code}), file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as error:
        print(json.dumps({"error": "Stitch connection failed", "reason": str(error.reason)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
