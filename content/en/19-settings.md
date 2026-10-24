---
title: Settings and security approvals
description: What each block of the Settings page is for, and the rules behind security approvals
section: Mobile & Security
order: 19
---

This page explains what each block of the Settings page looks after, and how SLATE asks for your consent before it acts. Settings opens from "Settings" in the top bar; the left navigation is generated live from the blocks on the page, one entry per block title, and there's a search field at the top: type a keyword and only blocks containing it remain, with the matching line outlined; press Enter or click to jump there, clear it and everything comes back exactly as it was.

## Settings blocks at a glance

| Block | What it looks after |
|---|---|
| Model configuration | Add custom models and keys for built-in models, set the Base URL, one "max context" row per model (slider + exact number box + probe window), optional Responses API mode |
| API test | Send the shortest possible request to check whether a model's key and endpoint work |
| Usage | Cumulative Token usage across all Chats, updated as you Chat |
| Context and Projects | Context Token cap, single-output cap, whether file writes are auto-confirmed, project constitution |
| Auto-advance | The retry policy when a reply seems to stall, plus Continue Autopilot |
| AI assistance | Per-item switches and per-item model choice for Token-consuming features outside Chat |
| Notifications | Sound and system notification when a big task ends |
| Background tasks | Wake-up switches once long commands move to their own channel: waking the model when a task has news, and how many times each Chat may auto-continue |
| Multi-tasking and Projects | Whether a session keeps running in the background when you switch away, and how many run at once |
| General UI | The minimal Codex-style layout switch (experimental) |
| Custom theme | Colours (a whole set derived from four source colours), fonts (system font families + importing your own font files), panel opacity, background image and overlay density, with the current wallpaper fetchable from Wallpaper Engine; 10 base presets, and the light/dark toggle locked while it's on |
| Web search | Default search engine, page JS rendering policy |
| Image generation | Model and API Key for generation Tools |
| Video generation | Model and API Key for generation Tools |
| Approval mode | The default Approval level for each Chat |
| Data backup and restore | Backup export and import |
| Archived chats | Sessions archived out of the "Tasks" column, restored or deleted one by one here |
| Storage | Storage footprint and management |
| LAN remote control | Remote address and QR code |
| Typing game | Test your typing speed on the side, with a customisable prompt bank |
| About SLATE | Version, check for updates, onboarding, website and GitHub |

:::note Skills and MCP aren't on this page
"What the model can use" — Skills, built-in Tools, reply modes, new features (Tools the tool factory produces itself), MCP, Expert Packs, Actions — is all managed on the "Extensions" page in the top bar; Settings no longer doubles as a list of capabilities. See [Built-in tools and Skills](./08-tools-skills.md).
:::

## AI assistance

Apart from Chat, team Chat and Prompt Factory, every feature that goes off to a model for a result on its own is registered here, 15 in total. Each one can be switched off on its own and can name its own model; with no model named, it follows the current main model.

| Feature | How it triggers | When off |
|---|---|---|
| Context compression Summary | Automatic | No more automatic compression, and a manual "Compress" sends no request either |
| Automatic memory distillation | Automatic | No more long-term memory distilled automatically |
| Manual memory extraction | Manual | "Extract from current chat" in the memory panel sends no request |
| Conversation insight capture | Automatic | No more insight cards generated automatically |
| Automatic chat titles | Automatic (after the first round) | New Chats keep the placeholder title "first 30 characters of the first message" and are never named |
| Code understanding docs | Manual | Scanning a Project no longer produces a guide and rulebook |
| Code review | Manual | Only the diff is taken; no four-dimension review |
| Whiteboard AI tidy-up | Manual | Whiteboard content is no longer handed to the model to reorder |
| Prompt polish | Manual | The button by the input still clicks, but sends no request and only says "turned off" |
| Parallel sub-agents | Model call | The Tool disappears from the tool catalogue, so the model can't see it and won't call it |
| Risky command purpose note | Automatic | The Approval dialog still stops it, just without the line on the command's purpose |
| Team Workflow execution | Manual | The Workflow no longer asks the model at each node |
| Scheduled and event tasks | Automatic | Tasks stop running; trigger records are kept |
| AI image generation | Model call | The Tool disappears from the tool catalogue |
| AI video generation | Model call | The Tool disappears from the tool catalogue |

Above the list a running tally reads "15 in total, N turned off". Off means not a single model request goes out — the most direct and most controllable way to throttle.

:::tip The first way to save Tokens
Turning off item by item what you never use saves more than compressing Context afterwards. If you only Chat and execute Tools day to day, compression, distillation, insight, image and video can all be off until you need them.
:::

## Continue Autopilot

Under "Auto-advance", on by default. What it does: Autopilot or Target Mode running out of rounds doesn't mean the work is done. If the last round was still executing Tools, the limit is pushed back 8 rounds (3 pushes at most) so the work in hand gets finished; if the last round stopped empty-handed, the items left on the list are read back to the model, pressing it to carry on or to state plainly that the task is done.

