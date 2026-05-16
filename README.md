# 🤖 Associate AI Engineer for Developers — DataCamp Career Track        
 
> **Personal notes and exercise repository** for the [Associate AI Engineer for Developers](https://www.datacamp.com/tracks/associate-ai-engineer-for-developers) career track on DataCamp.  
> This repo is a living document — it grows as I progress through the entire track.                        

---

## 📌 About This Track

This career track teaches you to integrate AI into software applications using industry-standard tools and APIs. By the end, you'll be able to:

- Build AI-powered backend systems and user-facing applications 
- Use **LLMs** to generate text and optimize outputs via prompt engineering
- Create **chatbots**, **recommendation engines**, and **semantic search** systems
- Work with **OpenAI API**, **Hugging Face**, **LangChain**, and **Pinecone** 
- Apply **LLMOps** best practices for production-grade AI deployments
- Integrate third-party APIs reliably with proper error handling and rate-limit management

**Track length:** ~26 hours | **Items:** 12 (9 courses + 3 bonus projects) | **Credential:** Associate AI Engineer for Developers Certificate 

---

## 🗂️ Repository Structure

```
Career-track-Associate-AI-Engineer-for-Developers/
│
├── Working with the OpenAI API/
│   ├── Introduction to the OpenAI API/
│   │   └── README.md
│   ├── Prompting OpenAI Models/
│   │   └── README.md
│   └── Building Conversations with the OpenAI API/
│       └── README.md
│
├── Prompt Engineering with the OpenAI API/
│   ├── Introduction to Prompt Engineering Best Practices/
│   │   └── README.md
│   ├── Advanced Prompt Engineering Strategies/
│   │   └── README.md
│   ├── Prompt Engineering for Business Applications/
│   │   └── README.md
│   └── Prompt Engineering for Chatbot Development/
│       └── README.md
│
├── Project: Planning a Trip to Paris with the OpenAI API/
│   └── Planning a Trip to Paris with the OpenAI API.py
│
├── Working with Hugging Face/
│   └── Getting Started with Hugging Face/
│       └── README.md
│
└── README.md   ← You are here
```

> More folders will be added as I progress through the remaining courses.

---

## 📚 Track Courses & Progress

| # | Item | Type | Status | Folder |
|---|------|------|--------|--------|
| 1 | **Working with the OpenAI API** | Course | ✅ Complete | [`Working with the OpenAI API/`](./Working%20with%20the%20OpenAI%20API/) |
| 2 | **Prompt Engineering with the OpenAI API** | Course | ✅ Complete | [`Prompt Engineering with the OpenAI API/`](./Prompt%20Engineering%20with%20the%20OpenAI%20API/) |
| — | **Planning a Trip to Paris with the OpenAI API** | Bonus Project | ✅ Complete | [`Project: Planning a Trip to Paris with the OpenAI API/`](./Project%3A%20Planning%20a%20Trip%20to%20Paris%20with%20the%20OpenAI%20API/) |
| 3 | **Working with Hugging Face** | Course | 🔄 In Progress | [`Working with Hugging Face/`](./Working%20with%20Hugging%20Face/) |
| 4 | **LLMOps Concepts** | Course | 🔜 Upcoming | — |
| 5 | **Developing AI Systems with the OpenAI API** | Course | 🔜 Upcoming | — |
| — | **Organizing Medical Transcriptions with the OpenAI API** | Bonus Project | 🔜 Upcoming | — |
| 6 | **Introduction to Embeddings with the OpenAI API** | Course | 🔜 Upcoming | — |
| — | **Topic Analysis of Clothing Reviews with Embeddings** | Bonus Project | 🔜 Upcoming | — |
| 7 | **Vector Databases for Embeddings with Pinecone** | Course | 🔜 Upcoming | — |
| 8 | **Software Engineering Principles in Python** | Course | 🔜 Upcoming | — |
| 9 | **Developing LLM Applications with LangChain** | Course | 🔜 Upcoming | — |

---

## 📖 Course Summaries

### ✅ Course 1 — Working with the OpenAI API

A foundation course covering how to interact with OpenAI's API programmatically. Split into three segments:

| Segment | Topics Covered | Notes |
|---------|---------------|-------|
| [Segment 1 — Introduction to the OpenAI API](./Working%20with%20the%20OpenAI%20API/Introduction%20to%20the%20OpenAI%20API/README.md) | What an API is, the Chat Completions endpoint, API authentication, making requests, interpreting response objects | — |
| [Segment 2 — Prompting OpenAI Models](./Working%20with%20the%20OpenAI%20API/Prompting%20OpenAI%20Models/README.md) | Text editing, summarization, generation, tokens, cost calculation, `temperature`, zero/one/few-shot prompting | — |
| [Segment 3 — Building Conversations with the OpenAI API](./Working%20with%20the%20OpenAI%20API/Building%20Conversations%20with%20the%20OpenAI%20API/README.md) | System/user/assistant roles, guardrails, developer-supplied assistant messages, multi-turn conversation history, building a chatbot | — |

**Key skills gained:** API calls, response parsing, shot prompting, cost estimation, multi-turn chatbot construction.

---

### ✅ Course 2 — Prompt Engineering with the OpenAI API

Dedicated to crafting high-quality prompts that reliably guide model outputs for real-world tasks. Covers four segments:

| Segment | Topics Covered | Notes |
|---------|---------------|-------|
| [Segment 1 — Introduction to Prompt Engineering Best Practices](./Prompt%20Engineering%20with%20the%20OpenAI%20API/Introduction%20to%20Prompt%20Engineering%20Best%20Practices/README.md) | Action verbs, output length control, delimiters, f-strings, structured outputs (tables/lists/custom formats), conditional prompts | — |
| [Segment 2 — Advanced Prompt Engineering Strategies](./Prompt%20Engineering%20with%20the%20OpenAI%20API/Advanced%20Prompt%20Engineering%20Strategies/README.md) | Zero/one/few-shot prompting, multi-step prompting, chain-of-thought, self-consistency, iterative refinement | — |
| [Segment 3 — Prompt Engineering for Business Applications](./Prompt%20Engineering%20with%20the%20OpenAI%20API/Prompt%20Engineering%20for%20Business%20Applications/README.md) | Text summarization & expansion, transformation (translation/tone/grammar), text classification, entity extraction, code generation & explanation | — |
| [Segment 4 — Prompt Engineering for Chatbot Development](./Prompt%20Engineering%20with%20the%20OpenAI%20API/Prompt%20Engineering%20for%20Chatbot%20Development/README.md) | System prompt design (purpose, guidelines, behavior), role-playing prompts, external context injection via sample conversations and system prompt | — |

**Key skills gained:** Structured output design, conditional logic in prompts, advanced prompting techniques, business-oriented text tasks, chatbot system prompt architecture.

---

### ✅ Bonus Project — Planning a Trip to Paris with the OpenAI API

A hands-on project applying the OpenAI API to a real-world use case: building a multi-turn travel guide chatbot for Paris.

| File | Description |
|------|-------------|
| [`Planning a Trip to Paris with the OpenAI API.py`](./Project%3A%20Planning%20a%20Trip%20to%20Paris%20with%20the%20OpenAI%20API/Planning%20a%20Trip%20to%20Paris%20with%20the%20OpenAI%20API.py) | Full solution — a conversational travel guide that loops through questions about Paris landmarks, maintaining context across turns using the `gpt-4o-mini` model |

**Key skills applied:** Multi-turn conversation history, system prompt persona definition, looping API calls, assistant message appending.

---

### 🔄 Course 3 — Working with Hugging Face

Covers navigating and using the Hugging Face Hub, running models locally and via inference providers, and working with datasets programmatically.

| Segment | Topics Covered | Notes |
|---------|---------------|-------|
| [Segment 1 — Getting Started with Hugging Face](./Working%20with%20Hugging%20Face/Getting%20Started%20with%20Hugging%20Face/README.md) | Hugging Face Hub, model & dataset cards, `pipeline` class for local inference, `InferenceClient` for remote inference providers, `datasets` library (`load_dataset`, `.filter()`, `.select()`), Apache Arrow format | — |
| Segment 2 — *Upcoming* | Natural language tasks with Hugging Face (summarization, classification, document Q&A) | — |

**Key skills gained so far:** Hub navigation, `transformers` pipeline, inference providers (Together.ai), dataset loading and filtering.

---

### 🔜 Course 4 — LLMOps Concepts

Covers the full lifecycle of LLM applications — from ideation to deployment — including monitoring, versioning, and production challenges.

*Notes folder will be added upon completion.*

---

### 🔜 Course 5 — Developing AI Systems with the OpenAI API

Focuses on building production-ready AI applications with the OpenAI API: structured outputs, function calling, error handling, rate limit management, and robustness patterns.

*Notes folder will be added upon completion.*

---

### 🔜 Course 6 — Introduction to Embeddings with the OpenAI API

Covers OpenAI's embedding model and how embeddings power semantic search, similarity scoring, and recommendation engines.

*Notes folder will be added upon completion.*

---

### 🔜 Course 7 — Vector Databases for Embeddings with Pinecone

Covers the Pinecone vector database — indexing embeddings, similarity search, and building scalable AI applications.

*Notes folder will be added upon completion.*

---

### 🔜 Course 8 — Software Engineering Principles in Python

Covers modularity, documentation, and automated testing to help solve data science problems more reliably and at scale.

*Notes folder will be added upon completion.*

---

### 🔜 Course 9 — Developing LLM Applications with LangChain

Covers building AI-powered applications using LLMs, prompts, chains, and agents in LangChain.

*Notes folder will be added upon completion.*

---

## 🔑 Key Technologies

| Technology | Purpose |
|------------|---------|
| **OpenAI API** | Accessing GPT models for text generation, classification, embeddings |
| **Hugging Face** | Open-source pre-trained models, datasets, and inference providers |
| **LangChain** | Building LLM-powered applications with chains and agents |
| **Pinecone** | Vector database for semantic search and recommendations |
| **Python** | Primary language for all exercises |

---

## 💡 How These Notes Are Organised

Each `README.md` inside a course/segment folder contains:

- **Concept explanations** — clear summaries of every topic with tables and examples
- **Code patterns** — reusable, well-commented code snippets from the exercises
- **Exercise walkthroughs** — step-by-step breakdowns of every exercise
- **Cheat sheets** — quick-reference summaries and common mistake tables

The goal is for each file to work as a self-contained revision guide for that segment.

---

## 🛠️ Setup

All exercises use Python. Core dependencies vary by course:

```bash
# OpenAI API courses
pip install openai

# Hugging Face courses
pip install transformers datasets huggingface_hub
```

A placeholder API key `"<OPENAI_API_TOKEN>"` is used throughout the OpenAI sections — replace it with your own key from [platform.openai.com](https://platform.openai.com) if running code locally. For Hugging Face exercises, store your token as the `HF_TOKEN` environment variable.

```python
# OpenAI
from openai import OpenAI
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Hugging Face (inference provider)
from huggingface_hub import InferenceClient
import os
client = InferenceClient(provider="together", api_key=os.environ["HF_TOKEN"])
```

---

## 📜 License

This repository contains personal study notes and exercise reproductions created for revision purposes. All course content belongs to [DataCamp](https://www.datacamp.com).
