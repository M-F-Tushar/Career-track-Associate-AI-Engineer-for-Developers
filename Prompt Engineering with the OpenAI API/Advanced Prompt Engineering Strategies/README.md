# Prompt Engineering with the OpenAI API
## Segment 2 — Advanced Prompt Engineering Strategies

*Comprehensive Revision Guide*

---

## Table of Contents

1. [Few-Shot Prompting](#1-few-shot-prompting)
2. [Multi-Step Prompting](#2-multi-step-prompting)
3. [Chain-of-Thought and Self-Consistency Prompting](#3-chain-of-thought-and-self-consistency-prompting)
4. [Iterative Prompt Engineering and Refinement](#4-iterative-prompt-engineering-and-refinement)
5. [Comparing All Advanced Techniques](#5-comparing-all-advanced-techniques)
6. [Practical Code Patterns](#6-practical-code-patterns)
7. [Summary Cheat Sheet](#7-summary-cheat-sheet)

---

## 1. Few-Shot Prompting

### 1.1 What is Few-Shot Prompting?

Few-shot prompting is a technique that involves including **example question-answer pairs** directly inside the prompt. The model reads these examples, learns the expected format or reasoning style from them, and then applies that learning to answer the new question you provide.

The workflow is: craft a prompt with examples → feed it to the model → receive an answer that follows the demonstrated pattern.

### 1.2 The Three Variants: Zero, One, and Few

The name of the technique changes depending on how many examples you provide:

| Variant | Examples Provided | Best For |
|:---|:---|:---|
| **Zero-shot** | 0 | Quick, simple tasks where no specific format is needed |
| **One-shot** | 1 | Teaching a specific output format or style consistently |
| **Few-shot** | 2 or more | Complex tasks requiring more context, such as multi-class classification |

**Zero-shot prompting** is the simplest approach. The model responds entirely from its pre-trained knowledge with no demonstrations. It is ideal when the task is straightforward and no particular structure is required.

```python
# Zero-shot example — no examples given
prompt = "Define prompt engineering."
response = get_response(prompt)
print(response)
```

**One-shot prompting** provides a single example to teach the model a format or convention. The model will apply that exact structure to the new question.

```python
# One-shot example — teaching a specific output format for summing numbers
prompt = """Q: What is three plus five plus six?
A: The sum of 3, 5, and 6 is 14.
Q: What is two plus nine plus one?
A:"""
response = get_response(prompt)
print(response)
```

The model will reply in the sentence format shown in the example: *"The sum of X, Y, and Z is N."*

**Few-shot prompting** provides two or more examples, which is especially powerful for classification tasks where multiple categories need to be demonstrated.

```python
# Few-shot example — sentiment classification
prompt = """Text: "I loved the product!" -> Sentiment: Positive
Text: "This is the worst purchase I ever made." -> Sentiment: Negative
Text: "It works as expected." -> Sentiment:"""
response = get_response(prompt)
print(response)
```

### 1.3 Few-Shot Prompting via the Chat API (Conversation Format)

When using the `chat.completions` endpoint, examples can be supplied as simulated prior conversations by alternating `user` and `assistant` messages. Each user message is the input text, and each assistant message is the expected classification or answer.

**Exercise example — Sentiment Analysis with Few-Shot Prompting:**

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        # Example 1
        {"role": "user",      "content": "The product quality exceeded my expectations"},
        {"role": "assistant", "content": "1"},
        # Example 2
        {"role": "user",      "content": "I had a terrible experience with this product's customer service"},
        {"role": "assistant", "content": "-1"},
        # New input to classify
        {"role": "user",      "content": "The price of the product is really fair given its features."}
    ],
    temperature=0
)
```

The model sees the two examples as a conversation it has already had, infers the pattern (positive → `1`, negative → `-1`), and classifies the new text accordingly.

### 1.4 One-Shot Prompting to Control Output Structure

One-shot prompting is not limited to content — it is highly effective for enforcing a precise output *structure*. The model mirrors whatever format the example demonstrates.

**Exercise example — Controlling Output Structure:**

```python
# Teaching the model to extract odd numbers and present them inside brackets
prompt = ("Q: Extract the odd numbers from the set {1, 3, 7, 12, 19}\n"
          "A: {1, 3, 7, 19}\n"
          "Q: Extract the odd numbers from the set {3, 5, 11, 12, 16}\n"
          "A:")
response = get_response(prompt)
print(response)
```

The model follows the `{...}` bracket format demonstrated in the example.

### 1.5 Choosing the Right Number of Examples

The number of examples should be proportional to the complexity of the task:

- **Simple tasks** (e.g., enforcing output format, basic extraction) → 1 example is sufficient.
- **Complex tasks** (e.g., multi-class text classification) → provide at least one example per class to ensure the model can distinguish between all categories.

For classification with multiple classes, if you omit a class from the examples, the model may never predict that class or may mis-assign inputs that belong to it.

---

## 2. Multi-Step Prompting

### 2.1 What is Multi-Step Prompting?

Multi-step prompting is a technique that **breaks a complex goal into a numbered sequence of explicit sub-tasks** and places all of those steps directly inside a single prompt. Rather than asking the model to do everything at once, you act as a project manager providing a step-by-step roadmap — like a treasure map that guides the model to the desired outcome through a sequence of clear directions.

This approach is beneficial for two categories of tasks:

- **Sequential tasks**, such as generating coherent long-form content from an outline, where the order of operations matters.
- **Cognitive/analytical tasks**, such as reviewing code for correctness, where breaking the problem into defined criteria leads to more thorough and accurate evaluation.

### 2.2 Single-Step vs. Multi-Step: A Concrete Comparison

**Single-step prompt — Planning a Beach Vacation:**

```python
# Vague; the model decides what to include
prompt = "Help me plan a beach vacation."
response = get_response(prompt)
print(response)
```

The output is generic because the model has no guidance on what aspects to cover or in what depth.

**Multi-step prompt — Planning a Beach Vacation:**

```python
# Structured; the model follows a defined plan
prompt = """Make a detailed plan for a beach vacation by following these steps:
Step 1: Identify four potential beach vacation locations.
Step 2: For each location, list several accommodation options and possible activities.
Step 3: For each location, provide an evaluation of the pros and cons."""
response = get_response(prompt)
print(response)
```

The output is now structured, comprehensive, and directly matches the required deliverable.

### 2.3 Multi-Step Prompting for Code Analysis

Multi-step prompting is especially powerful for analytical tasks where a single "yes/no" verdict is not useful. By spelling out specific criteria as numbered steps, you get targeted, actionable feedback.

**Exercise example — Analyze Solution Correctness:**

```python
code = '''
def calculate_rectangle_area(length, width):
    area = length * width
    return area
'''

prompt = f"""Assess the function provided in the delimited code string according to three criteria:
Step - 1: correct syntax
Step - 2: receiving two inputs
Step - 3: returning one output
```{code}```"""

response = get_response(prompt)
print(response)
```

A single-step prompt asking "Is this code correct?" only returns a vague "yes." The multi-step version forces the model to evaluate each criterion individually, exposing specific issues such as a missing division-by-zero check — details a simple yes/no would miss.

### 2.4 Multi-Step vs. Few-Shot: Key Distinction

These two techniques are often confused but serve fundamentally different purposes:

| Dimension | Multi-Step Prompting | Few-Shot Prompting |
|:---|:---|:---|
| Mechanism | Explicit numbered **instructions** inside the prompt | **Examples** of question-answer pairs inside the prompt |
| Role | Acts as a roadmap — tells the model *what to do* | Acts as a demonstration — *shows* the model how to respond |
| Model learns from | Direct commands | Observed input-output patterns |
| Best for | Sequential tasks, analytical tasks, structured generation | Format enforcement, classification, style mimicry |

---

## 3. Chain-of-Thought and Self-Consistency Prompting

### 3.1 What is Chain-of-Thought Prompting?

Chain-of-thought (CoT) prompting instructs the model to **show its intermediate reasoning steps** before arriving at a final answer. Rather than jumping straight to a conclusion, the model works through the problem aloud, step by step. This is especially valuable for complex reasoning tasks — math problems, logic puzzles, multi-step deductions — because it reduces errors by forcing the model to process each step sequentially.

A standard prompt for a math problem returns just a number, which you cannot verify without seeing the work. A chain-of-thought prompt returns the full derivation, making it easy to check and trust the answer.

### 3.2 Standard Prompt vs. Chain-of-Thought Prompt

**Standard prompt (no reasoning visible):**

```python
prompt = """A person starts with 20 books. They lend 5, buy 3, and give away 2.
How many books do they have?"""
response = get_response(prompt)
# Returns: "16" — but how did it get there?
```

**Chain-of-thought prompt (reasoning made explicit):**

```python
# Exercise example — Reasoning with Chain-of-Thought Prompts
prompt = """Determine my friend's father's age in 10 years.
My friend is 20 years old. His father is currently twice my friend's age.
Show your reasoning step by step and give the final answer."""
response = get_response(prompt)
print(response)
```

The model produces a sequence of labeled steps: *"Step 1: Friend's current age = 20. Step 2: Father's current age = 40. Step 3: Father's age in 10 years = 50."* This makes the reasoning transparent and auditable.

### 3.3 Chain-of-Thought via Few-Shot Examples (One-Shot CoT)

Instead of instructing the model to reason step-by-step, you can *demonstrate* the reasoning style through a one-shot example. The model observes the structure of the example answer and mirrors it when answering the new question.

**Exercise example — One-Shot Chain-of-Thought Prompts:**

```python
# Define the example that demonstrates step-by-step reasoning
example = """Q: Sum the even numbers in the following set: {9, 10, 13, 4, 2}.
             A: Even numbers: {10, 4, 2}. Adding them: 10+4+2=16"""

# Define the new question (with "A:" left blank for the model to complete)
question = """Q: Sum the even numbers in the following set: {15, 13, 82, 7, 14}
              A:"""

# Combine into the final prompt
prompt = f"""{example}

{question}"""

response = get_response(prompt)
print(response)
```

The model follows the demonstrated logic: first identify the target numbers, then show the addition, then give the final sum.

### 3.4 Chain-of-Thought vs. Multi-Step: Key Distinction

These two techniques are related but operate differently:

| Dimension | Multi-Step Prompting | Chain-of-Thought Prompting |
|:---|:---|:---|
| Where the steps live | **Inside the prompt** — as explicit instructions | **Inside the model's output** — as generated reasoning |
| Who defines the steps | You, the prompt engineer | The model, guided by your instruction or example |
| Purpose | Directs *what* the model should do | Exposes *how* the model is thinking |
| Best for | Structured generation, code review, content planning | Math, logic, complex reasoning, verifiable problems |

### 3.5 Limitation of Chain-of-Thought Prompting

Chain-of-thought prompting has one important weakness: if the model makes a reasoning error early in the chain, that flawed reasoning propagates and corrupts all subsequent steps, leading to an incorrect final answer. This is the motivation for **self-consistency prompting**.

### 3.6 Self-Consistency Prompting

Self-consistency prompting addresses the single-path reasoning flaw by generating **multiple independent chains of thought** and then selecting the final answer by **majority vote**. The underlying principle is that while one reasoning path may be wrong, the correct answer is likely to appear most frequently across many independent attempts.

**How it works:**

1. Prompt the model to imagine several independent experts (or reasoning paths) each solving the problem separately.
2. Each expert produces their own chain-of-thought and final answer.
3. The most frequently occurring answer across all experts is selected as the final output.

**Exercise example — Self-Consistency Prompts:**

```python
self_consistency_instruction = ("Imagine three completely different experts who "
                                 "reasons differently are answering this question. "
                                 "The result is based on the majority vote. The question is:")

problem_to_solve = ("If you own a store that sells laptops and mobile phones. "
                    "You start your day with 50 devices in the store, out of which 60% are mobile phones. "
                    "Throughout the day, three clients visited the store, each of them bought one mobile phone, "
                    "and one of them bought additionally a laptop. Also, you added to your collection 10 laptops "
                    "and 5 mobile phones. How many laptops and mobile phones do you have by the end of the day?")

prompt = self_consistency_instruction + problem_to_solve
response = get_response(prompt)
print(response)
```

The model presents all three expert answers and then aggregates them: if two of three experts reach the same number, that number becomes the final answer.

---

## 4. Iterative Prompt Engineering and Refinement

### 4.1 The Iterative Nature of Prompt Engineering

Prompt engineering is not a one-shot activity. Even the most experienced practitioners rarely get a perfect prompt on the first attempt. It is an **iterative cycle** that repeats until the output meets your requirements.

The correct order of the iterative prompt engineering process is:

1. **Craft a prompt** — write your initial attempt.
2. **Send the prompt to the model** — get an output.
3. **Observe and analyze the output** — assess what is right, wrong, missing, or misformatted.
4. **Identify potential issues with the prompt** — determine the root cause of the problem.
5. **Refine the prompt** — adjust the wording, structure, examples, or constraints.
6. Repeat from step 2 until the output is satisfactory.

### 4.2 Why Prompts Fail and How to Fix Them

Prompts fail for different reasons, and the fix depends on the root cause:

| Failure Type | Example | Fix |
|:---|:---|:---|
| Model misunderstands the request | Asking for an "Excel sheet" causes the model to try to create a file | Rephrase to "a table I can copy into Excel" |
| Response lacks required detail | Analysis in one sentence omits the programming language | Explicitly request each piece of information needed |
| Output has wrong structure | Free-form paragraphs returned instead of a table | Specify the exact output format in the prompt |
| Model lacks domain knowledge | Missing edge cases like division-by-zero | Add specific criteria or domain rules as steps |

### 4.3 Iterative Refinement for Standard Prompts

**Exercise example — Iterative Prompt Engineering for Standard Prompts:**

An initial prompt to analyze code returns a one-sentence description that is accurate but too brief:

```python
# Initial prompt — too vague
prompt = "Analyze the following code in one sentence."
# Output: "The code calculates a rectangle's area."
```

Refined to add the programming language:

```python
# Refined prompt — adds language requirement
prompt = "Analyze the following code in one sentence, and mention the programming language used."
# Output: "The Python function calculates a rectangle's area given its length and width."
```

Refined again to produce structured output with multiple fields:

```python
# Further refined prompt — structured output
prompt = f"""Create a table of 10 pre-trained language models, listing the model name,
release year, and owning company. Do not include any introductory or concluding text,
only output the table."""
response = get_response(prompt)
print(response)
```

Each iteration adds one specific requirement, and the output progressively matches the intended deliverable.

### 4.4 Iterative Refinement for Few-Shot Prompts

Refinement in few-shot prompts means **improving the examples**, not just the instructions. If the model misclassifies an input, it is usually because no example in the prompt covers that type of input. The fix is to add a representative example for the problematic case.

**Exercise example — Iterative Prompt Engineering for Few-Shot Prompts:**

Initial few-shot prompt for emotion classification works correctly for most inputs but incorrectly classifies the figurative phrase `"Time flies like an arrow"` as *Surprise* instead of *no explicit emotion*:

```python
# Refined few-shot prompt — adds an example for the "no explicit emotion" edge case
prompt = """Receiving a promotion at work made me feel on top of the world -> Happiness
The movie's ending left me with a heavy feeling in my chest -> Sadness
Walking alone in the dark alley sent shivers down my spine -> Fear
Time flies like an arrow -> no explicit emotion
It is meal time -> no explicate emotion
It is high time you have your meal -> Urgency
He is just sitting there -> no explicit emotion
They sat and ate their meal ->"""

response = get_response(prompt)
print(response)
```

By adding `"Time flies like an arrow -> no explicit emotion"` as an explicit example, the model now correctly handles metaphorical or non-emotional text.

### 4.5 What to Refine in Each Prompt Type

Prompt refinement applies universally, but the *target* of the refinement differs by technique:

| Prompt Type | What to Refine |
|:---|:---|
| Standard prompt | Wording, detail level, format requirements, domain-specific criteria |
| Few-shot prompt | The examples — add, replace, or diversify them to cover edge cases |
| Multi-step prompt | The steps — make them more specific, reorder them, or add missing criteria |
| Chain-of-thought prompt | The problem description — ensure it is unambiguous and complete |
| Self-consistency prompt | The problem description and the expert framing instruction |

---

## 5. Comparing All Advanced Techniques

This section provides a consolidated view of when to use each technique covered in this segment.

| Technique | Core Idea | When to Use | Key Limitation |
|:---|:---|:---|:---|
| **Zero-shot** | No examples; model relies on training | Simple, well-defined tasks | No format control |
| **One-shot** | One example to teach format or style | Consistent output structure needed | Limited to one demonstrated pattern |
| **Few-shot** | Multiple examples to teach complex patterns | Multi-class classification, complex formatting | Requires representative examples for all classes |
| **Multi-step** | Numbered instructions as a roadmap | Sequential or multi-criteria analytical tasks | Steps must be well-defined; vague steps produce vague output |
| **Chain-of-thought** | Model shows intermediate reasoning | Math, logic, complex reasoning tasks | One flawed reasoning step cascades into a wrong answer |
| **Self-consistency** | Multiple reasoning paths + majority vote | High-stakes reasoning where single-path CoT is unreliable | More tokens consumed; slower and more expensive |
| **Iterative refinement** | Continuous improvement cycle | All prompt types; when first attempt is insufficient | Requires patience and careful diagnosis of failure modes |

---

## 6. Practical Code Patterns

### Pattern 1: Zero-Shot Prompt

```python
prompt = "Classify the sentiment of the review 'the movie was wonderful' as positive or negative."
response = get_response(prompt)
print(response)
```

### Pattern 2: One-Shot Prompt (Format Control)

```python
prompt = ("Q: Extract the odd numbers from the set {1, 3, 7, 12, 19}\n"
          "A: {1, 3, 7, 19}\n"
          "Q: Extract the odd numbers from the set {3, 5, 11, 12, 16}\n"
          "A:")
response = get_response(prompt)
print(response)
```

### Pattern 3: Few-Shot Prompt via Conversation Messages

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user",      "content": "The product quality exceeded my expectations"},
        {"role": "assistant", "content": "1"},
        {"role": "user",      "content": "I had a terrible experience with this product's customer service"},
        {"role": "assistant", "content": "-1"},
        {"role": "user",      "content": "The price of the product is really fair given its features."}
    ],
    temperature=0
)
print(response.choices[0].message.content)
```

### Pattern 4: Multi-Step Prompt

```python
prompt = """Make a detailed plan for a beach vacation by following these steps:
Step 1: Identify four potential beach vacation locations.
Step 2: For each location, list several accommodation options and possible activities.
Step 3: For each location, provide an evaluation of the pros and cons."""
response = get_response(prompt)
print(response)
```

### Pattern 5: Multi-Step Prompt for Code Review

```python
code = '''
def calculate_rectangle_area(length, width):
    area = length * width
    return area
'''

prompt = f"""Assess the function provided in the delimited code string according to three criteria:
Step - 1: correct syntax
Step - 2: receiving two inputs
Step - 3: returning one output
```{code}```"""
response = get_response(prompt)
print(response)
```

### Pattern 6: Chain-of-Thought Prompt (Direct Instruction)

```python
prompt = """Determine my friend's father's age in 10 years.
My friend is 20 years old. His father is currently twice my friend's age.
Show your reasoning step by step and give the final answer."""
response = get_response(prompt)
print(response)
```

### Pattern 7: One-Shot Chain-of-Thought Prompt (Example-Driven)

```python
example = """Q: Sum the even numbers in the following set: {9, 10, 13, 4, 2}.
             A: Even numbers: {10, 4, 2}. Adding them: 10+4+2=16"""

question = """Q: Sum the even numbers in the following set: {15, 13, 82, 7, 14}
              A:"""

prompt = f"""{example}

{question}"""
response = get_response(prompt)
print(response)
```

### Pattern 8: Self-Consistency Prompt

```python
self_consistency_instruction = ("Imagine three completely different experts who "
                                 "reasons differently are answering this question. "
                                 "The result is based on the majority vote. The question is:")

problem_to_solve = "Your math problem here..."

prompt = self_consistency_instruction + problem_to_solve
response = get_response(prompt)
print(response)
```

### Pattern 9: Iterative Refinement for Few-Shot Prompts

```python
# Add a new example covering the edge case that the model previously got wrong
prompt = """Receiving a promotion at work made me feel on top of the world -> Happiness
The movie's ending left me with a heavy feeling in my chest -> Sadness
Walking alone in the dark alley sent shivers down my spine -> Fear
Time flies like an arrow -> no explicit emotion
It is meal time -> no explicate emotion
It is high time you have your meal -> Urgency
He is just sitting there -> no explicit emotion
They sat and ate their meal ->"""

response = get_response(prompt)
print(response)
```

---

## 7. Summary Cheat Sheet

### 7.1 Technique Reference

| Concept | Definition |
|:---|:---|
| Zero-shot | Prompt with no examples; relies on pre-trained knowledge |
| One-shot | Prompt with one example to teach format or style |
| Few-shot | Prompt with 2+ examples; useful for classification and complex patterns |
| Multi-step | Prompt containing numbered steps that instruct the model like a roadmap |
| Chain-of-thought | Prompt that asks the model to show intermediate reasoning before the final answer |
| Self-consistency | Runs multiple CoT reasoning paths and picks the answer by majority vote |
| Iterative refinement | Continuous loop of crafting → sending → analyzing → refining the prompt |

### 7.2 Choosing the Right Technique

| Task Type | Recommended Technique |
|:---|:---|
| Simple one-off question | Zero-shot |
| Need a specific output format | One-shot |
| Multi-class classification | Few-shot (one example per class) |
| Sequential content generation | Multi-step |
| Analytical evaluation with criteria | Multi-step |
| Math or logic problem (auditable) | Chain-of-thought |
| High-stakes reasoning (error-prone) | Self-consistency |
| First attempt produced wrong output | Iterative refinement |

### 7.3 Iterative Refinement Checklist

When a prompt does not produce the desired output, work through the following questions:

- [ ] Is the task description **specific and unambiguous**?
- [ ] Are all required **output fields** explicitly named?
- [ ] Is the **output format** (table, list, sentence) stated clearly?
- [ ] For few-shot prompts: does at least one example **cover each class or case**?
- [ ] For multi-step prompts: are all **domain-specific criteria** included as explicit steps?
- [ ] For chain-of-thought prompts: is the **problem description complete** with no missing facts?
- [ ] Does the prompt need a **self-consistency wrapper** to guard against reasoning errors?

### 7.4 Common Mistakes to Avoid

| Mistake | Better Approach |
|:---|:---|
| Using only one reasoning path for complex math | Use self-consistency with majority vote |
| Not including an example for every class in classification | Add at least one example per class to few-shot prompts |
| Asking for analysis without defining what "correct" means | Use multi-step prompts with explicit evaluation criteria |
| Expecting a perfect prompt on the first attempt | Adopt the iterative refinement cycle from the start |
| Confusing multi-step and chain-of-thought | Multi-step = instructions in the prompt; CoT = reasoning in the output |
| Abandoning few-shot examples when edge cases fail | Refine the examples by adding one that covers the failing case |

---

*End of Revision Guide — Segment 2: Advanced Prompt Engineering Strategies*
