---
title: Built-in tools and skills
description: The full list of tools SLATE ships with, how to call them, and how to extend them.
section: Chat & Automation
order: 8
---

This page is the capability list: which tools SLATE ships with, how the model uses them, which ones you can turn off, and how to connect more capabilities with `SKILL.md` and external MCP servers.

## Two kinds of capability, first things first

- **Built-in tools**: Python capabilities that ship with SLATE, usable out of the box — no configuration, no installation. Reading and writing files, running commands, generating documents and web search all fall in this group.
- **Skills**: external knowledge and procedures defined by `SKILL.md`. You write, upload or import them from a local path, to tell the model "which steps this kind of thing should follow".

Built-in tools are the "hands", Skills are the "way of doing it". Both can be used by the model on demand, and both can be named explicitly with `@`.

## Where to manage them: the Extensions page

The "Extensions" page in the top bar is the entry point for managing all capabilities; seven columns on the left each manage one kind, and the numbers and the list come from the same source:

| Column | What it manages |
|---|---|
| Skills | Importing, creating and deleting `SKILL.md` skills, with two sources, "GitHub" and "Discover plugins" |
| Tools | The list of built-in tools (viewable, not deletable); features you turn off don't even appear in the catalogue |
| Modes | The four built-in reply modes (read-only) and creating / editing / deleting custom modes: extra prompts, tool allowlist, reasoning effort and round cap |
| New features | Tools the tool factory produced itself: disable, view code, check versions, roll back, undo |
| MCP | Connections to external MCP servers and the remote tools they bring |
| Expert Packs | A role setting + knowledge base + skills combined; you can create one and import a zip |
| Actions | Editing, validating and rolling back `data/actions/*.yml` process specs |

The "Tools / Skills" and "MCP Server" blocks that used to be scattered on the settings page have moved wholesale onto this page; the settings page keeps configuration only and no longer doubles as capability management.

## Built-in tools at a glance

| Category | Tool | Purpose |
|---|---|---|
| Files & code | `file_tree` | Browse directories: recursive, filter by wildcard, fast scan |
| Files & code | `file_peek` | Read file contents: detects several encodings automatically, supports a line range or reading from the end |
| Files & code | `file_create` | Create a new file |
| Files & code | `file_edit` | Diff-preview editing: exact replacement, replace by line number, insert, delete, copy and paste |
| Files & code | `file_append` | Append to the end of an existing file, used to continue very long files in segments |
| Files & code | `code_search` | Global code search within the project: text or regex, narrowable to a subdirectory |
| Files & code | `repo_stats` | Statistics on project file types, size and count |
| Files & code | `todo_scan` | Scan the project for TODO / FIXME markers |
| Files & code | `python_api_extract` | Extract the public API docs of a Python library (signatures, class methods, attributes) |
| Terminal & background tasks | `terminal` | Restricted sandbox command execution, with multiple sessions and state kept across commands |
| Terminal & background tasks | `bg_task` | Background terminal tasks: start and go, the model is woken when it finishes |
| Office documents | `doc_write` | Generate Markdown technical docs or requirement notes |
| Office documents | `ppt_create` | Generate `.pptx` presentations |
| Office documents | `word_create` | Generate `.docx` Word documents |
| Office documents | `excel_tool` | Generate `.xlsx`, read spreadsheets, convert between csv and xlsx |
| Office documents | `pdf_tool` | PDF metadata, text and table extraction |
| Office documents | `html_render` | Generate an HTML skeleton |
| Office documents | `html_bundle` | Inline a page's css / js into a single html file for easy distribution |
| Data & charts | `json_tool` | JSON validation, formatting, minifying and reading by path |
| Data & charts | `regex_test` | Regular expression testing with a preview of the matches |
| Data & charts | `text_summarise` | Text summarising and keyword extraction |
| Data & charts | `chart_create` | Generate SVG charts: bar / horizontal bar / line / pie |
| Data & charts | `qrcode_create` | Generate SVG QR codes |
| Search & web | `web_search` | Web search, no Key required |
| Search & web | `web_fetch` | Fetch the body text of a web page, supporting JS-rendered pages and PDFs |
| Code & document security | `code_scan` | Code security scan: hard-coded keys, SQL injection, XSS, weak crypto, leftover debug code |
| Code & document security | `doc_scan` | Document security scan: PII, credentials, financial data, confidential markers, internal network information |
| Git | `git_tool` | Read-only Git repository information: branch status, commit log, change statistics, branch and remote lists |
| System & environment | `system_info` | System self-knowledge: date and time, hardware configuration, battery, network status |
| System & environment | `css_colour` | Generate CSS colour schemes |
| Automation | `browser_automation` | Browser automation: navigate, screenshot, click, type, run JS |
| Automation | `computer_use` | Desktop automation: mouse and keyboard control, window management, image targeting |
| Automation | `screenshot_to_code` | Screenshot to code: analyse a screenshot and generate HTML / CSS that reproduces the look |
| Generation | `image_gen` | AI image generation; requires a model and API Key configured in Settings |
| Generation | `video_gen` | AI video generation; requires a model and API Key configured in Settings |
| MCP factory | `mcp_factory` | Tool factory: generate new tools from a description; output lands in `data/evolved/` and can be disabled / rolled back / undone under "Extensions → New features" |

