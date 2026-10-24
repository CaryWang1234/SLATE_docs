---
title: Prompt Factory
description: Turn scattered thoughts into a deliverable Prompt
section: Projects & Data
order: 15
---

## What Prompt Factory does

It takes a task you have already thought through and organises it into a Prompt you can paste straight to an external Coding Agent: Context, project rules, constraints and delivery requirements each in their place, with no need to write it from scratch every time.

SLATE's role here is **organiser**, not executor: it lays out the Context and constraints, and the actual code changes are left to the external tool.

## The three areas on screen

| Area | What's there | How you use it |
|---|---|---|
| Left workbench | Three dropdowns — target Agent / task type / output tone — and three inputs: task description, relevant Context, constraints | Where you do most of the writing |
| Right sidebar | Project constitution, referenceable files, quality check | Tick files, check for gaps |
| Result area below | The generated Prompt, plus three buttons: copy, download Markdown, save as material | Take it away from here once generated |

At the top of the workbench there are two more: reference recent Chat, and clear.

## Who the output goes to

You pick the target Agent first; different presets rewrite the `# 执行对象` and `# 交付要求` sections:

| Target Agent | Positioning appended at generation | Delivery requirements |
|---|---|---|
| Codex | Implement, verify and explain the result in the current codebase | Make the changes directly, then state the changed files, how they were verified and the remaining risk |
| Claude Code | Complete the code changes in the existing engineering style | Read the relevant files first, then make the minimal necessary changes, then give the test results |
| Cursor | Used as an in-editor task instruction | Give clear editing steps, target files and the behaviour to preserve |
| General Agent | Hand to any Coding Agent to execute | Output an executable plan, the necessary changes and a verification checklist |

## Assembly order

After you click "Generate Prompt", SLATE assembles the final text in the order below. Empty sections are skipped entirely, so nothing in the result is a placeholder.

| Order | Section | What goes in | How to write it better |
|---|---|---|---|
| 1 | `# 任务` | What to do, why, and what counts as done (required) | Put the acceptance criteria straight into the task; "optimise it a bit" is the easiest way to invite improvisation |
| 2 | `# 执行对象` | Who it goes to, and how they should deliver | Decided by the target Agent preset; the preset can be changed |
| 3 | `# 工作方式` | Explore first or get straight to work; whether to audit risk first | Decided by "output tone": execute directly / audit cautiously / explore then implement; it also always requires "read the existing code before acting, and prefer the Project's existing patterns" |
| 4 | `# 项目宪法` | The currently effective constitution rules, numbered one by one | Comes from the Project or global copy, see [Projects, workspaces and per-project configuration](./14-projects.md); it does not appear when there are no rules |
| 5 | `# 重点文件` | The list of file paths you ticked | Paths cost fewer tokens than pasting content; the external Agent reads them itself |
| 6 | `# 已知上下文` | Errors, interface contracts, key code snippets, a summary of the recent Chat | Only what the other side cannot see; this content is carried over as is |
| 7 | `# 约束条件` | What must not change, what must be preserved, which styles or processes to follow | Complements the constitution: the constitution governs the long term, this governs this one job |
| 8 | `# 交付要求` | Decided by the preset, plus two fixed items | Fixed requirements: do not modify files unrelated to the task; if there are existing uncommitted changes, understand and accommodate them first; when done, state the verification command or why verification was not possible |

## Task templates

If you don't want to start from a blank page, pick a task type first; it pre-fills the task description and constraints:

| Task type | Pre-filled skeleton |
|---|---|
| Feature implementation | Implement / expected behaviour / acceptance criteria; constraints: follow the existing architecture and style, keep the change as small as possible, run checks when done |
| Bug fix | Symptom / reproduction path / expected result; constraints: locate the root cause first, do not roll back unrelated changes, add verification that covers the problem |
| Code review | What to review / what to focus on; constraints: list problems by severity, each with location, risk and a suggested fix |
| Refactoring | Refactoring goal / behaviour to keep unchanged / problems you want improved; constraints: external behaviour stays compatible, no large new dependencies, follow existing patterns |

A template only fills an input that is empty; it never overwrites what you have already written.

## Output tone

"Output tone" only affects the `# 工作方式` section of the result, independently of task type:

| Output tone | The sentence written into the Prompt |
|---|---|
| Execute directly | Please go straight into execution; no long plan preamble is needed |
| Audit cautiously | Please audit the risks and boundaries first, then make changes |
| Explore then implement | Please give 2-3 viable directions first, then choose the safest one to execute |

