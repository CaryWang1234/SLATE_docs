---
title: Chat & messages
description: The everyday moves — starting a Chat, sending messages, attaching files, @ mentions and Context usage.
section: Start
order: 5
---

This page covers what you use most in the Chat box: how to start a Chat, how to get a message sent, how to get files and Skills into that one message, and where the Tokens went.

## Starting a Chat

- Click "＋ New Chat" at the top of the "Tasks" tab in the sidebar, or press `Ctrl + N`.
- Click any session in the sidebar to switch to it; the full history of the current session is laid out again.
- The sort dropdown can switch between: Recently updated / By project / By status / Creation time / By usage. The sort preference syncs across devices.
- Each session carries a status marker: **Needs action** (the previous session still has a next step, or was stopped), **Error**, **In progress** (breathing animation), **Done, unread**. Clicking into a session counts as having read it.

`Enter` sends, `Shift + Enter` inserts a new line.

The markers record "how the previous session ended": if you later continued it on mobile or in another session, the old marker is voided automatically.

## Basic message operations

- **Streaming output**: the reply lands character by character, so you can start reading without waiting for the whole thing.
- **Stop**: during generation the send button becomes "Stop". Clicking it is a real cancel — the model stream and the streaming channel of tool calls are closed together, and the backend also terminates the running subprocesses and tasks, so you never get "the interface stopped but the work is still going".
- **Regenerate**: every assistant reply has "Regenerate" below it. It re-requests using the history before this reply, and rewrites everything after this reply.
- **One-click copy for code blocks**: code blocks have a "Copy" button at the top right.
- **Smart scroll following**: while the scrollbar is at the bottom the output follows along automatically; when you scroll up to read history you aren't dragged back down.

## Editing and deleting messages

Hovering over a message floats action buttons:

- "Copy" puts this message's content on the clipboard.
- "Regenerate" only appears on assistant messages.
- "Edit content" turns the body into an input box in place, and saving writes back to this message.
- "Delete this message" asks once first, and deletion cannot be undone.

## Comparing the four ways to input

| Input method | How to use | Best for |
|---|---|---|
| Text | Just type, `Enter` sends | The vast majority of requests |
| Voice | Click the microphone button on the right of the input box and dictate | When you don't want to type, or want to think out loud as you go |
| Polish prompt | Click the star button to the left of the voice button and let the model rewrite the draft | When the request is written vaguely and you want clearer wording |
| Attachments | Click the paperclip button and choose files | Letting the AI read a file you already have |
| @ mention | Type `@` and pick a candidate, or enter the matching group from the ＋ menu | Naming exactly which Tool, Skill or file to use |

## Attachments and multimodal input

Click the paperclip button on the left of the input box to add attachments; a single file can be up to 10MB.

- Text types (`.md` / `.html` / `.css` / `.js` / `.py` / `.json` / `.yaml` / `.log` and so on): the body is read directly.
- Spreadsheet types (`.csv` / `.tsv`): parsed into structured data instead of one block of text.
- Images (`.png` / `.jpg` / `.jpeg` / `.gif` / `.webp` / `.bmp` / `.svg`): converted into multimodal input for the model to look at.
- Document types (`.docx` / `.xlsx` / `.pdf`): SLATE parses out the paragraphs, tables and body text itself before sending them into the Chat.

:::tip Attachments are parsed before they are sent
SLATE parses the file locally into body text or structured data, instead of stuffing the whole raw file into Context. This step happens locally and doesn't cost extra Tokens.
:::

## Voice input

Click the microphone button on the right of the input box once to start dictating, click again to stop.

- Based on browser speech recognition, transcribing live as you speak; the transcription lands straight in the input box and doesn't interrupt the draft you already have.
- The recognition language follows the interface language: a Chinese interface recognises Chinese, an English interface recognises English.
- Requires browser and system support; Chrome / Edge work. The first use needs microphone permission.

:::warning Can't see the microphone button
The button only shows when the current browser supports speech recognition. If it doesn't appear, this environment doesn't support it — type instead.
:::

## Polish prompt

The star button to the left of the microphone button hands the draft already written in the input box to the model to rewrite. It rewrites **the message you haven't sent yet** — it isn't having the model answer in your place.

The flow is: click once → the model rewrites → see the original and the rewrite side by side in a popup → you decide.

