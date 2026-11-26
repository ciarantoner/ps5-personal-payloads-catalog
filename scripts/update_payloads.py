#!/usr/bin/env python3
"""Build payloads.json (PS5 Payload Manager format) from the repos/ folder.

For each repository listed in repos/*.txt (one per line), query the GitHub API
(/repos/{owner}/{repo} and /repos/{owner}/{repo}/releases/latest), take the
first asset ending in .elf or .bin and build the catalog entry.

No external dependencies (standard library only).
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPOS_DIR = ROOT / "repos"
OUTPUT_FILE = ROOT / "payloads.json"
CATALOG_NAME = "Personal PS5 Payloads List"
API = "https://api.github.com"
EXTENSIONS = (".elf", ".bin")

REPO_RE = re.compile(
    r"^(?:https?://)?(?:www\.)?(?:github\.com/)?"
    r"(?P<owner>[A-Za-z0-9](?:[A-Za-z0-9-]{0,38}))/(?P<repo>[A-Za-z0-9._-]+?)"
    r"(?:\.git)?(?:[/?#].*)?$"
)


class NotFound(Exception):
    pass


def parse_repo(line: str) -> tuple[str, str] | None:
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    m = REPO_RE.match(line)
    if not m:
        print(f"::warning::Skipping line (invalid URL): {line}")
        return None
    return m.group("owner"), m.group("repo")


def gh_get(path: str) -> dict:
    req = urllib.request.Request(API + path)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "personal-ps5-payloads-list-updater")
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise NotFound(path) from e
        raise


def build_entry(owner: str, repo: str) -> dict | None:
    info = gh_get(f"/repos/{owner}/{repo}")
    try:
        release = gh_get(f"/repos/{owner}/{repo}/releases/latest")
    except NotFound:
        print(f"::warning::{owner}/{repo}: no published release")
        return None

    asset = next(
        (a for a in release.get("assets", [])
         if a.get("name", "").lower().endswith(EXTENSIONS)),
        None,
    )
    if asset is None:
        print(f"::warning::{owner}/{repo}: release {release.get('tag_name')} has no .elf/.bin asset")
        return None

    tag = release.get("tag_name") or ""
    version = re.sub(r"^[vV](?=\d)", "", tag) or tag
    full_owner, full_repo = info["full_name"].split("/", 1)

    return {
        "id": f"{full_owner}-{full_repo}".lower(),
        "name": info.get("name") or full_repo,
        "description": (info.get("description") or "").strip(),
        "filename": asset["name"],
        "version": version,
        "url": asset["browser_download_url"],
    }


def load_previous() -> dict[str, dict]:
    """Current payloads.json entries keyed by id (used as a fallback)."""
    try:
        data = json.loads(OUTPUT_FILE.read_text(encoding="utf-8"))
        return {p["id"]: p for p in data.get("payloads", []) if "id" in p}
    except (FileNotFoundError, ValueError, KeyError, TypeError):
        return {}


def main() -> int:
    previous = load_previous()
    payloads: list[dict] = []
    seen: set[str] = set()

    lines: list[str] = []
    for f in sorted(REPOS_DIR.glob("*.txt"), key=lambda x: x.name.lower()):
        lines += f.read_text(encoding="utf-8").splitlines()

    for line in lines:
        parsed = parse_repo(line)
        if not parsed:
            continue
        owner, repo = parsed
        key = f"{owner}-{repo}".lower()
        if key in seen:
            continue
        seen.add(key)

        try:
            entry = build_entry(owner, repo)
        except NotFound:
            print(f"::warning::{owner}/{repo}: repository not found")
            continue
        except Exception as e:  # network error / rate limit: keep the previous entry
            print(f"::warning::{owner}/{repo}: API error ({e}); keeping previous entry")
            entry = previous.get(key)

        if entry:
            payloads.append(entry)
            print(f"OK  {owner}/{repo} -> {entry['filename']} ({entry['version']})")

    catalog = {"name": CATALOG_NAME, "payloads": payloads}
    new_text = json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"
    old_text = OUTPUT_FILE.read_text(encoding="utf-8") if OUTPUT_FILE.exists() else ""

    if new_text != old_text:
        OUTPUT_FILE.write_text(new_text, encoding="utf-8")
        print(f"payloads.json updated ({len(payloads)} payload(s))")
    else:
        print("payloads.json unchanged")
    return 0


if __name__ == "__main__":
    sys.exit(main())
