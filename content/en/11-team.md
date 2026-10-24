---
title: AI Team and Workflows
description: Multiple roles challenge each other, then a DAG pipeline runs the big jobs
section: Collaboration & Reasoning
order: 11
---

What one person — even a model — fails to think of is often caught by a role arguing from another position. Team mode puts several roles into a multi-round debate on the same question and ends with a summary that carries a signed-off conclusion; Workflow mode splits a long task into nodes with dependencies, and whatever can run in parallel runs in parallel.

## What AI Team solves

Its value is not "a few more voices" but **adversarial pressure**: one role is pragmatic, one is inventive, one calls it, and the views push against each other — so what you get back is no longer a first-reaction answer, but one that has been challenged once.

Good topics: choosing between approaches, technology selection, risk review, product direction, decisions where both sides need to be seen.

## How the debate runs

In the Chat workspace, switch the mode on the left of the title bar from "Chat" to "Team" to enter the Team Discussion view:

1. Pick a team preset, or configure the members yourself.
2. Write the question to discuss in the topic input.
3. Choose the number of rounds (default 5; 3 / 5 / 8 / 10 can be selected).
4. Click "Start discussion"; members speak in order.

In the first round each member makes their own proposal. From then on, every round the members can see all the speech so far and choose to propose, support, oppose, rebut or add, and can also address a named member. The whole process unfolds line by line, round by round, so you can always see who said what.

## The six speech actions

Every speech begins with an action marker; the system classifies speech by it, and the speech counts in the summary come from it too:

| Action | Meaning |
|---|---|
| 【提案】 | Proposes a new idea or plan |
| 【支持】 | Agrees with and reinforces an existing view |
| 【反对】 | Explicitly disagrees with a view |
| 【反驳】 | Rebuts the reasoning behind a view |
| 【补充】 | Adds what was missed in the same direction |
| 【决策】 | Gives the final plan; the discussion ends there |

To reply to a specific person, write `@member name` after the action, for example `【反驳】@性能专家 这个结论忽略了冷启动成本。` The system records it as a reply edge pointing at that person.

Every speech is required to be short (one to three sentences): it should read like a debate, not a paper, and it saves tokens.

## Roles and the model split

By default, three members map to three stances:

| Role | Stance | Responsibility |
|---|---|---|
| Analyst | Pragmatic | Feasibility and cost |
| Creative | Inventive | Possibility and user experience |
| Decider | Synthesis | Collects the views and gives the final plan with its reasoning |

Only the decider can call it: even if another member writes 【决策】, it is treated as an ordinary proposal. The decider can give a 【决策】 in any round to close the discussion; if the rounds run out with no consensus, the decider adds one final decision round.

The model split is deliberate: **lightweight models in the discussion seats, a heavyweight model in the decision seat**. The discussion phase speaks often but briefly, so a lightweight model is enough; the final plan is produced only once, and is worth the stronger model.

:::warning More rounds, more tokens
In every round each member reads all the speech so far. Rounds times members — the cost multiplies. Three to five rounds is usually enough to see where the disagreement lies; keep the number of roles to what you really need.
:::

## Built-in team presets

SLATE ships 9 presets; selecting one replaces the current member list (members can still be adjusted individually afterwards):

| Preset | Members |
|---|---|
| Classic trio | Analyst + Creative + Decider |
| Code review team | Security expert + Performance expert + Architect |
| Product brainstorm | Product manager + Designer + User advocate + Tech lead |
| Technology selection | Frontend expert + Backend expert + Infrastructure expert + Technical director |
| Red vs blue | Pro debater + Con debater + Judge |
| Full-stack review | Frontend reviewer + Backend reviewer + Database reviewer + Ops reviewer + Technical director |
| Writing workshop | Content planner + Copywriter + Editor |
| Startup advisory board | Marketing advisor + Technology advisor + Finance advisor + Operations advisor + CEO |
| Academic seminar | Methodology expert + Empirical researcher + Critic + Moderator |

## Custom teams

Treat a preset as a starting point and edit the member cards one by one:

- **Name**: change the name on the card directly; the debate record uses that name (and `@` replies recognise it).
- **Model**: pick a model on each card, grouped by "foreign / domestic / local / custom". Models with no key configured are marked with a hint.
- **Persona**: the role-setting text on the card is this member's stance and style; changing it redefines the role.
- **Expert Packs**: each card can take one Expert Pack, binding a persona and rules to that role, see [Expert Packs](./10-experts.md).
- **Add / remove**: "＋" at the top adds a member, "×" at the card's top right removes one. Members you add yourself are ordinary members by default and do not take part in calling it.

To make a member responsible for calling it, use the decider seat from a preset, or change a member to the decider seat and then adjust who fills it.

## The decision waits for your sign-off

"Decisions need my sign-off" is on by default: after the decider gives a 【决策】, the discussion does not close by itself — it stops and waits for your signature.

