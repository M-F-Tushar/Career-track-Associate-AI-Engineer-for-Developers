# Comprehensive Study Guide: Working with the OpenAI API — Segment 2: Prompting OpenAI Models

---

## 1. Overview of What Chat Completion Models Can Do

Beyond simple question answering, OpenAI's chat completion models can perform a wide range of tasks:

- **Text Editing** — updating, modifying, or transforming existing text
- **Text Summarization** — condensing long content into key points
- **Text Generation** — creating brand-new content from scratch
- **Classification & Sentiment Analysis** — categorizing text or scoring opinions
- **Data Extraction** — pulling specific information from unstructured text

---

## 2. Text Editing

### 2.1 What Is It?
Text editing uses a chat model to **modify, update, or rewrite** existing text based on instructions. This is far more flexible than traditional find-and-replace tools, which can only swap exact words or phrases.

### 2.2 Prompt Structure for Text Editing
A well-structured text editing prompt follows this pattern:
1. **Start with the instruction** (e.g., "Replace car with plane and adjust phrase:")
2. **Follow with the text to edit**

### 2.3 Multi-line Prompts with Triple Quotes
For longer prompts, use **triple quotes** (`"""`) to define multi-line strings, which improves readability and processing:

```python
prompt = """Replace car with plane and adjust phrase:
A car is a vehicle that is typically powered by an internal combustion engine or an
electric motor. It has four wheels, and is designed to carry passengers and/or cargo
on roads or highways. Cars have become a ubiquitous part of modern society, and are
used for a wide variety of purposes, such as commuting, travel, and transportation
of goods. Cars are often associated with freedom, independence, and mobility."""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    max_completion_tokens=100,
    messages=[{"role": "user", "content": prompt}]
)
print(response.choices[0].message.content)
```

> **Key advantage:** Unlike find-and-replace, this approach allows the model to contextually update the text — not just swap individual words, but adjust the entire meaning appropriately.

---

## 3. Text Summarization

### 3.1 What Is It?
Text summarization condenses long text into concise key points. This is highly valuable in business contexts such as:
- Summarizing customer support chats
- Condensing reports into one-pagers or bullet points
- Extracting next steps and timelines for stakeholders

### 3.2 Using F-strings to Insert Variables into Prompts
**F-strings** allow you to dynamically insert Python variables into a prompt string. They are denoted with an `f` before the opening quotation marks, and variables are placed inside `{}` curly braces:

```python
# finance_text is a pre-defined string variable
prompt = f"""Summarize the following text into two concise bullet points:
{finance_text}"""
```

This is equivalent to: *"Convert the Python variable to a string and insert it into the prompt in one step."*

### 3.3 Full Summarization Example

```python
prompt = f"""Summarize the following text into two concise bullet points:
{finance_text}"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    max_completion_tokens=400
)
print(finance_text)
print(response.choices[0].message.content)
```

---

## 4. Controlling Response Length: `max_completion_tokens`

