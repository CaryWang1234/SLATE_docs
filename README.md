# SLATE 文档

[SLATE（砚）](https://github.com/CaryWang1234/SLATE) 面向使用者的文档源文件与静态站点，中英双语。
`content/en/` 与 `content/zh/` 里的 Markdown 是唯一事实源，`docs/` 由生成器产出，**不要手改 `docs/`**。
站点里英文在根、中文在 `/zh/`，两套树共用一个 `assets/`。

线上入口：文档站 **https://docs.slate-ai.site/** ｜ 官网 **https://slate-ai.site/** ｜ 使用教程 **https://slate-ai.site/guide.html**

## 目录结构

```
SLATE_docs/
├── content/
│   ├── en/             # 英文正文（站点根）
│   └── zh/             # 中文正文（站点 /zh/）
├── theme/              # 站点皮肤
│   ├── layout.html     # 页面骨架（顶栏 / 侧栏 / 正文 / 本页目录 / 语言切换）
│   ├── home.html       # 首页模板（文案由 build.py 按语言填充）
│   ├── docs.css        # 样式（双主题）
│   ├── docs.js         # 交互（主题 / 抽屉 / 搜索 / 目录跟随 / 代码复制）
│   └── icon.png        # 站点图标
├── build.py            # 零依赖双语生成器（只用 Python 标准库）
├── docs/               # 生成产物 = GitHub Pages 发布目录（已带 .nojekyll）
└── README.md
```

## 本地构建与预览

```bash
python build.py              # 生成到 docs/
python build.py --check      # 只校验 frontmatter、双语配对、站内链接与锚点，不写文件
python build.py --clean      # 生成前清空输出目录
python build.py --out site   # 换输出目录

cd docs && python -m http.server 8129   # 本地预览 http://127.0.0.1:8129（中文在 /zh/）
```

生成器会把同语言页面之间的相对链接自动改写成 `.html`，因此 Markdown 源在
GitHub 上点得开、站点里也点得开，链接只需写一次。

双语是构建器的硬约束：两侧文件名必须一一对应、`order` 必须相同，缺任一侧
`--check` 即失败、不出站。

## 新增或修改一页

1. 在 `content/en/` 与 `content/zh/` 各新建一个**同名**的 `NN-slug.md`，文件名即站点路径（`NN` 是全局展示序号）。
2. 两侧文件头都必须有 frontmatter，`order` 必须相同：

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

5. 运行 `python build.py` 后再看 `docs/`；`--check` 会报出缺失 frontmatter、双语缺侧、order 不一致与死链。

## 写作口径

- **面向使用者**：只写用户看得见、点得到的东西，不写文件路径、函数名、HTTP 端点。
- **以源码为准**：功能名称、默认值、数量以 SLATE 仓库实现为准；`README-zh.md` 与源码冲突时以源码为准，不确定的不写。
- 中英文之间空格，术语保留英文（Agent Autopilot、Prompt、Skill、MCP、Token）。
- 英文侧沿用产品 i18n 词典的译法（Grind Mode、Target Mode、Prompt Factory、Expert Packs、Scheduled Tasks 等），不另造词。

## 部署

`docs/` 是纯静态产物，随仓库一起提交，已带 `.nojekyll`（GitHub Pages 就不会再走 Jekyll）。

仓库 Settings → Pages：Source 选 `Deploy from a branch`，分支 `master`，目录 `/docs`。

改过 `content/` 或 `theme/` 之后重新跑一次 `python build.py` 再提交，让产物与源文件保持同步。
换用其他静态托管时，把 `docs/` 整个目录传上去即可。
