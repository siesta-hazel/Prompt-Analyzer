# ⚡ PromptCraft Matrix: Automated LLM-as-a-Judge Benchmarking Suite

A Streamlit-powered evaluation tool that runs prompt variations against custom datasets and uses a structured LLM-as-a-Judge model to compare accuracy, relevance, formatting adherence, and execution latency.
This project was made for academic purposes.

---

## 📌 Project Overview

When building applications on top of Large Language Models (LLMs), evaluating prompt changes manually is slow and unscientific. **PromptCraft Matrix** automates this evaluation workflow by:
1. Running user test cases through two candidate prompt configurations (e.g., **Baseline Zero-Shot** vs. **Engineered Chain-of-Thought**).
2. Routing candidate outputs to a dedicated **LLM-as-a-Judge** evaluator that enforces step-by-step reasoning before assigning numerical scores.
3. Rendering side-by-side comparative analytics, latency benchmarks, and summary charts.

---

## 🛠️ Key Prompt Engineering Concepts Demonstrated

- **Structured Outputs & Schema Validation:** Leverages Pydantic models with JSON Schema generation to guarantee raw, deterministic JSON outputs from the LLM Judge.
- **Chain-of-Thought (CoT) Reasoning:** Forces the Judge model to state its step-by-step reasoning in `chain_of_thought` *before* outputting scores to eliminate rating hallucinations.
- **LLM-as-a-Judge Architecture:** Utilizes high-tier LLMs as automated, objective evaluators to score response quality across multiple criteria.
- **Token Efficiency & Optimization:** Implements model tiering (`llama-3.1-8b-instant` for execution vs. `llama-3.3-70b-versatile` for judging) and token capping to minimize API costs.

---

## 🏗️ System Architecture


```

┌──────────────────┐       ┌────────────────────────┐       ┌───────────────────────┐
│  User / Dataset  │       │    Execution Engine    │       │   Evaluation Stage    │
│                  │       │  (llama-3.1-8b-instant)│       │(llama-3.3-70b-versatile)
│  • Benchmark Case│ ────> │  • Run Prompt A        │ ────> │  • Structured JSON    │
│  • Prompt A      │       │  • Run Prompt B        │       │    Schema Judge       │
│  • Prompt B      │       │  • Track Latency       │       │  • CoT Reasoning      │
└──────────────────┘       └────────────────────────┘       └───────────────────────┘
│
▼
┌───────────────────────┐
│  Streamlit Dashboard  │
│                       │
│  • Side-by-Side Outputs│
│  • Metrics (1-5 Scores)│
│  • Visual Summary     │
└───────────────────────┘

```

---

## 📁 Repository Structure

```text
.
├── app.py                # Main Streamlit dashboard interface
├── runner.py             # Groq API runner & prompt execution logic
├── evaluator.py          # Pydantic evaluation schema & Judge system prompt
├── test_dataset.json     # Pre-loaded benchmark dataset
├── requirements.txt      # Python dependencies
├── .env.example          # Sample environment variables template
└── README.md             # Project documentation

```

---

## 🚀 Quickstart Guide

### Prerequisites

* Python 3.10 or higher
* Groq API Key ([Get one here](https://console.groq.com/))

### 1. Clone the Repository & Setup Venv

```bash
git clone [https://github.com/your-username/prompt-evaluator.git](https://github.com/your-username/prompt-evaluator.git)
cd prompt-evaluator

# Create and activate virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate

```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

### 3. Configure API Key

Create a `.env` file in the project root directory:

```env
GROQ_API_KEY=gsk_your_actual_groq_api_key_here

```

### 4. Run the Application

```bash
streamlit run app.py

```

Open your browser at `http://localhost:8501`.

---

## 📊 Evaluation Criteria

The Judge model evaluates candidates on a **1–5 scale** across three core pillars:

| Metric | Focus Area |
| --- | --- |
| **Accuracy** | Factual correctness and absence of hallucinated information. |
| **Relevance** | Directness of answer relative to the user prompt. |
| **Formatting** | Adherence to requested constraints (word limits, JSON schema, syntax). |

---
