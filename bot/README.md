# 笔记讨论区助手

读者在 [笔记网站](https://note.noughtq.top/) 的 GitHub Discussions 自然提问，助手读取相关公开笔记、检索网页资料，再决定回答、追问、跳过，或提出纠错。回复和纠错 PR 均由独立 GitHub App 的机器人账号发出；纠错 PR 是草稿，只有站长审核并合并后才会改变笔记。

## 先看当前状态

- 代码位于草稿 PR，合并前不会在正式仓库运行。
- `NOTE_BOT_MODE` 未设置时，讨论区助手工作流不会处理提问。仅配置密钥不会开启自动回复。
- `NOTE_BOT_DEPLOY` 未设为 `enabled` 时，自动部署任务会跳过。正式仓库的完整构建已在独立预览分支验证；是否上线以 `gh-pages` 和网站的实际结果为准。

## 启用讨论区助手

1. 在仓库 **Settings → Secrets and variables → Actions** 中确认 Secrets：`OPENROUTER_API_KEY`、`NOTE_BOT_APP_ID`、`NOTE_BOT_APP_PRIVATE_KEY`。GitHub App 须安装在这个仓库，并获 Discussions、Contents、Pull requests 的读写权限。令牌由工作流临时生成；不要改用个人账号令牌。
2. 在同一页面添加 Variables：`NOTE_BOT_MODEL` 为支持 OpenRouter Responses API、网页检索及严格 JSON Schema 的模型 ID；`NOTE_BOT_LOGIN` 为 App 的完整 bot 登录名（例如 `name[bot]`）；`NOTE_BOT_ENABLED_AT` 为开始处理提问的 UTC 时间，例如 `2026-10-02T08:00:00Z`。早于该时间的留言不会被补答。
3. 编辑 [`data/config.json`](data/config.json) 的 `public_paths`，逐个列入允许助手读取及提出修改的公开 Markdown。初始只列了两篇目录笔记；不要加入加密或私人内容。
4. 先设置 `NOTE_BOT_MODE=dry-run`，手动运行 **Actions → Notebook assistant → Run workflow**，检查上下文和模型输出。`dry-run` 不会发评论或 PR。需要小范围试用时可设为 `mention`，此时留言首行写 `/ask` 才会触发。
5. 检查答案、来源和纠错补丁后，设置 `NOTE_BOT_MODE=auto`。此模式下读者直接留言，无须 `/ask`；模型按 [`data/prompt.md`](data/prompt.md) 判断是否需要回答。设置 `NOTE_BOT_MODE=off` 可停止新回复。

`data/style.json` 保存历史回复范例，模型会挑选三个相近例子模仿语气。修改提示词或范例后，重新检查一次实际输出。工作流每小时补扫遗漏事件，也支持手动运行；GitHub 定时任务可能延迟。

## 启用网站部署

仓库已有 `NOTEBOOK_PASSWORDS_YML` Secret，用于完整构建。设置 `NOTE_BOT_DEPLOY=enabled` 后，`main` 的每次 push 都会触发 [MkDocs 官方的 GitHub Pages 部署命令](https://squidfunk.github.io/mkdocs-material/publishing-your-site/)：安装 [`requirements/site.txt`](requirements/site.txt) 与现有 TeX 工具，用 Secret 临时生成 `passwords.yml`，运行 `mkdocs gh-deploy --force --remote-branch gh-pages`。构建或推送失败时，网站不会被标记为已更新。

部署会让 `gh-pages` 与当前源码一致，包括删除源码里已经不存在的旧页面。生成的 `bot-deploy.json` 记录源码提交；纠错 PR 合并后，助手还会核对线上页面及该标记，才通知读者修正已上线。部署使用 GitHub App 的 bot 身份，不使用个人账号。

本地想检查构建，可在仓库根目录自行运行：

```sh
python -m pip install -r bot/requirements/site.txt
mkdocs build --clean
```

本地构建需要已有的 `passwords.yml` 和 `.ignored-commits`；这两个文件被 Git 忽略。`site/` 也被忽略。无需额外的构建脚本。

## 文件与审核

- [`core/`](core/)：事件筛选、笔记检索、模型调用、补丁校验和 GitHub 发布。
- [`data/`](data/)：配置、回答规则、语气范例及尚待整理的评估数据。
- [`requirements/`](requirements/)：机器人运行环境与 MkDocs 站点构建依赖。
- [`.github/workflows/note-assistant.yml`](../.github/workflows/note-assistant.yml)：处理留言，按阶段隔离模型密钥与 GitHub 写权限。
- [`.github/workflows/note-check.yml`](../.github/workflows/note-check.yml)：核对机器人纠错 PR 只修改获准的笔记，且规模不超过 80 行。站点完整构建在合并到 `main` 后由部署工作流执行。

纠错 PR 不会自动合并。站长应核对事实、引用和具体 diff，再决定是否合并。`data/eval.jsonl` 目前为空；正式开放自动回复前，应准备 30 条与语气范例不重叠的历史题目，覆盖纠错、解释、歧义和证据不足四类，并用 `python -m bot.core.run evaluate --input bot/data/eval.jsonl --output /仓库外的报告目录` 跑只读评估。评估报告仍需人工判定事实正确性。
