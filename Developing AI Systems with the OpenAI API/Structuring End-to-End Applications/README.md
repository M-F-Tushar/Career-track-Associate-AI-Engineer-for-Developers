# Developing AI Systems with the OpenAI API – Segment 1: Structuring End-to-End Applications
### Comprehensive Revision Guide

---

## Table of Contents

1. [Structuring an API Call](#1-structuring-an-api-call)
   - 1.1 [The Basic OpenAI API Request Structure](#11-the-basic-openai-api-request-structure)
   - 1.2 [Challenges of a Production Environment](#12-challenges-of-a-production-environment)
   - 1.3 [Requesting JSON Output](#13-requesting-json-output)
   - 1.4 [Extracting the Response](#14-extracting-the-response)
2. [Handling Errors](#2-handling-errors)
   - 2.1 [Why Error Handling Matters](#21-why-error-handling-matters)
   - 2.2 [Error Types in the OpenAI Python Library](#22-error-types-in-the-openai-python-library)
   - 2.3 [Handling Exceptions with try/except](#23-handling-exceptions-with-tryexcept)
3. [Batching and Rate Limits](#3-batching-and-rate-limits)
   - 3.1 [What are Rate Limits?](#31-what-are-rate-limits)
   - 3.2 [How Rate Limits Occur](#32-how-rate-limits-occur)
   - 3.3 [Solution 1: Retry with Exponential Backoff](#33-solution-1-retry-with-exponential-backoff)
   - 3.4 [Solution 2: Batching](#34-solution-2-batching)
   - 3.5 [Solution 3: Reducing Tokens with tiktoken](#35-solution-3-reducing-tokens-with-tiktoken)
4. [Exercise Solutions](#4-exercise-solutions)

---

## 1. Structuring an API Call

### 1.1 The Basic OpenAI API Request Structure

Before building production-ready systems, it helps to understand the foundational pattern for interacting with the OpenAI API using Python. The flow has three steps:

1. **Initialize the OpenAI client** using your API key
2. **Create a request** to the Chat Completions endpoint
3. **Extract the response** from the returned object

Here is the canonical minimal example:

```python
from openai import OpenAI

client = OpenAI(api_key="ENTER YOUR KEY HERE")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Who developed ChatGPT?"}
    ]
)

print(response.choices[0].message.content)
# Output: ChatGPT was developed by OpenAI, an artificial intelligence research lab.
```

Key points about this structure:
- `client.chat.completions.create(...)` is the method that calls the Chat Completions endpoint.
- `model` specifies which OpenAI model to use (e.g., `"gpt-4o-mini"`).
- `messages` is a list of message dictionaries, each with a `"role"` and `"content"`.
- Valid roles are: `"system"`, `"user"`, `"assistant"`, and `"function"`.
- The response is accessed via `response.choices[0].message.content`.

---

### 1.2 Challenges of a Production Environment

A basic API call is like planning a route with a paper map — it works in isolation but isn't optimized for real-world conditions. A well-structured, production-ready API call is like a GPS: specific, responsive, and reliable.

When integrating the API into production systems, you need to address four categories of challenges:

| Challenge Category | What It Requires |
|---|---|
| **Error Handling** | Display user-friendly error messages; provide alternatives when the service is unavailable |
| **Moderation and Safety** | Control unwanted inputs; minimize risk of data leaks |
| **Testing and Validation** | Check for off-topic responses; test for inconsistent behavior |
| **Communication with External Systems** | Call external functions and APIs; optimize response times |

> These are not just nice-to-haves — they are essential requirements for any AI application that real users will interact with.

---

### 1.3 Requesting JSON Output

For integration with external applications and downstream pipelines, it is preferable to receive model output in a **structured format like JSON** rather than unstructured plain text. JSON is widely recognized, easily parsed, and allows other parts of a system to access specific fields reliably.

This is done using the `response_format` parameter in the API request:

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": "Please write down five trees with their scientific names in json format."
        }
    ],
    response_format={"type": "json_object"}
)
```

**Two things are required when using JSON mode:**
1. Set `response_format={"type": "json_object"}` in the API call.
2. Also mention the desired JSON format explicitly **in the prompt itself** — the model uses both signals.

**Example output when JSON mode is active:**
```json
{
  "trees": [
    {"commonName": "Oak", "scientificName": "Quercus"},
    {"commonName": "Maple", "scientificName": "Acer"},
    {"commonName": "Pine", "scientificName": "Pinus"},
    {"commonName": "Birch", "scientificName": "Betula"},
    {"commonName": "Willow", "scientificName": "Salix"}
  ]
}
```

Without JSON mode, the same prompt might return a plain text list or a narrative response that is harder to parse programmatically.

---

### 1.4 Extracting the Response

The Chat Completions API returns a **response object** with several accessible fields. The most important access pattern is:

```python
response.choices[0].message.content
```

Breaking this down:
- `response.choices` — a list of possible completions (usually just one)
- `[0]` — access the first (and typically only) choice
- `.message` — the message object returned by the model
- `.content` — the actual text string of the model's response

> Important: `response.choices[0]` alone gives you the full choice object, not the text. `response.choices.content.message` is **incorrect** — the correct path always goes through `.choices[0].message.content`.

---

## 2. Handling Errors

### 2.1 Why Error Handling Matters

Error handling in AI applications goes beyond fixing code bugs. Because AI systems are typically complex, **simplifying the user experience** is critical — errors should be caught gracefully, with clear, human-readable messages, rather than exposing raw stack traces to the end user.

Well-handled errors eliminate barriers to using the application and increase trust in the system.

---

### 2.2 Error Types in the OpenAI Python Library

There are four main categories of errors you will encounter when using the OpenAI API.

#### Category 1: Connection Errors

Caused by network or server issues on either the user's side or OpenAI's side.

| Error | Description |
|---|---|
| `InternalServerError` | A server-side error occurred on OpenAI's end |
| `APIConnectionError` | The client could not connect to the API |
| `APITimeoutError` | The request timed out before a response was received |

**Solutions:**
- Check your internet connection and any firewall settings
- Wait a few minutes and retry
- Contact OpenAI support if the issue persists

---

#### Category 2: Resource Limits Errors

Caused by exceeding the API's restrictions on request frequency or payload size.

| Error | Description |
|---|---|
| `RateLimitError` | Too many requests sent in a given time window |
| `ConflictError` | A conflicting operation is already in progress |

**Solutions:**
- Pace your requests (add delays between them)
- Reduce the amount of text sent per request
- Use batching (covered in Section 3)

---

#### Category 3: Authentication Errors

Caused by invalid or missing credentials. These require **code-level fixes**.

| Error | Description |
|---|---|
| `AuthenticationError` (HTTP 401) | API key or token is invalid, expired, or revoked |

**Example that triggers this error:**
```python
client = OpenAI(api_key="This is an Invalid Key")
# AuthenticationError: Error code: 401 - Incorrect API key provided
```

**Solutions:**
- Verify the API key is copied correctly and is active
- If expired, generate a new key from the OpenAI account dashboard at `platform.openai.com/account/api-keys`

---

#### Category 4: Bad Request Errors

Caused by malformed requests — wrong parameter types, missing required fields, or invalid values.

| Error | Description |
|---|---|
| `BadRequestError` (HTTP 400) | Request is missing required parameters or contains invalid values |

**Example that triggers this error:**
```python
messages=[{"role": "This is not a Valid Role", "content": "..."}]
# BadRequestError: 'NotARole' is not one of ['system','assistant','user','function']
```

**Solutions:**
- Read the error message carefully — it usually specifies exactly what is wrong
- Review the API documentation for the endpoint being called
- Ensure all required keys (`"role"`, `"content"`) are present and valid in every message dictionary

---

### 2.3 Handling Exceptions with try/except

To prevent errors from crashing the application entirely, wrap API calls in `try/except` blocks. Python evaluates `except` clauses in order, so place more specific exceptions first and a generic catch-all last.

```python
try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "List five data science professions."}]
    )
    print(response.choices[0].message.content)

except openai.AuthenticationError as e:
    print(f"OpenAI API failed to authenticate: {e}")
    pass

except openai.RateLimitError as e:
    print(f"OpenAI API request exceeded rate limit: {e}")
    pass

except Exception as e:
    print(f"Unable to generate a response. Exception: {e}")
    pass
```

**How this works:**
- The code in the `try` block is executed first.
- If a specific OpenAI error occurs (e.g., `AuthenticationError`), the corresponding `except` block runs and the program continues.
- If any other unexpected error occurs, the final generic `except Exception` block catches it.
- Using `pass` after printing the error allows the program to continue running rather than crashing.

> The goal is not to silently ignore errors, but to handle them gracefully so the user sees a helpful message rather than a cryptic traceback.

---

## 3. Batching and Rate Limits

### 3.1 What are Rate Limits?

Rate limits are restrictions on how frequently or how heavily you can use the API within a given time window. Think of them like traffic regulations on a highway — they exist to:
- Prevent any single user from monopolizing the service
- Protect against malicious attacks (e.g., flood requests)
- Ensure fair distribution of resources across all users within an organization

When a rate limit is hit, the API returns a `RateLimitError`.

---

### 3.2 How Rate Limits Occur

There are two distinct ways a rate limit can be triggered:

| Cause | Description |
|---|---|
| **Too many requests** | The number of API calls within a given time window exceeds the allowed limit |
| **Too much text** | The number of tokens in the request exceeds the model's or account's token limit |

These two causes require different solutions:
- Too many requests → use **retry** or **batching**
- Too much text → **reduce tokens**

---

### 3.3 Solution 1: Retry with Exponential Backoff

When requests may occasionally exceed rate limits due to high frequency, configure the function to **automatically retry** with increasing delays between attempts. This is called **exponential backoff**.

The Python `tenacity` library provides a clean decorator-based way to do this:

```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential
)

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_response(model, message):
    response = client.chat.completions.create(
        model=model,
        messages=[message],
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content
```

**Key parameters explained:**

| Parameter | Function | Description |
|---|---|---|
| `wait=wait_random_exponential(min=1, max=60)` | Controls the delay between retries | Starts at a minimum of 1 second, grows exponentially up to 60 seconds maximum, with randomness to avoid thundering herd |
| `stop=stop_after_attempt(6)` | Sets the maximum number of retries | After 6 failed attempts, the error is raised |

**What is a decorator?**
A decorator (`@retry(...)`) is a way to modify a function's behavior without changing its internal code. Here it wraps `get_response()` so that it automatically retries when it fails, without any changes to the function logic itself.

**Why exponential backoff?**
Retrying immediately and repeatedly after a failure would just keep hitting the rate limit. Exponential backoff gives the API time to recover between retries, and the randomness prevents multiple clients from all retrying at exactly the same moment.

---

### 3.4 Solution 2: Batching

**Batching** means sending multiple items/questions in a single API call rather than making one call per item. This is the preferred approach when the **frequency** of requests (not the token count) is the problem.

**Without batching (inefficient — one call per country):**
```python
for country in ["United States", "Ireland", "India"]:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": country}]
    )
```
This sends 3 separate API calls.

**With batching (efficient — one call for all countries):**
```python
countries = ["United States", "Ireland", "India"]

message = [
    {
        "role": "system",
        "content": """You are given a series of countries and are asked to return the
        country and capital city. Provide each of the questions with an answer in the
        response as separate content."""
    }
]

[message.append({"role": "user", "content": i}) for i in countries]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=message
)

print(response.choices[0].message.content)
# United States: Washington D.C.
# Ireland: Dublin
# India: New Delhi
```

**How batching works:**
- One `"system"` message sets the overall instructions for the batch
- Each item from the list is appended as a separate `"user"` message
- A single API call processes all items together
- The model returns all answers in one response

> The system message must explicitly instruct the model to answer each item, since all items arrive as separate user messages in the same call.

---

### 3.5 Solution 3: Reducing Tokens with tiktoken

When the problem is **too many tokens** (not too many requests), the solution is to measure and reduce the token count of your prompts.

**What are tokens?**
Tokens are chunks of text — they can be full words, or groups of characters that commonly appear together. One word is typically 1–2 tokens. Tokens are the unit of measurement the API uses for both input and output limits.

**Using the `tiktoken` library to count tokens:**

```python
import tiktoken

# Create the encoding for the specific model you are using
encoding = tiktoken.encoding_for_model("gpt-4o-mini")

prompt = "Tokens can be full words, or groups of characters commonly grouped together: tokenization."

# Count the tokens
num_tokens = len(encoding.encode(prompt))
print("Number of tokens in prompt:", num_tokens)
# Number of tokens in prompt: 17
```

**Step-by-step:**
1. `tiktoken.encoding_for_model("gpt-4o-mini")` — creates an encoding object for the specific model (each model may tokenize slightly differently)
2. `encoding.encode(prompt)` — converts the text string into a list of token IDs
3. `len(...)` — counts the total number of tokens

**Why this matters:**
- Each OpenAI model has a **maximum context window** (token limit for input + output combined)
- Exceeding it triggers a `RateLimitError` or an error specific to context length
- You can use `tiktoken` to check that a prompt stays within limits **before** sending it to the API

**Practical use pattern:**
```python
num_tokens = len(encoding.encode(input_message["content"]))

if num_tokens <= 100:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[input_message]
    )
    print(response.choices[0].message.content)
else:
    print("Message exceeds token limit")
```

---

## 4. Exercise Solutions

### Exercise 1 — Decoding the Response
**Question:** You submitted a request to the API to list three Python libraries with the year they were first released. What is the correct way to extract the content of the message only?

**Correct Answer:**
```python
response.choices[0].message.content
```

**Why the others are wrong:**
- `response.choices[0]` — returns the full choice object, not just the text content
- `response.choices.content.message` — incorrect structure; `.choices` is a list, so you must index it first with `[0]`, then access `.message`, then `.content`

---

### Exercise 2 — Formatting Model Response as JSON
**Task:** As a librarian, use the OpenAI API to convert text notes about books into structured JSON.

**Correct Solution:**
```python
# Create the OpenAI client
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Create the request
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": "I have these notes with book titles and authors: New releases this week! The Beholders by Hester Musson, The Mystery Guest by Nita Prose. Please organize the titles and authors in a json file."
        }
    ],
    # Specify the response format
    response_format={"type": "json_object"}
)

# Print the response
print(response.choices[0].message.content)
```

**Key things demonstrated:**
- `OpenAI(api_key=...)` initializes the client
- `client.chat.completions.create(...)` creates the Chat Completions request
- `response_format={"type": "json_object"}` forces JSON output
- The prompt itself also specifies JSON format ("Please organize the titles and authors in a json file")
- Response is extracted with `response.choices[0].message.content`

---

### Exercise 3 — Interpreting Error Messages
**Task:** Match each error's definition and solution to the correct error type.

| Error Type | Definition | Possible Solution |
|---|---|---|
| `AuthenticationError` | Your API key or token was invalid, expired, or revoked | Check that your API key or token is correct and has not been revoked or expired |
| `BadRequestError` | Your request is missing required parameters, or some of the parameters are invalid | Double check the variables and parameters you are passing as input and ensure they are valid and in the correct format |
| `RateLimitError` | You have exceeded the number of requests you can send within a given time | Decrease the number of requests you are sending to the API within a given time |

**Memory tip:**
- **Authentication** = identity problem (who are you?) → check your key
- **BadRequest** = structure problem (what did you send?) → check parameters
- **RateLimit** = volume problem (how much did you send?) → slow down

---

### Exercise 4 — Handling Exceptions
**Task:** Build an application that catches authentication errors and displays a friendly message.

**Correct Solution:**
```python
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Use the try statement
try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[message]
    )
    # Print the response
    print(response.choices[0].message.content)

# Use the except statement to catch authentication errors
except openai.AuthenticationError:
    print("Please double check your authentication key and try again, the one provided is not valid.")
```

**Key takeaways:**
- The `try` block wraps the API call and the success path (printing the response)
- The `except openai.AuthenticationError:` block catches only this specific error type
- The custom message replaces a raw Python traceback with something a non-technical user can understand
- No `except Exception` catch-all is needed here since the task only asks for authentication error handling

---

### Exercise 5 — Avoiding Rate Limits with Retry
**Task:** Add a `@retry` decorator using the `tenacity` library to retry at 5-second intervals up to 40 seconds maximum, stopping after 4 attempts.

**Correct Solution:**
```python
# Import the tenacity library
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential
)

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Add the appropriate parameters to the decorator
@retry(wait=wait_random_exponential(min=5, max=40), stop=stop_after_attempt(4))
def get_response(model, message):
    response = client.chat.completions.create(
        model=model,
        messages=[message]
    )
    return response.choices[0].message.content

print(get_response("gpt-4o-mini", {"role": "user", "content": "List ten holiday destinations."}))
```

**Parameter mapping from the instructions:**
- "start retrying at an interval of 5 seconds" → `min=5`
- "up to 40 seconds" → `max=40`
- "stop after 4 attempts" → `stop_after_attempt(4)`

> Important: The interval values must match exactly — using `min=1, max=60` instead of `min=5, max=40` would cause the exercise to time out.

---

### Exercise 6 — Batching Messages
**Task:** A fitness app needs to convert distance measurements from kilometers to miles. Instead of looping, batch all measurements in a single API call using a `system` message.

**Correct Solution:**
```python
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

messages = []

# Provide a system message and user messages to send the batch
messages.append({
    "role": "system",
    "content": "You are a helpful assistant. Convert the following measurements from kilometers to miles and present them in a table."
})

# Append measurements to the message
[messages.append({"role": "user", "content": str(i)}) for i in measurements]

response = get_response(messages)
print(response)
```

**Why this approach is better than a `for` loop:**
- A `for` loop would send one API request per measurement — potentially hitting rate limits
- Batching sends all measurements in one request — one call processes everything
- The `system` message tells the model how to handle and format all items together

---

### Exercise 7 — Setting Token Limits
**Task:** An e-commerce customer service bot should only process messages under 100 tokens. Use `tiktoken` to gate the API call.

**Correct Solution:**
```python
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

input_message = {"role": "user", "content": "I'd like to buy a shirt and a jacket. Can you suggest two color pairings for these items?"}

# Use tiktoken to create the encoding for your model
encoding = tiktoken.encoding_for_model("gpt-4o-mini")

# Check for the number of tokens
num_tokens = len(encoding.encode(input_message["content"]))

# Run the chat completions function and print the response
if num_tokens <= 100:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[input_message]
    )
    print(response.choices[0].message.content)
else:
    print("Message exceeds token limit")
```

**Key observations:**
- `encoding_for_model("gpt-4o-mini")` creates a model-specific tokenizer
- `encoding.encode(input_message["content"])` tokenizes only the message `content` string (not the whole dictionary)
- `len(...)` gives the token count
- The `if/else` gate prevents oversized messages from being sent, avoiding a rate limit error before it occurs

---

## Summary: Chapter 1 at a Glance

| Topic | Core Concept |
|---|---|
| **API Call Structure** | Initialize client → create request with model + messages → extract `response.choices[0].message.content` |
| **JSON Output** | Set `response_format={"type": "json_object"}` AND mention JSON in the prompt |
| **Production Challenges** | Error handling, moderation/safety, testing/validation, external system communication |
| **Error Categories** | Connection (network), Resource limits (rate/tokens), Authentication (bad key), Bad Request (malformed parameters) |
| **try/except** | Wrap API calls to catch specific OpenAI errors + a generic fallback; show user-friendly messages |
| **Rate Limits** | Caused by too many requests OR too many tokens; solutions differ for each cause |
| **Retry / Backoff** | Use `tenacity` `@retry` decorator with `wait_random_exponential` and `stop_after_attempt` |
| **Batching** | One `system` message + multiple `user` messages in a single API call; far more efficient than looping |
| **Token Counting** | Use `tiktoken.encoding_for_model()` then `len(encoding.encode(text))` to count tokens before sending |
