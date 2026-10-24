---
title: What SLATE is
description: What SLATE is, what it can do, and who it is for
section: Start
order: 1
---

SLATE (砚 — the inkstone) is an AI collaboration console that runs on your own computer. It grinds rough inspiration into a structured plan, then decides whether to do the work itself or produce a high-quality Prompt for an external Coding Agent.

This page gives you the overall picture: what problem it solves, what it can do, and who it suits.

## What SLATE is

SLATE is a local-first AI collaboration tool focused on prompt engineering, context management and organizing project inspiration. It brings mainstream large models, built-in tools, team debates, workflows and whiteboard-style logic chains into a single interface.

**It has two faces; pick one by scenario:**

1. **Do it yourself** — drive the built-in tools directly to get work done: read the project, write files, run commands, generate documents and diagrams.
2. **Produce a Prompt** — pack context, constraints and acceptance criteria into a deliverable Prompt and hand it to an external Coding Agent such as Claude Code, Codex or Cursor.

:::tip In one line
Inspiration is for diverging; SLATE is for condensing it into a plan you can actually execute.
:::

## From inspiration to delivery

An idea usually travels from vague to delivered like this:

1. **Grind** — hand a rough sentence to Grind Mode; the AI asks about goals, audience, deliverables and acceptance criteria, and finally condenses it into an ink draft.
2. **Reason it out** — drop the ink draft onto the Whiteboard and use cards plus connections to make dependencies and order explicit; you can also let the AI Team debate a round first.
3. **Execute** — open Target Mode and let the model push forward autonomously through six stages, verifying item by item, and only close out when everything is settled.
4. **Hand off** — if the work suits an external Coding Agent better, use Prompt Factory to pack context and constraints into one Prompt and hand it over.

Each step can be used on its own; you don't have to walk the whole way.

## What problems it solves

An AI tool that gives you nothing but a chat window means the following four things are all on you. SLATE takes them over.

| Common trouble | What SLATE does |
|---|---|
| Context management | Full-text search and export of conversation history, automatic compression past a threshold, long-term memory recalled across sessions, knowledge base injected on demand |
| Prompt engineering | Prompt Factory packs the constitution, context and constraints into one Prompt; Grind Mode questions a vague idea into a structured task brief |
| Project-level operations | With a project open you can read files, change code, run commands and check Git status, without copying and pasting back and forth |
| Token consumption | Smart compression, tiered calls, lightweight models for discussion and heavy models for decisions, every AI-assisted feature individually switchable off |

## Core capabilities at a glance

| Capability | What it is | Value in one line |
|---|---|---|
| Multi-model Chat | Mainstream models from home and abroad + any OpenAI-compatible endpoint + local models, unified in one Chat interface | Change models without changing tools |
| Agent Autopilot & Target Mode | Detects requests like inspecting a project, editing files, running commands or debugging and automatically enters a multi-turn Agent loop; Target Mode is the explicit six-stage, tighter closed-loop version | No repeatedly sending "continue" — it closes out on its own |
| Grind Mode | One rough sentence, three rounds of questions from the AI, ground into a task brief | When the idea is still fuzzy, grind it clear before you start |
| MCP tools & Skills | Thirty-plus built-in tools, and new capabilities can be added with `SKILL.md` | The model can actually operate your files and command line |
| Actions | Write "the necessary process for doing something" as a manual, and the model advances along it | Settle a repeated process once, then follow it every time |
| Expert Packs | Persona + rules + knowledge + skills packed into one package, importable and exportable | Configure a domain expert once, reuse it everywhere |
| AI Team & Workflow | Multi-role multi-round debate (propose / rebut / decide), plus DAG workflow pipelines | Debate the important decisions once, then act |
| Whiteboard | Cards plus connections to organise thinking; tool runs are automatically recorded as step cards | See the whole reasoning process on one screen |
| Memory & Knowledge | Automatically settles conversation points, recalls across sessions, and can capture technical insights when a conversation ends | No re-explaining the background every time |
| Prompt Factory | One click to integrate project context, task description and constraints into a deliverable Prompt | The Prompt you hand to an external Coding Agent comes from here |
| Mobile remote control | Open the LAN address in a phone or tablet browser to get the dedicated mobile interface | Check progress and give instructions away from your computer |

