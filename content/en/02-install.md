---
title: Install & launch
description: Two ways to install, the first-launch flow, and where your data lives
section: Start
order: 2
---

This page gets SLATE installed and running, and explains what happens on first launch and where your data lives.

## System requirements

| Item | Requirement |
|---|---|
| Windows desktop | Use the installer directly; no extra runtime needed |
| macOS desktop | Use the `.dmg` directly; no extra runtime needed |
| Running from source | Python 3.13 or later |
| Source platforms | Windows / Linux / macOS all work |
| Network | After the first launch, a network connection is needed to call the models you configured |
| Browser | When running from source, open the local address in a fairly recent version of Chrome / Edge / Firefox |

## Option 1: Windows installer

Suits most users: install and go, no Python needed.

1. Go to the project's GitHub Releases page and download the latest installer `SLATE-Setup-x.x.x.exe`.
2. Double-click to run the installer.
3. During installation, choose the interface language: **简体中文** or **English**.
4. When it finishes, launch from the Start menu or the desktop shortcut.

:::tip The interface language is chosen at install time
The language is fixed at the install step; the interface and all UI text then use that language throughout. To change it, run the installer again and pick.
:::

:::tip Double-clicking again won't open a second window
One installation only ever runs one SLATE. If the window is already open (or already collapsed into the system notification area) and you launch again, you don't get a second window or a second backend: the new launch brings the running window back to the front, then exits itself. The lock goes away with the process, so a crash or being ended from Task Manager never leaves it in a "can never open again" state.
:::

## Option 2: macOS installer

On an Apple computer use the `.dmg`: install and go, also with no Python needed.

1. Go to the project's GitHub Releases page and download the latest `SLATE-Setup-x.x.x.dmg` (the same directory has `SLATE-Setup-x.x.x.dmg.sha256`; if you want to verify before installing, use `shasum -a 256 -c`).
2. Double-click to mount, then drag "SLATE 砚" into the "Applications" folder.
3. **First launch**: in Finder, right-click (or long-press) the SLATE icon → "Open" → then click "Open" once more.
4. After that you can launch it normally by double-clicking.

:::warning This build is not code-signed or notarized
The `.dmg` is produced directly by CI, with no Apple Developer certificate signature and no notarization, so the first open is stopped by Gatekeeper with "cannot verify the developer". Step 3 above — right-click → Open — is the proper way around it, and it only needs doing once. To check that the download is intact, compare it against the `.sha256` file of the same name.
:::

:::tip Where data lives on a Mac
The installed app keeps conversation history, API Keys, backend logs and the WebView profile in `~/Library/Application Support/SLATE`, not inside the `.app` bundle. Upgrading replaces the whole `.app`, and your data isn't taken along with it. Running from source still keeps data in the repository's `data/`.
:::

:::note Tray and single instance are Windows-only for now
On a Mac, closing the window quits the app, and launching twice opens two copies. Both will be addressed later.
:::

## Option 3: run from source

For people who want to change a few things themselves, or who use Linux (macOS can run this way too, it's just unnecessary — there's a ready-made `.dmg`).

```bash
git clone https://github.com/CaryWang1234/SLATE.git
cd SLATE
pip install -r requirements.txt
```

**Windows:**

```bash
start.bat
```

**Linux / macOS:**

```bash
chmod +x start.sh
./start.sh
```

Once it has started, open this in a browser:

```text
http://127.0.0.1:8000
```

You can also run the desktop entry directly with `python desktop.py` to open the same app as a desktop window.

## Choosing between the three

| Item | Windows installer | macOS installer | From source |
|---|---|---|---|
| Needs Python | No | No | Yes, Python 3.13+ |
| Platforms | Windows | macOS | Windows / Linux / macOS |
| Upgrading | Download the new installer and install over it | Download the new `.dmg` and drag once | Pull the latest code and restart |
| Changing the source | Not suited | Not suited | Suited; changes take effect after a restart |
| Who it suits | People who just want to draft ideas and run tasks | People who just want to draft ideas and run tasks | People who want to tinker with the interface and internal flows |

## What happens on first launch

1. After the main window opens, a **new user guide** appears first, using a few cards to introduce the multi-model Chat, Target Mode, Grind Mode, built-in tools, Memory & Knowledge, and the other panels.
2. Click "Get Started" to close the guide and enter the main interface.
3. The main interface's top bar has five tabs: **Chat / Whiteboard / Extensions / Factory / Settings**, one shown at a time. It opens on "Chat" by default, and that area is itself split into two columns: the left sidebar holds Projects and Tasks, the right side is the Chat message stream and the input box, and the right edge of the message area slides out the Task list and the background task panel on demand. Skills, Tools, modes, MCP, Expert Packs and Actions — everything about "what the model can use" — lives on the Extensions tab.

You only see the new user guide once. To see it again, go to **Settings → About** and click the "New user guide" button.

## First thing after installing

A freshly installed SLATE has no model available yet. Configure an API Key first:

1. Click the **Keys** button on the right of the top bar, or switch straight to the **Settings** tab.
2. In "Model config", find the model you want to use, fill in the matching API Key and save.
3. To connect another provider's endpoint, click "+ Add model" in the same block and fill in the model ID and API address.
4. Back in the Chat interface, pick the model you just configured in the model dropdown in the input area.

Configuration details and the list of providers are in [Models & API Keys](./04-models.md).

:::note The first launch needs a network connection
SLATE itself runs on your machine, but it calls the models you configured to do Chat and inference. So before the first use, make sure this computer can reach the service endpoint you chose and that the API Key has quota available. Without a working model configured you can still see the interface and your history, but messages you send will get no reply.
:::

:::warning Don't put API Keys anywhere public
API Keys are stored in the local app configuration; you don't need to copy them into notes or project files. Please avoid writing them into documents that will be committed to a code repository or shared with others; if one leaks, revoke it in the provider's console immediately and generate a new one.
:::

## Automatic update check at launch

SLATE checks for a new version every time it starts:

- When a new version is found, a banner appears just below the top bar, with entry points to download and to read the release notes.
- The top-right corner of the banner closes it; after choosing "Ignore This Version" it stops prompting for that version.
- You can also check manually at any time: **Settings → About**, click "Check for Updates", where your current version number is also shown.

The installer always comes from the project's GitHub Releases; SLATE never downloads executables from anywhere else.

## Uninstalling and your data

**Uninstall**: on Windows, uninstall SLATE from the system's "Apps" list; the uninstaller removes the application itself.

**Data**: conversation history, memory, knowledge documents, Expert Packs, action flows and all settings are saved as files on this machine and are not uploaded to the cloud. So:

- To move to a new computer, export a backup first, then import it on the new machine (see [Data, backup & storage](./17-data.md)).
- To clean up completely, it's also best to export a backup once and confirm it is correct before deleting anything.
- Uninstalling the app and deleting data are two separate things; handle each according to what you need.

## If it won't start

- Nothing appears after double-clicking the icon: most likely a SLATE is already running (the window may be tucked into the system notification area). Launching again only brings that window back, it doesn't open a second one; look for it in the notification area or the taskbar.
- If starting from source fails, first confirm Python is at least 3.13 and the dependencies are fully installed, then run the start script again.
- Watch the command line for errors during startup; in most cases the last few lines show the cause.
- If the interface opens but messages get no reply, it's most likely a model key or network problem. Go to **Settings → API test** and use the shortest possible request to verify the link works.

If it still doesn't work, check [FAQ](./20-faq.md).
