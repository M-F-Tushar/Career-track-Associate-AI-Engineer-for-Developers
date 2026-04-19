# 🤖 Associate AI Engineer for Developers — DataCamp Career Track

> **Personal notes and exercise repository** for the [Associate AI Engineer for Developers](https://www.datacamp.com/tracks/associate-ai-engineer-for-developers) career track on DataCamp.  
> This repo is a living document — it grows as I progress through the track.

---

## 📌 About This Track

This career track teaches you to integrate AI into software applications using industry-standard tools and APIs. By the end, you'll be able to:

- Build AI-powered backend systems and user-facing applications
- Use **LLMs** to generate text and optimize outputs via prompt engineering
- Create **chatbots**, **recommendation engines**, and **semantic search** systems
- Work with **OpenAI API**, **Hugging Face**, **LangChain**, and **Pinecone**
- Apply **LLMOps** best practices for production-grade AI deployments
- Integrate third-party APIs reliably with proper error handling and rate-limit management

**Track length:** ~26 hours | **Courses:** 9 | **Credential:** Associate AI Engineer for Developers Certificate

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
│   └── Introduction to Prompt Engineering Best Practices/
│       └── README.md
│
└── README.md   ← You are here
```

> More folders will be added as I progress through the remaining courses.

---

## 📚 Track Courses & Progress

| # | Course | Status | Notes Folder |
|---|--------|--------|--------------|
| 1 | **Working with the OpenAI API** | ✅ Complete | [`Working with the OpenAI API/`](./Working%20with%20the%20OpenAI%20API/) |
| 2 | **Prompt Engineering with the OpenAI API** | 🔄 In Progress | [`Prompt Engineering with the OpenAI API/`](./Prompt%20Engineering%20with%20the%20OpenAI%20API/) |
| 3 | **Developing AI Systems with the OpenAI API** | 🔜 Upcoming | — |
| 4 | **Working with Hugging Face** | 🔜 Upcoming | — |
| 5 | **Introduction to Embeddings with the OpenAI API** | 🔜 Upcoming | — |
| 6 | **Vector Databases for AI Applications** | 🔜 Upcoming | — |
| 7 | **Developing LLM Applications with LangChain** | 🔜 Upcoming | — |
| 8 | **Introduction to LLMOps** | 🔜 Upcoming | — |
| 9 | **Software Engineering Principles for Data Scientists** | 🔜 Upcoming | — |

---

## 📖 Course Summaries

### ✅ Course 1 — Working with the OpenAI API

A foundation course covering how to interact with OpenAI's API programmatically. Split into three segments:

| Segment | Topics Covered |
|---------|---------------|
| [Segment 1 — Introduction to the OpenAI API](./Working%20with%20the%20OpenAI%20API/Introduction%20to%20the%20OpenAI%20API/README.md) | What an API is, the Chat Completions endpoint, API authentication, making requests, interpreting response objects |
| [Segment 2 — Prompting OpenAI Models](./Working%20with%20the%20OpenAI%20API/Prompting%20OpenAI%20Models/README.md) | Text editing, summarization, generation, tokens, cost calculation, `temperature`, zero/one/few-shot prompting |
| [Segment 3 — Building Conversations with the OpenAI API](./Working%20with%20the%20OpenAI%20API/Building%20Conversations%20with%20the%20OpenAI%20API/README.md) | System/user/assistant roles, guardrails, developer-supplied assistant messages, multi-turn conversation history, building a chatbot |

**Key skills gained:** API calls, response parsing, shot prompting, cost estimation, multi-turn chatbot construction.

---

### 🔄 Course 2 — Prompt Engineering with the OpenAI API

Dedicated to crafting high-quality prompts that reliably guide model outputs for real-world tasks.

| Segment | Topics Covered |
|---------|---------------|
| [Segment 1 — Introduction to Prompt Engineering Best Practices](./Prompt%20Engineering%20with%20the%20OpenAI%20API/Introduction%20to%20Prompt%20Engineering%20Best%20Practices/README.md) | Action verbs, output length control, delimiters, f-strings, structured outputs (tables/lists/custom formats), conditional prompts |

**Key skills gained:** Structured output design, conditional logic in prompts, maintainable prompt patterns.

---

## 🔑 Key Technologies

| Technology | Purpose |
|------------|---------|
| **OpenAI API** | Accessing GPT models for text generation, classification, embeddings |
| **Hugging Face** | Open-source pre-trained models and datasets |
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

All exercises use Python. The core dependency is the `openai` package:

```bash
pip install openai
```

A placeholder API key `"<OPENAI_API_TOKEN>"` is used throughout — replace it with your own key from [platform.openai.com](https://platform.openai.com) if running code locally.

```python
from openai import OpenAI

client = OpenAI(api_key="<OPENAI_API_TOKEN>")
```

---

## 📜 License

This repository contains personal study notes and exercise reproductions created for revision purposes. All course content belongs to [DataCamp](https://www.datacamp.com).
