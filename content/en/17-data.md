---
title: Data, backups and storage
description: Your data all stays on this machine — how to back it up, restore it and free up storage
section: Projects & Data
order: 17
---

This page answers three questions: where your data lives, how to back it up and restore it, and which item to touch when storage grows. SLATE is a local-first Tool: Chats, memory and Settings all stay on your own machine, and the API Key is only used when a model is called.

## Your data is all on your own machine

Data sits in two layers: one in the database, one in the files and folders of the data directory. You only need to remember one unit — "the local data directory" — and handle the whole directory together when deleting or copying.

| What is stored | Which layer | Notes |
|---|---|---|
| Sessions and messages | Local data directory · database | Title, message body, model used, Token usage |
| Long-term memory and User Profile | Local data directory · database | Memory entries distilled automatically, recalled across sessions |
| Prompt material | Local data directory · database | Snippets saved from Prompt Factory |
| Knowledge base documents | Local data directory · database | Knowledge snippets and Spark archives |
| Playbooks / Expert Packs / custom Skills | Local data directory · files and folders | A playbook is a single file; an Expert Pack and a Skill each get a directory |
| Preferences | Local data directory · configuration file | Theme, models and keys, Approval mode, the various switches |
| Backup files | Local data directory · backup folder | Every "Download Backup" also leaves a copy on this machine |

:::tip Want to move the whole thing
The local data directory is your entire estate. Either export a JSON with "Download Backup", or copy the whole data directory onto the new machine.
:::

## Managing chat history

In the "Tasks" list in the sidebar, every session carries its own information and actions:

- **Search box**: typing filters titles; 2 characters or more also runs a full-text search of the content, and hits are listed as "content matches · N" with the session title and an excerpt of the surrounding text — click one to jump straight to that session.
- **Hover buttons**: move the mouse over a session and three buttons appear on the right — rename, export Markdown (labelled `MD`), delete (`×`). Export produces a Markdown file with every question and answer, its filename carrying the session title and the date.
- **Archive**: the row actions include "Archive"; press it and this session leaves the "Tasks" column without a single message touched. The one that is generating can't be archived (stop it first). Archived sessions are restored or deleted one by one under "Settings → Archived chats" — restore puts it back in the Tasks column; delete wipes it along with its messages, with no way back.
- **Sort dropdown**: in the sidebar header; switch between recently updated / by Project / by status / creation time / by usage.
- **Manage**: the "Manage" button in the sidebar header opens the "Manage chat history" dialog, where you tick rows and then "Delete selected", or go straight to "Clear all"; the "All" checkbox at the top selects every current session in one go.

Deleting a session, deleting a message and clearing everything can't be undone. Export a copy under "Data backup" first.

## Message-level actions

In the message area, every message has a row of small buttons at its top right:

| Button | What it does | Applies to |
|---|---|---|
| Copy | Copies the body of this message | All messages |
| Edit content | Turns it into an input box in place; saving writes it back and re-renders | User messages |
| Delete this message | Removes this one message from the session | User messages |
| Regenerate | Asks for an answer again from the history before this message | The last assistant message |

Editing or deleting a message only affects that one message and doesn't touch other sessions. For how Chat itself works, see [Chat and messages](./05-chat.md).

## One-click Backup and restore

One export collects Chats, memory, material and Settings into a single JSON file.

**What the Backup contains**

- Every session and message, long-term memory, prompt material, and usage records.
- Local preferences: models and API Keys, custom models, theme, Approval mode, AI assistance switches and so on.
- So a Backup file contains your API Keys — don't pass it around.

**When to back up**

- Before uninstalling, reinstalling or moving to another computer.
- Before an irreversible action such as "Clear chats".
- Before a big tidy-up or a round of session deletions.

**What importing does**

- Sessions, messages, memory and material merge by ID: data that already exists is skipped, never overwriting what you have.
- Local preferences are replaced by the copy inside the Backup, and when the import finishes the page reloads itself to apply them.
- You get one confirmation before the import starts, and it begins only after you confirm.

:::warning Check before you import
Import merges into the current data; it doesn't clear and restore. Your preferences on this machine are overwritten by the copy in the Backup; if both sides hold model keys you want to keep, the result after import may not be what you expect. If in doubt, export the current Backup first, then import the old one.
:::

## Managing storage

Below "Settings → Data backup" is "Storage", which first shows the total footprint, then lists the size of each item.

| Item | What is in it | What you can do | When to use it |
|---|---|---|---|
| Chat history database | Sessions and messages, long-term memory, prompt material, usage | Compress, clear chats | After deleting a lot of sessions and wanting the space back; or when history is too messy and you want a clean start |
| Built-in browser cache | Cache files produced by the built-in browser | Clear cache | Pages render oddly, or this item has grown noticeably |
| Custom Skills | Skill documents you imported or created | Can't be cleared | Best kept |
| Configuration file | Theme, models and keys, the various switches | Can't be cleared | Best kept |
| Other | Knowledge base, logs, playbooks, Expert Packs and so on | Can't be cleared | Best kept |

The three actions differ:

- **Compress**: actually gives back to disk the space taken up by deleted data in the database, without touching any existing content. Best right after "I just deleted a lot of sessions".
- **Clear chats**: deletes every session and message; long-term memory, the knowledge base and preferences are unaffected. Irreversible, with one confirmation before it runs.
- **Clear cache**: removes the built-in browser's cache files. Files held by a running process are released for good on the next start.

## Cross-device sync and local preferences

If you drive the same SLATE from your phone, some preferences follow you and others deliberately stay on this machine.

| Preference | Cross-device? |
|---|---|
| Sort order of the sidebar Tasks list | Synced |
| Theme and light/dark, general UI mode | Synced |
| Models and API Keys, custom models, current model | Synced |
| Approval mode, reasoning effort, AI assistance switches | Synced |
| Notification switches, web search, image and video generation config | Synced |
| Read progress and unread markers (needs action / error / in progress / finished but unread) | Local only |
| Collapsed state of the Task list column | Local only |
| Switches for Continue Autopilot and parallel multi-tasking | Local only |

Read progress stays local because "have I looked at this one" is a feeling of this device: having read it on another device shouldn't turn it read here.

## Uninstall or change computers: three steps

1. On the old machine open "Settings → Data backup" and click "Download Backup"; check you have `SLATE-backup-<date>.json`.
2. Install SLATE on the new machine, start it, and go to "Settings → Data backup".
3. Click "Import Backup", choose that JSON, confirm, and wait for the page to reload itself.

If knowledge base documents, playbooks, Expert Packs or custom Skills don't come across after the move, copy the whole local data directory from the old machine to the matching place on the new one — they aren't in that JSON; they're stored as files and folders. If models and API Keys didn't come in with the Backup, just fill them in again under model configuration on the new machine.

:::note Don't use a Backup as a sync drive
A Backup is a snapshot of one moment. Importing the same old Backup over and over doesn't merge into "the latest state"; it only mixes old and new records. For continuous sync, reach the same machine over LAN remote control instead — see [Mobile remote control and LAN access](./18-mobile.md).
:::
