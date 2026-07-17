# 开源日报

每日自动展示 GitHub 上最热门的 10 个新开源项目。全自动运行在 GitHub Pages 上，只需一次设置，每天自动更新。

## 设置步骤（0 基础可操作）

1. **Fork 本仓库** — 点击页面右上角的 Fork 按钮
2. **启用 GitHub Pages** — 进入仓库 Settings → Pages，在 "Source" 处选择 `Deploy from a branch`，选择 `main` 分支，`/ (root)` 目录，点 Save
3. **允许 Actions 写入** — 进入仓库 Settings → Actions → General，在 "Workflow permissions" 中选择 "Read and write permissions"，点 Save
4. **等待或手动触发** — 第二天会自动更新，也可以到 Actions 页面手动运行一次 "Daily Update" 工作流
5. **访问网站** — 打开 `https://<你的用户名>.github.io/daily-github`

> 如果 Settings 中没有 Pages 选项，请先在仓库创建任意一个文件（如修改 README）并提交，GitHub 会自动激活 Pages 功能。

## 技术栈

- 纯 HTML/CSS/JS — 零依赖，GitHub Pages 原生支持
- Python 数据获取脚本 — 调用 GitHub API + googletrans 翻译
- GitHub Actions — 每天 UTC 0:00 自动运行
