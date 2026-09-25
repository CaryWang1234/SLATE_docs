# SLATE 文档

[SLATE（砚）](https://github.com/CaryWang1234/SLATE) 面向使用者的文档源文件与静态站点。
`content/` 里的 Markdown 是唯一事实源，`site/` 由生成器产出，**不要手改 `site/`**。

## 目录结构

```
SLATE_docs/
├── content/            # 文档正文（Markdown 源，GitHub 可直接阅读）
├── theme/              # 站点皮肤
│   ├── layout.html     # 页面骨架（顶栏 / 侧栏 / 正文 / 本页目录）
│   ├── home.html       # 首页文案与卡片区
│   ├── docs.css        # 样式（双主题）
│   ├── docs.js         # 交互（主题 / 抽屉 / 搜索 / 目录跟随 / 代码复制）
│   └── icon.png        # 站点图标
├── build.py            # 零依赖生成器（只用 Python 标准库）
├── site/               # 生成产物（可直接部署）
└── README.md
```

## 本地构建与预览

```bash
python build.py              # 生成到 site/
python build.py --check      # 只校验 frontmatter 与站内链接，不写文件
python build.py --clean      # 生成前清空输出目录
python build.py --out docs   # 换输出目录（GitHub Pages 认 main 分支的 /docs）

cd site && python -m http.server 8129   # 本地预览 http://127.0.0.1:8129
```

生成器会把 `content/*.md` 之间的相对链接自动改写成 `.html`，因此 Markdown 源在
GitHub 上点得开、站点里也点得开，链接只需写一次。

## 新增或修改一页

1. 在 `content/` 新建 `NN-slug.md`，文件名即站点路径（`NN` 是全局展示序号）。
2. 文件头必须有 frontmatter：

```markdown
---
title: 页面标题
description: 30 字内的摘要（用于搜索与分享）
section: 分组名
order: 12
---
```

3. 正文**不写 H1**（标题由 frontmatter 提供），从 `##` 开始，最深到 `###`。
4. 可用语法：

| 写法 | 效果 |
|------|------|
| `:::note 小标题` … `:::` | 说明块，另有 `tip` / `warning` / `danger` |
| GFM 管道表格 | 带边框与横向滚动的表格 |
| 三反引号 + 语言 | 代码块，右上角带复制按钮 |
| `[文字](./06-autopilot.md)` | 跨页链接，构建时自动改写为 `.html` |

5. 运行 `python build.py` 后再看 `site/`；`--check` 会报出缺失 frontmatter 与死链。

## 写作口径

- **面向使用者**：只写用户看得见、点得到的东西，不写文件路径、函数名、HTTP 端点。
- **以源码为准**：功能名称、默认值、数量以 SLATE 仓库实现为准；`README-zh.md` 与源码冲突时以源码为准，不确定的不写。
- 中英文之间空格，术语保留英文（Agent Autopilot、Prompt、Skill、MCP、Token）。

## 部署

产物是纯静态文件，已带 `.nojekyll`，不需要任何构建步骤。

- **GitHub Pages（推荐）**：`python build.py --out docs --clean`，提交后在仓库
  Settings → Pages 里把 Source 设为 `Deploy from a branch`，分支选 `main`，目录选 `/docs`。
- **任意静态托管**：把 `site/` 整个目录传上去即可。

改过 `content/` 或 `theme/` 之后重新跑一次生成命令再提交，让产物与源文件保持同步。
