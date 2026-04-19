# Prompt Engineering with the OpenAI API
## Segment 1 — Introduction to Prompt Engineering Best Practices

*Comprehensive Revision Guide*

---

## Table of Contents

1. [What is Prompt Engineering?](#1-what-is-prompt-engineering)
2. [The OpenAI API — Recap](#2-the-openai-api--recap)
3. [Key Principles of Prompt Engineering](#3-key-principles-of-prompt-engineering)
4. [Structured Outputs](#4-structured-outputs)
5. [Conditional Prompts](#5-conditional-prompts)
6. [Practical Code Patterns](#6-practical-code-patterns)
7. [Summary Cheat Sheet](#7-summary-cheat-sheet)

---

## 1. What is Prompt Engineering?

**Prompt engineering** is the practice of crafting precise instructions — called *prompts* — given to Large Language Models (LLMs) in order to guide them toward producing desired, high-quality responses.

A useful analogy is cooking: just as a chef selects and combines the right ingredients to produce a great dish, a prompt engineer selects and structures the right words to get a great response from the model. High-quality prompts lead to high-quality answers; low-quality prompts lead to vague, incomplete, or unhelpful ones.

Without prompt engineering, the model has no guidance on the format, length, style, or audience for its response and may misinterpret the task entirely. With it, you gain fine-grained control over every aspect of the output.

---

## 2. The OpenAI API — Recap

### 2.1 How the API Works

The course uses the **OpenAI Python package** to interact with the API programmatically. Creating a real API key is not required to complete the exercises — the placeholder `"<OPENAI_API_TOKEN>"` is used throughout. The primary endpoint used for chatting is **`chat.completions`**.

### 2.2 The Three Message Roles

Every message passed to the API must carry one of three roles:

| Role | Purpose |
|:---|:---|
| `system` | Provides background instructions that guide the model's behavior throughout the entire conversation — the "rules of engagement." |
| `user` | The actual prompt or question from the human. |
| `assistant` | The model's response. Can be pre-filled to steer a multi-turn conversation. |

**Exercise example — OpenAI API Message Roles:**

```python
conversation_messages = [
    {"role": "system",    "content": "You are a helpful event management assistant."},
    {"role": "user",      "content": "What are some good conversation starters at networking events?"},
    {"role": "assistant", "content": ""}   # left blank for the model to fill
]
```

This structure lets the model understand its assigned role and the context of the conversation before it generates a reply.

### 2.3 Control Parameters

Two parameters shape the nature of every response:

| Parameter | What it Controls | Notes |
|:---|:---|:---|
| `temperature` | Randomness of the output. Range: `0` – `2`. | `0` = fully deterministic. `2` = highly random/creative. |
| `max_tokens` | Hard upper limit on response length. | May produce incomplete responses if set too low. |

> **Key insight:** `temperature=0` is ideal during development and testing because it produces consistent, repeatable outputs for the same prompt.

### 2.4 Setting Up the Client and Making a Request

```python
from openai import OpenAI

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What is prompt engineering?"}],
    temperature=0
)

print(response.choices[0].message.content)
```

`model="gpt-4o-mini"` specifies which model to use, and `response.choices[0].message.content` extracts the text of the reply.

### 2.5 The `get_response()` Helper Function

To avoid rewriting the boilerplate above in every exercise, the course wraps it into a reusable function:

```python
def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content
```

```python
# Usage
response = get_response("Write a poem about ChatGPT")
print(response)
```

> This function is **pre-loaded in most course exercises**, so you typically only need to call it with a single prompt string.

### 2.6 Prompt Improvement in Action

Modifying the same request with clearer instructions changes the output dramatically:

| Prompt Version | Result |
|:---|:---|
| `"What is prompt engineering?"` | Generic, technical explanation. |
| `"Explain prompt engineering in terms that a 5-year-old can understand."` | Simple vocabulary, relatable analogies (e.g., giving clear instructions to a friend). |

This demonstrates that the *same underlying question*, refined with context and style guidance, yields a vastly better answer.

---

## 3. Key Principles of Prompt Engineering

### 3.1 Use Clear and Precise Prompts

The goal is to guide the model along the most direct and effective path to your desired answer — like giving someone the clearest walking directions rather than a vague sense of direction.

### 3.2 Use Action Verbs

Be explicit about what you want the model to *do*. Strong action verbs give the model a concrete task to execute, while ambiguous verbs leave it guessing.

| ✅ Good Action Verbs | ❌ Ambiguous Verbs to Avoid |
|:---|:---|
| `Write`, `Complete`, `Explain`, `Describe`, `Evaluate`, `Summarize`, `Generate`, `List`, `Compare`, `Translate` | `Think`, `Understand`, `Feel`, `Try`, `Know` |

**Example comparison:**

| Ineffective | Effective |
|:---|:---|
| `"Think about deforestation."` | `"Propose three strategies to reduce deforestation."` |
| `"Tell me about dogs."` | `"Describe the behavior and characteristics of Golden Retrievers, including their suitability for families."` |

### 3.3 Provide Detailed and Specific Instructions

A well-crafted prompt typically specifies several of the following dimensions:

| Dimension | Description | Example |
|:---|:---|:---|
| Context | Background or situation | `"You are helping a 10-year-old student..."` |
| Output length | How long the answer should be | `"in 2–3 sentences"` / `"in one paragraph"` |
| Format | Structure of the output | `"as a numbered list"` / `"as a table"` |
| Style | Tone or writing style | `"in the style of Shakespeare"` / `"in plain English"` |
| Audience | Who the content is for | `"for a high school student"` / `"for a senior engineer"` |

### 3.4 Controlling Output Length

There are two ways to limit how long the model's response is:

| Approach | How | Trade-off |
|:---|:---|:---|
| `max_tokens` parameter | Set in the API call | Strict hard limit, but may cut the response off mid-sentence. |
| Length instruction in the prompt | e.g., `"in no more than 3 sentences"` | Ensures complete responses, but the model can technically exceed it. |

> **Best practice:** For coherent, complete outputs, specify length limits *in the prompt itself* in addition to — or instead of — relying on `max_tokens`.

### 3.5 Use Delimiters to Separate Instructions from Input Data

When a prompt contains both instructions and raw input data (e.g., a text to summarize or complete), use **delimiters** to clearly mark where the input begins and ends. This prevents the model from confusing the two.

Common delimiter options include triple backticks (` ``` `), triple quotes (`"""`), angle brackets (`<text></text>`), square brackets (`[]`), and parentheses (`()`). The recommended structure for a well-formed prompt is: **instructions first**, then the **delimited input data last**.

```python
prompt = f"""Summarize the following text delimited by triple backticks in 2 sentences:
```{text}```"""
```

### 3.6 Use Python f-strings to Embed Variables

Instead of pasting long input text directly into the prompt string, use Python's **f-strings** to embed a pre-defined variable cleanly. This keeps the code readable and the prompt reusable.

```python
story = "It was a dark and stormy night..."

prompt = f"Complete the following story delimited by triple backticks:\n```{story}```"
response = get_response(prompt)

print("\n Original story: \n", story)
print("\n Generated story: \n", response)
```

Add `f` before the opening quote of the string, then place the variable name inside `{}` wherever its value should appear. This technique is used in virtually every exercise throughout the course.

---

## 4. Structured Outputs

By default, LLMs produce free-form text. However, many real-world applications require output in a specific, predictable format. The model will not produce structured output unless you **explicitly request it** in the prompt.

### 4.1 Tables

To generate a table, mention the word "table" explicitly and list the desired column names.

```python
prompt = "Generate a table of 10 books, with columns for Title, Author, and Year, that you should read given that you are a science fiction lover."
response = get_response(prompt)
print(response)
```

### 4.2 Lists

The model defaults to numbered lists for enumeration tasks, but you must specify the list type if you want something different.

```python
# Numbered list (default)
prompt = "Generate a list of the top 5 cities to visit."

# Unordered list (explicitly requested)
prompt = "Generate an unordered list of the top 5 cities to visit."
```

> Always state explicitly whether you want an **ordered (numbered)** or **unordered (bullet)** list.

### 4.3 Structured Paragraphs

To get output organized with headings and subheadings, ask for them directly:

```python
prompt = "Write a paragraph with clear headings and subheadings about the benefits of exercising."
```

The model will then structure its output with sections such as *Introduction*, *Physical Health Benefits*, and *Mental Health Benefits*, each with their own subheadings.

### 4.4 Custom Output Format

For fully custom formats, break the prompt into separate components — an `instructions` string, an `output_format` string, and the input data — then combine them in the final prompt.

**Exercise example — Customizing Output Format:**

```python
instructions = "Determine the language and generate a suitable title for the pre-loaded text excerpt that will be provided using triple backticks (```) delimiters."

output_format = "Include the text, language, and title, each on a separate line, using 'Text:', 'Language:', and 'Title:' as prefixes for each line."

prompt = f"{instructions}\n{output_format}\n```{text}```"
response = get_response(prompt)
print(response)
```

This approach keeps the instruction, format requirement, and input data cleanly separated, making the prompt both explicit and maintainable.

---

## 5. Conditional Prompts

### 5.1 What Are Conditional Prompts?

Conditional prompts embed **if-else logic** directly into the instructions. Rather than writing Python branching code, you describe the decision rules to the model in plain language, and it applies them to the input data. The general structure is: `"If [condition], then [action X]; otherwise, [action Y]."`

### 5.2 Single Condition

**Exercise example — Using Conditional Prompts:**

```python
instructions = """Infer the language and the number of sentences of the given delimited text;
then if the text contains more than one sentence, generate a suitable title for it,
otherwise, write 'N/A' for the title."""

output_format = """Include the text, language, number of sentences, and title, each on a separate line,
and ensure to use 'Text:', 'Language:', 'Sentences:', and 'Title:' as prefixes for each line.\n"""

prompt = instructions + output_format + f"```{text}```"
response = get_response(prompt)
print(response)
```

For a single-sentence input the model writes `Title: N/A`. For a multi-sentence input it generates an appropriate title.

### 5.3 Multiple Chained Conditions

You can nest or chain multiple conditions for more complex decision logic:

```python
prompt = f"""
If the text is written in English, check if it contains the keyword 'technology'.
  If it does, suggest a title.
  Otherwise, respond with 'keyword not found'.
If the text is not in English, respond with 'I only understand English'.
```{text}```"""
```

The resulting behavior by input scenario:

| Input Scenario | Model Response |
|:---|:---|
| English text containing `'technology'` | Suggests a title |
| English text without `'technology'` | `"keyword not found"` |
| Non-English text | `"I only understand English"` |

> **Key takeaway:** Conditional prompts enable sophisticated branching logic without writing a single Python `if` statement — the model handles all decision-making internally.

---

## 6. Practical Code Patterns

The following patterns consolidate every technique covered in this segment. Each builds on the previous one.

### Pattern 1: Multi-Role Conversation Setup

```python
from openai import OpenAI

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

conversation_messages = [
    {"role": "system",    "content": "You are a helpful event management assistant."},
    {"role": "user",      "content": "What are some good conversation starters at networking events?"},
    {"role": "assistant", "content": ""}
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=conversation_messages
)
print(response.choices[0].message.content)
```

### Pattern 2: The Reusable `get_response()` Function

```python
def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content
```

### Pattern 3: Delimited Prompt with f-string

```python
story = "It was a dark and stormy night..."

prompt = f"Complete the following story delimited by triple backticks:\n```{story}```"
response = get_response(prompt)
```

### Pattern 4: Specific and Constrained Prompt

```python
prompt = f"""Continue the following story delimited by triple backticks,
the story should only contain two paragraphs and it should follow the style of Shakespeare:
\n```{story}```"""
response = get_response(prompt)
```

### Pattern 5: Custom Format Prompt (Instructions + Format + Input)

```python
instructions = "Determine the language and generate a suitable title for the pre-loaded text excerpt that will be provided using triple backticks (```) delimiters."

output_format = "Include the text, language, and title, each on a separate line, using 'Text:', 'Language:', and 'Title:' as prefixes for each line."

prompt = f"{instructions}\n{output_format}\n```{text}```"
response = get_response(prompt)
print(response)
```

### Pattern 6: Conditional Prompt (Assembled from Parts)

```python
instructions = """Infer the language and the number of sentences of the given delimited text;
then if the text contains more than one sentence, generate a suitable title for it,
otherwise, write 'N/A' for the title."""

output_format = """Include the text, language, number of sentences, and title, each on a separate line,
and ensure to use 'Text:', 'Language:', 'Sentences:', and 'Title:' as prefixes for each line.\n"""

prompt = instructions + output_format + f"```{text}```"
response = get_response(prompt)
print(response)
```

---

## 7. Summary Cheat Sheet

### 7.1 Core Concepts at a Glance

| Concept | Key Idea |
|:---|:---|
| Prompt Engineering | Crafting precise instructions to steer LLM outputs |
| `temperature=0` | Deterministic, consistent outputs |
| `temperature=2` | Highly random, creative outputs |
| `max_tokens` | Hard limit on output length; may truncate responses |
| `system` role | Sets the model's overall behavior and persona |
| `user` role | The actual query or prompt |
| `assistant` role | The model's response; can be pre-seeded in multi-turn conversations |
| Action verbs | Use `write`, `explain`, `generate` — avoid `think`, `feel`, `try` |
| Delimiters | Separate instructions from input data (e.g., triple backticks) |
| f-strings | Embed variables into prompt strings using `f"...{variable}..."` |
| Structured output | Explicitly request tables, lists, or custom formats in the prompt |
| Conditional prompt | Embed if-else logic directly into the prompt instructions |

### 7.2 Prompt Quality Checklist

Before sending a prompt, verify each of the following:

- [ ] Uses a clear **action verb** (`write`, `explain`, `generate`, etc.)
- [ ] Includes relevant **context** or background
- [ ] Specifies the desired **output length**
- [ ] Specifies the desired **format** (table, list, paragraph, custom)
- [ ] Specifies **style or tone** if relevant (formal, simple, Shakespearean)
- [ ] Identifies the **target audience** if relevant
- [ ] Uses **delimiters** to separate instructions from input data
- [ ] States all **conditions** explicitly if branching behavior is needed

### 7.3 Common Mistakes to Avoid

| Mistake | Better Approach |
|:---|:---|
| Using vague verbs like `"think about X"` | Use `"describe X"`, `"list X"`, `"evaluate X"` |
| Overly broad questions like `"tell me about dogs"` | Specify breed, characteristics, context, and audience |
| Relying only on `max_tokens` for length control | Include length limits in the prompt text as well |
| Pasting long texts directly into the prompt string | Use Python f-strings to keep code readable |
| Not specifying output format | Explicitly state `"generate a table"`, `"use bullet points"`, etc. |
| Mixing instructions and input data without delimiters | Separate them with triple backticks or another clear delimiter |

---

*End of Revision Guide — Segment 1: Introduction to Prompt Engineering Best Practices*