:::note About the tool count
The table above has 36 entries and covers every built-in tool you can see in the tool panel and in the `@` mention candidates. `file_append` and `file_create` belong to the same family: one creates and one continues, and together they handle segmented writes of very long files.
:::

## Key tools

### file_edit: you see the change first

- Changes are presented as a diff: file name, `+N -M` line statistics, red and green added and removed lines — what moved is visible in one screen.
- The card has three buttons, "Accept", "Reject" and "Copy diff": only accepting writes to disk, while rejecting just closes the card (this change isn't written, but content already written earlier in the same round isn't rolled back by this card).
- When "Auto-confirm file creation/modification" is ticked in "Settings → Context & Projects" (ticked by default), changes whose preview reports no errors are written directly, the card shows "Applied automatically", and Accept and Reject are no longer offered. When part of the content doesn't match, manual confirmation is kept, so that only half a set never gets written.
- Files that really landed on disk this round are summarised into a "Which files this round changed" card after the model's last sentence, where you can review the diff file by file and undo the whole round; see [Agent Autopilot and Target Mode](./06-autopilot.md).
- Encoding safety: existing encodings such as UTF-8, BOM, GB18030, GBK and UTF-16 are preserved on write, so Chinese text and emoji don't turn into mojibake.

### terminal: run commands in a restricted sandbox

- A single command times out after 30 seconds, output over 50,000 characters is truncated, and command length is capped too.
- Several terminal sessions can coexist: create, list, close, and also terminate processes running in a session.
- On Windows every command gets its own PowerShell process: multi-line blocks (`foreach` / `if`) and `&&` / `||` both work; session state such as `cd` and `$env:` persists across commands.
- Interactive command lines (a bare `python` / `node` REPL waiting for input) get no input and either exit or drag on until timeout, so they aren't suitable here.
- No command window pops up on screen, and output capture for native commands supports Chinese and emoji.

### bg_task: three ways a background terminal task wakes you

Work measured in minutes — compiling, training, starting an experiment server — hands over to it, without holding the conversation:

1. **Ask on demand**: it returns the task id, the first stretch of output and the log path right away; afterwards use status and log queries to fetch new output.
2. **Wake on finish**: start the task with `notify=true`, and when the task ends the result comes back to the conversation with the tail of the output, and the model is woken to carry on.
3. **Wake early**: attach a regex, and a matching output wakes it early, without waiting for the command to finish.

It is a one-shot "start and go" task and doesn't accept interactive input; you can give it a timeout so it terminates itself when due, and stop the whole process tree at any time. Task lifetime equals SLATE process lifetime — close SLATE and the task is gone; logs stay on your machine for later inspection.

:::warning Background doesn't mean approval-free
Background tasks go through exactly the same approval tier as the terminal: high-risk commands still pop up to ask you, and catastrophic commands are refused outright.
:::

### Search, Git and the web

- `code_search`: global code search in the project, supporting text and regex, starting from the project root by default, narrowable to a subdirectory.
- `git_tool`: read-only — branch and working tree status, recent commits, change statistics, branch and remote lists. It won't commit, push or do other write operations for you; those commands are run by the model in the terminal and are subject to approval too.
- `web_search`: web search without a Key, two engines queried concurrently with results merged and de-duplicated, for real-time information.
- `web_fetch`: fetch the title, description and body text of a given page, supporting pages that need JS rendering and PDFs.

## How tools get called

- **The model calls them on its own**: you just describe the need ("turn this data into a chart") and the model decides which tool to use; no naming required.
- **Visible in the chat**: every call becomes a tool card showing the tool name, key arguments and execution status, with the result expandable.
- **High-risk commands need approval**: commands and web access both pass through the approval gate. There are four approval tiers — manual approval / auto approval / full access / night mode — switchable at any time within the session; full access closes the command and web gates, but the AI still pops a multiple-choice question at you when it lacks a condition; night mode goes one step further, fully managed — commands, web access and the model's clarifying questions all stop popping windows. Catastrophic commands are blocked unconditionally in every tier. For the rules, see [Settings and security approval](./19-settings.md).
- **Failures are reported honestly**: when a capability can't run (say the runtime is missing a dependency), the tool card shows a failure, and what the model receives is a failure message too — it tells you what's missing and that you need to install it yourself; it won't describe a file it never generated as generated. Installing dependencies is your job in the terminal; the model won't install things on your behalf.
- **Background tasks have their own panel**: running background terminal tasks are listed in the task centre in the right column, where you can view and stop them directly.