### 4.1 What Are Tokens?
- **Tokens** are units of one or more characters that language models use to understand and interpret text.
- A single word can be one or more tokens. Short common words are often a single token; longer or uncommon words may be split into multiple tokens.
- Both **input** (your prompt) and **output** (the model's reply) are measured in tokens.
- You can explore tokenization at: [https://platform.openai.com/tokenizer](https://platform.openai.com/tokenizer)

### 4.2 The `max_completion_tokens` Parameter
- By default, the API limits response length.
- `max_completion_tokens` sets the **upper limit** on how many tokens the model will output.
- You can use it to make responses **shorter** (reduce cost, enforce brevity) or **longer** (allow more detailed answers).

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    max_completion_tokens=500  # Upper limit on response length
)
```

> **Important:** This is a ceiling, not a guaranteed length. The model may produce fewer tokens if it finishes sooner.

---

## 5. Calculating API Cost

### 5.1 How Pricing Works
- The OpenAI API charges based on:
  - The **model** used
  - The **number of input tokens** (your prompt)
  - The **number of output tokens** (the model's response)
- Pricing is expressed as a **cost per million tokens**, so you divide by 1,000,000 to get cost per token.
- Input and output tokens may have **different prices**.

> **Always estimate costs before deploying AI features at scale.**

### 5.2 Accessing Token Usage from the Response
The number of input tokens used is available in the API response:

```python
input_tokens = response.usage.prompt_tokens
```

For output tokens, use `max_completion_tokens` as an **upper bound estimate**.

### 5.3 Cost Calculation Formula

```python
# Price per token (example: gpt-4o-mini)
input_token_price = 0.15 / 1_000_000   # $0.15 per million input tokens
output_token_price = 0.6 / 1_000_000   # $0.60 per million output tokens

# Token counts
input_tokens = response.usage.prompt_tokens
output_tokens = max_completion_tokens   # Use as upper bound

# Total cost
cost = (input_tokens * input_token_price) + (output_tokens * output_token_price)
print(f"Estimated cost: ${cost}")
```

> **Note:** For a small request with 500 max output tokens, the cost is typically around a tenth of a cent — but costs add up quickly for longer documents or larger-scale deployments.

---

## 6. Text Generation

### 6.1 How Does a Model Generate Text?
When a prompt is sent to a chat model, it returns the text it believes **most likely completes the prompt**, based on its training data. For example, sending *"Life is like a box of chocolates"* will likely return the correct quote completion.

> **Non-determinism:** Model outputs are **non-deterministic** — the exact same prompt can produce slightly different outputs on different runs.

### 6.2 Controlling Randomness: The `temperature` Parameter

| Value | Behavior |
|---|---|
| `0` | Almost entirely deterministic — consistent, predictable output |
| `1` (default) | Balanced randomness |
| `2` | Highly random and creative output |

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0,    # Most deterministic
    max_completion_tokens=150
)
```

**When to use lower temperature:**
- Customer service chatbots (consistent answers)
- Data extraction tasks
- Classification problems

**When to use higher temperature:**
- Creative writing
- Brainstorming / idea generation
- Marketing copy experimentation

### 6.3 Text Generation Use Cases

#### Marketing — Generating Taglines
```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Create a catchy slogan for a new restaurant"}],
    max_completion_tokens=100
)
print(response.choices[0].message.content)
```

> Tip: Experiment with different cuisine types (Italian, Chinese) or restaurant styles (fine-dining, fast-food) to see how the response changes.

#### Product Descriptions
A well-crafted product description prompt should include:
1. **Product features** (listed clearly)
2. **Desired tone** (e.g., professional, engaging)
3. **Target audience** (e.g., fitness enthusiasts, busy professionals)

```python
prompt = """Write a persuasive product description for SonicPro headphones.
Highlight the following features:
- Active Noise Cancellation (ANC) for immersive listening
- 40-hour long-lasting battery life
- Foldable and portable design for convenience
Use a professional marketing tone.
Make it engaging, benefit-focused, and appealing to modern consumers."""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    max_completion_tokens=150,
    temperature=0.9   # Higher creativity for marketing
)
print(response.choices[0].message.content)
```

> **Iteration tip:** If the output isn't satisfactory, update the original prompt with more specific information and re-run the request.

---

## 7. Shot Prompting

### 7.1 What is Shot Prompting?
**Shot prompting** is the technique of **including examples in a prompt** to guide the model's response. The number of examples provided determines the "shot" type.

### 7.2 The Three Types of Shot Prompting

| Type | Examples Provided | Description |
|---|---|---|
| **Zero-shot** | 0 | Just an instruction, no examples |
| **One-shot** | 1 | One example to guide the format/style |
| **Few-shot** | 2+ | Multiple examples for better consistency |

### 7.3 Why Does Shot Prompting Matter?
Adding examples dramatically improves AI performance for tasks like:
- **Classification** — sorting text into defined categories
- **Sentiment analysis** — identifying opinions or emotions
- **Data extraction** — pulling specific information from unstructured text
- **Any structured output task** where format consistency matters

---

### 7.4 Zero-Shot Prompting Example

```python
prompt = """Classify the sentiment of each review from 5 (very good) to 1 (very negative):
1. Unbelievably good!
2. Shoes fell apart on the second use.
3. The shoes look nice, but they aren't very comfortable.
4. Can't wait to show them off!"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    max_completion_tokens=100
)
print(response.choices[0].message.content)
```

**Observed problem:** The model may assign scores correctly but **append extra text** (e.g., "3 - Neutral") that wasn't requested, because it has no example of the expected output format.

---

### 7.5 One-Shot Prompting Example

Add one example before the items to classify, and use formatting cues (like `=`) to indicate the expected output format:

```python
prompt = """Classify sentiment as 1-5 (negative to positive):
1. Love these! = 5
2. Unbelievably good! =
3. Shoes fell apart on the second use. =
4. The shoes look nice, but they aren't very comfortable. =
5. Can't wait to show them off! ="""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    max_completion_tokens=100
)
print(response.choices[0].message.content)
```

**Improvement:** Formatting is now followed precisely. The model also adjusts scores based on the extra context the example provides.

---

### 7.6 Few-Shot Prompting Example

Add two or more examples for even greater consistency and accuracy:

```python
prompt = """Classify sentiment as 1-5 (negative to positive):
1. Comfortable, but not very pretty = 2
2. Love these! = 5
3. Unbelievably good! =
4. Shoes fell apart on the second use. =
5. The shoes look nice, but they aren't very comfortable. =
6. Can't wait to show them off! ="""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    max_completion_tokens=100
)
print(response.choices[0].message.content)
```

**Result:** Formatting is fully consistent, and scores become more nuanced and reasonable. Adding a **moderate example** (like score = 2) helps the model better calibrate middle-range scores.

> **Experiment:** Try 4, 5, or even 10 examples to observe increasing consistency.

---

### 7.7 Shot Prompting for General Categorization

Shot prompting works for **any categorization**, not just sentiment. Example — categorizing animals by habitat (land / sea / both):

**Zero-shot problem:** Without examples, the model may:
- Add unwanted reasoning
- Produce incorrect results (e.g., classifying salmon as "Both" by confusing freshwater/saltwater with land/sea)

**Few-shot fix:**
```python
prompt = """Categorize each animal as Land, Sea, or Both:
Zebra = Land
Crocodile = Both
Salmon =
Eagle =
Dolphin ="""
```

**Result:** With two examples (zebra and crocodile) and equals signs to define the format, the output becomes perfectly consistent and the spurious result is corrected.

---

## 8. Exercise Walkthroughs

### Exercise 1: Find and Replace (Text Editing)
- **Task:** Use a chat model to replace "car" with "plane" and update the text accordingly.
- **Key skills:** Multi-line prompts with triple quotes, passing prompt as a variable.

```python
prompt = """Replace car with plane and adjust phrase:
A car is a vehicle that is typically powered by an internal combustion engine or an
electric motor..."""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    max_completion_tokens=100,
    messages=[{"role": "user", "content": prompt}]
)
print(response.choices[0].message.content)
```

> **Warning from exercise:** If you send many requests or use many tokens in a short period, you may hit a **rate limit** (`openai.error.RateLimitError`). Wait a minute for the quota to reset before retrying.

---

### Exercise 2: Text Summarization
- **Task:** Summarize a passage about financial investment (`finance_text`) into two concise bullet points.
- **Key skills:** F-string prompt construction, `max_completion_tokens`.

```python
prompt = f"""Summarize the following text into two concise bullet points:
{finance_text}"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    max_completion_tokens=400
)
print(finance_text)
print(response.choices[0].message.content)
```

---

### Exercise 3: Calculating the Cost
- **Task:** Calculate the estimated cost of summarizing customer chat transcripts.
- **Key skills:** Accessing `response.usage.prompt_tokens`, cost formula.

```python
input_token_price = 0.15 / 1_000_000
output_token_price = 0.6 / 1_000_000

# Extract token usage
input_tokens = response.usage.prompt_tokens
output_tokens = max_completion_tokens

# Calculate cost
cost = (input_tokens * input_token_price) + (output_tokens * output_token_price)
print(f"Estimated cost: ${cost}")
```

---

### Exercise 4: Content Generation (Restaurant Slogan)
- **Task:** Generate a catchy slogan for a new restaurant.
- **Key skills:** Simple content generation prompt, `max_completion_tokens`.

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Create a catchy slogan for a new restaurant"}],
    max_completion_tokens=100
)
print(response.choices[0].message.content)
```

> Encourage experimenting: change cuisine type (Italian, Chinese) or restaurant type (fine-dining, fast-food) and observe the change in output.

---

### Exercise 5: Generating a Product Description (SonicPro Headphones)
- **Task:** Create a persuasive product description using a detailed, structured prompt.
- **Key skills:** Detailed prompt structure (features + tone + audience), experimenting with `temperature` and `max_completion_tokens`.

```python
prompt = """Write a persuasive product description for SonicPro headphones.
Highlight the following features:
- Active Noise Cancellation (ANC) for immersive listening
- 40-hour long-lasting battery life
- Foldable and portable design for convenience
Use a professional marketing tone.
Make it engaging, benefit-focused, and appealing to modern consumers."""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    max_completion_tokens=150,
    temperature=0.9
)
print(response.choices[0].message.content)
```

---

### Exercise 6: Zero-Shot Prompting with Reviews
- **Task:** Classify sentiment of shoe store reviews (scale 1–5) using zero-shot prompting.
- **Key skills:** Zero-shot classification prompt, multi-line string.

```python
prompt = """Classify the sentiment of each review from 5 (very good) to 1 (very negative):
1. Unbelievably good!
2. Shoes fell apart on the second use.
3. The shoes look nice, but they aren't very comfortable.
4. Can't wait to show them off!"""
```

---

### Exercise 7: One-Shot Prompting
- **Task:** Improve the zero-shot prompt by adding one example (`Love these! = 5`) and `=` signs after each review.
- **Goal:** Achieve more consistent formatting and more accurate scores.

```python
prompt = """Classify sentiment as 1-5 (negative to positive):
1. Love these! = 5
2. Unbelievably good! =
3. Shoes fell apart on the second use. =
4. The shoes look nice, but they aren't very comfortable. =
5. Can't wait to show them off! ="""
```

---

### Exercise 8: Few-Shot Prompting
- **Task:** Add the example `Comfortable, but not very pretty = 2` to the prompt to handle moderate reviews better.
- **Goal:** Achieve full formatting consistency and more accurate middle-range scores.

```python
prompt = """Classify sentiment as 1-5 (negative to positive):
1. Comfortable, but not very pretty = 2
2. Love these! = 5
3. Unbelievably good! =
4. Shoes fell apart on the second use. =
5. The shoes look nice, but they aren't very comfortable. =
6. Can't wait to show them off! ="""
```

---

## 9. Key Parameters Summary

| Parameter | Purpose | Default | Range/Notes |
|---|---|---|---|
| `model` | Selects which AI model to use | — | e.g., `"gpt-4o-mini"` |
| `messages` | List of role/content dicts | — | Required |
| `max_completion_tokens` | Limits output length | API default | Higher = longer, costlier |
| `temperature` | Controls randomness | `1` | `0` (deterministic) to `2` (random) |

---

## 10. Key Concepts Summary

| Concept | Summary |
|---|---|
| Text editing | Instruct model to transform existing text — far more flexible than find-and-replace |
| Text summarization | Use f-strings to insert text variables into prompts for dynamic summarization |
| Tokens | Units of text used for processing; both input and output are measured in tokens |
| `max_completion_tokens` | Upper bound on model output length; directly affects cost |
| Cost calculation | `(input_tokens × input_price) + (output_tokens × output_price)` |
| `response.usage.prompt_tokens` | Where to find the number of input tokens used |
| Non-determinism | Same prompt may produce slightly different results each run |
| `temperature` | Lower = consistent; higher = creative/random |
| Zero-shot prompting | No examples given — model relies only on the instruction |
| One-shot prompting | One example given — improves output format consistency |
| Few-shot prompting | Multiple examples — maximizes consistency and accuracy |
| F-strings | Python technique to insert variables into strings using `f"...{variable}..."` |
| Triple quotes | Used for multi-line prompts: `"""..."""` |

---

## 11. Practical Tips & Best Practices

- **Be clear and detailed in your prompts** — vague instructions lead to vague outputs.
- **Structure product/generation prompts** with features first, then tone and audience.
- **Use `=` signs or arrows** in prompts to signal expected output format to the model.
- **Add a moderate example** in few-shot prompts (not just extremes) to help the model handle middle-range cases.
- **Always estimate costs** before scaling — small per-request costs multiply rapidly.
- **Watch for rate limits** — if you send too many requests too quickly, you'll hit `openai.error.RateLimitError`. Wait a moment before retrying.
- **Iterate on prompts** — if the output isn't right, add more specific instructions or more examples and re-run.

---
