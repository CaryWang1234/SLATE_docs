---
title: "Interface overview: tabs and the three-column workspace"
description: The top bar, the five workspace tabs, the Chat area and the input area, explained piece by piece
section: Start
order: 3
---

This page walks you through the main interface from end to end, so you know where each entry point is and what happens when you click it.

Remember one sentence first: SLATE is **one top bar plus four workspaces**; only one is shown at a time, and clicking a top-bar tab switches between them.

## Overall layout

| Area | Where | What you can do |
|---|---|---|
| Chat | Top-bar tab "Chat" | Talk to the model, run Agent loops, see tool cards and the Task list, manage conversation history |
| Whiteboard | Top-bar tab "Whiteboard" | Cards plus connections to organise thinking; switch between the Git tree / flow / kanban / outline / Workflow views |
| Extensions | Top-bar tab "Extensions" | Manage what the model can use: seven columns — Skills, built-in tools, modes, new features (self-made tools), MCP, Expert Packs, Actions |
| Factory | Top-bar tab "Factory" | Integrate project context, task and constraints into a deliverable Prompt |
| Settings | Top-bar tab "Settings" | Model keys, Context, Approval mode, Backup, LAN and About |

Settings is a standalone configuration area and doesn't count as a workspace.

:::note "Three columns" refers to inside the Chat page
What people usually call "three columns" is not in the top bar; it's the three columns the **Chat** workspace splits into itself: the **left sidebar** holds three tabs — Projects, Tasks and Summary; the **middle message stream** holds the Chat content and the input box; the **right edge** slides out the Task list column, the background task panel and the Ink panel on demand. Team Chat is a mode switch inside the message stream, not a fourth workspace.
:::

:::note A suggested order for finding your way around
The interface is fairly dense; on first use, walk it in this order: **top bar → four workspaces → Chat area left sidebar → message area → input area**. Pause at each spot and just see what buttons are there; there's no need to memorize everything at once.
:::

## Top bar

The top bar spans the whole window and splits into three sections:

- **Left**: the app mark (砚 · SLATE).
- **Centre**: five tabs — **Chat / Whiteboard / Extensions / Factory / Settings** — for switching workspaces.
- **Right**: four round buttons.

| Top-bar button | What it does |
|---|---|
| Keys | Jumps straight to "Model config" in Settings, to manage model keys |
| Remote | Jumps straight to "LAN remote control" in Settings, to see the mobile access address |
| Light/Dark | One-click switch between the light and dark themes; while a custom theme is on it dims and locks, and clicking it explains why |
| Settings | Opens the Settings page |

When a new version is found, the banner appears directly below the top bar, with a download entry point and "Ignore This Version".

:::tip Can't find a setting
"Keys" and "Remote" at the top right of the top bar are two shortcuts: they open the very same Settings page, just scrolling automatically to the matching block. So when you can't remember where something lives, these two buttons in the top bar are the fastest way in.
:::

## Left sidebar

On the left of the Chat area is the sidebar, with three tabs at the top: **Projects / Tasks / Summary**. The divider between the sidebar and the message area can be dragged to adjust the width.

### Projects tab

- At the top is the current project name and its action entry points; when the project is a workspace it carries a "Workspace" badge.
- Below is the project file tree; click a file to preview its content right underneath.
- In the registered projects list you can switch projects, or open a new directory.

### Tasks tab

This is the entry point for all your sessions:

| Element | Description |
|---|---|
| ＋ New Chat | Start a new session, shortcut `Ctrl + N` |
| Sort dropdown | Recently updated / By project / By status / Creation time / By usage |
| Manage | Bulk manage historical sessions |
| Search box | Search historical sessions; a match shows a Context excerpt |
| Session list | Each session carries its own status marker |

**There are four status markers in total**, and they record "how the previous session ended":

| Marker | Meaning |
|---|---|
| Needs action | The previous session was stopped, or there is a next step waiting for your decision |
| Error | The previous session ended in failure |
| In progress | This session is genuinely generating right now; the icon has a breathing animation |
| Done, unread | It finished but you haven't clicked into it yet; clicking into the session clears it |

The sort preference syncs across devices; status markers only travel on your own machine and never reach another device.

### Summary tab

Summarizes the usage of the current session in one place, so you can see how much this session cost.

## Middle Chat area

On the left of the message area's title bar is a two-mode switch, **Chat / Team**: everyday Q&A and writing code go in "Chat"; to have several roles debate or to run a Workflow, switch to "Team".

On the right of the title bar is a row of action buttons:

