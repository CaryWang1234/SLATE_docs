---
title: Whiteboard logic chains
description: Cards and connectors put your thinking, dependencies and the live run on one screen
section: Collaboration & Reasoning
order: 12
---

When you can't think it through, lay it out and look. The Whiteboard lets you turn ideas, features and to-dos into cards and mark dependencies and data flow with connectors; it is also the dashboard for this conversation — how far a tool has got and how this session is controlled are both visible on the same screen.

## What the Whiteboard is for

Three things:

- **Externalise thinking**: write whatever comes up as a card first — no need to order it yet, connect and tidy it later.
- **See dependencies**: a connector means "who depends on whom" and "where data flows from and to"; the arrow direction is the order.
- **Act as the live run**: tool execution leaves step cards automatically, and the workflow view can control how this conversation runs, in place.

The Whiteboard is linked to the current conversation: a Team Discussion can read the cards on the board as background, and you can also post an ink brief to the Whiteboard to work through it.

## Basic operations

Enter from "Whiteboard" in the top bar; it opens on the free canvas.

- **New card**: the "＋" button in the top bar, or click "Root card" in the flow view to start a new process.
- **Move and lay out**: drag cards directly. "Auto-arrange layout" in the top bar arranges them in layers by connector relationships (shortcut `Ctrl + L`).
- **Edit a card**: double-click a card to open the edit dialog, where you can change the title, body, colour and connections.
- **Multi-select**: hold `Shift` (or `Ctrl` / `Cmd`) and click to add to or remove from the selection; with several selected, `Ctrl + D` duplicates and `Delete` removes.
- **Connect**: switch the tool to "Connect", then click the start card and the end card. A connector is dependency and data flow.
- **Pen and text notes**: the toolbar switches to the pen for freehand drawing; in "Text" mode, click a blank spot to write a note.
- **Hide pen marks**: "Undo stroke" undoes the last stroke; "Clear all strokes" wipes them all at once.
- **Export and clear**: the top bar exports the whole board (cards, links, colours, Mermaid source and JSON); "Clear board" removes every card — confirm the prompt before you do.

Press `Esc` at any time to clear the selection and return to the "Select / Move" tool.

## Card colour is its category

Colour is not just looks: the kanban view and AI organisation both categorise by it:

| Colour | Meaning |
|---|---|
| Default | Uncategorised |
| Red | Risk |
| Orange | To do |
| Yellow | Idea |
| Green | Done |
| Blue | Information |
| Purple | Creative |

If unsure, leave it on default and colour things in one pass when you tidy up — in the kanban view, changing column changes colour.

## Links with Chat, Team and Ink

The Whiteboard is not an isolated picture; it connects to several capabilities:

- **Models can read and write the board directly**: reading existing cards, adding cards, updating titles and bodies, changing dependencies, changing colours, plus batch operations and clearing. So you can simply say "turn these ideas into cards and connect them", and it will do the arranging.
- **AI organise into a flow chart**: the organise button in the top bar rebuilds card titles, bodies, dependencies and colours as a whole, keeping existing card IDs unchanged. It is "Whiteboard AI organisation" under "Settings → AI-assisted features", and can be turned off separately or pointed at a specific model.
- **Team Discussion reads the Whiteboard**: when you start a Team Discussion, the cards currently on the board are handed to each member as background, so they discuss what you have already written down instead of guessing again.
- **ink briefs can be posted here**: after Grind Mode collects the ink, click "Post to Whiteboard to work through" to lay the task brief out as cards and keep working it, see [Grind Mode](./07-grind.md).

## Live Mermaid rendering

Cards and connectors automatically produce a Mermaid diagram (direction left to right), rendered live into a flow chart by Mermaid.js. The chart button in the top bar shows or hides this rendered area; the diagram is redrawn as soon as a card changes.

If rendering fails (for example, a special character in a card title), the panel shows the reason in place, and the Whiteboard itself is unaffected.

## Six display modes

The top bar has five view buttons, plus the default free canvas — six ways to look at it in all. Clicking the currently selected button again returns to the free canvas.

