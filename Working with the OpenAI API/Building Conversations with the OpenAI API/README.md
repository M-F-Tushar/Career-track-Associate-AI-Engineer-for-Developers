# Comprehensive Study Guide: Working with the OpenAI API — Segment 3: Building Conversations with the OpenAI API

---

## 1. Single-Turn vs. Multi-Turn Conversations

### 1.1 Single-Turn Tasks (What We've Done So Far)
- All tasks covered in previous segments involved **one input and one output**.
- Examples: text generation, text transformation, sentiment analysis, summarization.
- These are called **single-turn tasks** because the interaction ends after one exchange.

### 1.2 Multi-Turn Conversations (What This Segment Introduces)
- The Chat Completions endpoint also supports **multi-turn conversations**.
- This means you can **build on previous prompts** depending on how the model responds.
- Multi-turn conversations are the foundation of AI chatbots like ChatGPT.

---

## 2. The Three Chat Roles

Roles are at the **heart of how chat models function**. Every message in the `messages` list must have a `"role"` assigned to it.

| Role | Who Uses It | Purpose |
|---|---|---|
| `"system"` | Developer | Controls the **behavior** and persona of the assistant |
| `"user"` | The end user | Provides **instructions or questions** to the assistant |
| `"assistant"` | The model (or developer) | Represents the **model's responses**; can also be provided by developers as examples |

### 2.1 The System Role
- Sets **how the assistant should behave** throughout the conversation.
- It is typically the **first message** in the `messages` list.
- Powerful uses include:
  - Defining the assistant's persona (e.g., "You are a polite customer service assistant.")
  - Setting the tone or communication style (e.g., "Speak concisely.")
  - Adding **guardrails** — restrictions on what the model can say or do.

### 2.2 The User Role
- Used to send **prompts or questions** from the user to the model.
- This is the role we have used exclusively in previous segments.

### 2.3 The Assistant Role
- Represents the **model's responses** returned to us.
- As a **developer**, you can also manually craft assistant messages in your requests.
- These manually provided assistant messages act as **examples** to guide the model toward the desired output format or style — essentially a more structured form of few-shot prompting.

---

## 3. Adding a System Message to a Request

