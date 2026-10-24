---
title: Actions process specs
description: Write repeated processes as a spec and let the model follow it
section: Chat & Automation
order: 9
---

By the second time you do the same thing you're restating the order, the conventions and the pitfalls you already hit. Actions is the cure: write "the necessary process for doing something" down ahead of time as a spec, and the model reads it when needed and follows it — you don't have to brief it every time.

## What Actions are

An Action is a process spec. It states three things: when this thing should be done, in what order it should be done, and what counts as passing.

Once written, in agent mode the model first sees an Action catalogue (each entry only has an id, name, one-line description and when it applies); when it judges that this task matches a spec, it reads the full text and actually executes the steps. You define the process; the model is only responsible for following it.

## How it differs from a Skill

Both live in the local data directory and are managed in the same place, but they answer different questions.

| Aspect | Action process spec | Skill |
|---|---|---|
| Nature | An executable agreement on steps | Knowledge and role |
| Question it answers | In what order this should be done | How this kind of thing is done, and in whose identity |
| Content form | Ordered steps, each may note a suggested tool and a checkpoint | A description document, `SKILL.md` |
| How it's used | The model searches the catalogue → reads the full text → executes the steps | Once written as a Skill, an `@` mention in chat injects it into context |
| Limits | Follows a strict writing format; a broken file reports the line number | Document form, free writing |

In one line: a Skill makes the model "know", an Action makes the model "act in your order". The two can be used at the same time. For the complete list of built-in tools and skills, see [Built-in tools and skills](./08-tools-skills.md).

## Where the files live

One file per process; the file name without `.yml` is its id (for example, the id of `weekly_report.yml` is `weekly_report`). An id may only contain `a-z0-9_-` starting with a lowercase letter, at most 48 characters, and doesn't need to be written inside the file again.

- The global one: shared by every project on this machine.
- The project one: put it in the current project's `.slate/actions/`; on a name clash it overrides the global one.

If you're not sure where to put it, start with global and override it in the project when needed.

## How to write the fields

A spec consists of the following fields, all written by people and read by the model:

| Field | What to write | What the model judges from it |
|---|---|---|
| `name` | Process name, at most 40 characters | Recognising it in the catalogue |
| `description` | One-line description, at most 120 characters | Whether this spec is worth opening to read in full |
| `when` | When it should apply, at most 200 characters | Whether this request should follow this process |
| `inputs` | Inputs to collect from you before starting, at most 8 | What to ask you first, then what to do next |
| `steps` | Step list, 1 to 24 steps | In what order, which tool to call, what counts as passing |
| `output` | Output requirements: format and destination | What is finally delivered, and where it goes |
| `tags` | Tags, at most 8, each at most 24 characters | Keywords matched during retrieval |

Each `inputs` item can have:

| Key | Description |
|---|---|
| `key` | Name of the input item, starts with a lowercase letter, only `a-z0-9_` allowed |
| `label` | The name shown to people; `key` is used if omitted |
| `type` | One of `text` / `number` / `textarea` / `select`; `text` if omitted |
| `required` | Only `true` or `false` |
| `options` | Needed for `select` only, at most 20 items |

Each `steps` item can have:

| Key | Description |
|---|---|
| `title` | What this step does, required, at most 60 characters |
| `tool` | Suggested tool name, e.g. `git_tool`, `doc_write` |
| `detail` | Specific requirements for this step; multi-line text uses a `|` literal block |
| `check` | Checkpoint for this step, at most 200 characters |

In `output`, `format` states the format of the produced file or body text; `destination` may only be `message` (stays in the chat), `file` (write a file) or `board` (back to the whiteboard); when it is `file` you must also give `path`.

## A minimal example to copy

```yaml
name: Weekly report
description: Turn this week's commits and progress into a weekly report
when: When the user asks for a weekly report or to organise this week's progress
inputs:
  - key: scope
    label: Scope
    type: text
    required: true
steps:
  - title: Collect material
    tool: git_tool
    detail: |
      Read this week's commit log and change statistics, grouped by module.
    check: Every module has a corresponding commit source
  - title: Draft the report
    detail: Draft in three sections — "this week's progress / risks / next week's plan", each with no more than five items.
  - title: Write to disk
    detail: Write into the docs/weekly/ directory, with this week's date in the file name.
output:
  format: markdown
  destination: file
  path: docs/weekly/weekly.md
tags:
  - weekly report
```

