---
title: Agent Autopilot and Target Mode
description: The execution layer where the AI reads files, edits code and runs commands, plus an 80-round hard closed loop.
section: Chat & Automation
order: 6
---

Whenever your message asks the AI to look at the project, modify files, run commands, troubleshoot a problem or commit code, it enters the Agent loop automatically and comes back when the work is done — no repeated "continue" needed. Target Mode is a stricter form of the same loop: six explicit stages and an 80-round hard closed loop.

## What Agent Autopilot is

Autopilot is SLATE's default execution layer; you don't turn it on manually.

- It recognises environment-operation requests such as viewing, fixing, running, committing or project files, and enters a multi-round loop on its own.
- Ordinary tasks default to at most 24 rounds; full audits, project-level and multi-file tasks default to at most 40 rounds.
- The round count is a **stop-loss line, not a budget**: once the work is delivered and verified item by item the loop should end, rather than "using up all 24 rounds".
- Every tool call in the chat becomes a card, so you can see which file it read and what command it ran.

## The three run strengths compared

| Run strength | When to use it | Round cap | Creates a task list automatically | How it exits |
|---|---|---|---|---|
| Normal chat | Q&A, writing, explaining code — no need for the AI to touch your files | Does not enter the tool loop | No | Ends when the reply ends |
| Agent Autopilot | Fixing one bug, running a test suite once and fixing the failures, generating a batch of files | 24 rounds normally; 40 for full audits / project-level work | Recommended for complex tasks, not enforced | The model closes out explicitly; if it doesn't, marked as interrupted |
| Target Mode | Multi-file rewrites, complete audits, long-chain tasks | 80 rounds | Yes, and it may not claim completion until everything is resolved | Manual stop / rounds used up / list fully resolved / model closes out |

Target Mode is toggled in the + menu on the left of the input box; send a message after turning it on and it takes effect.

## What happens inside the loop

Each round moves roughly to this rhythm:

1. **Observe**: read the relevant directories, files, configuration or Git state — no guessing from memory.
2. **Execute**: call tools to move forward; reads and scans that can be combined into one batch are done in the same round.
3. **Verify**: after a change, re-read, run a command or run tests; keep fixing while it fails.
4. **Report**: check results, verification method and remaining risks item by item.

Tool results are fed back to the model as hidden context so it can carry on, instead of spreading a pile of raw output across your screen.

If the tool calls issued in one round are exactly the same as the previous round, the system blocks that duplicate execution and reminds it to change approach — running the same action again only wastes rounds.

## Stop when it's done

Autopilot does not accept "stopping halfway":