After the curtain there's one more layer: when a run exits not because it "completed" but because it ran out of rounds, and it isn't on a manual Approval level (Auto Approval / Full access / Night mode), SLATE presses that "continue to the end" for you — sent once the run has gone completely quiet (compression, distillation and the other wrap-up steps still take a few seconds), at most twice per run, and a toast says "rounds exhausted · auto-continued (1/2)". Manual Approval levels are excluded: that level means every step needs a human nod, so it still just hangs the "continue to the end" bar there for you. When the quota runs out, or a continuation doesn't connect, the manual button is still right where it was.

Turn it off and you're back to the old behaviour: stop when rounds run out, and say so yourself to continue. This switch stays on the local machine and doesn't sync over LAN remote control. For the mechanism, see [Agent Autopilot and Target Mode](./06-autopilot.md).

## Task completion notifications

When a big task ends (Target Mode, a team discussion, a Workflow finishing) you can get a nudge, and the two switches are independent:

| Switch | Default | Notes |
|---|---|---|
| Play a sound when a task completes | On | A short chime, no permission needed |
| Send a system notification when a task completes | Off | Needs notification permission from the browser; until it's granted, the block says so below |

Turning both off doesn't affect the task itself, it just stops the nudge. Good for hanging a long task in the background while you do something else; with them on you're back at the screen the moment work is done.

## Theme and language

- **Light and dark**: toggle it with the "light/dark" button in the top bar, and mobile has the same button to the right of the top status bar. The choice syncs across devices: switch it on the phone and a refresh on the computer agrees.
- **Custom theme**: this block takes only four source colours — base, panel, body text, accent — and the other thirty-odd colour tokens are derived from them. Why not open them one by one: tuning tokens individually easily produces a mess whose body text can't be read, whereas with only four sources the derivation sorts a light and a dark set by luminance and falls back on contrast, so the palette is bound to hold together. Code blocks keep dark backgrounds and light text under any palette; the danger / done / needs-action status colours switch as a group with the base colour's luminance and don't follow your accent, or red and green would stop meaning what they mean. Model brand marks don't take part in this derivation either: those with a colour original are drawn in brand colours, those without get a fixed neutral grey, and the ink colour you pick can't tint them.
- **10 base presets**: Paper Ink, Night Gold, Mist Blue, Deep Sea, Pine Ink, Moss Green, Clay, Dusk Purple, Graphite, Movable Type. Clicking a preset fills all four source colours at once, and you can still change just one of them afterwards; change the palette and this set is no longer that preset, with the highlight cleared automatically.
- **Fonts**: one dropdown each for body text and code; the candidates list font families already on the system first (including "follow system"); the "Import font" button below the dropdown imports your own .woff2 / .woff / .ttf / .otf (a single file, up to 16MB), and once imported it appears in both dropdowns like a system font, with the list reporting each file's size and letting you remove them one by one. Font files exist only in the local `data/theme/fonts/`, never enter the chat record and aren't copied to another device; import a single weight and the browser fakes bold and italic. The font stack ends with a generic family fallback, so moving to a machine that has neither installed nor imported the font won't leave you with a blurry default serif.
- **Panel opacity**: one "panel opacity" slider (55%–100%, default 100%) controls the opacity of the base colour behind panels, cards, the input and assistant bubbles. 100% is solid, behaving exactly as the old version did, pixel for pixel; lowering it lets the page background show through, and a background image too. Your own bubbles and code blocks always stay solid, so body text never becomes hard to read because of it. It and the overlay density each look after one layer: the panel takes the lower of the two, so the two don't each apply once and wash the panels out.
- **Background image**: pick a local PNG / JPG / GIF / WebP (no more than 4MB); only that one file lives in the local data directory, isn't uploaded over LAN remote control and doesn't enter the Backup. Once it's laid down the interface turns semi-transparent and rides on top of it, and the "overlay density" slider adjusts the base colour's opacity (40%–95%, default 72%): below 40% the body text sits straight on the image, above 95% it's as if there were no image at all. Setting and removing the image both go through the "Remove" button in the top bar; once removed the base colour is solid again.
- **Wallpaper Engine**: on a machine with Wallpaper Engine installed there's an extra "Fetch current wallpaper" button here — it takes the preview of the wallpaper it's using as the background image above, and "Detect again" beside it re-identifies it after it was closed or its directory changed. This step is read-only: SLATE only reads the config and preview image Wallpaper Engine writes in its own directory; it doesn't start it or change any of its settings. Change the wallpaper there and this won't follow — click again; video and scene wallpapers give you that static preview, and only a dynamic preview gives you the gif (which keeps moving behind the interface). The status line reports only the wallpaper name, file size and source screen number, never the absolute path on this machine.
- **Can't switch light/dark while a custom theme is on**: the whole token set is derived from those four source colours, and switching the light/dark base again would only set two palettes against each other. So the light/dark button dims and says "locked"; clicking it won't change colours but pops a hint telling you where to turn the custom theme off — mobile too. Turn the custom theme off and every trace (injected styles, colours, fonts, background image) is cleared on the spot, and light/dark switching comes back at once.
- **Interface language**: chosen at install — Simplified Chinese or English — and there's no in-app switch while the app runs. The English interface translates the interface copy itself — buttons, block titles, the grey placeholder text in inputs and hover hints all count; model-generated content, the text you type, and code you paste into Chat are always shown as they are and never translated. The brand wordmark "砚" stays as it is too.
- To change language, run the installer again and pick the other one; to change it on just one device, that too is decided at install time.