Save this file as `weekly_report.yml` and it appears in the Action catalogue.

## Hard constraints on the writing format

Actions use a trimmed YAML subset that only supports what you actually need. Syntax outside that range isn't "guessed at" — it's refused outright, and you're told which line it's on.

- Indentation is fixed at 2 spaces, with at most two levels of nesting. Tab indentation is forbidden.
- Arrays use block style: one `- ` per line, and the `-` at the same level must line up.
- Multi-line text uses `|` or `|-` literal blocks, with consistent indentation inside the block.
- Booleans accept only `true` / `false`.
- Anchors and aliases (`&`, `*`), multiple document separators (`---`), folded scalars (`>`), flow style (`[]`, `{}`) and unclosed quotes are not accepted.
- A single file is capped at 64 KB; all `detail` text together may not exceed 20000 characters.

A validation error reads "Line N: reason"; fix it and save again.

:::warning Don't write keys into a spec
The content of an Action goes into the model's system prompt for the long term, which amounts to putting the Key right in front of the model. When you need credentials, write "reference an environment variable or file location", not plain text. The panel warns about suspected credentials but won't stop them for you.
:::

## How the model uses it

In agent mode the model first receives an Action catalogue listing at most 20 entries; beyond that it's told only the count, plus to use Action retrieval to see them all. Its typical behaviour is three steps: retrieve → read the full text → execute the steps. In chat mode no tools are available, and the whole catalogue isn't injected.

One point worth stressing: **reading a process is not the same as having done it**. Where a step names a suggested tool, the model still has to actually call a tool to complete it; it won't claim the work is done just because it "read this file".

## Sending a process into the chat manually

If you don't want to wait for the model to retrieve on its own, you can name it directly:

- Type `@` in the input box and pick an Action from the candidates; the whole process is injected into that message.
- Injection is capped at 6000 characters; anything beyond is truncated, with a hint for the model to use the read tool to fetch the whole thing.
- Mentions use the id (file name); the display name and tags serve only as search aliases.

The use case is when you already know which process to use and just want it followed strictly this one time.

## Running one on the whiteboard

Open the board → "Workflow" display mode, and every Action becomes a card on the card wall, with the card face saying how many steps, how many inputs, who wrote it and where the output goes. "Run this" on the card sends it into the current chat as an @ mention, "View steps" expands the step list in place, and "Pin" puts frequently used ones first.

The workflow view also shows how far this run has got; for details see [Whiteboard-style logic chains](./12-whiteboard.md).

## Editing on the settings page

"Extensions" → "Actions" in the top bar: click "+ New Action", or click an existing entry to open the editor.

The editor validates as you write, and errors point out the line and the reason; you can't save until validation passes. The top of the editor states which one you're editing: the global one, or a project's override.

## Letting the model write it for you

You can also just have the model write the process down — on condition that it declares `author: model` as required, and the panel marks the file as "model-written" accordingly.

In "Ask" permission mode a dialog shows you the original text before writing, and it only lands on disk when you click allow; switch to "Auto" or "Bypass" and the dialog no longer appears. In every tier the format check runs before writing, so content that doesn't pass never gets in.

:::tip The Action with the best return
Pick a process you've already explained to the model twice or more. Write it once, and from then on it reads it and follows it itself; what you save is every future restatement.
:::

## Backup and rollback

Before every overwrite or deletion, SLATE backs up the original text first, keeping at most 5 versions per file. "Version history" in the editor lets you view any version and roll back in one click; a rollback is itself a write and is validated before it lands.

Backups follow the destination: the project copy's history stays in the project's own directory and never mixes with the global one.

## Per-project overrides

Place a spec with the same id in an open project (`<project-root>/.slate/actions/<id>.yml`) and it overrides the global one, while the other processes stay visible as before — processes don't "all disappear the moment you enter a project".

The list marks which entry is the "this project" copy, and the editor states which one you're editing. Delete the project copy and the process with the same name falls back to the global one automatically — this isn't deleting the process outright. For how project and global relate, see [Projects, workspaces and per-project configuration](./14-projects.md).

## Broken files don't vanish into thin air

Break a file and it isn't silently ignored: the Actions list on the settings page still lists it along with "Line N: reason"; the tool return the model gets also tells it which ones are temporarily unavailable; and the card wall in the workflow view indicates how many specs failed to parse. When you see a notice like that, fix it back using the line number.
