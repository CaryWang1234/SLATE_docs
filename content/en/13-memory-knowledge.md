---
title: Memory, User Profile and Knowledge Base
description: Let SLATE remember your preferences, background and project knowledge
section: Collaboration & Reasoning
order: 13
---

## Why memory exists

Having to explain "I use Python and TypeScript", "this repo doesn't want drive-by refactors" and "don't write long preambles" again every time you open a new Chat is pure overhead. Memory & Knowledge turns this kind of information from "repeated every time" into "distilled once, reused long-term": SLATE accumulates the points itself during Chat, and already knows the background before the next conversation starts.

This page covers four things: where long-term memory comes from and how to change it, what the User Profile is, what Spark captures, and how the knowledge base is divided by ownership.

## Where the memory panel is

The "Memory & Profile" button in the top bar opens the same panel, which has four tabs:

| Tab | What it manages |
|---|---|
| Long-term memory | The points distilled one by one; add, edit and delete |
| User Profile | Structured information such as role, style and tech stack |
| Knowledge Center | Search, adding and ownership of knowledge documents |
| Vault | Markdown notes, with `[[wikilinks]]`, tags and backlinks |

On mobile, manage long-term memory in the "Memory" tab at the bottom; see [Mobile remote control and LAN access](./18-mobile.md).

## Long-term memory: what is kept, and where it comes from

- **Distilled automatically during Chat**: after each reply, SLATE quietly reads the recent conversation and distils information worth keeping long-term into memory entries — your preferences, decisions you have made, project background, terminology conventions, explicit constraints.
- **Add manually**: click "+ Add memory", write an entry and pick a category.
- **Extract from Chat**: click "Extract from chat" to turn the current conversation into candidate memories.
- **Automatic deduplication**: identical or highly similar memories are not added again; the extraction result tells you how many were skipped.

Categories: preference / decision / project / terminology / fact / general / other; plus architecture / technology / convention / build / log / configuration for knowledge-type entries. Category only affects organisation and retrieval, not whether an entry is used.

Memory is stored on this machine and persists across sessions. Every conversation attaches the most recent batch of memories and the User Profile to the Context, so a new Chat does not need the background explained again.

:::tip What is worth distilling
- Long-standing preferences and habits: "give the conclusion first", "don't commit automatically"
- Decisions already made, and the reasoning at the time
- Background, terminology and directory conventions unique to the Project
- Explicit boundaries: "this repo takes no new dependencies"

One-off tasks, transient state, small talk, raw tool output and bare code snippets are not worth keeping — automatic distillation filters them out too.
:::

## Correcting and cleaning up memory

Information goes stale, and memory has to be editable too. Three routes:

1. **Automatic overwrite and deletion**: if in conversation you explicitly correct, overturn or discard an existing memory, distillation rewrites that entry with the new content (overwrite, the entry itself stays), or clears it outright (delete). Each distillation reports honestly how many were "added / overwritten / deleted / skipped as duplicates".
2. **Distil manually once**: click "Auto-distil profile" to run it immediately, without waiting for the next conversation.
3. **Edit entry by entry**: double-click a memory's content to change the text, click the pencil button to change the category, click × to delete. Deleting also clears its mirror document in the knowledge base.

A corrected memory takes part in later conversations immediately; no new session needed.

## User Profile

The profile is the more structured part of memory: it does not record a particular sentence, but describes who you are and how you prefer to work together.

| Field | What to fill in |
|---|---|
| Role / occupation | Full-stack developer, product manager… |
| Working style | Detail-oriented, rapid prototyping, iterative… |
| Tech stack preferences | Python, React, TypeScript… |
| Communication habits | Concise and direct, lots of examples… |
| Other | Anything you want SLATE to know in advance |

The profile is distilled automatically from conversations and memory, so usually you only add or correct a field or two; you can also fill it in by hand and click "Save profile" — "Reset profile" clears every field. It is attached to every conversation alongside long-term memory, with an explicit instruction that the model must not repeat this content back to you.

## How memory enters the conversation

