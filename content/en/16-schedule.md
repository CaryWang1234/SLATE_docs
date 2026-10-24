---
title: Task list and Scheduled Tasks
description: List progress, Scheduled Tasks and event triggers
section: Projects & Data
order: 16
---

## What the task list is

When Target Mode runs a multi-step task, the model first builds a TODOLIST: it breaks the big task into small items you can check off, then works through them one by one. The list isn't decoration — until every item is closed out, the model isn't allowed to claim it is done.

The list is isolated per Chat: every session has its own, they don't interfere with each other, and it's still there when you reopen that Chat.

## Reading the list panel

The list shows live in the right-hand column of the message area:

- The header reads `Task list {done}/{total}`, with "blocked n" and "in progress n" beside it, plus a progress bar.
- Every item carries a status marker: to-do, in progress, done, blocked.
- Whenever an item or a batch is finished, the model syncs the status at once — progress doesn't wait for the wrap-up.

The "Task list" button in the top bar collapses the whole column and gives the width back to the message area; click it again to expand. Collapsing doesn't make the progress vanish entirely — hovering the button reports `{done}/{total}`. When this session has no list, the button is greyed out. The collapsed state is remembered on your machine: it survives a refresh and a restart, and the list carrying on won't push the column back open on its own.

## Who builds the list, and how status changes

The list isn't something you maintain by hand. In Target Mode, when a task spans many files or many steps, or is a debugging or implementation job, the model builds the list first and then starts; a simple single-step task skips the list and just does the work, so not seeing a list is normal.

Each item's status moves as execution goes on:

| Status | Meaning |
|---|---|
| To-do | Not reached yet |
| In progress | Working on this item |
| Done | Finished, and verified |
| Blocked | Held up by an outside condition (missing dependency, waiting for confirmation, environment not ready); the model explains why in its reply |

Until every item is closed out, the model isn't allowed to write a wrap-up report; the system reads the remaining items back to it and pushes it to keep going.

## To-dos and mobile

The phone has a "Tasks" tab at the bottom (panel title "Tasks / Scheduled"), where you can view, create, run now and delete Scheduled Tasks; tasks created on the computer are the same list when you open the phone. See [Mobile remote control and LAN access](./18-mobile.md).

## What Scheduled Tasks are for

A Scheduled Task = one preset prompt + one trigger time. When the time comes, SLATE executes it locally: it hands the prompt to the chosen model and runs it once, and the result lands as its own session — you don't have to sit there, and it doesn't take over the Chat you're working in.

Creating one takes four things: a name, a prompt (the text sent to the model when the time comes), a model, and a mode.

## Creating a Scheduled Task

The entry point is the ＋ menu to the left of the Chat input (choose "Scheduled Tasks"); the panel title is "Scheduled / Event Tasks". On mobile it's the "Tasks" tab at the bottom, then "＋ New".

1. Fill in the **task name**. It appears in the title of the session that run creates, so make it a name you'll recognise at a glance.
2. Write the **prompt**: the text sent to the model when the time comes. Say exactly what it should produce.
3. Choose the **model**: the dropdown groups by domestic / international / local / custom, and defaults to the model you're using now.
4. Choose the **mode**: daily / once / interval, then fill in the time or the number of minutes.
5. Click "+ Add task"; the task appears in the list below and can be disabled or deleted at any time.

## Writing a prompt for unattended runs

Every Scheduled Task run is a new session with no earlier context to lean on; the system prompt for the run also tells the model to carry out the instruction directly and completely and to output the result rather than ask back. So the prompt has to be self-contained:

- **State the output format**: for example "use Markdown to list three blocks: what was finished yesterday, what wasn't, and the suggested order for today".
- **State where the information comes from**: for example "read TODO.md in the working directory and the recent Git commits", not "carry on from where we left off".
- **Don't write branches that need your answer to move on** — nobody is there to answer when the time comes.
- **Pin length and structure inside the prompt**, otherwise how long the output runs depends entirely on how the model feels that day.

## The three schedules

| Schedule | How the time is counted | Good for |
|---|---|---|
| Once | One point in time, run once | A one-off reminder or a one-off Summary; the task disables itself after the run |
| Daily | One point in time, run every day; if today's time hasn't come yet, wait; if it has and today's run hasn't happened, run | A daily Summary, the routine check before you stop work for the day |
| Fixed interval | Every N minutes (60 by default, 1 minimum) | Short actions you need to watch over and over, such as glancing at the build status every so often |

## Event-driven triggers

Besides the clock, a task can be pushed along by an event: it runs when the event happens, and the result is archived as its own session too. Three sources:

| Event | Trigger condition | Configurable |
|---|---|---|
| File change | A file under the watched path is created or modified | Watched file / directory paths (one per line; empty means the root of the Project the task belongs to); cooldown |
| Git push detection | HEAD of the specified repository changes | Repository path; cooldown |
| Webhook receive | An external system sends a request to this task's callback address | Secret (used to check where the request came from, optional; the request body is injected into the prompt as Context) |

Cooldown is the minimum gap between triggers (60 seconds by default, 10 minimum); its job is to stop one bulk change from firing the task over and over. An event task's prompt automatically carries the trigger Context — the files that changed, the latest commit, the Webhook content — so the model knows what woke it this time.

:::note Event tasks are configured once and left running
The event type and watched paths are saved with the task and take effect as soon as you change them. On startup SLATE takes a snapshot of file changes and Git state first, so history from before the launch isn't mistaken for a new event.
:::

## Where results go

Every run creates its own session, with a prefix and a time in the title:

```text
[定时] 每日汇总 · 09-25 09:00
[事件] 构建看门 · 09-25 14:32
```

The session lands under the Project the task belongs to — whichever Project the task was created in, that's where the result hangs; after switching to another Project, filtering by Project won't misplace it. Open the session and you get the full prompt and the model's reply.

## Managing tasks

Every row in the task list shows: schedule · model used · result of the last run (a run writes its time; a failure writes the reason; never run shows "not run yet").

- The checkbox enables / disables, so you can park a task without deleting it.
- ▶ runs it now instead of waiting for the next time; a task already running isn't triggered twice.
- × deletes the task.

## When it won't run

Scheduled Tasks are executed by a local scheduler, so a few limits are worth knowing up front:

- They only run while SLATE is running. Nothing runs while the app is closed; after you reopen it, a task whose time has passed today and that hasn't run today runs once to catch up.
- The model must have its API Key configured, and must be an OpenAI-compatible model. When the Key can't be had or the model isn't compatible, the reason is written into the task status instead of failing silently.
- If "Scheduled and event tasks" is turned off under "Settings → AI assistance", tasks stop running; trigger records are kept, and the status says it was this switch that turned them off. See [Settings and security approvals](./19-settings.md).

:::tip What Scheduled Tasks are good for, and what they aren't
**Good for**: fixed actions that don't need you to make a call halfway. A Summary of yesterday's progress, a periodic check of the repository state, a glance at the build every so often, a nudge when files change — the model can wrap these up in one reply.

**Not good for**: long tasks that need you to come in and choose. A Scheduled Task won't stop to ask you, and won't wait for your confirmation before going on. Writing the decision part as "list the options and what each one costs" and keeping the call to yourself is safer than letting it decide for you.
:::
