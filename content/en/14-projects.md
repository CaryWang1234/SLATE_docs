---
title: Projects, workspaces and per-project configuration
description: Opening Projects, multi-folder workspaces and per-project overrides
section: Projects & Data
order: 14
---

## What a Project is

SLATE treats one folder as one Project, both conceptually and operationally. Once you open a directory, the file tree, Git information, the terminal's working directory and the scope of code search all follow it.

A Project's identity follows the folder's absolute path: reopening the same folder returns to the same Project, with its sessions, constitution and scene (which session you last stopped at, drafts, the board, the default model) all intact, so history does not split into two piles.

## Opening, the register and switching

- The "Open Project…" button in the top-bar Project strip opens a dialog: the top is the "registered Projects" list, where every Project you have opened stays — click one to go back and carry on from the last session and draft; below is a directory path input and disk shortcuts.
- After opening, the **Project name itself is the switcher**: click it to pop up the registered Projects, where you can switch to another Project, pin the ones you use, or remove one from recent (removal only drops the index; it deletes no files or sessions).
- The × in the Project strip **collapses the current Project**, it does not delete it: it stays in the register, and its sessions, constitution and files on disk are untouched; switch back from the Project name at any time.
- ↻ reopens and refreshes the current Project; a Workspace reopens its host directory.
- The number of registered Projects is capped; at the limit, the archived entry that has not been opened for longest is evicted first, and pinned entries are never evicted.

## Project strip and file tree

The Project strip has three more buttons: Better Project Understanding, Code Review, and Project settings (which jumps straight to the constitution section of the Settings page).

The file tree on the left supports descending level by level, breadcrumb jumps and ".." to go up; click a file to preview it in place, and the ＋ in the preview header inserts a snippet into the Chat input — it takes an excerpt first, so a whole large file is not poured in at once.

## Workspace: several folders in one Project

Some work is inherently spread across directories: one repo for the frontend, one for the backend, another directory for docs. A Workspace brings them together in one Project, so you don't have to keep opening Projects.

- In the "Open Project" dialog, fill in a name and one folder path per line, then click "New workspace".
- Member directories appear as pills above the file tree: click one to make it the **current working folder**; the × on a pill removes it from the Workspace (files on disk are untouched), and ＋ adds a folder.
- A "Workspace" badge sits next to the Project name; hover to see how many folders it contains and which one is current.

Why work on only one root at a time: file writes, Git operations and terminal commands all need a single definite target. If you were "on several roots" at once, where a `git status` or a file write should land would be a matter of luck. So a Workspace gathers **scope**, not concurrency — switching the current root is one click, but actions at any moment land clearly in the directory you selected.

## Per-project constitution

The constitution is the Project's rules for the model (technical boundaries, code conventions, architecture constraints). It can belong to one Project alone:

- With a Project open, saving the constitution writes it into that Project's `.slate/config.json` and applies only to that Project; it travels with the repository, so it is still there when handed to a colleague.
- When a Project has no constitution of its own, it falls back to the global one. The two store to their own places, and neither overwrites the other.
- The line under the constitution box on the Settings page states which one you are changing: "Editing the constitution of Project 'X'…" or "Editing the global constitution…". "Project constitution" on the right of Prompt Factory also reads the currently effective one, see [Prompt Factory](./15-prompt-factory.md).

Field names and format:

```json
{
  "rules": [
    "Keep the existing code style; no drive-by refactors",
    "Check that an equivalent implementation already exists before adding a dependency",
    "Write commit messages in Chinese, one line stating the motivation"
  ]
}
```

`rules` is an array of strings, one sentence each. Without `rules`, or with an empty array, no rules are injected. If the content is not valid JSON, the save is rejected and you are told the format is wrong.

## Per-project overrides: Actions, knowledge base and MCP

Same principle as the constitution: **one global copy as the base, and the Project's copy overrides it**. The three differ in the granularity of the override:

| Overridden | Granularity | Where it lives in a Project | How to drop the override |
|---|---|---|---|
| Actions process specs | Overridden by id: put a spec of the same name in the Project and this Project uses it; the global one still applies in other Projects | `.slate/actions/<id>.yml` | Delete the Project copy and you are back to global |
| Knowledge base | Override by title + merge: the Project's batch comes first and overrides global documents of the same title, the rest of the global set stays visible | Ownership is recorded in the knowledge base, not in your repository | Delete the Project's knowledge entry |
| MCP servers | Mask: records only whether this machine enables it and which tools are allowed; it does not change the global configuration | `mcp.servers` in `.slate/config.json` | Remove the mask and you are back to following global |

Lists and editors both mark which copy you are looking at: a Project copy carries a "This Project" badge, and the editor states which copy is being changed. The Action editor also has "Save a copy in this Project", which saves the global copy you have in hand as a Project override; when you are editing the Project copy, the delete button reads "Drop override" and notes that dropping it returns this Project to the global copy.