### 3.1 Basic Structure with System + User Messages
To include multiple messages, **extend the `messages` list** with multiple dictionaries, each having their own `"role"` and `"content"`:

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    max_completion_tokens=150,
    messages=[
        {"role": "system",
         "content": "You are a Python programming tutor that speaks concisely."},
        {"role": "user",
         "content": "What is a Python list?"}
    ]
)
print(response.choices[0].message.content)
```

**Result:** The model follows the system instruction — answering concisely in a single sentence.

### 3.2 Correct Ordering of Messages
Messages should always be ordered as follows in the list:

```
1. system   ← Sets behavior (first)
2. user     ← First user message
3. assistant ← (optional) Example response or previous reply
4. user     ← Follow-up user message
...
```

> **Key rule:** The system message always comes first. User and assistant messages follow in chronological conversation order.

---

## 4. Guardrails with System Messages

### 4.1 What Are Guardrails?
**Guardrails** are specific **restrictions** embedded in the system message that prevent the model from producing certain types of outputs. They are one of the most important uses of system messages.

### 4.2 Why Are Guardrails Needed?
- Misuse is a major challenge when deploying AI systems.
- Example: A finance exam study chatbot should **not** provide specific investment advice or encourage particular financial decisions that could put users' finances at risk.
- Guardrails prevent the model from straying outside its intended purpose.

### 4.3 Structure of a Guardrail System Message
A well-constructed guardrail system message typically has two parts:
1. **Define the role and task** of the assistant.
2. **State the restriction** — what the model should do if asked something outside its scope, including what to say instead.

```python
sys_msg = """You are a study planning assistant that creates plans for learning new skills.

If these skills are non related to languages, return the message:
'Apologies, to focus on languages, we no longer create learning plans on other topics.'"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": sys_msg},
        {"role": "user", "content": "Help me learn to Math."}
    ]
)
print(response.choices[0].message.content)
```

**Result:** The model returns exactly the apologetic message specified in the system prompt, instead of providing math content.

### 4.4 More Complex Guardrail Example (Finance Education)
```python
sys_msg = """You are a finance education assistant that helps students study for finance exams.
If asked to provide specific, real-world financial advice with risks to their finances,
respond with an apologetic message stating that you can only provide educational content."""
```

---

## 5. Adding Assistant Messages (In-Context Learning)

### 5.1 What Are Developer-Provided Assistant Messages?
Besides being the model's response role, **developers can manually provide assistant messages** in the `messages` list. These act as **worked examples** for the model to learn from — a more structured form of few-shot prompting.

### 5.2 User-Assistant Pairs as Examples
You provide examples as **user-assistant pairs** in the messages list, followed by the actual user query you want the model to answer:

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system",
         "content": "You are a helpful Geography tutor that generates concise summaries for different countries."},
        # Example pair (in-context learning)
        {"role": "user",    "content": "Give me a quick summary of Portugal"},
        {"role": "assistant","content": "Portugal is a country in Europe that borders Spain. The capital city is Lisboa."},
        # Actual query
        {"role": "user",    "content": "Give me a quick summary of Greece."}
    ]
)
print(response.choices[0].message.content)
```

### 5.3 Multiple Example Pairs (Few-Shot via Assistant Messages)
You can add more examples to further guide the format and style of responses:

```python
messages=[
    {"role": "system",    "content": "You are a helpful Geography tutor that generates concise summaries for different countries."},
    {"role": "user",      "content": "Give me a quick summary of Portugal."},
    {"role": "assistant", "content": "Portugal is a country in Europe that borders Spain. The capital city is Lisboa."},
    {"role": "user",      "content": "Give me a quick summary of Japan."},
    {"role": "assistant", "content": "Japan is an island nation in East Asia known for its technology and culture. The capital city is Tokyo."},
    {"role": "user",      "content": "Give me a quick summary of Brazil."},
    {"role": "assistant", "content": "Brazil is the largest country in South America, famous for the Amazon rainforest. The capital city is Brasília."},
    {"role": "user",      "content": "Give me a quick summary of Kenya."},
    {"role": "assistant", "content": "Kenya is a country in East Africa known for its wildlife and savannas. The capital city is Nairobi."},
    # Actual query
    {"role": "user",      "content": "Give me a quick summary of Greece."}
]
```

> **Note:** The more consistent examples you provide, the more consistent the model's output format becomes — the same principle as few-shot prompting, but implemented through the roles structure.

---

## 6. Building Multi-Turn Conversations

### 6.1 The Core Idea
To build a true multi-turn conversation:
1. Send a user message → receive an assistant response.
2. **Store the assistant's response** and add it back to the `messages` list.
3. Send the updated messages list (which now includes the conversation history) with the next user message.
4. The model can now **draw from the full conversation history** to produce a contextually aware reply.

> This is exactly what powers chatbots like ChatGPT under the hood.

### 6.2 Extracting and Storing the Assistant Response
After getting a response, convert it to a message dictionary and append it to the messages list:

```python
# Extract the assistant message from the response
assistant_dict = {
    "role": "assistant",
    "content": response.choices[0].message.content
}
# Append it to the conversation history
messages.append(assistant_dict)
```

### 6.3 Full Conversation Loop — Complete Code

```python
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Initialize messages with a system message
messages = [
    {"role": "system", "content": "You are a helpful math tutor that speaks concisely."}
]

# List of user questions (second question requires context from the first)
user_msgs = ["Explain what pi is.", "Summarize this in two bullet points."]

for q in user_msgs:
    print("User: ", q)

    # Create and append the user message dictionary
    user_dict = {"role": "user", "content": q}
    messages.append(user_dict)

    # Send the full conversation history to the model
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_completion_tokens=100
    )

    # Extract the assistant's response and append it to messages
    assistant_dict = {
        "role": "assistant",
        "content": response.choices[0].message.content
    }
    messages.append(assistant_dict)

    # Print the assistant's response
    print("Assistant: ", response.choices[0].message.content)
```

### 6.4 Step-by-Step Breakdown of the Loop

| Step | What Happens |
|---|---|
| 1 | Loop begins for each user question `q` |
| 2 | A `user_dict` is created: `{"role": "user", "content": q}` |
| 3 | `user_dict` is appended to `messages` using `.append()` |
| 4 | The full `messages` list (including history) is sent to the model |
| 5 | The assistant's response is extracted from `response.choices[0].message.content` |
| 6 | The response is packaged as `assistant_dict` and appended to `messages` |
| 7 | The loop moves to the next question with the full context available |

> **Why this works:** Because the second question — *"Summarize this in two bullet points"* — refers to "this" without specifying what it is. The model can answer correctly because it has access to its own previous response in the conversation history.

---

## 7. Exercise Walkthroughs

### Exercise 1: Utilizing System Messages
- **Task:** Design an AI study planner using a system message to set behavior, then ask it a question.
- **Key skills:** System + user message structure, `max_completion_tokens`.

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    max_completion_tokens=150,
    messages=[
        {"role": "system",
         "content": "You are a study planning assistant that creates plans for learning new skills."},
        {"role": "user",
         "content": "I want to learn to speak Dutch."}
    ]
)
print(response.choices[0].message.content)
```

---

### Exercise 2: Adding Guardrails
- **Task:** Add a restriction to the study planning assistant so it only creates language learning plans and rejects non-language topics.

```python
sys_msg = """You are a study planning assistant that creates plans for learning new skills.