- **Sign off**: ends with that decision, and the summary is generated as usual.
- **Keep discussing**, or closing the dialog without choosing: counts as "not signed"; the discussion carries on with "unsigned" for another round, and the next member's prompt states that this decision has not been signed off.
- Reopening is capped; once the cap is used up the discussion closes itself — every reopen is another round of everyone speaking, and it is not given an opening to burn indefinitely.

The sign-off line is a separate record within the discussion: it enters the next member's Context and the backend record, but it does not count as any member's speech, and the star map does not count it towards anyone's viewpoint.

In night mode (full autopilot) there is no dialog to interrupt; the decision is adopted directly, but that line is still drawn and states that it was adopted automatically — it never reads as if you had clicked through. If you don't want to be stopped, clear that checkbox in the Team panel to go back to "the decision ends it".

## Discussion summary and close

When the discussion ends, a "debate summary" is generated automatically, containing:

- The topic and the list of participating members.
- Speech counts: how many in total, and how many fall under propose / support / oppose / rebut / add / decide.
- The final plan and who proposed it; if no decision was ever formed, it says plainly "no clear decision reached".

Beyond the summary, every line of the debate stays in the discussion area and can be scrolled back through.

## Stopping midway

Click "Stop discussion" to interrupt it. **Speech already completed is kept as is**; stopping never throws away what the debate has already produced.

A session stopped by hand generates no summary — with no conclusion, it does not make one up; but it still goes into team history, marked "interrupted", and opening it shows the rounds that did finish.

## Failure and absence are not speech

If a member's request fails this round, or the model they are bound to has no API Key configured, that cell is marked plainly "failed" / "did not participate":

- That error line does not enter the next member's Context — otherwise the model would take an error message as someone's claim and rebut it.
- It is not counted in the speech statistics; that member's speech count in the star map is 0.
- The backend still keeps a line with error / skipped, so you can trace afterwards who did not speak in which round; these two states can only be marked by the system — a 【失败】 written by a model does not parse.

## Switch away and find it again

The debate keeps running while you are switched to the Chat panel. Waiting for your signature and the closing of this session both go into the task centre on the right, in the same table as background terminal tasks and subagent batches: the row carries the topic, is marked "waiting for your sign-off" while it waits, the team button on the row jumps back to this session to review it, and it is this session that the stop button interrupts.

## Where the discussion record goes

Every speech lands in two places at once:

- **Local history**: the "Team history" list on the left keeps the last 50 sessions, listing the time, number of speeches and approximate token usage; click one to review it.
- **Backend team session**: one discussion corresponds to one session record, one member roster, and one event ledger record for each member.

The backend copy is the data source for the "team star map" in the Whiteboard · workflow view: it lays out the most recent discussion by role — who replied to whom, who touched which Tools, who spawned subagents — all taken from real records. If the backend write fails, local history is still there and that list entry is marked "local record only"; when this conversation has no team record at all, the star map says so directly rather than drawing a decorative graph. For how to read the star map, see [Whiteboard logic chains](./12-whiteboard.md).

## Team Workflow: hand the pipeline to a DAG

Debate is thinking together; Workflow is working separately. Switch to the "Workflow" tab of the Team panel:

1. Pick a Workflow template.
2. Fill in the task requirements below; they are passed to each node as `$input`.
3. Click "Run workflow".

Nodes are chained by dependency edges: an upstream output can serve as a downstream input (referenced as `$node_id`), and **nodes with no dependency between them execute at the same time**. Once a node runs, its state is echoed live — waiting, running, succeeded, failed, skipped; if a node fails or is skipped, everything downstream of it is skipped automatically rather than forced to run with empty input. You can stop at any time during a run; nodes that have not started are marked skipped.

A node's model binding is resolved in this priority order: a bound team member role (inheriting its model and persona) → a model the node specifies itself → the model set for the "Workflow" slot under "Settings → AI-assisted features" → the current model.

When the whole pipeline has run, the output is archived into the knowledge base automatically under a title like "Workflow output · template name", viewable in the Memory panel.

## Built-in workflow templates

SLATE ships 8 templates:

| Template | Node pipeline |
|---|---|
| Standard development | Requirements analysis → Task breakdown → Implementation → Code review → Summary & handoff |
| Parallel research & analysis | Requirements analysis → Technical research / Risk assessment / Resource assessment → Summary decision |
| Code review | Change scan → Quality review / Security review / Performance review → Summary report |
| Document generation | Outline planning → Drafting → Summary extraction → Delivery assembly |
| Data analysis | Data understanding → Trend analysis / Anomaly detection → Statistical summary → Decision recommendations |
| Research report | Topic definition → Background research → Option comparison / Feasibility analysis → Report generation |
| Product requirements | Idea sorting → User stories → Feature breakdown → Prioritization → Requirements document |
| Bug investigation | Bug description → Log analysis / Code analysis / Environment analysis → Root cause |

## Importing, exporting and deleting workflows

Workflow templates are provided as JSON definition files containing nodes, dependency edges and each node's prompt. "Standard development" and "Parallel research & analysis" are built-in and cannot be deleted; other custom templates can be imported, exported and deleted. Deletion only affects the template — output that has already been produced stays in the knowledge base.