:::warning MCP addresses and keys never enter the repository
The Project's `.slate/config.json` records only whether this server is enabled (and optionally a tool allowlist); addresses and keys stay in SLATE's local MCP configuration:

```json
{
  "mcp": {
    "servers": {
      "my-server": { "enabled": false },
      "another": { "enabled": true, "tools": ["search", "fetch"] }
    }
  }
}
```

`tools` omitted or empty means everything is allowed. Pushing the whole repository to a remote carries no URL or key with it.
:::

## Better Project Understanding

When you take over a Project, the most time-consuming part is not writing code but working out how this pile of directories actually runs. This feature has AI read the Project within a budget and produce two documents:

- **Tour · encyclopedia**: Project overview, tech stack, annotated directory structure, core modules, entry points and how to start it (the detailed level also maps data flow and call chains).
- **Rulebook**: technical boundaries, code conventions, architecture constraints, run and build commands. Every rule must be derived from evidence that actually exists in the Project, written as directly executable imperatives.

The scan budget has three levels:

| Level | Directory tree depth | Files read closely | Output size |
|---|---|---|---|
| Brief | 2 levels | 6 key files | about 900 characters |
| Balanced | 3 levels | 16 key files | about 1800 characters |
| Detailed | 5 levels | 36 key files | about 3200 characters |

Files to read closely are picked by priority: README, dependency manifests and build configuration, and core entry files come first; at the same level, shorter paths win, so deep generated artifacts do not crowd out entry files. Generation can be cancelled at any time; it writes only from the evidence it scanned, and anything it cannot determine is marked plainly "to be determined".

The result is persisted in the Project's `.slate/config.json`, so the next time you open the Project you can read it directly without regenerating. The two documents can be switched between and copied separately, and you can change level and regenerate. This is the most expensive AI feature in the whole table; it can be turned off under Settings → AI-assisted features, or pointed at a cheaper model.

## Code Review

Code Review reads `git diff` and has AI do a structured review along four dimensions. There are three ways to take the diff, suited to different situations:

| Mode | What it reads | When to use |
|---|---|---|
| Unstaged changes | What changed in the working tree but has not been `git add`ed | Self-checking the batch in hand before committing |
| Staged changes | What has been `git add`ed and is ready to commit | Gatekeeping the batch about to enter a commit |
| Commit range | Commits between a start point and an end point (end defaults to `HEAD`) | Reviewing one commit, or a few changes on a branch |

Four review dimensions: code quality (naming, style, logic, duplication, error handling), security (injection, sensitive information leakage, authentication and authorisation, input handling), performance (complexity, needless computation, memory risk, N+1 queries) and maintainability (coupling, interface design, comments, test hints). Results come in three views:

- **Full report**: overall assessment + analysis of the four dimensions, formatted in Markdown.
- **List of line-level comments**: cards sorted by severity, in four levels — "critical / major / suggestion / info"; clicking `文件:行号` on a card copies the location to the clipboard, so you can jump to it back in your editor.
- **Four-dimension cards**: the four dimensions side by side, each with a summary and its number of related comments.

The report can be copied whole; to review again, change the mode or the range. The prerequisites are that the directory really is a Git repository and has changes — if it is not a Git repository it tells you straight away, and with no changes it says plainly "no review needed". Very large changes are truncated, with a note in the summary. The model used can be set separately under Settings → AI-assisted features → Code Review.

## Running in parallel across Projects

Switching Projects no longer interrupts a Chat that is generating. The relevant Settings are all under Settings → Multitasking and Projects:

| Setting | Default | Description |
|---|---|---|
| Let it keep running when I switch sessions | On | The session you leave carries on in the background, its progress and outcome landing in the task centre on the right; turn it off for the old behaviour: switching sessions interrupts this one |
| How many run at once | 2 | Overall cap for cross-Project parallelism, 1–4 |
| How many per Project | 1 | Serial by default within a Project, 1–3 |

A send beyond the cap is not swallowed: it goes into the queue, and both above the input box and in the task centre on the right it states "queued" and how many sessions are still waiting; it picks up automatically when the previous one finishes. Under any Settings, the stop button only stops the session on screen.

The background session works with its own Project scene — files, terminal, constitution and knowledge base snippets all follow the Project it belongs to, and are not written into the Project you are currently looking at. Each session's tokens are counted separately, and the usage bar reflects only the session on screen.

:::tip When to use global, when to write into the Project
**Write into the Project**: rules, processes and knowledge that hold only for this one repository — "this repo uses pnpm", "lint must run before any change", "the pitfalls of this deployment script". They travel with the code, and survive a machine change or a handover to a colleague.

**Keep it global**: things that hold across Projects — your preferred way of phrasing, general Workflows, frequently used reference excerpts. The global copy is the fallback for every Project; when a Project has nothing of its own, it is used.

The test is simple: if this content were copied into another Project, would it mislead? If yes, write it into the Project.
:::