All three tones append the same requirement: read the existing code before acting, and prefer the Project's existing patterns.

## What the result looks like

The result is a Markdown document assembled in the order above, with sections separated by `#` headings:

```text
# 任务
修复登录接口在密码为空时返回 500 的问题，修复后接口应返回 400 与明确错误码。

# 执行对象
交给 Claude Code 按现有工程风格完成代码修改。

# 工作方式
请先审计风险和边界，再做修改。
阅读现有代码后再行动，优先沿用项目已有模式。

# 项目宪法
1. 改动必须保持现有代码风格，不做顺手重构
2. 新增依赖前先确认项目里已有等价实现

# 重点文件
- backend/routers/auth.py

# 约束条件
不要改动返回体的字段名，前端已在依赖。

# 交付要求
请先阅读相关文件，再执行最小必要修改，最后给出测试结果。
不要修改与任务无关的文件；遇到已有未提交改动时，先理解并兼容它们。
完成后说明验证命令或无法验证的原因。
```

What you get is final text: paste the whole thing into the external tool, with no preamble to add.

## Where the constitution comes from

"Project constitution" in the right sidebar shows the currently effective rules; clicking "Insert project constitution" writes them into the constraints, numbered by item. The rules come from the Project's own `.slate/config.json`; if the Project has none, the global copy is used, and the sidebar follows when you switch Projects. The full rules are in [Projects, workspaces and per-project configuration](./14-projects.md).

## Division of labour with Grind Mode

Both turn thoughts into text; the difference is the starting point:

| | Grind Mode | Prompt Factory |
|---|---|---|
| Starting point | A rough idea; you don't yet know exactly what you want | The task is already clear; you just need a delivery format |
| What it does | AI's three-stage questioning (Intake → Grind → Collect), one question at a time, drawing out the gaps | Fills known information into a fixed skeleton and assembles final text |
| Output | A structured task brief (ink brief): goal / audience / deliverable / acceptance criteria / boundaries / suggested path / open questions | A Prompt you can hand straight to an external Agent |
| Next step | Send it to Target Mode to execute, post to Whiteboard to work through, or save as a template for reuse | Copy, download or save as material, then hand to an external tool to execute |

One line if you can't tell them apart: if you still can't say what you want, go to [Grind Mode](./07-grind.md); if you can, come to the Factory.

## Division of labour with Target Mode

Target Mode has SLATE do the work itself: it has its own Tools (read and write files, run commands, inspect Git) and runs a six-stage loop until verification passes, see [Agent Autopilot and Target Mode](./06-autopilot.md). Prompt Factory executes nothing; what it produces is **a Prompt for someone else to execute** — if you want Claude Code, Codex or Cursor to do the work, use the Factory.

## How to use the result

1. **Check it section by section**: the result appears below; read from `# 任务` down, focusing on whether acceptance criteria and boundaries are missing.
2. **Copy / download / save material**: the three buttons at the top right of the result area are copy, download Markdown and save as material. Material goes into your Prompt material library, ready to reuse next time.
3. **Iterate**: change one input and click "Generate Prompt" again — the output is reassembled whole, not appended to. To start over, click "Clear".

"Quality check" on the right gives four live prompts as you write: whether the task is clear enough, whether Context or files are included, whether constraint boundaries are declared, and whether a target Agent is selected. All four lit does not guarantee a good result, but a missing item usually means this Prompt needs another pass.

Two shortcuts: "Reference recent Chat" puts a summary of the last few messages in the current session into the known Context; "Insert ticked files" reads the content of the files ticked on the right (at most 8 at a time, the first 6000 characters of each). The file list reads the current Project directory; with no Project open it prompts you to open one first.

:::tip The acceptance criteria and boundaries matter most
External Agents fear two things above all: not knowing when the job counts as done, and not knowing what must not be touched.

- **Write acceptance criteria as decidable facts**: "`npm test` is all green" is clearer than "tests pass"; "the response fields and signature are unchanged" is clearer than "stay compatible".
- **Write boundaries as explicit prohibitions and protections**: "do not touch files under `src/legacy/`", "keep the existing public API signatures", "add no new dependencies".
- **Also state what not to do**: saying "this time change only this one file" is far safer than letting the Agent guess the scope.
:::