:::note Background images and imported fonts are local only
The background image and the font files under `data/theme/fonts/` live only in this machine's data directory; they aren't written into the Backup and don't sync. After moving to another device or reinstalling, the same switch says "no background image on this machine" and "no imported fonts on this machine" — just pick them again. Colours, opacity and font choices are unaffected and keep working.
:::

## The About block

"About" gathers the version and update actions in one place:

- **Current version**: which build you're running now.
- **Check for Updates**: also checked once at startup. When a new version turns up it shows the current and latest versions, a summary of the release notes, and "Download Update" and "Release notes" buttons, both opening in your system browser.
- **Onboarding**: forgotten how the three-column workspace works? Watch it again here.
- **Project links**: the website and the GitHub repository, again opening in your system browser.

## Security and Approval

SLATE follows the "no self-directed changes" rule: say the word and it really changes things; say nothing and it never touches them on its own. To make that rule hold, a few gates stand in front of every action.

**Approval mode** ("Settings → Approval mode" sets the default; a single Chat can be changed at any time from the Approval mode selector by the input, and a Chat you've changed stops following the default):

| Mode | Meaning |
|---|---|
| Manual Approval | Running commands and reaching the network both ask you first |
| Auto Approval | Only hits on risky rules ask; everything else goes straight through |
| Full access | Commands and network access stop asking; but the model still pops a multiple-choice question at you when it lacks a condition. Catastrophic commands are still blocked dead by the backend, and this level is marked red in the selector |
| Night mode | Fully hands-off: commands and network access don't ask, and even the model's "I'd like to ask you something" doesn't ask — it picks a plan itself and carries on. Good for leaving it to run and checking later |

Night mode's promise to you is "nothing is waiting for a human": the Approval dialog won't wait for your approval, and the multiple-choice question won't wait for you to come back and choose. That's why catastrophic commands stay blocked dead by the backend in every mode — that gate isn't "ask", it's "not allowed".

**Risky commands** are judged by hard-coded rules, blocked at two layers, frontend and backend: the frontend blocks once, the backend blocks again independently, so even getting past the interface is still caught. On a hit the dialog states the command verbatim and the rule it triggered, plus a one-line note on the command's purpose generated by the model, and you decide to approve or reject; when rejected, the model gets a clear reason and is told not to retry. Catastrophic commands (wiping the root directory, formatting a disk) are forbidden unconditionally in every mode.

**File edits** go through a diff preview: changes appear as a diff card, and only an accept writes to disk; a reject writes nothing. Settings has an "auto-confirm file creation/modification" switch, on by default — that is, ordinary writes don't need your accept every time; to look over every single one yourself, turn it off and per-write confirmation comes back.

| Action | Needs Approval | Goes straight through |
|---|---|---|
| Running terminal commands | Confirmed by rule under Manual Approval and Auto Approval | Full access and Night mode |
| Starting background tasks | Same as above | Full access and Night mode |
| Web search, page fetching, browser automation | Confirmed one by one under Manual Approval | Auto Approval, Full access and Night mode |
| The model asking you a question when it lacks a condition (multiple-choice dialog) | Waits for your choice under Manual, Auto Approval and Full access | Night mode (the model decides for itself instead) |
| Read-only operations such as reading files, listing directories and searching code | No Approval | Any mode |
| Creating and editing files | Depends on the "auto-confirm file creation/modification" switch | When that switch is on |
| Catastrophic commands | Forbidden unconditionally in any mode | None |
| Accessing credential files (keys, certificates, environment variable files) | Forbidden in any mode | None |

**Transparent protection**: path traversal is blocked, and sensitive system directories can't be read or written; credential files can't be accessed; Tool output over the limit is truncated automatically, and single-file operations have a size limit too; uploaded file names are sanitised. All of this takes effect quietly in the background, with nothing for you to configure.

:::note The trade-offs behind Approval modes
Auto Approval suits watching the screen when you already know what the model does; Full access goes one step further and doesn't even pop the risky confirmation — it only leaves "the model asks when it lacks a condition", which suits letting it act widely while the direction is still yours; Night mode suits leaving the screen and checking the result afterwards — precisely because it won't turn around and ask, it matters more to write the goal and acceptance criteria clearly in the task description, since a wrong direction will simply keep going. If in doubt, use Manual Approval: a click or two more, and every change to your environment passes through your permission.
:::

For which Tools exist and how to write a playbook, see [Built-in tools and Skills](./08-tools-skills.md); for Backup and storage cleanup, see [Data, backups and storage](./17-data.md).
