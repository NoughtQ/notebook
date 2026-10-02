#!/usr/bin/env bash
set -euo pipefail

mode=${1:?usage: build-notes.sh public|full OUTPUT_DIR}
output=${2:?usage: build-notes.sh public|full OUTPUT_DIR}
root=$(cd "$(dirname "$0")/.." && pwd)

if [ "$mode" = public ]; then
  tmp=$(mktemp -d)
  trap 'rm -rf "$tmp"' EXIT
  mkdir -p "$tmp/docs"
  python3 - "$root" "$tmp/docs" <<'PY'
import json
import shutil
import sys
from pathlib import Path

root, target = map(Path, sys.argv[1:])
for name in json.loads((root / 'notebook_bot/config.json').read_text())['public_paths']:
    source = root / name
    if source.suffix != '.md' or not source.is_file() or not source.resolve().is_relative_to((root / 'docs').resolve()):
        raise SystemExit(f'Invalid public path: {name}')
    destination = target / source.relative_to(root / 'docs')
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
PY
  cat > "$tmp/mkdocs.yml" <<'YAML'
site_name: Public note check
theme: material
markdown_extensions:
  - pymdownx.arithmatex:
      generic: true
  - pymdownx.superfences
  - admonition
  - footnotes
YAML
  mkdocs build --clean -f "$tmp/mkdocs.yml" -d "$output"
elif [ "$mode" = full ]; then
  [ -n "${NOTEBOOK_PASSWORD_FILE:-}" ] && [ -r "$NOTEBOOK_PASSWORD_FILE" ] || { echo 'NOTEBOOK_PASSWORD_FILE is required for full build' >&2; exit 1; }
  created_password=0
  created_ignored=0
  if [ ! -e "$root/passwords.yml" ]; then
    ln -s "$NOTEBOOK_PASSWORD_FILE" "$root/passwords.yml"
    created_password=1
  fi
  if [ ! -e "$root/.ignored-commits" ]; then
    : > "$root/.ignored-commits"
    created_ignored=1
  fi
  cleanup() {
    if [ "$created_password" = 1 ]; then rm -f "$root/passwords.yml"; fi
    if [ "$created_ignored" = 1 ]; then rm -f "$root/.ignored-commits"; fi
  }
  trap cleanup EXIT
  mkdocs build --clean -f "$root/mkdocs.yml" -d "$output"
else
  echo "unknown build mode: $mode" >&2
  exit 2
fi
