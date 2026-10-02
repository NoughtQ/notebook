# Notebook assistant

The assistant is off for publishing until `OPENAI_MODEL`, `BOT_ENABLED_AT`, the public page allowlist and a GitHub App are configured. `config.json` starts in `dry-run` mode.

Build checks:

```sh
bash scripts/build-notes.sh public /tmp/notebook-public-build
NOTEBOOK_PASSWORD_FILE=/path/to/passwords.yml bash scripts/build-notes.sh full /tmp/notebook-full-build
```

The full build also uses the existing MkDocs plugins, local hooks and LaTeX tools. `requirements-site.txt` captures versions observed in the maintainer's local MkDocs environment on 2026-10-02; the full build is the actual deployment gate. The public build is a narrower Markdown/rendering check and is not a substitute for it. The password file is read from a local or CI secret; it is never committed.