## Turning tools on and off

"Settings → AI assistance" is the switchboard for every token-consuming feature outside the chat. Three of them are tool-related:

- Subagent parallelism (`subagent_run`)
- AI image generation
- AI video generation

Turn any one of these three off and the corresponding tool **disappears from the tool catalogue** — the model can't see it, so it won't call it. Image and video generation also need a model and API Key configured separately in the "Image generation" and "Video generation" sections.

## Custom Skills

`SKILL.md` is plug and play. The entry point is "Extensions" → "Skills" in the top bar; that column holds skills only, while built-in tools sit in the "Tools" column next to it, read-only and not deletable.

How to write a Skill:

- One `SKILL.md` per directory, and the directory name is the skill name.
- The file states the purpose of the skill (the `description:` line) and the steps, conventions and caveats to follow.
- Besides `SKILL.md`, the same directory can hold any reference documents it needs.

Adding and deleting:

- "New skill" creates one by uploading a file; "Import skill" imports from a local path (a directory containing `SKILL.md`, or a single `.md` file).
- "GitHub" imports from a repository; "Discover plugins" scans the standard Codex / Claude plugin directories installed on this machine.
- Skills can be deleted; once deleted, neither the model nor `@` mentions see them any more; built-in tools are unaffected.

## Connecting external MCP servers

In "Extensions" → "MCP" in the top bar, click "+ Add MCP Server" and fill in the name and address to connect external MCP tools. The list shows the connection status, the number of tools it provides and the tool names, and offers connect, disconnect and delete.

Once connected, its tools appear in the tool catalogue and in the `@` mention candidates, and the model can call them the way it calls built-in tools.

**Project-level overrides**: after opening a project, each server in the list gains an extra project button, where you can "disable in this project", "enable separately in this project" or "remove this project's mask", and can also allow only a few of its tools. Overrides like these affect the current project only; other projects stay as they were; the server's address and key always stay in the global configuration and are never written into your project directory. See [Projects, workspaces and per-project configuration](./14-projects.md).

:::tip Naming things in the input box
To specify exactly which tool or skill to use, type `@` in the input box and pick from the candidates; on send, its definition is injected into that message. For the scope and usage of `@` candidates, see [Chat and messages](./05-chat.md).
:::

## Self-evolving tools (tool factory)

`mcp_factory` lets SLATE write the tools it lacks for its own use. Output always lands in the user data area `data/evolved/`, two files per tool: `<name>.py` is the generated code and `<name>.json` is the description and parameter list.

- **Why not write into `backend/skills/`**: that's the program's own source tree — one upgrade wipes out every self-made tool you've accumulated, and a program shouldn't modify itself at runtime. `data/` isn't touched by upgrades, and the list is read as usual after a restart.
- **Old output is moved over automatically**: generated files that historical versions wrote into the source directory are copied into `data/evolved/` at startup (copy only; files in the program's own directory aren't deleted).
- **Where to manage them**: "Extensions" → "New features" in the top bar. Each entry states its current status: normal / disabled / code has a problem (with the syntax error line number) / same name as a built-in tool (already taken over by the built-in).
- **Disabling removes the whole entry**, so it disappears from the model's tool system rather than "reporting an error at call time"; you can enable it again at any time.
- **Overwrite, undo and rollback all back up first** to `data/evolved/.history/` (at most 5 versions per tool). "Version history" in the entry dialog lets you view the original text of any version and roll back; rollback is itself a write, and an older version that doesn't compile isn't allowed to overwrite.
- **Generated code that doesn't compile never lands on disk at all**: the factory only does a compile self-check and never runs it once for you; a create request with the same name as a built-in tool is refused on the spot.
- **On a name clash the built-in wins**: if an upgrade brings a built-in tool with the same name, that self-made code is bumped and marked in the column — visible, undoable at any time, no need to fight the new version.

:::warning These tools grew out of your own use
Self-made tools are written by the model, and their capabilities and side effects don't go through the audit that built-in tools get. Before using one, you can open it in the "New features" column to read the code; if you're not comfortable, disable it or undo it — the backup is still there, ready to roll back at any time.
:::