- Clicking **Use it** is what writes it back into the input box; then you press `Enter` to send as usual.
- Clicking **Keep original**, pressing `Esc`, or clicking outside the popup all count as keeping the original, and not one character in the input box changes.
- You can keep typing in the input box during the few seconds of waiting. If you (or voice dictation) change the draft, this rewrite result is discarded and won't overwrite what you just wrote.
- When the model wraps its result in a code block, what's taken is the body inside; the pair of backtick fences isn't written back.
- Which model is used is set separately here: [Settings → AI-assisted features → Prompt polish](./19-settings.md). Turn it off and clicking the button only says it's off, without sending a single request.

:::tip It doesn't change your meaning
The instruction written into the prompt to the model is "keep the original meaning, don't add goals or details you didn't mention", and it requires `@` mentions, code, paths and numbers to be kept as-is. Rewriting only makes the words clearer; it doesn't swap out the request.
:::

## @ mentions

Typing `@` in the input box pops up candidates; you can also click the ＋ menu on the left of the input box and open one category directly from the "Mention (@ prefix)" group:

- **Skill**: injects the process defined by `SKILL.md` into this one message.
- **Tool**: names which built-in Tool to use.
- **MCP**: uses tools provided by an external MCP Server.
- **File**: injects the body (or directory structure) of a project file into this message; available only after a project is open.

Process manuals and Expert Packs also appear among the candidates: `@` a process id injects the whole process, and `@` an Expert Pack name injects its persona, rules and knowledge files.

The full list of tools and Skills is in [Built-in tools & Skills](./08-tools-skills.md).

## Context and usage

There is a usage info bar at the top of the Chat area; hovering over it shows who took the Context:

| Bucket | What it holds |
|---|---|
| System prompt | Fixed content such as the role setting and the project constitution |
| Tool catalog | Which tools the model can see in this Chat |
| Skill injection | Skills and file content brought in by `@` mentions |
| Tool calls & results | What the model called and what the tools returned |
| Chat messages | What you and the model actually said |

- The denominator of the context bar is the context budget you set for that model, not the model's nominal window size, so it is more like a forecast of "how far until compression".
- When usage passes the threshold, SLATE automatically compresses earlier conversation into a history summary, keeping the most recent turns as they are.
- The nudges the system sends to the model and the tool results fed back (see [Agent Autopilot & Target Mode](./06-autopilot.md)) appear only on the model's side and don't take up the message area; after compression they stay in Context and keep working, and they never suddenly turn into a bubble.
- The summary is still sent to the model as full original text, and only folded into one collapsible bar in the message area: click the title to expand, so a long history doesn't push the recent turns off screen.
- You can also compress manually: click the compress button on the toolbar, choose Light or Heavy, and start.

| Level | What is kept |
|---|---|
| Light compression | Keeps key details and facts such as file names and numbers that may be referenced, about 50% compression |
| Heavy compression | Keeps only core conclusions, key decisions and explicit to-dos, about 80% compression |

:::tip When to compress manually
Automatic compression only happens when the threshold is exceeded. If the first half of this session is full of intermediate work — "reading files, trial and error, back-and-forth confirmation" — and what you're about to discuss is something else, compressing manually ahead of time pays off more than waiting for it to trigger: the light level keeps file names and numbers, while the heavy level keeps only conclusions and details are lost.
:::

## Automatic injection of memory and profile

Long-term memory and the User Profile are selected and injected into the Chat by SLATE in the background; you don't need to paste them by hand. To view them, add or remove them, or extract memory from the current conversation, see [Memory, profile & knowledge](./13-memory-knowledge.md).

## Historical sessions

Above the "Tasks" tab in the sidebar there is "Search historical sessions"; typing a keyword searches full text, a match shows a Context excerpt, and clicking one takes you straight to that session. A new session first takes the first 30 characters of its first message as a placeholder title, and after the first round the model fills in a short name — it only replaces placeholder titles like that; names you changed yourself are left alone (this can be turned off in "Settings → AI-assisted features"). The "Manage" button on the right enters bulk management, where you can rename, export as Markdown and delete in bulk. Each row's actions also include "Archive": it only takes this session off the taskbar, not a single message changes, and to get it back go to "Settings → Conversation archive". Backup and export details are in [Data, backup & storage](./17-data.md).

## Sessions produced by Scheduled Tasks

Scheduled and event tasks, when they finish, automatically land as a standalone session whose title carries a `[定时]` or `[事件]` prefix, so you can recognise them directly in the sidebar. To see how tasks are created, see [Task list & Scheduled Tasks](./16-schedule.md).

When you need the AI to actually change files and run commands, see [Agent Autopilot & Target Mode](./06-autopilot.md) and [Grind Mode](./07-grind.md).