Memory and the profile need no manual "mounting": each time you send a message, SLATE picks the most recent batch of long-term memories and the User Profile, attaches them to this conversation's Context, and asks the model to use them to adjust style and content rather than restate them as a topic. The knowledge base works another way — only when automatic retrieval is on and a passage is genuinely relevant to the current question are matching snippets injected, see the next section.

Three practical implications:

- **More memory is not better**: attachment applies length truncation, and wordy entries eat into the Context budget. Keep what earns its place, clear out what has expired.
- **Memory is global**: it does not change as you switch Projects — it is there in whichever Project you enter (the knowledge base, by contrast, is divided by ownership).
- **The profile beats correcting**: filling in "tech stack preference: TypeScript" once saves you correcting the model in every conversation.

## Spark: insights from Chat worth keeping

Spark is an automatic harvest at the end of a conversation. When you switch sessions, SLATE judges whether the previous one contains technical insight genuinely worth reusing across conversations —

- Important technical decisions: which approach was chosen, why, what was traded off
- Non-obvious solutions to problems
- Reusable code or architecture patterns
- Discoveries about key configuration and environment setup
- Engineering lessons worth writing down

Matching content is filed as a knowledge document titled like "Spark · something" and takes part in later retrieval injection; ordinary Q&A, small talk, tool output and ad-hoc debugging are not collected. When something is captured, it tells you how many entries were collected. This pipeline can be turned off under Settings → AI-assisted features → Conversation insight capture.

## Knowledge base

The knowledge base is the "retrieve on demand" layer: it does not sit in the Context permanently, and injects snippets only when relevant.

- **Add**: click "+ Add knowledge", fill in a title and content; Markdown is supported.
- **Retrieval**: tick "Search knowledge base automatically during chat"; "Snippets" next to it sets how many can be injected at most each time (1–12, default 5); you can also search by keyword in the search box right away.
- **Sources**: hand-added notes, mirrors of long-term memory, insights captured by Spark and output from team Workflows all flow in over time.
- **Divided by ownership**: adding knowledge with a Project open first asks whether to "save into this Project" or "save as global". For the same title (case and leading/trailing whitespace ignored) the Project entry overrides the global one, while the rest of the global set stays visible; documents from other Projects do not enter the current view. Full rules in [Projects, workspaces and per-project configuration](./14-projects.md).
- **Delete**: from a Project's view you cannot delete the global copy (that would take away a document other Projects share). Collapse the Project first and delete from the global-only view.

## Vault

The panel's fourth tab is the Vault: a Markdown note library. Folders and notes are arranged as a tree, source on the left and live preview on the right. Notes can carry tags (comma-separated), and you can use `[[note name]]` to create a wikilink; with a note selected, the bottom lists its **backlinks** — which notes mention it. The search box finds by title, the tag bar filters by tag. Good for long material you want to keep but that does not belong in knowledge snippets.

## How the three kinds of information divide the work

| | Long-term memory | User Profile | Knowledge documents |
|---|---|---|---|
| Source | Distilled automatically during Chat, or added manually | Distilled from memory and interaction history, or filled in by hand | Added manually, memory mirrors, Spark, Workflow output |
| Stored where | On this machine in SLATE, persisted across sessions | SLATE's local Settings | SLATE's local knowledge base, divided into global / Project ownership |
| When it is used | The most recent batch attached to every conversation | Attached to every conversation | Snippets injected by relevance once automatic retrieval is on |
| How to change it | Add, edit and delete in the panel | Edit the five fields in the panel, or reset | Search, add, delete |

## Token cost and switches

Memory distillation, conversation insight and Context compression all call a model themselves, so they are all registered under "Settings → AI-assisted features": each can be turned off, or pointed at a cheaper model of its own. The three memory-related slots are automatic memory distillation, manual memory extraction and conversation insight capture. Turned off means not a single model call is sent. See [Settings and security approval](./19-settings.md).

:::note After turning it off
Turning off automatic distillation does not affect memory already accumulated, nor manual adding and editing; it only stops new entries being added, overwritten or deleted automatically. Knowledge and Spark entries already in the library still take part in retrieval as usual.
:::
