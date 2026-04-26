# Prompt Engineering with the OpenAI API
## Segment 3 — Prompt Engineering for Business Applications

*Comprehensive Revision Guide*

---

## Table of Contents

1. [Text Summarization and Expansion](#1-text-summarization-and-expansion)
2. [Text Transformation](#2-text-transformation)
3. [Text Analysis](#3-text-analysis)
4. [Code Generation and Explanation](#4-code-generation-and-explanation)
5. [Practical Code Patterns](#5-practical-code-patterns)
6. [Summary Cheat Sheet](#6-summary-cheat-sheet)

---

## 1. Text Summarization and Expansion

### 1.1 What is Text Summarization?

Text summarization condenses a longer piece of text into a shorter, coherent version while preserving its essential meaning. It is widely used across industries to streamline workflows. In finance, it speeds up decision-making by condensing lengthy reports. In marketing, it converts verbose customer feedback into actionable insights. LLMs can handle summarization tasks effectively when given well-crafted prompts.

### 1.2 The Ineffective Summarization Prompt

A naive approach — providing the text and simply asking to "summarize it" — does produce output, but it gives the model no guidance on length, format, or focus. The result is often a summary that is too long, too short, incorrectly structured, or focused on the wrong aspects. This is the baseline to improve upon.

### 1.3 Three Levers for Effective Summarization Prompts

A summarization prompt can be made significantly more effective by specifying three things: output limits, output structure, and summarization focus.

**Output Limits** constrain the length of the summary. You can express limits in sentences, words, or characters. The model will respect whichever unit you specify.

```python
# Limit by sentences
prompt = f"Summarize the {report} in maximum five sentences, while focusing on aspects related to AI and data privacy."
response = get_response(prompt)
print("Summarized report: \n", response)
```

**Output Structure** specifies the format in which the summary is returned. Instead of a free-form paragraph, you can request bullet points, numbered lists, headings, or any other structure.

```python
# Limit by bullet points
prompt = f"Summarize the {product_description} in no more than five bullet points."
response = get_response(prompt)
print("Original description: \n", product_description)
print("Summarized description: \n", response)
```

**Summarization Focus** directs the model to highlight specific aspects of the source text rather than summarizing it uniformly. This is especially useful when a document covers many topics but you only care about a subset.

```python
# Focus on specific aspects
prompt = f"Summarize the {report} in maximum five sentences, while focusing on aspects related to AI and data privacy."
```

By combining all three levers, you produce a summary that is the right length, in the right format, and covering the right content.

### 1.4 What is Text Expansion?

Text expansion is the opposite of summarization. It takes a few ideas, keywords, or bullet points and generates a longer, more complete and coherent piece of text from them. This boosts business productivity by reducing the time spent on writing tasks such as composing emails, drafting reports, or generating product descriptions from brief notes.

### 1.5 Effective Text Expansion Prompts

A well-crafted expansion prompt should specify four things: the focus areas to expand on, the desired tone, the target length, and the intended audience. The input text should be delimited so the model knows exactly what to expand.

```python
# Exercise example — Product Description Expansion
prompt = f"""Expand the {product_description}, you need to write a one paragraph comprehensive
overview capturing the key information of the product: unique features, benefits, and potential applications."""

response = get_response(prompt)
print("Original description: \n", product_description)
print("Expanded description: \n", response)
```

In the course's illustrative example, bullet points describing a company's social media services (content creation, community building, etc.) are expanded into a professional two-sentence overview of the service's features and benefits. The model produces a fluent, polished paragraph that preserves all the original facts while adding structure, tone, and readability.

### 1.6 Summarization vs. Expansion at a Glance

| Dimension | Summarization | Expansion |
|:---|:---|:---|
| Direction | Long text → Short text | Short text/bullets → Long text |
| Key prompt elements | Output limit, structure, focus | Tone, length, audience, focus areas |
| Business use cases | Report digests, review analysis, meeting notes | Email drafts, product descriptions, service overviews |

---

## 2. Text Transformation

### 2.1 What is Text Transformation?

Text transformation changes an existing piece of text to produce new text while retaining the same underlying information. The content stays the same but the form, language, or style is altered. The main applications covered in this segment are language translation, tone adjustment, and grammar and writing improvement.

### 2.2 Language Translation

When asking the model to translate text, you must specify both the source and target language in the prompt. The model can handle single-language and multi-language translation in a single request.

**Single-language translation:**

```python
prompt = f"Translate the following English product description to French:\n{product_description}"
response = get_response(prompt)
```

**Detecting an unknown language:** When the source language is unknown, ask the model to identify it first using a delimited prompt.

```python
prompt = f"What language is the following text written in?\n```{text}```"
response = get_response(prompt)
```

**Multi-language translation in one prompt:**

```python
# Exercise example — Translation for Multilingual Communication
prompt = f"""Translate text {marketing_message} from one language to multiple language.
You need to translate them in following language:
French -
Spanish -
Japanese -"""

response = get_response(prompt)
print("English:", marketing_message)
print(response)
```

The model generates all three translations in a single response, formatted with the target language as a label for each output. An important practical note from the course: LLMs are useful for initial translations but the accuracy should always be **verified before publishing customer-facing content**.

### 2.3 Tone Adjustment

Tone adjustment rewrites text to match a different communication register — for example, converting an informal promotional message into a formal and persuasive one, or making technical content accessible to a non-technical audience.

**Specifying tone directly:**

```python
# Exercise example — Tone Adjustment for Email Marketing
prompt = f"Transform the {sample_email} by changing its tone to be professional, positive, and user-centric."
response = get_response(prompt)
print("Before transformation: \n", sample_email)
print("After transformation: \n", response)
```

**Specifying target audience to drive tone:** A highly effective strategy is to specify *who* will read the transformed text. The model will adapt the vocabulary, sentence complexity, and style automatically.

```python
# Re-writing technical content for a non-technical audience
prompt = f"Re-write the following product description for a non-technical audience:\n{tech_description}"
```

### 2.4 Grammar and Writing Improvements

Text transformation also includes two distinct levels of writing quality improvement, and the prompt must clearly specify which level you want.

**Proofreading only** — corrects spelling, grammar, and punctuation without changing the structure or style of the text. Use the word "proofread" in the prompt.

```python
prompt = f"Proofread the following text for spelling, grammar, and punctuation errors:\n```{text}```"
```

**Proofreading and restructuring** — corrects errors *and* improves readability, flow, and coherence by potentially rewriting sentence structure. Both goals must be stated explicitly.

```python
prompt = f"Proofread and restructure the following text for enhanced readability, flow, and coherence:\n```{text}```"
```

### 2.5 Combining Multiple Transformations with Multi-Step Prompts

When several transformations need to be applied to the same text, a multi-step prompt chains them sequentially. Each step is numbered and performs one transformation; the model processes them in order.

**Exercise example — Writing Improvement (Multi-Step):**

```python
prompt = f"""You will transform the text delimited by triple backticks.

Step 1: Proofread the text for spelling, grammar, and punctuation errors.
Step 2: Adjust the tone to be formal and friendly.
Step 3: Preserve the original structure and meaning.

Return only the transformed text. Do not add any introduction, explanation, labels, or triple backticks.
```{text}```"""

response = get_response(prompt)
print("Before transformation:\n", text)
print("After transformation:\n", response)
```

Key observations from this pattern: the steps are numbered, each step has a single responsibility, and the final instruction — "Return only the transformed text" — suppresses unwanted preamble or explanation in the output.

---

## 3. Text Analysis

### 3.1 What is Text Analysis?

Text analysis is the process of examining text to extract relevant information and insights. The two main analysis techniques covered in this segment are text classification and entity extraction.

> **Privacy Note from the Course:** The examples use fictional customer data. Companies using real customer data for such tasks should seek legal advice to ensure compliance with applicable privacy regulations.

### 3.2 Text Classification

Text classification assigns a given text to one of several predefined categories. Sentiment analysis — categorizing text as positive, negative, or neutral — is the most common example.

**With specified categories:** The best practice is to explicitly list the allowed categories and specify the output format (e.g., one word only) to prevent the model from generating explanatory text.

```python
# Exercise example — Customer Support Ticket Routing
prompt = f"""Classify the following support ticket into one of these categories: technical issue,
billing inquiry, or product feedback. Respond with only the category name, with no additional text.

Ticket: {ticket}
Category:"""

response = get_response(prompt)
print("Ticket: ", ticket)
print("Class: ", response)
```

**With unspecified categories:** For standard tasks like sentiment analysis, the model can rely on its own knowledge even if no categories are listed. However, for more complex or domain-specific classification, always specify the categories explicitly to ensure expected and consistent outcomes.

**Assigning multiple classes:** A single text can belong to more than one category. For instance, a product review might express several emotions at once. Ask the model to identify up to a maximum number of classes rather than forcing a single label.

```python
# Classify up to three emotions from a product review
prompt = f"What emotions are expressed in this review? List up to three emotions:\n{review}"
```

### 3.3 Entity Extraction

Entity extraction identifies and pulls out specific named entities from text. Common entity types include names of people and organizations, locations, dates, product names, and technical specifications.

**With explicit entity specification:** The most reliable approach is to name the exact entities you want, and to specify the output format. This prevents the model from returning a free-form prose description of the entities.

```python
# Extracting specific product attributes
prompt = f"""From the following product description, identify and extract:
- Product name
- Display size
- Camera resolution

Format the answer as an unordered list.
{product_description}"""
```

**With few-shot prompting for complex structures:** When the entities and their relationships are too complex to describe in instructions alone (e.g., hierarchical entities with parent and sub-entities that vary per record), a few-shot prompt is the better approach. You provide two or three examples showing both the raw input and its extracted entity structure, then present the new input for the model to process.

**Exercise example — Customer Support Ticket Analysis:**

```python
prompt = f"""Here are some support tickets and their extracted entities:

Ticket 1: {ticket_1}
Entities 1: {entities_1}

Ticket 2: {ticket_2}
Entities 2: {entities_2}

Ticket 3: {ticket_3}
Entities 3: {entities_3}

Now, extract the entities from this new ticket:

Ticket 4: {ticket_4}
Entities:"""

response = get_response(prompt)
print("Ticket: \n", ticket_4)
print("Entities: \n", response)
```

The model observes the parent-child entity structure from the provided examples (e.g., `customer` → `name`, `phone`, `id` and `reservation details` → `destination`, `date`) and applies the same structure to the new ticket, including any sub-entities that were absent in the examples but present in the new data.

### 3.4 Classification vs. Entity Extraction

| Dimension | Text Classification | Entity Extraction |
|:---|:---|:---|
| Goal | Assign a label/category to the text | Extract specific named values from the text |
| Output | One or more category names | A list or structured set of named values |
| Prompt design | Specify categories, one-word output | Specify entity names, output format |
| When to use few-shot | Complex/domain-specific categories | Complex hierarchical entity structures |

---

## 4. Code Generation and Explanation

### 4.1 What is Code Generation?

Code generation uses LLMs to write code that solves a problem. It is valuable across any domain that relies on software. Because the model may make subtle errors, the course emphasizes that using LLMs for code generation requires **a solid understanding of the generated code** before it is put into production.

### 4.2 Code Generation from a Problem Description

The most direct approach is to describe the problem in natural language and specify the target programming language and the desired form of the output (function, script, class, etc.).

**Exercise example — Code Generation with Problem Description:**

```python
prompt = """write a Python function that receives a list of 12 floats representing monthly
sales data as input and, returns the month with the highest sales value as output."""

response = get_response(prompt)
print(response)
```

Key elements to include in a code generation prompt: the programming language, the input (type and meaning), the output (type and meaning), and the form of the result (function, script, or class).

### 4.3 Code Generation from Input-Output Examples

When you have example input-output pairs but cannot articulate the underlying logic in words, you can provide those examples and ask the model to infer and implement the function.

**Exercise example — Input-Output Examples for Code Generation:**

```python
examples = """input = [10, 5, 8] -> output = 23
input = [5, 2, 4] -> output = 11
input = [2, 1, 3] -> output = 6
input = [8, 4, 6] -> output = 18"""

prompt = f"You need to infer the Python function that maps the inputs to the outputs in the provided {examples}."

response = get_response(prompt)
print(response)
```

The model first identifies the pattern (e.g., that the output is the sum of the inputs multiplied by some factor, or a different formula), then provides the corresponding function and shows how it applies to the examples.

### 4.4 Code Modification

Instead of generating code from scratch, you can ask the model to modify existing code. This is useful for refactoring, adding functionality, or enforcing new requirements.

**Single modification:** Ask the model to convert a script into a callable function, rename variables, or restructure logic.

```python
prompt = f"Transform the following Python script into a function that computes the total sales:\n{script}"
```

**Multiple modifications in one prompt using multi-step:**

**Exercise example — Modifying Code with Multi-Step Prompts:**

```python
function = """def calculate_area_rectangular_floor(width, length):
    return width*length"""

prompt = f"""You are given this Python function as a string:

{function}

Modify the function so that it:
1. Calculates the area of a rectangular floor.
2. Calculates the perimeter of the rectangular floor.
3. Checks whether width and length are positive numbers.
4. If width or length is zero or negative, return a clear error message.
5. If both inputs are positive, return both the area and perimeter.

Return only the corrected Python function code."""

response = get_response(prompt)
print(response)
```

The instruction "Return only the corrected Python function code" is important — it suppresses the model's tendency to add explanatory prose around the code.

### 4.5 Code Explanation

LLMs can explain unfamiliar or complex code in human-readable terms. The explanation depth depends on how you frame the prompt.

**High-level explanation** (one sentence): Ask for a brief one-sentence summary. The result is a top-level description of what the function does, without details about how.

```python
prompt = f"Explain what the following Python function does in one sentence:\n{function}"
```

**Detailed step-by-step explanation** using chain-of-thought prompting: Ask the model to think step by step and break down each part of the code.

**Exercise example — Explaining Code Step by Step:**

```python
prompt = f"""You are given the following Python function:
{function}
Explain what this function does in step by step.
Break down each part of the code and describe its purpose clearly."""

response = get_response(prompt)
print(response)
```

The model processes the code in chunks — starting with the function definition, moving through the computation logic, and ending with the return value — before providing a final summary of the function's overall purpose. This approach is directly analogous to chain-of-thought prompting applied to code.

### 4.6 Code Task Summary

| Task | Prompt Approach | Key Prompt Elements |
|:---|:---|:---|
| Generate from scratch | Problem description | Language, input type, output type, form (function/script) |
| Generate from examples | Input-output pairs | Show pairs clearly; ask model to infer the function |
| Modify existing code | Multi-step prompt | Number each modification; specify return format |
| Explain briefly | Direct instruction | Specify "one sentence" or "high-level" |
| Explain in detail | Chain-of-thought | "Step by step", "break down each part" |

---

## 5. Practical Code Patterns

### Pattern 1: Focused Summarization with Length Limit

```python
# Summarize a report with a sentence limit and topic focus
prompt = f"Summarize the {report} in maximum five sentences, while focusing on aspects related to AI and data privacy."
response = get_response(prompt)
print("Summarized report: \n", response)
```

### Pattern 2: Bullet-Point Summarization

```python
# Summarize a product description as bullet points
prompt = f"Summarize the {product_description} in no more than five bullet points."
response = get_response(prompt)
print("Original description: \n", product_description)
print("Summarized description: \n", response)
```

### Pattern 3: Text Expansion to a Comprehensive Paragraph

```python
# Expand a short product description into a full narrative
prompt = f"""Expand the {product_description}, you need to write a one paragraph comprehensive
overview capturing the key information of the product: unique features, benefits, and potential applications."""
response = get_response(prompt)
print("Original description: \n", product_description)
print("Expanded description: \n", response)
```

### Pattern 4: Multi-Language Translation

```python
# Translate a marketing message into three languages simultaneously
prompt = f"""Translate text {marketing_message} from one language to multiple language.
You need to translate them in following language:
French -
Spanish -
Japanese -"""
response = get_response(prompt)
print("English:", marketing_message)
print(response)
```

### Pattern 5: Tone Adjustment

```python
# Change the tone of a marketing email
prompt = f"Transform the {sample_email} by changing its tone to be professional, positive, and user-centric."
response = get_response(prompt)
print("Before transformation: \n", sample_email)
print("After transformation: \n", response)
```

### Pattern 6: Multi-Step Writing Improvement

```python
# Proofread, adjust tone, and preserve structure in one prompt
prompt = f"""You will transform the text delimited by triple backticks.

Step 1: Proofread the text for spelling, grammar, and punctuation errors.
Step 2: Adjust the tone to be formal and friendly.
Step 3: Preserve the original structure and meaning.

Return only the transformed text. Do not add any introduction, explanation, labels, or triple backticks.
```{text}```"""
response = get_response(prompt)
print("Before transformation:\n", text)
print("After transformation:\n", response)
```

### Pattern 7: Text Classification with Specified Categories

```python
# Classify a customer support ticket into one of three categories
prompt = f"""Classify the following support ticket into one of these categories: technical issue,
billing inquiry, or product feedback. Respond with only the category name, with no additional text.

Ticket: {ticket}
Category:"""
response = get_response(prompt)
print("Ticket: ", ticket)
print("Class: ", response)
```

### Pattern 8: Few-Shot Entity Extraction

```python
# Extract entities from a new ticket using three labeled examples
prompt = f"""Here are some support tickets and their extracted entities:

Ticket 1: {ticket_1}
Entities 1: {entities_1}

Ticket 2: {ticket_2}
Entities 2: {entities_2}

Ticket 3: {ticket_3}
Entities 3: {entities_3}

Now, extract the entities from this new ticket:

Ticket 4: {ticket_4}
Entities:"""
response = get_response(prompt)
print("Ticket: \n", ticket_4)
print("Entities: \n", response)
```

### Pattern 9: Code Generation from Problem Description

```python
# Ask the model to write a Python function from a problem description
prompt = """write a Python function that receives a list of 12 floats representing monthly
sales data as input and, returns the month with the highest sales value as output."""
response = get_response(prompt)
print(response)
```

### Pattern 10: Code Generation from Input-Output Examples

```python
# Ask the model to infer and implement a function from input-output examples
examples = """input = [10, 5, 8] -> output = 23
input = [5, 2, 4] -> output = 11
input = [2, 1, 3] -> output = 6
input = [8, 4, 6] -> output = 18"""

prompt = f"You need to infer the Python function that maps the inputs to the outputs in the provided {examples}."
response = get_response(prompt)
print(response)
```

### Pattern 11: Multi-Step Code Modification

```python
# Modify an existing function with multiple numbered requirements
function = """def calculate_area_rectangular_floor(width, length):
    return width*length"""

prompt = f"""You are given this Python function as a string:

{function}

Modify the function so that it:
1. Calculates the area of a rectangular floor.
2. Calculates the perimeter of the rectangular floor.
3. Checks whether width and length are positive numbers.
4. If width or length is zero or negative, return a clear error message.
5. If both inputs are positive, return both the area and perimeter.

Return only the corrected Python function code."""
response = get_response(prompt)
print(response)
```

### Pattern 12: Chain-of-Thought Code Explanation

```python
# Explain a function step by step using chain-of-thought prompting
prompt = f"""You are given the following Python function:
{function}
Explain what this function does in step by step.
Break down each part of the code and describe its purpose clearly."""
response = get_response(prompt)
print(response)
```

---

## 6. Summary Cheat Sheet

### 6.1 Business Application Reference

| Application | What It Does | Core Prompt Technique |
|:---|:---|:---|
| Summarization | Condenses long text to key points | Specify length limit, structure, and focus |
| Expansion | Grows short text into full content | Specify tone, length, audience, focus areas |
| Translation | Converts text between languages | Specify source and target languages; can do multi-language at once |
| Tone adjustment | Changes register or style of text | Specify target tone and/or target audience |
| Proofreading | Fixes grammar/spelling errors only | Use "proofread" without restructuring instruction |
| Writing improvement | Fixes errors and improves structure | Use "proofread and restructure" |
| Multiple transformations | Applies several changes sequentially | Multi-step prompt with numbered steps |
| Classification | Assigns labels to text | Specify categories and output format; use few-shot for complex cases |
| Entity extraction | Extracts named values from text | Specify entity names and output format; use few-shot for complex structures |
| Code generation | Writes code from a description | Include language, input/output types, desired form |
| Code from examples | Infers and implements from I/O pairs | Provide examples clearly; ask model to infer the function |
| Code modification | Edits existing code to new requirements | Multi-step prompt; specify return format |
| Code explanation | Explains what code does | One sentence for high-level; chain-of-thought for detailed |

### 6.2 Prompt Design Checklist by Application

**For summarization:**
- [ ] Length limit specified (sentences / words / bullet points)?
- [ ] Output structure specified (paragraph / bullets / numbered list)?
- [ ] Specific focus area mentioned if relevant?

**For expansion:**
- [ ] Key focus areas to include stated?
- [ ] Desired tone specified (professional, casual, persuasive)?
- [ ] Target length defined?
- [ ] Intended audience identified?

**For translation:**
- [ ] Source and target language(s) both specified?
- [ ] All target languages listed if doing multi-language output?
- [ ] Reminder to verify accuracy for customer-facing content?

**For text classification:**
- [ ] All allowed categories explicitly listed?
- [ ] Output format specified (e.g., "one word only", "respond with only the category name")?
- [ ] Few-shot examples included for complex or domain-specific categories?

**For entity extraction:**
- [ ] All entity names to extract explicitly listed?
- [ ] Output format specified (unordered list, JSON, labeled lines)?
- [ ] Few-shot examples provided for hierarchical or variable entity structures?

**For code generation:**
- [ ] Target programming language stated?
- [ ] Input type and meaning described?
- [ ] Output type and meaning described?
- [ ] Desired code form stated (function / script / class)?
- [ ] "Return only the code" included to suppress prose output?

**For code explanation:**
- [ ] Level of detail specified (one sentence vs. step by step)?
- [ ] Chain-of-thought instruction added for detailed breakdowns?

### 6.3 Common Mistakes to Avoid

| Mistake | Better Approach |
|:---|:---|
| Asking to "summarize" without any constraints | Specify length, format, and focus in every summarization prompt |
| Asking to "expand" without tone or length guidance | Include tone, target length, audience, and key areas to cover |
| Translating without specifying languages | Always name both source and target language(s) explicitly |
| Changing tone without specifying target audience or register | State the target tone and/or audience clearly |
| Asking to "proofread" when structural improvement is needed | Distinguish between "proofread" and "proofread and restructure" |
| Mixing multiple transformations in a single vague instruction | Use multi-step prompts with numbered, single-responsibility steps |
| Classifying without naming the allowed categories | Always list the categories and specify a clean one-word output format |
| Trying to describe a complex entity structure in instructions alone | Use few-shot examples to demonstrate the expected entity format |
| Not specifying code language or form | Include language, input, output, and desired form (function/script/class) |
| Expecting only clean code back from the model | Add "Return only the code" to suppress explanatory prose |

---

*End of Revision Guide — Segment 3: Prompt Engineering for Business Applications*