## How it relates to external Coding Agents

SLATE doesn't replace Claude Code, Codex or Cursor — it stands in front of them.

- Working directly in SLATE: suited to tasks that need reading a project, running commands and repeated verification, without ever leaving this interface.
- Preparing in SLATE: suited to big overhauls you'd hand to an external Agent. It first organises project context, constraints and acceptance criteria into a structurally clear Prompt that you copy out.

Both ways of working share the same memory, the same project constitution and the same set of Expert Packs.

## Design principles

- **Pure black, white and grey** — the interface itself uses no colour gradients or decorative shadows, leaving attention for the content; the only colour is each provider's brand mark, drawn in its official colours and not changed with the theme.
- **Native stack** — zero npm, zero build tools; the interface is the files.
- **Local-first** — all data lives on this machine and passes through no cloud relay.
- **Token thrift** — smart compression, tiered calls, silent handling; not a single request is wasted.
- **Never hangs** — idle watchdog, automatic retry on empty content, request timeouts, and a UI fallback: several layers of defence.

## Where your data is

Conversation history, long-term memory, knowledge documents, Expert Packs, action flows, Scheduled Tasks and all settings are saved as files on this machine. API Keys are stored locally (encrypted at rest) and are used only to call the models you configured.

Specifically:

- every conversation and every message;
- long-term memory entries and the User Profile;
- knowledge documents and document archives;
- your own Skills, Expert Packs and process manuals;
- scheduled / event tasks and their run records;
- preferences for models, Approval, themes, typography and so on.

Backup, restore and cleanup for all of this is handled in the data-related block of Settings, and you can also export everything to a single file to migrate machines.

:::note About going online
SLATE itself is a local app, but model inference happens at the model provider you choose. So Chat needs access to the model endpoint you configured; the built-in web search, web fetch and update checks each need network access too.
:::

## Who it is for

- People who have an idea but don't know how to turn it into an executable plan.
- People already using Claude Code / Codex / Cursor who want to produce a high-quality Prompt locally first.
- People who need an AI workbench that remembers project background long-term and doesn't forget things across sessions.
- People who care about data staying on their machine and don't want project content handed to a cloud collaboration platform.
- People used to local models (Ollama / LM Studio) who want local and online models in one interface.

## Who it is not for

- People looking for an IDE replacement: SLATE is the collaborator and the dispatcher; it doesn't provide a full IDE with editor, debugger and completion.
- People looking for a cloud multi-person collaboration platform: SLATE is a local app, with no account system and no shared cloud space.
- People who expect it to work out of the box without bringing their own API Key: model quota is yours to arrange.
- People who want to train large models with it: SLATE is a console, not a training framework.

## Glossary

| Term | Meaning |
|---|---|
| Agent Autopilot | The default auto-advance layer: on detecting an environment-operation request it enters a multi-turn Agent loop and closes out on its own when done |
| Target Mode | A strongly closed mode you turn on explicitly, advancing through six stages — "goal → plan → execute → verify → report → trace" — with a larger turn budget |
| Grind (磨墨) | The process of grinding a rough idea into a structured task brief: three rounds of questioning, up to ten turns |
| Actions | Process manuals that state "the necessary process for doing something"; the model reads them as needed and advances along them |
| Skill | A pluggable capability described by one `SKILL.md`, injected into context as soon as it is mentioned in Chat |
| MCP | The protocol layer through which the model calls external tools; both SLATE's built-in tools and external MCP Servers come in through it |
| Expert Pack | A distributable configuration packing persona, rules, knowledge and skills |
| Ink Flow (砚流) | When the model writes tool parameters token by token, the preview mechanism that renders the shaping of those parameters live in the interface |

## Next steps

Install it, then run it: [Install & launch](./02-install.md).