If these skills are non related to languages, return the message:
'Apologies, to focus on languages, we no longer create learning plans on other topics.'"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": sys_msg},
        {"role": "user",   "content": "Help me learn to Math."}
    ]
)
print(response.choices[0].message.content)
```

**Expected output:** The apologetic message defined in `sys_msg`.

---

### Exercise 3: Structuring Chat Messages (Ordering Exercise)
- **Task:** Drag the message blocks into the correct order for a chat message request.
- **Correct order:**

```
1. {"role": "system",    "content": "You are a patient and informative teacher."}
2. {"role": "user",      "content": "I'm really struggling with a coding problem."}
3. {"role": "assistant", "content": "Don't worry, we'll get you sorted! How can I help?"}
4. {"role": "user",      "content": "How do I access dictionary values using their keys?"}
```

> **Rule to remember:** System message first → then user/assistant exchanges in chronological order → ending with the final user message the model needs to respond to.

---

### Exercise 4: Adding Assistant Messages (One Example)
- **Task:** Improve a geography tutor by providing one example user-assistant pair in the messages list.

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system",    "content": "You are a helpful Geography tutor that generates concise summaries for different countries."},
        {"role": "user",      "content": "Give me a quick summary of Portugal"},
        {"role": "assistant", "content": "Portugal is a country in Europe that borders Spain. The capital city is Lisboa."},
        {"role": "user",      "content": "Give me a quick summary of Greece."}
    ]
)
print(response.choices[0].message.content)
```

---

### Exercise 5: More Assistant Messages (Multiple Examples)
- **Task:** Expand the geography tutor with additional example user-assistant pairs (Japan, Brazil, Kenya) to further guide the format.

```python
messages=[
    {"role": "system",    "content": "You are a helpful Geography tutor that generates concise summaries for different countries."},
    {"role": "user",      "content": "Give me a quick summary of Portugal."},
    {"role": "assistant", "content": "Portugal is a country in Europe that borders Spain. The capital city is Lisboa."},
    {"role": "user",      "content": "Give me a quick summary of Japan."},
    {"role": "assistant", "content": "Japan is an island nation in East Asia known for its technology and culture. The capital city is Tokyo."},
    {"role": "user",      "content": "Give me a quick summary of Brazil."},
    {"role": "assistant", "content": "Brazil is the largest country in South America, famous for the Amazon rainforest. The capital city is Brasília."},
    {"role": "user",      "content": "Give me a quick summary of Kenya."},
    {"role": "assistant", "content": "Kenya is a country in East Africa known for its wildlife and savannas. The capital city is Nairobi."},
    {"role": "user",      "content": "Give me a quick summary of Greece."}
]
```

