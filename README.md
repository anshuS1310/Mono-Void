# ✨ Mono Void

> *A calm space to refine your prompts — so every LLM interaction counts.*

Mono Void is a minimalist, beautifully designed **prompt refinement workspace** built with Streamlit. You write a message, choose your LLM (paid API or local), hit **Transmit**, and Mono Void sends it through an intelligent rewriting system that returns a cleaner, sharper version of your prompt — using fewer tokens while keeping all the intent intact.

Think of it as a quiet editor between your thoughts and the AI.

---

## 🌌 What It Does

When you type a prompt into Mono Void, it does three things:

1. **Estimates your token count** — so you know how heavy your message is before sending
2. **Rewrites your prompt** using the LLM you selected — trimming filler, removing redundancy, sharpening intent, without adding anything new
3. **Shows you both versions side by side** — original vs. refined — along with a token count comparison so you can see the difference immediately

The refined prompt is displayed in a copy-ready code block. Your original stays visible so you can compare, decide, and iterate.

---

## 🎨 Why It Looks The Way It Does

Mono Void was built to feel premium — not like a utility tool thrown together overnight. It features:

- **Aurora gradient background** — a slow-shifting multi-colour radial gradient that makes the page feel alive without being distracting
- **Glassmorphism sidebar** — the workspace panel uses frosted glass styling with subtle inner shadows and a soft backdrop blur
- **Outfit + Inter typography** — Google Fonts that make text feel editorial and intentional
- **Micro-animations** — cards appear with spring physics, buttons lift on hover, alerts pop in with a subtle bounce
- **Dark-glass code block** — the refined prompt sits in a deep dark card that makes the output feel important and copyable

---

## 🧠 Supported LLM Backends

Mono Void is backend-agnostic. You can plug in whichever model you have access to.

### 💳 Paid APIs

| Provider | How to use | Example models |
|---|---|---|
| **OpenAI** | Paste your API key | `gpt-4o`, `gpt-4o-mini`, `gpt-3.5-turbo` |
| **Anthropic** | Paste your API key | `claude-opus-4-5`, `claude-haiku-4-5-20251001` |
| **Google Gemini** | Paste your API key | `gemini-2.0-flash`, `gemini-1.5-pro` |

API keys are entered per-session in the sidebar. They are **never stored, logged, or sent anywhere other than the provider's official API endpoint.**

### 🖥️ Local / Hosted

| Provider | How to use | Example models |
|---|---|---|
| **Ollama** | Run `ollama serve` locally | `llama3.2:3b`, `mistral`, `phi3`, `qwen2.5` |
| **Hugging Face API** | Paste a model repo ID + optional token | `HuggingFaceH4/zephyr-7b-beta`, `mistralai/Mistral-7B-Instruct-v0.3` |

For **Ollama**, Mono Void will automatically detect if the model is not downloaded yet and pull it for you, showing a live download progress indicator.

For **Hugging Face**, Mono Void uses the Inference API. Public models can be used without a token; private or gated models require an `hf_` token.

---

## 🚀 Running Locally

### Prerequisites

- Python 3.9 or newer
- `pip`
- *(Optional)* [Ollama](https://ollama.com) installed and running if you want local models

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/Mono-Void.git
cd Mono-Void

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
streamlit run app.py
```

The app opens at `http://localhost:8501` in your browser.

If you are using Ollama, make sure it is running first:

```bash
ollama serve
```

---

## 🗂️ Project Structure

```
Mono-Void/
├── app.py                  # Everything — UI, styling, API logic, state management
├── requirements.txt        # Python dependencies (streamlit, requests)
└── .streamlit/
    └── config.toml         # Theme config (colours, font)
```

The entire application lives in a single `app.py` file. There is no build step, no frontend framework, no database.

---

## ⚙️ How The Refinement Works

When you click **Transmit**, Mono Void:

1. **Freezes the current backend selection** so you can change settings for the next session without breaking the current run
2. **Calculates a minimum token floor** — at least half the original prompt length — so the model cannot over-compress and strip away meaning
3. **Submits the rewrite job to a background thread** using `ThreadPoolExecutor` so the UI stays responsive
4. **Polls the job every second** with Streamlit's `@st.fragment(run_every=1)` until it finishes
5. **Strips any preamble** the model might have added (e.g. "Here is the rewritten message:") and validates the output length
6. **Falls back to your original prompt** if the model's output is too short to be trusted

The system prompt instructs the model to: *rewrite for clarity and brevity, preserve all intent and essential detail, remove filler and redundancy, and return only the refined prompt — no explanation.*

---

## 🛡️ Privacy & Security

- **API keys are session-only.** They live in Streamlit's session state for your browser session only. They are never written to disk, logged, or transmitted anywhere other than the official LLM provider endpoint.
- **No user data is stored.** Prompts, refined outputs, and model history exist only in your browser session and are wiped when you reset or close the tab.
- **All LLM requests go directly from the server to the provider.** There is no proxy, no analytics, no telemetry.

---

## 🙏 Built With

- [Streamlit](https://streamlit.io) — the Python framework that powers everything in a single file
- [Requests](https://docs.python-requests.org) — HTTP calls to every LLM provider
- [Outfit & Inter](https://fonts.google.com) — the typography
- [Ollama](https://ollama.com) — local model support without configuration pain

---