- The model must close out explicitly (you'll see a close-out call) before the work really counts as finished.
- If it exits without going through the completion channel (rounds used up, idling, you pressed Stop), the status is honestly marked "Interrupted · task not confirmed complete", and the message area offers a "Keep going" entry point.
- "Keep going" doesn't start over; it resumes from the breakpoint.

## Automatic nudging

When the model talks halfway and doesn't act, the system nudges it on its own:

- It only states a forward-looking plan — "I will check / next I'll modify / shall I continue" — and issues no tool call: nudge it to call tools directly.
- It runs no tool yet says "done" verbally: require it to verify first, or to actually do the work.
- For several rounds in a row it only describes plans without acting: give a firmer warning and, if necessary, cut losses early to avoid burning quota for nothing.

These nudges are only added to the context sent to the model and never take up your message area; even if context compaction happens in between, they don't turn into a bubble that pops up.

## Continue Autopilot

Running out of rounds doesn't mean being done. **Continue Autopilot is on by default**; you can turn it off in "Settings → Auto-advance".

- The model is still working in the final round: push the cap out by 8 rounds so it can finish what's in hand. At most 3 extensions; it never runs on indefinitely.
- The model stops empty-handed in the final round: read the remaining items of the task list back to it and urge it to keep going, or to reply explicitly with 【Task complete】.

If after 3 pushes it still hits the cap and the session hasn't closed out on its own, you don't have to click manually once it ends: as long as the session isn't on a manual approval tier (auto approval / full access / night mode), SLATE presses "Keep going" for you. It waits until the session really goes quiet — compaction and memory distillation still occupy it for a few seconds — then sends that "continue", at most 2 automatic continuations per session, with an echo reading "Rounds exhausted · auto-continued (1/2)". Manual approval tiers are not pressed automatically: the meaning of that tier is that every step needs a human nod, so it only leaves the "Keep going" bar in the message area waiting for you. When quota runs out or the automatic continuation doesn't connect, that manual button is still right there, resuming from the breakpoint instead of starting over.

:::warning Extensions are capped
Extensions only relax the cap; they don't remove the stop-loss line. If the task itself needs a longer closed loop, turn on Target Mode directly instead of relying on repeated extensions.
:::

## Ink Flow: what you write is what you see

As the model writes tool arguments token by token, Ink Flow infers in real time from the tool's parameter schema which fields are already written and which one is being written, turning the shaping of the arguments into a visible one-line preview.

- It **only previews**: half-formed arguments never trigger execution.
- Body-type fields (file contents, Markdown, HTML and so on) are always folded into line and character counts, never flooding the screen.
- Tools with very short arguments get no writing animation, to avoid pointless flicker.

## Stop really cancels

Clicking "Stop" does more than quiet the interface:

- It closes both the model stream and the streaming channel of tool calls at the same time.
- The backend then terminates the corresponding child processes and running tasks.
- Cancelled calls are accounted for under a separate status, counted apart from "completed", so later you can trace whether this one was stopped or finished.

## Which files this round changed, laid out when it's done

When this round really wrote files to disk (edit / create / append), a card is attached to the end of the message after the model's last sentence. It reports facts only and doesn't sing the model's praises.

- The header says how many files this round changed and the line delta for each; click "Review" to expand the diff file by file (three listed by default, the rest shown on click).
- Click "Undo" to restore the files this round wrote to how they were **before** the round started; files created this round are deleted along with them; a red confirmation comes first.
- Files you changed yourself after this round are skipped with the reason stated — undo only restores what it wrote itself and doesn't eat your own changes.
- No card is left when nothing was written to disk this round; the same goes for auto-apply being off: that write is still recorded in the list of the round that proposed it, but it only really lands on disk after you click "Accept".
- Original snapshots are stored in `data/round_snapshots/` and kept for only 7 days; large files over 2MB aren't stored and are skipped with an explanation on undo. Everything stays on your machine and is never uploaded.
- On mobile the list is shown only; undo stays on desktop.

## Target Mode

Target Mode is the explicit hard closed-loop mode: you give the goal, and the model advances through six stages on its own.

### Six-stage closed loop

Goal → Plan → Execute → Verify → Report → Trace.

- Every tool result in a round is tagged with the current round (round x/N), so the model can pace what's left.
- Stop only interrupts the current round; the Target Mode toggle stays on and standing by, ready to keep running at any time.

### Task list

- Multi-file, multi-step, audit or implementation tasks get a task list automatically; simple single-step tasks can skip it.
- The list shows live in the right sidebar of the message area; the "Task list" button in the top bar collapses it at any time, giving the width back to the message area.
- Once collapsed the button still reports `{done}/{total}` progress; when the session has no list the button is greyed out.
- Until everything is resolved the model may not claim completion; status is written back as soon as each batch is finished.

### Four ways to exit

Target Mode has only these four exit paths:

1. You press Stop manually.
2. 80 rounds are used up.
3. The list is fully resolved.
4. The model closes out explicitly and ends the loop.

Model-side failures, zero output and duplicate calls all recover and keep going automatically — one exception doesn't cut the whole session short.

:::tip When to turn on Target Mode
Turn it on when the task needs a full closed loop of "change it, then verify it, then go back and patch it": multi-file refactors, whole-project audits, long tasks that need fixing while running. If you're changing one file or asking one question, leave it off — Target Mode spends extra rounds on building and closing out the list.
:::

## Four lines of defence against truncated output

When writing very long files the model may be cut off by the output limit; SLATE uses four layers to make sure the file ends up complete:

1. **Breakpoint anchor continuation**: take the model's own last output as the anchor and let it continue precisely from the breakpoint (at most 6 rounds).
2. **Truncation guard**: a tool call that isn't closed is refused, and the model is required to split it and retry rather than write half a file.
3. **Segmented completion**: create and write the first part, then use the append action to fill in the rest; the card marks that this segment is truncated and waiting to be completed.
4. **Prompt prevention**: the prompt asks it in advance to write large files in batches.

## A whole round of thinking, no body text

There is another kind of truncation unrelated to files: the thinking process and the body share the same output limit, so when thinking fills it up there's no room left to write the body this round. SLATE reports this kind of ending honestly instead of letting it slip past:

- When the stream ends naturally after receiving content but has neither a finish marker nor a finish reason, the round is flagged.
- At wrap-up it says separately whether "thinking filled the output limit" or "the upstream cut off early", and offers a clickable "Continue" entry point to resume from the current context.
- If the body has content but the stream broke early, it is marked as possibly incomplete.
- This notice and the "Continue" entry point are given in every mode, not only in auto-advance mode — otherwise, with auto-advance turned off, "it stopped by itself" would be the only explanation left.

## Cross-project parallelism

Switching projects no longer interrupts a reply that's being generated: the session you left keeps running in the background, and its progress and outcome land in the task centre in the right column.

- Within one project it's serial by default (two sessions editing the same files at once makes it hard to trace who broke what).
- Across projects, at most two sessions run at once; adjust it to 1–4 in "Settings → Multitasking & Projects".
- Sends over the limit aren't swallowed: they go into the queue marked "Queued" and pick up automatically as soon as the previous one finishes.
- Each session counts its own tokens; the usage bar only reflects the session on screen.

For how projects and workspaces are organised, see [Projects, workspaces and per-project configuration](./14-projects.md).
