---
title: Models & API Keys
description: Configure preset models, custom endpoints and local models
section: Start
order: 4
---

This page shows you how to bring models in: how to fill in keys for preset models, how to add a custom endpoint, how to point at local models, and how to read the context budget and usage.

## Where to configure

Two entry points, leading to the same page:

- the **Keys** button on the right of the top bar;
- the top-bar **Settings** tab, then **Model config** in the left navigation.

The "Model config" block holds three things: the **custom models** list, the **built-in model keys** list, and the Responses API mode toggle. Each model row is followed by a "Max context" control (slider + exact number box + probe window button; see "How to set the context budget" below).

## Preset models

SLATE ships with a model list, appearing in four groups in the model dropdown of the input area:

| Group | Contains |
|---|---|
| International models | GPT series, Claude series, Gemini series |
| Domestic models | DeepSeek, Kimi, Qwen, GLM, Doubao, MiniMax, ERNIE |
| Local models | One built-in local model entry, for Ollama / LM Studio |
| Custom | Endpoints you added yourself |

In the dropdown, the dot in front of each entry is the key status: **configured** is solid, **not configured** is hollow. Hovering over an option also shows the model ID, the API address and whether that model supports the Responses API.

Next to the dot is that provider's brand mark. Built-in models and models you add yourself go through the same judgment: they are recognised by **model name**, and only when the name doesn't reveal a brand is the **API address** consulted — which is why `deepseek-r1:1.5b` running on local Ollama still draws the DeepSeek mark rather than Ollama's. If it can't be recognised, nothing is drawn: better to leave it blank than to slap another provider's logo on it. The marks are each provider's official graphics shipped with the app: the 47 that have colour originals are drawn in the brand's own colours, while the other 11 (OpenAI, Anthropic, xAI, Ollama, Z.ai and others) only ship a monochrome version and are drawn in a neutral grey. Neither follows the theme — the ink and accent colours picked in "Extensions → Appearance" can't tint brand colours, and switching light/dark won't smear them into a black blob. Next to GLM (Zhipu) the mark drawn is **Z.ai**: that company has changed its outward identity to Z.ai and we follow the new mark, for which the app ships only a monochrome version.

Which specific models are available depends on what your interface lists. Steps to configure a key for one model:

1. Find it in "Built-in model keys".
2. Paste the API Key into the input box and click the save button on the right.
3. A configured input box shows "Configured"; clear the content and save again to delete that key.

## Adding a custom model

As long as your provider offers an OpenAI-compatible interface, you can connect it.

1. Click **+ Add model** at the top right of "Model config".
2. Fill in these fields:

| Field | Description |
|---|---|
| Model name / ID | The model identifier your provider requires; also the text shown in the dropdown |
| Request mode | OpenAI-compatible, Anthropic, or direct curl |
| Base URL | Your API address |
| API Key | Optional; endpoints that are local or need no auth can be left blank |
| Context Window | The context size this model can hold |

3. Click "Add" to save; it appears in the "Custom" group of the model dropdown.

:::tip Don't rush to switch models
After adding an endpoint, first fire the shortest possible request in **Settings → API test**. Once it works, set it as your regular model — that saves a lot of back-and-forth guessing about "is the model bad or is the config wrong".
:::

## Using local models

To keep inference entirely on your machine, use Ollama or LM Studio.

- The model list already has a **local model** entry, pointing by default at the local Ollama compatibility address (default port 11434).
- When using LM Studio, put the listening address it shows into that entry's Base URL.
- If you changed the port yourself, enter the port actually being listened on.
- Local models don't verify an API Key; the dropdown labels them as local models.

:::note What "local address" means
A local model's address points at your own computer and needs no internet. So it also works offline; conversely, whether the model can run at all and how large a context it can open depend on your machine's graphics card and memory.
:::

## API Keys and data safety

- API Keys are stored locally (encrypted at rest) and used only to call the models you configured.
- Keys are never written into conversation records, nor do they land in your working directory along with project files.
- They can be carried along when you export a Backup and keep working after importing to a new machine.

:::warning Don't put keys anywhere public
Don't copy API Keys into project files, notes or screenshots. They spread along with code repositories and chat logs; once you suspect a leak, revoke it in the provider's console immediately and generate a new one.
:::

## How to set the context budget