---

### Exercise 6: Creating a Conversation History
- **Task:** Build a math tutor POC where model responses are stored in message history for contextual follow-up.
- **Key steps:** Send initial messages, extract assistant response, convert to dictionary, append to messages.

```python
messages = [
    {"role": "system", "content": "You are a helpful math tutor that speaks concisely."},
    {"role": "user",   "content": "Explain what pi is."}
]

# Send the chat messages to the model
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    max_completion_tokens=100
)

# Extract the assistant message and append to messages
assistant_dict = {
    "role": "assistant",
    "content": response.choices[0].message.content
}
messages.append(assistant_dict)
```

---

### Exercise 7: Creating an AI Chatbot (Full Loop)
- **Task:** Complete the math tutor POC by integrating the message history with a `for` loop to handle multiple sequential user questions.

```python
messages = [{"role": "system", "content": "You are a helpful math tutor that speaks concisely."}]
user_msgs = ["Explain what pi is.", "Summarize this in two bullet points."]

for q in user_msgs:
    print("User: ", q)

    # Create and append user message
    user_dict = {"role": "user", "content": q}
    messages.append(user_dict)

    # Send to the model
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_completion_tokens=100
    )

    # Append assistant message to history
    assistant_dict = {"role": "assistant", "content": response.choices[0].message.content}
    messages.append(assistant_dict)

    print("Assistant: ", response.choices[0].message.content)
```

**Result:** The model successfully handles the follow-up ("Summarize this") because it has the previous answer in its conversation history.

---

## 8. Key Concepts Summary

| Concept | Summary |
|---|---|
| Single-turn task | One input, one output — no conversation history |
| Multi-turn conversation | A sequence of exchanges where context is preserved |
| `"system"` role | Sets the assistant's behavior, persona, and restrictions |
| `"user"` role | Sends instructions or questions to the model |
| `"assistant"` role | Represents model responses; can be manually added as examples |
| Guardrails | Restrictions in system messages that prevent misuse |
| Developer assistant messages | Examples provided in the messages list to guide output format (structured few-shot prompting) |
| Conversation history | The full `messages` list including all previous exchanges, sent with each new request |
| `.append()` | Python list method used to add new messages to the conversation history |
| `response.choices[0].message.content` | Standard way to extract the text from any API response |

---

## 9. Practical Tips & Best Practices

- **Always start the `messages` list with a system message** to define context and behavior before any user interaction.
- **Craft guardrails carefully** — be specific about what the model should and should not do, and include the exact fallback message you want the model to return.
- **User-assistant example pairs in `messages`** are a more structured and powerful alternative to inline few-shot examples in a single user prompt — use them when you need strict output formatting.
- **The full `messages` list must be re-sent with every API call** — the model has no memory between separate requests; all context must be included each time.
- **Use `.append()`** consistently to grow the conversation history dynamically — do not manually re-index or rewrite the list.
- **Context window limit:** Be aware that very long conversation histories consume more tokens and may eventually exceed the model's context window limit, increasing costs.
- **Print both user and assistant turns** during development to verify that the conversation is flowing correctly.

---

## 10. Full Course Summary (All Three Segments)

| Segment | Key Topics |
|---|---|
| **Segment 1** | What the OpenAI API is, making requests, interpreting responses, API authentication, endpoints |
| **Segment 2** | Text editing, summarization, generation, tokens, cost calculation, `temperature`, zero/one/few-shot prompting |
| **Segment 3** | System, user, and assistant roles; system messages; guardrails; assistant messages as examples; multi-turn conversation history; building an AI chatbot |

---

*This guide covers all content from Segment 3 of "Working with the OpenAI API," including both video topics (chat roles/system messages and multi-turn conversations) and all seven exercises.*
