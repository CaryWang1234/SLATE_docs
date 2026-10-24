---
title: Mobile remote control and LAN access
description: Drive the SLATE on your desktop from your phone on the same LAN
section: Mobile & Security
order: 18
---

This page is for "I've left the computer but the work isn't finished": connect a phone or tablet to the same LAN and you can drive the SLATE on your desktop from the browser — the interface switches itself to a dedicated mobile layout. SLATE has LAN access open the moment it starts, so there's nothing extra to configure.

## What you can do

- Watch a running Chat and the progress of its tool calls, and keep talking.
- Create, switch, rename and delete sessions.
- Add, edit and delete long-term memory, and view and manage to-dos (Scheduled Tasks).
- Switch models, enter an API Key, toggle dark mode.
- Risky commands and file changes raise a bottom sheet for you to confirm, under the same rules as the desktop.

## How to connect

1. Put the phone and the computer on the same LAN (the same Wi-Fi).
2. On the computer open "Settings → LAN remote control"; you'll see an access address and a QR code.
3. Scan the code, or copy the address into the phone's browser, and the dedicated mobile interface opens.

The port in the address is 8001 by default; when that port is taken SLATE walks up to the next free one, so go by the address shown in Settings. The "Remote" button in the top bar jumps straight to that Settings block too.

## Why the desktop interface doesn't change

The mobile interface is a separate entry point: only phones and tablets hitting the LAN address land on it. In your computer's browser you still get the full three-column desktop workbench — same features, same layout, same shortcuts, zero regression.

:::tip Want the desktop interface on a phone
Add `slate_mobile=0` after the address and open it, and you stay on the desktop interface. That's how to get the full layout on a tablet with a screen big enough for it.
:::

## The five bottom tabs

| Tab | Main purpose | What you can do |
|---|---|---|
| Chat | Keep working | Watch streaming output, folded thinking cards and tool cards; ask a follow-up or stop the current round |
| Chats | Find history | The session list; create, switch, rename, delete |
| Memory | Manage long-term memory | Add, edit, delete and look things up; pick a category when creating |
| Tasks | Manage Scheduled Tasks | See the next trigger, enable or disable, run now, delete, create |
| Settings | Adjust local preferences | Model switching, reasoning effort, keys, appearance, remote info |

**Chat**: the input is pinned to the bottom; Enter sends, `Shift + Enter` adds a line, typing `@` brings up mention candidates. Messages come as bubbles, the model's thinking sits in a collapsible card, tool calls show as tool cards with status; scrolling up during generation isn't interrupted by auto-scroll.

**Chats**: shares the same backend data as the desktop, so a title changed or a session created on the phone shows up after a refresh on the computer, and the other way round. When a session is continued on the phone, stale desktop markers such as "finished but unread" are voided automatically — no out-of-date conclusions left behind.

**Memory**: lists long-term memory one by one; tap in to edit the content or change the category, or delete it outright. When creating an entry, fill in the content and pick a category; from then on it's recalled automatically in Chat.

**Tasks**: one Scheduled Task per row; see its time or interval, enable or disable it for now, tap "Run now" to execute once immediately, or delete it. Creating one means filling in name, prompt, model, mode and the time or interval in that order.

**Settings**: the few things you most need on a phone, changed on one screen and taking effect immediately.

## Who does what while you're remote

The mobile side is the remote control, not a second copy of the data:

- The data is still one copy: Chats, memory and to-dos all live in the local data directory on the desktop machine; the phone only operates it.
- Tasks still run on the computer: model requests and tool execution happen on the computer side, and the phone only starts and watches. So close SLATE on the computer and remote control is over.
- Don't let the computer sleep while it runs: sleep cuts off generation and background tasks in flight.
- The desktop window doesn't need to stay in the foreground, but the app has to be running.

## When to use remote control, and when to walk back to the computer

| Situation | Suggestion |
|---|---|
| A long task is half done and you have to go out | Watch progress remotely, and add an instruction if needed |
| You only want to rename something, delete a session, glance at memory | Remote control is enough |
| Bulk-cleaning history, pasting large chunks of Context into a template | Back to the desktop: bigger screen, faster |
| Managing Skills, editing playbooks, configuring an MCP Server | Back to the desktop; these blocks live only in desktop Settings |
| Collaborating, showing the interface to someone else | Not advised — the remote address is the key |