Every model has its own context budget. The larger you open it, the more material a single request can carry, and the higher the consumption.

- The **Max context** on each row of model config consists of three things: a slider generated from this model's window, an exact number box, and a **probe window** button.
- Choosing **Auto** takes this model's own nominal window ×0.8 instead of snapping to the public levels. So a local model with only an 8K window gets 6553, rather than not even filling the lowest level and occupying the whole window with no room left to write the reply.
- The number box keeps the exact value you enter (131072 is 131072), clamped only within the 1K–4M range; when the chosen value exceeds this model's window it is capped automatically, and the readout shows both the value you chose and the value actually in effect.
- Local and custom endpoints (Ollama / llama.cpp / vLLM / OpenAI-compatible) can click **probe window** to ask that server directly how much it can actually take. The probed value is kept in a separate override table, participates in the auto level and the cap, can be cleared with one click at any time to return to the endpoint's own value, and when nothing can be probed it says plainly "this endpoint does not expose a context window" instead of making a number up for you.
- Only for a model with neither a nominal window nor a probe result does the auto level fall back to the global "Context Token limit" (changed in **Settings → Context & Projects**).

The threshold that triggers automatic compression and the context bar in the interface are both computed from the same number, so you never get the mismatch of "the bar is full but nothing compresses". The context bar can be clicked directly; one click jumps to that model's row.

## How to choose the thinking effort

The level capsule on the left of the input box controls "how long this session lets the model think" (Auto / Off / Low / Medium / High), stored separately for each Chat. The scale isn't a fixed table — SLATE sorts endpoints into nine categories by capability, and the popup only offers the levels this model can genuinely accept:

- Models that force thinking have no "Off" level; the lowest is "Low".
- Endpoints that can only be switched on or off as a whole, without level adjustment, are annotated next to the scale with "Low / Medium / High all count as on".
- Levels a model doesn't support are greyed out with the reason stated; the popup says so the moment you switch to that model.
- If upstream rejects this field with a 400 naming it, SLATE strips it and resends once — the worst case is that the level doesn't take effect this time, not that the model is unusable.
- The small text below a level (Free ink / Clear ink / Light ink / Rich ink / Charred ink) is only a density hint; dragging only previews, and it takes effect and is saved when you let go.

## Responses API mode

There is a toggle in "Model config": **Enable Responses API mode**. It sends requests in the newer API format, and only some models support it.

- Off by default; sending requests in the existing format works fine.
- Turn it on only when you know for certain that your endpoint supports the Responses API and you need its capabilities.
- If unsure, don't turn it on; turned on wrongly, it usually shows up as the request being rejected upstream.

## Division of labor between lightweight and heavy models

Models at different tiers can each do their part, saving money without sacrificing the quality of the conclusions.

| Scenario | Division of labor |
|---|---|
| AI Team debate | Lightweight models handle the discussion and the speaking, heavy models make the final decision |
| AI-assisted features | A dozen-plus items such as compression summaries, memory distillation, code understanding and command explanation, each individually switchable and individually assignable to a model |
| Auto-advance review | Assign the review model separately in the "Auto-advance" block |

These toggles and assignment entry points are all in Settings; the item-by-item description is in [Settings & security approvals](./19-settings.md).

## Switching models and usage display

- **Switching**: pick in the model dropdown of the input area; it only affects this session. The last item in the dropdown is "+ Custom model…", where you can add one on the spot.
- **Per-reply usage**: every reply is tagged with the model used and the Token usage.
- **Session usage**: the usage info bar below the title bar reflects the session on screen; the **Summary** tab in the left column gives a summary of a session.
- **Cumulative usage**: **Settings → Usage statistics** shows the cumulative consumption of all conversations.

Several sessions may be running at the same moment; each keeps its own books, and the usage bar only reflects the session in front of you.

## FAQ

**I filled in the key but it still errors**

Go to **Settings → API test**, select the model in question and click "Run Test". This request goes through the same path as a real conversation, so it can tell you directly whether it's "wrong key", "wrong address", "insufficient balance" or "wrong model name".

**The model I want isn't in the dropdown**

Connect it as a custom endpoint with "+ Add model"; there's no need to wait for the list to update.

**The list shows "No built-in models"**

That means the built-in list couldn't be fetched this time. You can add a custom model by hand as a stand-in first, then check [FAQ](./20-faq.md).
