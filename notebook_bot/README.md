# Notebook assistant

The assistant is off for publishing until `OPENAI_MODEL`, `BOT_ENABLED_AT`, the public page allowlist and a GitHub App are configured. `config.json` starts in `dry-run` mode.

Build checks:

```sh
bash scripts/build-notes.sh public /tmp/notebook-public-build
NOTEBOOK_PASSWORD_FILE=/path/to/passwords.yml bash scripts/build-notes.sh full /tmp/notebook-full-build
```

The full build also uses the existing MkDocs plugins, local hooks and LaTeX tools. `requirements-site.txt` captures versions observed in the maintainer's local MkDocs environment on 2026-10-02; the full build is the actual deployment gate. The public build is a narrower Markdown/rendering check and is not a substitute for it. The password file is read from a local or CI secret; it is never committed.

The Actions workflow starts only when repository variable `NOTE_BOT_MODE` is set. Keep it unset while configuring. Set `NOTE_BOT_ENABLED_AT` to an ISO-8601 UTC time, `NOTE_BOT_MODEL` to the verified OpenAI model ID, and `NOTE_BOT_LOGIN` to the installed App's bot login. Add `OPENAI_API_KEY`, `NOTE_BOT_APP_ID`, and `NOTE_BOT_APP_PRIVATE_KEY` as repository secrets. The App needs Discussions read/write and Contents read/write on this repository; its `bot-state` branch stores reservations, while correction branches contain only approved public Markdown edits. Start with `dry-run`, then `mention` for `/ask` messages. `auto` admits all eligible messages from the configured start time. Set `NOTE_BOT_MODE=off` to stop publishing immediately.

`note-assistant.yml` separates state reservation, model calls, static verification, and GitHub publishing into jobs with distinct credentials. `note-check.yml` runs without secrets on correction PRs. A correction PR remains a draft for human review and is never merged by the bot. The initial public allowlist covers only `docs/math/toc/1.md` and `docs/math/toc/2.md`; review each additional page before adding it. The scheduled hourly run recovers missed events and expired reservations. GitHub Actions schedules can be delayed, so a manual workflow dispatch also triggers a scan.

The deployment workflow is independently disabled until repository variable `NOTE_BOT_DEPLOY=enabled` and secret `NOTEBOOK_PASSWORDS_YML` are configured. It builds the complete site on trusted `main`, then updates the existing `gh-pages` branch with `ghp-import`; keep any older external deployment process disabled before enabling it. The bot adds `bot-deploy.json` to the published files with the source commit and build time. A merged correction is marked live only after that commit appears in the public marker and the changed text is present on the public page. A build failure or an unverified page leaves the correction pending and sends no live notice. The workflow installs TeX tools for the existing automata hook; verify the full build in a test repository before enabling production deployment.
