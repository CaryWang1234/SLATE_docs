---
title: Expert Packs
description: Package a persona, rules, knowledge and skills into one expert
section: Chat & Automation
order: 10
---

Every time you change scenario you have to explain again "who you are, what rules you follow, which material you reference". Expert Packs put all of that into one folder: install once, attach it when needed, and the model works in this expert's identity and tone.

## What an Expert Pack is

An Expert Pack is a **distributable** role configuration: how a person thinks, what rules they keep, what they know and which methods they use, all packed into one folder. It can live only on your machine, or be zipped up and shared with colleagues.

Once loaded it isn't written into the chat history; it's injected as part of the system prompt — so it survives switching sessions and switching models, until you take it off.

## The five-part structure

An Expert Pack consists of five parts:

| Part | Role | What to write |
|---|---|---|
| `persona.md` | Persona: who this expert is | Identity and experience, what they're good at solving, how they speak and think |
| `rules.md` | Rules: what must be followed | Judgement conventions, output format requirements, things never allowed |
| `knowledge/` | Knowledge: the material they hold | Excerpts of material they'll really use, one topic per file |
| `skills/` | Skills: the methods they know | Step-by-step methodology, checklists, templates |
| `data.json` | Metadata | Name, one-line description, version, author |

`knowledge/` and `skills/` are both folders and can hold several files; the file name is its label.

`persona.md` decides "whether it feels like that person", and `rules.md` decides "whether it's stable". If you only write one, write `rules.md` first — the persona gives the expression flavour, but the rules are what make it deliver every time.

## Building an Expert Pack from scratch

In the Expert Pack management panel click "New", then fill in, in order:

1. **Write the name and description**: the name is what it shows in each dropdown, and the description is a one-line explanation; both are exported along with the pack.
2. **Write the persona** (Persona tab): who this expert is, what they're good at, what tone they speak in. Short sentences, concrete.
3. **Write the rules** (Rules tab): what it must do, what it must never do, what format to output.
4. **Add knowledge files** (Knowledge tab): upload them one by one; the file name is its label, e.g. "judgement-conventions.md", "common-pitfalls.md".
5. **Add skill documents** (Skills tab): put in the methodology, checklists and templates you use often.
6. **Save**: it takes effect as soon as you save; to give it to someone else, click "Export" and save it as a zip.

## How to write rules that work

Rules aren't slogans; they're executable constraints. Rather than "please be professional", write clearly "what must be done, what must not be done, what the output looks like". A usable set of rules looks roughly like this:

```text
## Output requirements
- Give the conclusion first, then the reasoning, then the executable next step.
- Cite the source when numbers are involved; if there's no basis, write "no data" rather than estimating.

## Checking conventions
- Every recommendation must state its applicable conditions and its cost.
- When a conclusion has preconditions, write the preconditions before the conclusion.

## Prohibited
- Don't use vague wording such as "possibly" or "roughly" to dodge a judgement.
- Don't cite cases or data that don't appear in the material.
```

Use it as a reference: the more specific the entries and the more they read like a checklist, the more consistently the model performs.

## Import and export

Export is a zip, and import uses the same format, so it can go straight to a colleague.

- An imported pack must contain the three files `persona.md`, `rules.md` and `data.json`; these three may sit inside a single root directory within the zip.
- A pack is capped at 50 MB uncompressed and at most 500 files.
- What you import is a copy on your machine; changing it doesn't affect the original in someone else's hands.

In the Expert Pack management panel, click "Import" to choose a zip, and "Export" to save the current one as a zip.

:::tip Try the built-in sample before writing your own
SLATE ships with a sample pack, "创意写作导师" (Creative Writing Mentor), ready to use once installed. Have one conversation with it first to see what persona and rule injection looks like, then break down its way of writing to build your own expert.
:::

## Built-in sample: 创意写作导师 (Creative Writing Mentor)

The sample pack is named "创意写作导师" (Creative Writing Mentor), positioned as "a narrative expert who helps you polish inspiration into a story: structural diagnosis, style advice and concrete rewrite examples".

Its five parts include two knowledge files and one skill document, ready to use as a template: swap `persona.md` for your role, `rules.md` for your conventions, and the knowledge files for the material you hold.

## The difference between the three injection routes

The same Expert Pack can be attached from three places, with completely different scope:

| Injection route | Where to pick it | Scope | What is injected |
|---|---|---|---|
| The expert dropdown in the chat input area | Left of the chat input area | Takes effect for the whole conversation | Persona + rules + the list of knowledge file names |
| The team member card | The "Expert Pack" dropdown on each member in team mode | Takes effect only for this role's speech | Persona + rules |
| Chat `@` mention | Type `@` in the input box and pick an Expert Pack | Takes effect only for this one message | Persona + rules + the full text of the first 6 knowledge files (up to 4000 characters each) |

The key difference is in the last two columns: the first two routes give only the **names** of the knowledge files — the model knows "this file exists" but may not be able to read the content; only the `@` mention route stuffs the knowledge text into the message, at the cost of a noticeably larger token count for that message.

So the division of labour can be: for a stable expert identity, attach it with the dropdown; for it to really open a piece of material this time, use an `@` mention.

## When to use an Expert Pack

- **Across many sessions, doing the same kind of thing repeatedly**: long-term technical design reviews, long-term external copywriting, for example.
- **With clear conventions and taboos**: writing these into `rules.md` is more reliable than stressing them verbally every time.
- **To share with others**: one zip is the whole thing; whoever receives it imports it and reproduces it.

Conversely, if you just want its tone to shift this one time, saying so clearly in the message is enough; there's no need to build a pack for it.

## Maintenance and updates

- **Changes take effect on save**: after saving in the panel, if this pack is attached to this conversation, the injected content updates in step — no need to pick it again.
- **Files can be added and removed**: knowledge files and skill documents can be uploaded and deleted at any time; deleted ones disappear from the list.
- **Deletion is irreversible**: deleting an Expert Pack asks for one confirmation, and after that it can't be undone; to keep a copy, export a zip first.
- **A backup is recommended**: hand-written rules and organised knowledge material are all hard work, and the exported zip is the simplest backup.

## Things to watch

- **The bigger the knowledge files, the more tokens they cost**. An `@` mention reads at most 6 files, each truncated to 4000 characters; the more you load in, the higher the fixed overhead on every message.
- Include only what you **will really use**: one "common judgement conventions" file is more useful than a "complete collection of material".
- Rules and persona should be short and specific. Written as long prose, the model loses the point instead; short sentences and lists stated clearly make it perform more consistently.
- Keep one pack to one kind of role. When you need several roles, make several packs and attach them separately in team mode — that's clearer (see [AI Team and Workflows](./11-team.md)).

:::warning If you can't take it off, switch instead
An Expert Pack attached to a conversation takes effect throughout. If you find its conventions don't suit the current task, switch back to "No expert" in the dropdown right away; don't force it in the same conversation — with two sets of conventions mixed together, the model is pulled both ways.
:::