| Mode | What you see | When to use |
|---|---|---|
| Main board (free canvas) | Cards, connectors, pen, text notes | Divergent tidying, laying things out freely |
| Flow | Cards listed in stages by dependency level, each marked with its input and output counts | Seeing the order and the merge points |
| Kanban | Columns by card colour; drag into another column to recategorise | Moving one thing through its states |
| Outline | A tree expanded by connector hierarchy, collapsible level by level | Long lists, hierarchies |
| Git tree | The repository structure of the currently open Project | Understanding branches, commits and worktree state |
| Workflow | Control bar + process card wall + current run + team star map | Watching while it runs |

The flow and kanban views both carry an "Arrange" button that syncs the current view's levels or column order back to the canvas. The outline view lists cards with no connectors separately under "Unconnected cards", reminding you there are still isolated ideas.

## Git tree view

You need a Project open first; the Git tree reads the state of that Project's repository. It recognises and draws:

- The repository itself, HEAD, the current branch, local branches, remote branches, tags and remotes.
- The worktree list, and stashes.
- The working tree's three counts: staged, modified, untracked (each with a file count; "no changes" when there are none).
- Unpushed commits, and the recent commit log.

Node positions and the whole view can be dragged; the arrangement you make is stored on this machine, so it is as you left it next time. With no Project open it says so, rather than drawing an empty graph.

## Tool step cards recorded automatically

Every tool execution automatically creates a step card on the canvas; you don't have to note it down.

- The card title reads like "Step N: <what this step does>", the body summarises the step's parameters and is replaced by a result excerpt once the step finishes.
- Colour shows state: **yellow = running, green = done, red = error**; cancelled is the default grey.
- Cards are automatically chained in call order.
- State changes only write back to the card body and colour; the number and position stay put, so the board does not jump around mid-run.
- When a new run starts, the previous batch of step cards is cleared as a batch, leaving only this round's on the board.

In the flow, kanban and outline views, step cards are hidden by default; "Show tool steps" at the top right brings them out.

:::note Step cards are passive
They record what this session actually called; they consume no tokens and take no prompt budget. To see what a tool actually did, this is the most reliable place to look.
:::

## Workflow view: four blocks on one screen

Switch to Workflow mode: this screen is both console and live floor.

**Control bar**: stop, resume and finish, auto-advance (the Target Mode switch), reply mode (four built-in levels + custom, any level selectable), thinking effort (auto / off / low / medium / high). The available levels follow the current model's capabilities; a level the upstream does not recognise never appears. These controls do not keep a separate state — they write the same state as the top of the chat box, so the two can never disagree. Next to them is "Go to Team", which jumps straight to Team mode.

**Process card wall**: each Action process spec is one card; the card face shows how many steps, how many inputs, who wrote it (you / the model), where the output lands, and the tags. "Run this" sends it into the current conversation as an @-mention, "View steps" expands the step list in place, and "Pin" puts the ones you use most first (with "Pinned only" to narrow the wall). If a spec fails to parse, a hint appears here. For how to write a spec, see [Actions process specs](./09-actions.md).

**Current run**: projected straight from the run record — which step is running, how long it has run, whether it succeeded. With no record it says so plainly: this session has no run record yet, or this round is still thinking and has not called a tool.

**Team star map**: lays out the most recent Team Discussion of this conversation by role — who replied to whom, which Tools each touched, which subagents they spawned — all taken from real records. Click a member to see its recent speech sequence. With no team record for this conversation, it says so directly rather than drawing a decorative graph.

## Thinking process display

The model's reasoning and thinking before it acts is shown live in a collapsible panel; once thinking is done it collapses automatically, and clicking the header expands it again to review. It is a separate block and never mixed into the actual answer.

:::tip Whiteboard contents stay on this machine
Cards, text notes, pen strokes, Git node positions and the workflow view's pin preferences are all stored on this machine and survive refreshes and restarts. They do not travel with the conversation, and they are not overwritten by other Projects.
:::
