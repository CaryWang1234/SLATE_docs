---
title: Grind Mode
description: Use paced questioning to grind a rough idea into an executable task brief.
section: Chat & Automation
order: 7
---

Grind Mode is for the moment when "I know I need to do something, but I can't say what": you throw in a rough idea, the AI asks one key question per round, and it finally delivers a structured task brief (the ink brief) that can go straight to execution.

## What Grind is

In normal chat the cost of an unclear requirement is yours to carry — if you can't say it clearly, the AI can only guess. Grind hands the "think it through" work to questioning.

- You don't have to write a spec up front; a rough outline will do.
- The AI asks one question at a time, offers options when it can, and doesn't make you write an essay.
- Questioning has a round cap and won't go on forever; when there's enough information it collects the ink early.
- Collecting gives you a task brief: goal, deliverables and acceptance criteria all spelled out, ready to run.

## How to start

Three ways in:

1. Type `/grind your idea` in the input box, for example `/grind build a weekly report generator for the team`.
2. Click the + button on the left of the input box and choose "Grind Mode" under "Modes & features". This opens a new Grind session; if you haven't thought of the content yet, the input box is filled with `/grind ` for you to complete.
3. Do nothing special and just type an abstract task — say "make a website". In a new session with no conversation yet, SLATE offers a "Grind suggestion": you can choose "Enter Grind" to refine it first, or "Send directly" to send it as usual.

:::warning Starting Grind opens a new session
Whichever way you enter Grind, SLATE clears the current chat view and starts a separate Grind session; the one currently generating on screen is interrupted. It only stops that one — tasks running in other projects are unaffected.
:::

## Three-stage questioning

Grind follows a fixed three-stage progression, never more than 10 rounds:

| Stage | What the AI does |
|---|---|
| Intake | Restates the core of your idea in one or two sentences, lists 3–5 gaps that need clearing, then asks only the first one |
| Grind | Asks about the next most important gap round by round, one question at a time, offering options where it can, with no small talk and no repeating what's already settled |
| Collect | Stops asking, summarises the agreement in one or two sentences, then gives the complete structured ink brief |

Collecting starts in three cases:

- You reply directly with something like `收墨`, "that's enough", "that'll do" or "good".
- There is already enough information and the AI decides there's no need to ask more, collecting on its own.
- The questioning reaches its round cap, and it collects in that round.

:::tip Question quality depends on your answers
Grind's question chain follows your previous answer. Put concrete information in your answers (who uses it, when it's needed, what result counts as passing) and the later questions get sharper; reply only "whatever" or "you decide" and the AI can only circle in place.
:::

## Ink panel

The Ink panel in the sidebar lays out the results of this grinding session in real time:

- The panel sits to the right of the message area, in the same column as the task list.
- ✔ marks items that are settled, ✘ marks open unknowns that have no home yet.
- The top shows counts: N settled · M open, so you can see at a glance how far the draft still is.
- The panel updates as the conversation moves on; you don't need to click refresh.
- While questioning is in progress it shows the current round (round x of 10); once in the collecting stage it hints that you can reply `收墨` to get the draft right away.
- Once the ink brief exists the panel keeps a summary view of the finished draft, so looking back later doesn't lose it.
- The "Grind Mode" row in the + menu on the left of the input box follows along too; switch back and one glance tells you where this session stands.

## What the ink brief contains

After collecting, the ink brief consists of seven elements, each answering a specific question:

| Element | Question it answers |
|---|---|
| Goal | How will the world be different once this is done |
| Audience | Who will use it, who reads this result |
| Deliverables | What has to be handed over in the end, how many, in what form |
| Acceptance criteria | Which conditions must be met to count as acceptable |
| Boundaries and limits | What is not being done, which hard constraints apply (time, technology, compliance) |
| Suggested path | What order is recommended for moving forward |
| Open questions | Things not yet settled, left for the execution stage to assume reasonably and note |

Items that weren't discussed clearly are listed honestly under "Open questions"; it won't fill them in for you out of thin air.

## After the ink brief: three destinations

Below the ink brief there are three buttons; pick by what you want to do next:

| Button | What it does | When to use it |
|---|---|---|
| Send to Target Mode | Turns the ink brief into a task description and opens a Target Mode session that executes on its own | You've thought it through and want to start |
| Post to Whiteboard | Places the ink brief as a whiteboard card | Still in design: you need to draw dependencies, split modules or discuss with people |
| Save as template | Saves it into the knowledge base as a reusable task brief template | The same kind of request will come again; next time you take it out, tweak it and use it |

What each of the three buttons does when clicked:

- **Send to Target Mode**: the Target Mode toggle turns on automatically, the ink brief is organised into a task description and sent, and the model starts executing right away. Items the ink brief left open are handed to the model to assume reasonably, with a requirement that it notes the assumptions.
- **Post to Whiteboard**: generates a card titled "ink brief · your title", with the goal from the ink brief as its body, ready for you to carry on drawing connections.
- **Save as template**: saved as a knowledge document, visible in the knowledge center, ready to pull out and reuse at any time.

To see how it runs after being sent to Target Mode, see [Agent Autopilot and Target Mode](./06-autopilot.md); to see how cards on the whiteboard connect, see [Whiteboard-style logic chains](./12-whiteboard.md); for where templates are stored, see [Memory, profile and knowledge base](./13-memory-knowledge.md).

## Session persistence

Grind state follows the session, not the screen:

- Refresh the page, switch to another session and come back, and the Ink panel and questioning progress restore automatically.
- The same session doesn't ask everything from the start again because it was reopened.
- After collecting, reopen this session and the three buttons are still below the ink brief.

## FAQ

**I want to start running halfway through the questions — can I?**
Yes. Reply `收墨` and the draft appears immediately; the buttons below the ink brief appear with it, and clicking "Send to Target Mode" starts execution.

**Will Grind touch my files?**
No. Grind only produces a text task brief; it doesn't touch files or run commands. The real work happens after you click "Send to Target Mode".

**Can several Grind sessions run at once?**
Each session keeps its own Grind state, independently of the others; starting Grind in another session doesn't affect the progress of the previous one.

## When not to use Grind

Grind is for ideas that aren't thought through yet. Skip it in these cases:

- The requirement is already clear, and you could even write the acceptance criteria yourself — go straight to Target Mode and execute.
- It's a one-off question or a small change — just say it clearly as a normal chat.
- You already have a ready-made spec document — sending that document as an attachment is less trouble.

:::note Grind produces a task brief, not execution
Grind itself doesn't touch your files or run commands; it only grinds the idea into text. To actually do the work, click "Send to Target Mode" after collecting.
:::