| Button | What it does |
|---|---|
| Compress context manually | Compress the conversation history right away, without waiting for the automatic threshold |
| Memory & profile | View and manage long-term memory and the User Profile |
| Expert Pack management | Import, export and edit Expert Packs |
| Prompt material | Manage reusable prompt snippets |
| Task list | Collapse or expand the Task list column on the right of the message area |
| Background tasks | See the status and output of background terminal tasks |

Below the title bar is a usage info bar, showing the Token consumption of this session.

**The message area body**, from top to bottom:

- the Chat message stream, each reply tagged with the model name and usage;
- tool call cards, showing the Tool name, parameters and execution status;
- a collapsible thinking panel that expands live while the model reasons and collapses automatically once thinking is done;
- the Task list column on the right, showing progress item by item while a big task runs, and collapsible as a whole;
- the background terminal task panel and the Grind Mode Ink panel, which appear only in their own contexts.

## Input area

The input area sits at the bottom of the message area and consists of a multi-line input box row plus a toolbar row.

**Input box**: supports multiple lines. `Enter` sends, `Shift + Enter` inserts a new line.

**Toolbar left side**, starting from the "＋" button:

| Control | Description |
|---|---|
| ＋ Mode menu | Collects every mode entry point; see the next section |
| Reply mode | The mode capsule at the lower left of the input box, deciding how this session works: four levels — Smart / Chat / Economy / Turbo — each with its own icon and colour, and custom modes are possible too; switching only changes this session, while the default level and custom modes are managed in "Extensions → Modes" |
| Approval mode | When this session should stop and ask you, four levels, changeable at any time: Manual approval / Auto approval / Full access (capsule marked red) / Night mode; pick "Night mode" and it asks nothing at all |
| Add attachment | Send files along with the message |
| Expert Pack | Pick an Expert Pack; its persona and rules apply throughout |
| Model | Which model this session uses |
| Reasoning effort | Offers levels based on what the model can do, each labelled below with the matching ink tone; levels this model can't handle are greyed out with the reason stated |

**Toolbar right side**, in order: polish prompt, voice input and send. While generating, the send button becomes **Stop** — clicking it really cancels, it doesn't just make the interface go quiet.

Clicking **Polish prompt** (the star to the left of the voice button) hands the half-written draft in the input box to the current model to rewrite, but the rewrite doesn't go straight into the input box: it is first placed side by side with the original in a popup for you to compare, and only clicking **Use it** writes it back. Clicking **Keep original**, pressing Esc, or clicking outside the popup all count as keeping the original, and not one character in the input box changes. If you edit the draft again during the few seconds you're waiting (including characters written in live by voice), that result is discarded and won't overwrite what you just wrote. Which model is used can be set separately in [Settings → AI-assisted features](./19-settings.md); turn it off and not a single request is sent.

### ＋ Mode menu

Click the "＋" to the left of the input box and a "Modes & features" menu pops up, containing four mode rows plus a mention group:

This menu is pinned directly above the "＋" button and feels the same as the Approval mode and reasoning effort on the same toolbar: pressing "＋" again, clicking anywhere outside the menu, or pressing Esc all collapse it.

- **Grind Mode** — grinds a rough idea into a task brief; the small inline text shows the current grinding progress.
- **Brainstorm** — a toggle.
- **Target Mode** — a toggle, the explicit six-stage strong closed loop.
- **Scheduled Tasks** — create and manage scheduled / event tasks.
- **Mention (@ prefix)** — Skill / Tool / MCP / file; clicking any of them pops up the matching candidate list, and the selection is written into the message as a mention.

## Theme and appearance

The "Light/Dark" button in the top bar switches between light and dark in one click, effective immediately. This preference syncs along with your settings, so accessing the same SLATE from another device gives you the same theme.

To change the whole face, go to **Settings → Custom theme**: four source colours (background / panel / body text / accent) plus two font sets — body text and code (you can import your own font files too) — plus section opacity, one local background image and mask density, with 10 basic presets you can click straight away; if you have Wallpaper Engine installed, you can even grab the preview image of the wallpaper it is currently using as the background. The other thirty-odd colour tokens are derived from these four source colours, with contrast as the fallback during derivation, so the palette never smears into something unreadable.

While a custom theme is on, the light/dark switch is locked — two palettes talking at once would only contradict each other. The button doesn't grey out; clicking it tells you why nothing changed and where to turn it off. Details are in [Settings & security approvals](./19-settings.md).

## Mobile switches to its own interface automatically

When you open the LAN address in a phone or tablet browser, SLATE automatically enters the mobile interface, with five tabs along the bottom. Accessing from a desktop browser still gives you the full desktop interface. See [Mobile remote control & LAN access](./18-mobile.md).

## New user guide

A guide pops up on first launch, using cards to introduce the most-used entry points. To see it again, go to **Settings → About** and click the "New user guide" button.