## What mobile Chat can do

- **Streaming output**: appears character by character over the same protocol as the desktop; scrolling up isn't interrupted by auto-scroll, and it follows along while you're at the bottom.
- **Tool loop**: shares the same Agent loop logic as the desktop, so the model can observe, execute, verify and report; the interface is the same source, so tool card titles don't degrade into bare English tool names.
- **Risky command confirmation**: when a hard-coded risky rule matches, a bottom sheet appears with the command and the rule it hit, plus a one-line note on the command's purpose generated by the model, and you decide to approve or reject.
- **File change confirmation**: edits and new files show you the diff first; only an accept writes to disk, and a reject writes nothing.
- **@ mentions**: typing `@` opens a candidate overlay for Skills, Tools and Project files; arrow keys to choose, Tab or a click to insert.
- **Stop really cancels**: stopping shuts the streaming channel of the tool calls as well, and the backend terminates the matching child process and running tasks.

## What mobile Settings can change

| Setting | Notes |
|---|---|
| Model choice | Listed by domestic / international / local / custom group; tap to switch, with each model's context budget shown |
| Reasoning effort | The levels offered follow the current model's abilities (auto / off / low / medium / high), sharing the same state as the selector by the desktop input |
| Keys | Enter or clear the API Key for the current model |
| Appearance | Dark mode switch; the top status bar also has a handy theme toggle. When a custom theme is on for the computer, this item says "locked", and tapping the toggle only explains why — no colour change |
| Remote info | The authorised access address and QR code, copyable in one tap |

## Auth and risk

LAN access is let in by the auth code carried inside the address: only a device that comes in through the address shown in Settings (or its QR code) gets access; a request without the auth code is stopped at a "authorization required" page. The auth code is kept on the device, so the same browser doesn't need to scan again later.

:::danger Don't send the access address out
That address with its auth code is the key. Any device that gets it, as long as it's on the same LAN, can open and operate your SLATE — read files, run commands, see every historical session. Don't expose the address in group chats, on forums or in screenshots. When you no longer need remote control, close SLATE on the computer and the address stops working.
:::

**Security advice**: this opens a local service to the LAN, so use it only on a network you trust. On public Wi-Fi such as a café, hotel or airport, close SLATE or don't use remote control.

## Troubleshooting a connection

1. **Are the phone and the computer on the same Wi-Fi?** A phone on cellular data, or on a guest network on another band, isn't on the same LAN.
2. **Is the computer's firewall blocking the port?** The first time LAN access opens, the system may ask about the firewall and you need to choose allow; if you said no back then, let SLATE through in the firewall settings.
3. **Does the address use the computer's LAN IP?** Use the address shown in Settings, not the loopback address.
4. **Is a guest network isolating devices?** Plenty of routers have "AP isolation" on by default, so devices on the same Wi-Fi can't see each other either; turn it off in the router settings, or switch to a phone hotspot.

Matching the symptom gets you there faster:

| Symptom | Most likely cause | What to do |
|---|---|---|
| The page spins forever and won't open | The computer isn't running, or the port is blocked by the firewall | Check that SLATE is running on the computer; let it through the firewall |
| It opens and stops on "authorization required" | The address is missing its auth code | Copy the full address from Settings again, or scan again |
| A tablet opens the desktop interface | The tablet is judged a desktop device | Expected behaviour, nothing is lost; for the mobile interface, open the same address in a phone browser |
| It worked yesterday but not today | The computer changed network and the IP changed | Open Settings again and use the newly shown address |
| Only one phone can't connect | Guest network isolation or system rate limiting | Check the router's AP isolation, or try a phone hotspot once |

Other things to check: if Settings says "remote service not started", restart the app; when the port in the address is taken by another program, SLATE switches to another one, so always go by the address Settings shows at that moment.

:::note Does the address change
Change the computer's Wi-Fi and the router hands out the address again, so the access link changes with it; a taken port changes it too. So after switching networks, don't reuse the old address — look at Settings again before you scan.
:::
