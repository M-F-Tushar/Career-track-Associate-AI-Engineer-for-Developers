# Prompt Engineering with the OpenAI API
## Segment 4 — Prompt Engineering for Chatbot Development

*Comprehensive Revision Guide*

---

## Table of Contents

1. [Why Prompt Engineering Matters for Chatbots](#1-why-prompt-engineering-matters-for-chatbots)
2. [The Dual-Prompt get_response() Function](#2-the-dual-prompt-get_response-function)
3. [Designing the System Prompt](#3-designing-the-system-prompt)
4. [Role-Playing Prompts for Chatbots](#4-role-playing-prompts-for-chatbots)
5. [Incorporating External Context](#5-incorporating-external-context)
6. [Practical Code Patterns](#6-practical-code-patterns)
7. [Course-Wide Summary and Final Notes](#7-course-wide-summary-and-final-notes)
8. [Summary Cheat Sheet](#8-summary-cheat-sheet)

---

## 1. Why Prompt Engineering Matters for Chatbots

### 1.1 The Unique Challenge of Chatbot Development

Building a chatbot is fundamentally different from sending a one-off prompt to a model. In a chatbot, the range of questions a user might ask is essentially unbounded — you cannot predict every query in advance, even with detailed data on past site searches or support tickets. This unpredictability makes guiding the model's behavior especially important.

Prompt engineering for chatbots solves this problem by encoding the chatbot's rules, scope, tone, and fallback behavior directly into the conversation setup, ensuring reliable and consistent responses regardless of what the user asks.

### 1.2 The Role of the System Message

Previous segments of the course focused almost exclusively on `user` messages. In chatbot development, the **`system` message becomes the primary engineering surface**. It is sent at the beginning of the conversation and persists throughout, guiding how the model interprets and responds to every subsequent `user` message.

The `chat.completions` endpoint is the ideal API endpoint for chatbot development because it accepts messages as a list of role-tagged dictionaries, allowing the system message, conversation history, and new user input to all be passed together in a single request.

---

## 2. The Dual-Prompt `get_response()` Function

### 2.1 Why the Function Needs to Change

In earlier segments, `get_response()` accepted only a single `user` prompt. For chatbot development, every API call must include both a `system_prompt` (which defines the chatbot's behavior) and a `user_prompt` (the actual user query). The function is therefore updated to accept both parameters.

### 2.2 The Updated Function

**Exercise example — Creating a Dual-Prompt `get_response()` Function:**

```python
def get_response(system_prompt, user_prompt):
    # Assign the role and content for each message
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": user_prompt}
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content
```

```python
# Try the function with a system and user prompt of your choice
response = get_response(
    "You are a helpful assistant",
    "Explain what a binary search in simple terms"
)
print(response)
```

Key differences from the original single-prompt version: the `messages` list now always contains two entries — one `system` and one `user` — and both are passed as arguments when calling the function. This dual-prompt structure is used in **all subsequent exercises** in this segment.

---

## 3. Designing the System Prompt

A well-constructed system prompt for a chatbot typically contains three distinct components: a **purpose statement**, **response guidelines**, and **behavior guidance**. These can be defined as separate string variables and concatenated into a single `system_prompt`. Building them modularly makes the prompt easier to maintain, extend, and debug.

### 3.1 Component 1: Purpose Statement

The purpose statement tells the model what the chatbot is, what domain it operates in, and what kinds of tasks it is expected to handle. This lets the model know what questions to anticipate and improves the accuracy of domain-specific answers. A vague or absent purpose statement leads to irrelevant responses.

```python
# Exercise example — Customer Support Chatbot
chatbot_purpose = ("This is a customer support chatbot for an e-commerce company "
                   "specializing in electronics. This chatbot will assist users with "
                   "inquiries, order tracking, and troubleshooting common issues.")
```

When a user asks "Who are you?", a chatbot with a clear purpose statement will answer with its defined role. Without one, the model will generate a generic response that does not match the intended product.

### 3.2 Component 2: Response Guidelines

Response guidelines control *how* the chatbot communicates — its tone, target audience, output length, and output structure. You do not need to specify everything, but you should be explicit about whatever matters most for your use case.

Common response guideline dimensions include:

| Dimension | Example Values |
|:---|:---|
| Tone | Professional, friendly, empathetic, formal, casual, persuasive |
| Audience | Tech-savvy users, general public, non-technical customers, children |
| Output length | Concise, detailed, no more than three recommendations |
| Objectivity | Precise and objective, avoid personal opinions |

```python
# Audience and tone guidelines assembled separately for clarity
audience_guidelines = "tech-savvy individuals interested in purchasing electronic gadgets."
tone_guidelines     = "Be professional and user-friendly."

system_prompt = chatbot_purpose + audience_guidelines + tone_guidelines
```

In the financial chatbot example from the video, when a user asks for an opinion on cryptocurrencies, the chatbot responds precisely and objectively — starting with a definition, then covering advantages and disadvantages, and finishing with a summary — because the response guidelines specifically required precision and objectivity.

### 3.3 Component 3: Behavior Guidance (Conditional Logic)

Behavior guidance uses **conditional if-else instructions** to control the chatbot's response to out-of-scope or edge-case queries. This is where you restrict the chatbot's domain, define fallback messages, or instruct it to ask clarifying questions when needed.

**Domain restriction example — Financial chatbot:**

```python
# Instruct the chatbot to stay within its domain
domain_restriction = ("Answer financial questions to the best of your knowledge. "
                      "For all other questions, respond with: 'Sorry, I only know about finance.'")
```

If a user asks about the weather, the chatbot will respond: *"Sorry, I only know about finance."*

**Conditional behavior for incomplete inputs — Customer support chatbot:**

```python
# Exercise example — Behavioral Control of a Customer Support Chatbot
order_number_condition = """If the user asks about an order but does not provide an order number,
ask them for their order number and save it to order_number_condition."""

technical_issue_condition = """If the user reports a technical issue, start your response with:
'I'm sorry to hear about your issue with ...'"""

refined_system_prompt = base_system_prompt + order_number_condition + technical_issue_condition

response_1 = get_response(refined_system_prompt, "My laptop screen is flickering. What should I do?")
response_2 = get_response(refined_system_prompt, "Can you help me track my recent order?")

print("Response 1: ", response_1)
print("Response 2: ", response_2)
```

Response 1 will begin with *"I'm sorry to hear about your issue with..."* because `technical_issue_condition` is triggered. Response 2 will prompt the user for their order number because `order_number_condition` is triggered. The system prompt components are defined separately and concatenated to form the final `refined_system_prompt`, which makes the modular design pattern clear and practical.

### 3.4 Complete System Prompt Architecture

The full system prompt is assembled by concatenating all three components:

```python
system_prompt = chatbot_purpose + audience_guidelines + tone_guidelines
# Or for a more refined chatbot:
system_prompt = base_system_prompt + behavior_guidelines + response_guidelines
```

The order matters: purpose → audience/tone guidelines → behavior conditions is the natural reading order and helps the model prioritize the instructions correctly.

---

## 4. Role-Playing Prompts for Chatbots

### 4.1 What Are Role-Playing Prompts?

Role-playing prompts instruct the chatbot to adopt a specific professional role or persona. Like an actor being given a character to portray, the model adjusts its tone, vocabulary, depth of response, and overall behavior to match the assigned role. This produces tailored, domain-appropriate responses rather than generic ones. The model is able to play these roles because it has been trained on vast quantities of text from many professional domains.

### 4.2 How the Same Question Gets Different Answers from Different Roles

The course illustrates this with a single user question — asking about the technical specifications of a product — answered by three different roles:

| Role | Response Style |
|:---|:---|
| Customer Support Agent | General guidance, directs to the website for details, offers further assistance |
| Product Manager | Strategic benefits, how the product aligns with business goals and professional needs |
| Sales Engineer | Technical specifics — processor details, key features, security capabilities |

The same question, answered from three different role perspectives, produces three substantively different and contextually appropriate responses.

### 4.3 Basic Role Assignment

The minimal instruction to trigger role-playing behavior is to ask the model to "act as" a specific role:

```python
# Basic role assignment
system_prompt = ("Act as an expert financial analyst and offer insights about "
                 "retirement planning for individuals approaching retirement age.")
```

The model will respond as if a real financial analyst were answering, providing professional considerations such as asset allocation, withdrawal strategies, and tax planning.

### 4.4 Enriching the Role with Specific Traits

Simply naming a role (e.g., "journalist") may produce generic responses, because many journalists have different styles. Adding **specific traits and expertise** to the role description makes the persona much more distinctive and useful.

```python
# Enriched role-playing — specific traits added beyond just the job title
system_prompt = ("Act as a seasoned technology journalist specializing in thorough "
                 "tech industry analysis.")
user_prompt   = "What is the impact of AI on job markets?"
```

The model responds as a journalist with the described qualities — producing a detailed, analytical, and structured article-style response rather than a brief conversational answer.

### 4.5 Role-Playing in Practice — Exercise Examples

**Learning Advisor Chatbot (basic role):**

```python
# Exercise example — Learning Advisor Chatbot
system_prompt = ("Act as a learning advisor who receive queries from learners about their "
                 "background, experience, and goals, and accordingly, recommends a learning "
                 "path of textbooks, including both beginner-level and more advanced options.")

user_prompt = ("Hello there! I'm a beginner with a marketing background, and I'm really "
               "interested in learning about Python, data analytics, and machine learning. "
               "Can you recommend some books?")

response = get_response(system_prompt, user_prompt)
print(response)
```

**Learning Advisor Chatbot with added guidelines (role + behavior + response):**

```python
# Exercise example — Adding Guidelines to the Learning Advisor Chatbot
base_system_prompt = ("Act as a learning advisor who receives queries from users mentioning their "
                      "background, experience, and goals, and accordingly provides a response that "
                      "recommends a tailored learning path of textbooks, including both beginner-level "
                      "and more advanced options.")

behavior_guidelines = ("Ask a user about their background, experience, and goals, whenever any "
                       "of these is not provided in the prompt.")

response_guidelines = "Recommend no more than three textbooks."

system_prompt = base_system_prompt + behavior_guidelines + response_guidelines

user_prompt = "Hey, I'm looking for courses on Python and data visualization. What do you recommend?"

response = get_response(system_prompt, user_prompt)
print(response)
```

The `behavior_guidelines` make the chatbot ask for missing user information rather than giving generic recommendations. The `response_guidelines` cap the number of suggestions at three, keeping responses concise and practical.

### 4.6 Role-Playing Does Not Replace Other Guidelines

A critical point from the course: **assigning a role does not automatically enforce response constraints or domain restrictions**. If you want the chatbot to stay within a specific topic area, you must still add explicit behavior guidance.

```python
# Role alone does NOT restrict the domain — you must add this explicitly
tech_domain_restriction = ("If the user asks about a topic that is not related to technology, "
                           "respond with: 'I specialize in technology topics only.'")

system_prompt = "Act as a seasoned technology journalist..." + tech_domain_restriction
```

Without the domain restriction, the chatbot would answer questions about American literature, cooking, or any other topic — just styled as a tech journalist.

---

## 5. Incorporating External Context

### 5.1 Why External Context is Needed

Pre-trained LLMs have two fundamental knowledge gaps that are relevant to chatbot development:

**Knowledge cut-off:** The model was trained on data collected up to a specific date. Any events, reports, or information produced after that date are unknown to the model. If asked about recent developments, the model may either admit ignorance or, worse, fabricate an answer.

**Private/proprietary information:** Company-specific data — internal products, pricing, service descriptions, policies, employee names — was never part of the training data because it was not publicly available on the web. The model has no way of knowing this information without being told.

To bridge both gaps, relevant context must be injected into the conversation manually, either through sample conversations or through the system prompt.

### 5.2 Method 1: Providing Context Through Sample Conversations

Context can be supplied by adding simulated prior conversation turns — a `user` message asking about the topic and an `assistant` message providing the answer — before the live user query. The model uses these planted exchanges as its factual basis for answering related questions.

**Exercise example — Providing Context Through Sample Conversations:**

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        # System message — defines chatbot purpose and tone
        {"role": "system",    "content": "You are a helpful customer service chatbot "
                                         "for MyPersonalDelivery that responds in a gentle way"},
        # Planted context — a simulated prior exchange
        {"role": "user",      "content": context_question},   # "What types of items can be delivered?"
        {"role": "assistant", "content": context_answer},     # Full list of delivery options
        # Live user query — the model uses the planted exchange as context
        {"role": "user",      "content": "Do you deliver furniture?"}
    ]
)
response = response.choices[0].message.content
print(response)
```

The model answers "Do you deliver furniture?" by drawing from `context_answer`, which it read in the simulated prior exchange. Without this planted exchange, the model would have no knowledge of `MyPersonalDelivery`'s delivery offerings.

**Limitation:** This method requires creating a separate question-answer pair for every piece of context the chatbot may need. For a complex domain, this quickly becomes unwieldy.

### 5.3 Method 2: Providing Context Through the System Prompt

A more scalable and maintainable approach is to embed the context information directly inside the system prompt using an f-string. The system prompt is already sent with every request, so any information placed there is always available to the model.

**Exercise example — Providing Context Through System Prompt:**

```python
service_description = "... (full text of the company's service description) ..."

system_prompt = f"""You are a helpful customer service chatbot for a delivery service called MyPersonalDelivery.

Here is the service description:
{service_description}

Use this information to answer user questions in a gentle and clear manner."""

user_prompt = "What benefits does MyPersonalDelivery offer?"

response = get_response(system_prompt, user_prompt)
print(response)
```

The model uses `service_description` — which could be the company's full "About Us" text, a product catalog, or a policy document — to answer any question that relates to it. Because this information is in the system prompt, it is available for every user query in the session without having to plant individual conversation turns.

### 5.4 Choosing Between the Two Methods

| Dimension | Sample Conversations | System Prompt |
|:---|:---|:---|
| Best for | A few specific facts or Q&A pairs | Larger blocks of reference text |
| Scalability | Low — each fact needs its own Q&A | High — paste any text directly into the prompt |
| Maintainability | Harder to update | Easier — just update the string variable |
| Naturalness | Mimics real conversation history | Declarative; more like a briefing document |

### 5.5 Important Limitation: Context Window Size

Both methods work well for **relatively small amounts of context**. Every LLM has a maximum context window — the total number of tokens it can process in a single request (system prompt + conversation history + user query combined). Embedding very large documents in the system prompt will eventually hit this limit. When a large amount of context is needed (e.g., a full product documentation site), more sophisticated techniques such as retrieval-augmented generation (RAG) are required. These techniques are noted in the course as being outside the scope of the material covered.

---

## 6. Practical Code Patterns

### Pattern 1: Dual-Prompt `get_response()` Function

```python
def get_response(system_prompt, user_prompt):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": user_prompt}
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content
```

### Pattern 2: Modular System Prompt Assembly

```python
# Define each component separately, then concatenate
chatbot_purpose    = "This is a customer support chatbot for an e-commerce company specializing in electronics. This chatbot will assist users with inquiries, order tracking, and troubleshooting common issues."
audience_guidelines = "tech-savvy individuals interested in purchasing electronic gadgets."
tone_guidelines     = "Be professional and user-friendly."

system_prompt = chatbot_purpose + audience_guidelines + tone_guidelines
response = get_response(system_prompt, "My new headphones aren't connecting to my device")
print(response)
```

### Pattern 3: Behavioral Control with Conditions

```python
# Append conditional behavior rules to a base system prompt
order_number_condition = """If the user asks about an order but does not provide an order number,
ask them for their order number and save it to order_number_condition."""

technical_issue_condition = """If the user reports a technical issue, start your response with:
'I'm sorry to hear about your issue with ...'"""

refined_system_prompt = base_system_prompt + order_number_condition + technical_issue_condition

response_1 = get_response(refined_system_prompt, "My laptop screen is flickering. What should I do?")
response_2 = get_response(refined_system_prompt, "Can you help me track my recent order?")
print("Response 1: ", response_1)
print("Response 2: ", response_2)
```

### Pattern 4: Basic Role-Playing Prompt

```python
# Assign a professional role through the system prompt
system_prompt = ("Act as a learning advisor who receive queries from learners about their "
                 "background, experience, and goals, and accordingly, recommends a learning "
                 "path of textbooks, including both beginner-level and more advanced options.")

user_prompt = ("Hello there! I'm a beginner with a marketing background, and I'm really "
               "interested in learning about Python, data analytics, and machine learning. "
               "Can you recommend some books?")

response = get_response(system_prompt, user_prompt)
print(response)
```

### Pattern 5: Role-Playing with Behavior and Response Guidelines

```python
# Role + behavior conditions + response constraints combined
base_system_prompt = ("Act as a learning advisor who receives queries from users mentioning their "
                      "background, experience, and goals, and accordingly provides a response that "
                      "recommends a tailored learning path of textbooks, including both beginner-level "
                      "and more advanced options.")

behavior_guidelines = ("Ask a user about their background, experience, and goals, whenever any "
                       "of these is not provided in the prompt.")

response_guidelines = "Recommend no more than three textbooks."

system_prompt = base_system_prompt + behavior_guidelines + response_guidelines

user_prompt = "Hey, I'm looking for courses on Python and data visualization. What do you recommend?"
response = get_response(system_prompt, user_prompt)
print(response)
```

### Pattern 6: Providing Context via Sample Conversations

```python
# Inject context as simulated prior conversation turns
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system",    "content": "You are a helpful customer service chatbot for MyPersonalDelivery that responds in a gentle way"},
        {"role": "user",      "content": context_question},
        {"role": "assistant", "content": context_answer},
        {"role": "user",      "content": "Do you deliver furniture?"}
    ]
)
response = response.choices[0].message.content
print(response)
```

### Pattern 7: Providing Context via the System Prompt

```python
# Embed reference text directly into the system prompt using an f-string
system_prompt = f"""You are a helpful customer service chatbot for a delivery service called MyPersonalDelivery.

Here is the service description:
{service_description}

Use this information to answer user questions in a gentle and clear manner."""

user_prompt = "What benefits does MyPersonalDelivery offer?"
response = get_response(system_prompt, user_prompt)
print(response)
```

---

## 7. Course-Wide Summary and Final Notes

### 7.1 What Was Covered Across All Four Segments

| Segment | Topic | Key Takeaways |
|:---|:---|:---|
| 1 | Prompt Engineering Best Practices | Action verbs, delimiters, f-strings, structured outputs, conditional prompts |
| 2 | Advanced Strategies | Zero/one/few-shot, multi-step, chain-of-thought, self-consistency, iterative refinement |
| 3 | Business Applications | Summarization, expansion, transformation, classification, entity extraction, code generation/explanation |
| 4 | Chatbot Development | System prompt design (purpose, guidelines, behavior), role-playing, external context injection |

### 7.2 Important Limitations of LLMs (Final Course Note)

The course closes with a critical reminder that applies to all four segments:

> *"While prompt engineering enhances performance and yields better outcomes from a language model, such models have limitations, just like any other system. Even with precise prompt engineering, desired results are not always guaranteed."*

The three practical implications of this are:

**Always review for accuracy.** LLMs can generate factually incorrect, outdated, or subtly misleading information. Every output intended for real-world use must be verified by a human with domain knowledge.

**Check for potential bias.** Because LLMs are trained on web-scale data, they can reflect biases present in that data. Outputs used in customer-facing or decision-making contexts should be reviewed for unintended bias.

**Never use outputs mindlessly.** Prompt engineering is a tool, not a guarantee. It improves the probability of a good output; it does not eliminate the possibility of a bad one.

---

## 8. Summary Cheat Sheet

### 8.1 Chatbot System Prompt Components

| Component | Purpose | What to Include |
|:---|:---|:---|
| Purpose statement | Defines what the chatbot is and what it does | Domain, tasks it handles, company/product name |
| Response guidelines | Controls how the chatbot communicates | Tone, target audience, output length, objectivity |
| Behavior guidance | Handles edge cases and out-of-scope queries | Conditional if-else rules, domain restrictions, fallback messages |

### 8.2 Role-Playing Prompts Quick Reference

| Role-Playing Level | How | When to Use |
|:---|:---|:---|
| Basic role | `"Act as a [role]..."` | When any response in that professional domain is acceptable |
| Enriched role | `"Act as a [role] specializing in [domain] with [traits]..."` | When a specific style, depth, or expertise is required |
| Role + guidelines | Role instruction + behavior/response guidelines concatenated | Always — role alone does not enforce domain restrictions or response constraints |

### 8.3 External Context Methods

| Method | How | Best For | Limitation |
|:---|:---|:---|:---|
| Sample conversations | Add `user`/`assistant` message pairs before the live query | A few specific factual Q&A pairs | Each fact requires its own planted exchange |
| System prompt injection | Embed the context text via f-string in the `system_prompt` | Larger blocks of reference text | Subject to the model's context window size limit |

### 8.4 Prompt Design Checklist for Chatbots

**System prompt checklist:**
- [ ] Does the system prompt include a clear **purpose statement**?
- [ ] Are the **target audience** and **tone** specified in the response guidelines?
- [ ] Are **conditional behavior rules** included to handle out-of-scope questions?
- [ ] Is the **domain restriction** message defined for off-topic queries?
- [ ] Is **external context** (company info, product data) embedded if needed?

**Role-playing checklist:**
- [ ] Is the role named explicitly with `"Act as a..."`?
- [ ] Are **specific traits or areas of expertise** added beyond the job title?
- [ ] Are **behavior and response guidelines** appended to the role instruction?
- [ ] Is a **domain restriction condition** included if the chatbot should not answer off-topic questions?

**External context checklist:**
- [ ] Is the context injected via the preferred method (system prompt for larger text, sample conversation for a few facts)?
- [ ] Is the total amount of context small enough to fit within the model's context window?
- [ ] Is the context text embedded using an **f-string** to keep the prompt dynamic and maintainable?

### 8.5 Common Mistakes to Avoid

| Mistake | Better Approach |
|:---|:---|
| Using a single-prompt `get_response()` for chatbot work | Update to the dual-prompt version accepting both `system_prompt` and `user_prompt` |
| Writing the system prompt as one long, unstructured string | Define purpose, guidelines, and behavior conditions as separate variables, then concatenate |
| Assigning a role and assuming the chatbot will stay on-topic | Always append an explicit domain restriction condition to the role instruction |
| Expecting the role itself to define response length or structure | Add explicit response guidelines for length, format, and objectivity |
| Embedding very large documents in the system prompt | Keep context small; use retrieval-augmented generation (RAG) for large knowledge bases |
| Not testing with out-of-scope queries | Always test conditional behavior rules with queries that should trigger the fallback message |

---

*End of Revision Guide — Segment 4: Prompt Engineering for Chatbot Development*
