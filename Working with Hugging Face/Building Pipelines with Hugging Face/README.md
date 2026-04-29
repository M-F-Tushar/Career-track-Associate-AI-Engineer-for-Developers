# Working with Hugging Face
## Segment 2 — Building Pipelines with Hugging Face

*Comprehensive Revision Guide*

---

## Table of Contents

1. [Text Classification](#1-text-classification)
2. [Text Summarization](#2-text-summarization)
3. [Auto Models and Tokenizers](#3-auto-models-and-tokenizers)
4. [Document Question Answering](#4-document-question-answering)
5. [Choosing the Right Task and Approach](#5-choosing-the-right-task-and-approach)
6. [Practical Code Patterns](#6-practical-code-patterns)
7. [Summary Cheat Sheet](#7-summary-cheat-sheet)

---

## 1. Text Classification

### 1.1 What is Text Classification?

Text classification is the process of labeling input text with one or more predefined categories. It is one of the most widely applied natural language processing tasks and forms the foundation for many real-world AI systems including review analysis, spam detection, content moderation, and recommendation systems.

The course covers four distinct types of text classification, each serving a different purpose but all using the `"text-classification"` task in a pipeline — the model chosen is what determines which type of classification is performed.

### 1.2 Type 1: Sentiment Analysis

Sentiment analysis labels text based on its emotional tone. The standard output labels are **Positive** and **Negative**, though some models also include **Neutral**.

```python
from transformers import pipeline

# Create a sentiment analysis pipeline
sentiment_pipeline = pipeline(task="text-classification", model="<sentiment-model>")

# Run inference
output = sentiment_pipeline("I love pineapple on pizza")
print(output)
# Returns: [{'label': 'POSITIVE', 'score': 0.99}]
```

The output is a list of dictionaries, each containing a `label` (the predicted class) and a `score` (the model's confidence, between 0 and 1).

**Use cases:** product reviews, social media monitoring, customer feedback analysis.

### 1.3 Type 2: Grammatical Correctness

Grammatical correctness classification checks whether a piece of text follows proper grammatical rules. The output labels are typically `LABEL_0` (unacceptable / incorrect grammar) and `LABEL_1` (acceptable / correct grammar) — the exact label names depend on the specific model used.

**Exercise example — Grammatical Correctness:**

```python
# Create a pipeline for grammar checking
grammar_checker = pipeline(
    task="text-classification",
    model="abdulmatinomotoso/English_Grammar_Checker"
)

# Check grammar of the input text
output = grammar_checker("I will walk dog")
print(output)
# Returns: [{'label': 'LABEL_0', 'score': 0.99}]  <- grammatically incorrect
```

A sentence like `"He eat pizza every day"` is labeled `LABEL_0` (incorrect) with a very high confidence score of 0.99. **Use cases:** grammar checkers, language learning tools, writing assistants.

### 1.4 Type 3: Question Natural Language Inference (QNLI)

QNLI checks whether a given **premise** (a piece of text) contains enough information to answer a posed **question**. The possible outputs are:

- **Entailment** (`LABEL_0`) — the premise *does* answer the question.
- **Not Entailment** (`LABEL_1`) — the premise does *not* answer the question.

**Exercise example — QNLI:**

```python
# Create the pipeline
classifier = pipeline(
    task="text-classification",
    model="cross-encoder/qnli-electra-base"
)

# Pass the question and premise as a comma-separated string
output = classifier("Where is the capital of France?, Brittany is known for its stunning coastline.")
print(output)
# Returns: Not Entailment — the premise does not answer the question
```

> **Important:** For QNLI pipelines, the question and premise must be passed together as a single string, **separated by a comma**. The model reads the comma as the boundary between the two inputs.

**Use cases:** question-answering systems, fact-checking applications.

### 1.5 Type 4: Dynamic Category Assignment (Zero-Shot Classification)

Dynamic category assignment classifies text into user-defined categories **without the model having been explicitly trained on those categories**. This is called **zero-shot classification** because the model receives zero training examples for the specific categories it is being asked to classify into.

Unlike the other three types — where the category names are fixed by the model's training — zero-shot classification lets you define any set of category labels at runtime.

**Exercise example — Dynamic Category Assignment:**

```python
text = "AI-powered robots assist in complex brain surgeries with precision."

# Create the pipeline — note the different task name
classifier = pipeline(
    task="zero-shot-classification",
    model="facebook/bart-large-mnli"
)

# Create the categories list
categories = ["politics", "science", "sports"]

# Predict the output
output = classifier(text, categories)

# Print the top label and its score
print(f"Top Label: {output['labels'][0]} with score: {output['scores'][0]}")
```

The output from a zero-shot pipeline has a different structure: `output['labels']` is a list of category names ranked by confidence, and `output['scores']` is the corresponding list of confidence scores. To get the top result, access index `[0]` of both lists.

> **Note:** Because the model was not trained specifically for your custom labels, results may occasionally be surprising. For example, the course notes that when classifying a newsletter feature request, the model chose "support" over "marketing" — a reminder that zero-shot models generalize from their training data and may not always match human intuition for niche category definitions.

**Use cases:** content moderation, recommendation systems, dynamic customer query routing.

### 1.6 Challenges of Text Classification

The course explicitly identifies three challenges that all text classification approaches must grapple with:

**Ambiguity** — text can have multiple valid interpretations, making a single-label assignment difficult.

**Sarcasm and irony** — these are extremely difficult for models to detect reliably because the literal meaning of the words contradicts the intended meaning.

**Multilingual complexity** — processing text in multiple languages requires tailored preprocessing and models specifically trained for each language's grammatical and syntactic structures.

Addressing these challenges demands advanced preprocessing pipelines and more robust, often larger, models.

---

## 2. Text Summarization

### 2.1 What is Summarization?

Summarization is the process of reducing a large piece of text into a shorter one while retaining the key information. The pipeline task string is `"summarization"`.

### 2.2 Extractive vs. Abstractive Summarization

There are two fundamentally different approaches to summarization, and understanding their trade-offs is essential for choosing the right model.

| Dimension | Extractive | Abstractive |
|:---|:---|:---|
| Mechanism | Selects and copies key sentences directly from the source text | Generates entirely new sentences that capture the main ideas |
| Flexibility | Low — output is constrained to original phrasing | High — output is rephrased for clarity and readability |
| Resources | Fewer computational resources required | More computationally intensive |
| Coherence | May produce less cohesive summaries | Produces more natural, readable summaries |
| Fabrication risk | None — only copies existing sentences | May introduce information not in the original text |
| Best for | Legal documents, financial research (accuracy critical) | News articles, content recommendations (readability critical) |

The key difference in *implementation* between extractive and abstractive summarization lies entirely in the **model chosen** — the `pipeline` task string (`"summarization"`) is the same for both. You select an extractive or abstractive model by choosing the appropriate model name.

### 2.3 Implementing Summarization

**Abstractive summarization exercise example — Summarizing Long Text:**

```python
# Create the summarization pipeline
summarizer = pipeline(
    task="summarization",
    model="cnicu/t5-small-booksum"
)

# Summarize the text
summary_text = summarizer(original_text)

# Compare the length of the original and summary text
print(f"Original text length: {len(original_text)}")
print(f"Summary length: {len(summary_text[0]['summary_text'])}")
```

The output is a list of dictionaries. The summarized text is stored under the `'summary_text'` key, so you access it with `summary_text[0]['summary_text']`.

The `distilbart` model is specifically mentioned in the course as a model designed for generating abstractive summaries.

### 2.4 Controlling Summary Length with Token Parameters

Two parameters control the length of the generated summary. Both are set directly when instantiating the pipeline.

| Parameter | Effect |
|:---|:---|
| `min_new_tokens` | Sets the minimum number of tokens the summary must contain |
| `max_new_tokens` | Sets the maximum number of tokens the summary can contain |

These are useful for: space-constrained environments (small storage or UI display limits), improving readability by preventing overly short or overly long outputs, and matching the quality requirements of different downstream applications.

**Exercise example — Adjusting the Summary Length (short):**

```python
# Generate a summary between 1 and 10 tokens
short_summarizer = pipeline(
    task="summarization",
    model="cnicu/t5-small-booksum",
    min_new_tokens=1,
    max_new_tokens=10
)

short_summary_text = short_summarizer(original_text)
print(short_summary_text[0]["summary_text"])
```

**Exercise example — Adjusting the Summary Length (long):**

```python
# Generate a summary between 50 and 150 tokens
long_summarizer = pipeline(
    task="summarization",
    model="cnicu/t5-small-booksum",
    min_new_tokens=50,
    max_new_tokens=150
)

long_summary_text = long_summarizer(original_text)
print(long_summary_text[0]["summary_text"])
```

> **Reminder:** Tokens are the basic units of text that language models process. A token is roughly a word or a sub-word fragment — they are not identical to characters or words.

---

## 3. Auto Models and Tokenizers

### 3.1 Pipelines vs. Auto Classes

The `pipeline` class is fast and convenient, but it abstracts away all control over the underlying process. For tasks that require fine-grained customization, Hugging Face provides **Auto classes**, which give direct access to the model and tokenizer as separate, individually configurable objects.

The choice between them is tested directly in the drag-and-drop exercise: pipelines are appropriate for quick experiments and standard tasks, while Auto classes are required when customization is needed.

| Use Case | Approach |
|:---|:---|
| Quickly compare multiple models for text generation | Pipelines |
| Simple text summarization for news articles | Pipelines |
| Quick sentiment classification of customer reviews | Pipelines |
| Customer support model that should prioritize 'Urgent' more often (custom thresholding) | Auto Classes |
| Financial report tokenization with custom tokens like 'EBITDA' or 'ROI' | Auto Classes |

### 3.2 AutoModels

`AutoModel` classes download and load a specific pre-trained model. The class name encodes the task: for text classification (sequence classification), you use `AutoModelForSequenceClassification`. Other tasks have their own corresponding Auto class names.

```python
from transformers import AutoModelForSequenceClassification

# Load the model by its Hub name
my_model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased-finetuned-sst-2-english"
)
```

The `.from_pretrained()` method downloads the model weights from the Hub using the model name as the identifier.

### 3.3 AutoTokenizers and How Tokenization Works

Before text can be fed to a model, it must be converted into a numerical representation the model understands. This is the job of the **tokenizer**. Every model was trained with a specific tokenizer, and it is critical to use the *same* tokenizer during inference to ensure the text is processed identically to how it was during training. With pipelines, this pairing happens automatically; with Auto classes, you must handle it yourself.

A tokenizer performs two main operations:

1. **Cleaning** — lowercasing text, removing accents, and other normalization steps.
2. **Splitting** — dividing the cleaned text into **tokens** (sub-word units).

Different models tokenize the same input differently, which is why the tokenizer must be paired with its corresponding model.

**Exercise example — Tokenizing Text with AutoTokenizer:**

```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Load the tokenizer for the specific model
tokenizer = AutoTokenizer.from_pretrained(
    "distilbert-base-uncased-finetuned-sst-2-english"
)

# Split input text into tokens
tokens = tokenizer.tokenize("AI: Making robots smarter and humans lazier!")

# Display the tokenized output
print(f"Tokenized output: {tokens}")
```

The `.tokenize()` method returns a list of token strings showing exactly how the model will process the input text.

### 3.4 Building a Custom Pipeline with Auto Classes

Once you have both the model and tokenizer loaded separately, you can combine them with the `pipeline()` function to create a fully custom pipeline that gives you the benefits of both the Auto class flexibility and the pipeline interface's convenience.

**Exercise example — Using AutoClasses:**

```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

# Download the model and tokenizer
my_model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased-finetuned-sst-2-english"
)
my_tokenizer = AutoTokenizer.from_pretrained(
    "distilbert-base-uncased-finetuned-sst-2-english"
)

# Create the pipeline with explicit model and tokenizer
my_pipeline = pipeline(
    task="sentiment-analysis",
    model=my_model,
    tokenizer=my_tokenizer
)

# Predict the sentiment
output = my_pipeline("This course is pretty good, I guess.")
print(f"Sentiment using AutoClasses: {output[0]['label']}")
```

By passing `model=my_model` and `tokenizer=my_tokenizer` explicitly to `pipeline()`, you take control of exactly which model and tokenizer are used, while still leveraging the pipeline's clean inference interface.

### 3.5 Why and When to Use Auto Classes

The three scenarios where Auto classes are preferred over simple pipelines:

**Advanced text preprocessing and tokenization** — adding custom tokens to the vocabulary (e.g., domain-specific abbreviations like `EBITDA` or `ROI` in finance), applying domain-specific text cleaning before tokenization, or controlling normalization behavior.

**Custom thresholding in classification** — setting category-specific confidence thresholds to bias predictions toward certain classes. For example, configuring a customer support model to label tickets as `'Urgent'` more aggressively by lowering the confidence threshold required for that label.

**Complex multi-stage workflows** — when you need to integrate the model into a larger pipeline involving multiple processing steps, custom pre- and post-processing logic, or integration with other libraries.

---

## 4. Document Question Answering

### 4.1 What is Document QA?

Document Question Answering (Document QA) generates answers to questions about the content of a document. It requires two inputs: a **document** (typically a PDF or long text passage) and a **question** (a natural language string). The answer is extracted or synthesized from the document's content.

The pipeline task string is `"question-answering"`.

### 4.2 Use Cases for Document QA

| Industry | Application |
|:---|:---|
| Legal | Identifying specific clauses in contracts (e.g., termination terms) |
| Finance | Extracting key figures like revenue and expenses from reports |
| HR / Internal Ops | Answering employee questions about policies from HR documents |
| Customer Support | Retrieving answers to common questions from manuals or FAQs |

### 4.3 Extracting Text from a PDF with pypdf

Before you can run a QA pipeline on a PDF, you must extract its text as a Python string. The course uses the **`pypdf`** library and its `PdfReader` class for this.

**Exercise example — Extracting Text with PyPDF:**

```python
from pypdf import PdfReader

# Load the PDF file
reader = PdfReader("US_Employee_Policy.pdf")

# Extract text from all pages
document_text = ""
for page in reader.pages:
    document_text += page.extract_text()

print(document_text)
```

Key steps and components:

- `PdfReader("path/to/file.pdf")` — loads the PDF.
- `reader.pages` — the `.pages` attribute returns an iterable of all pages.
- `page.extract_text()` — extracts the text content of a single page as a string.
- The loop concatenates all pages into a single `document_text` string, which becomes the `context` for the QA pipeline.

### 4.4 Building the QA Pipeline

Once the text has been extracted, it is passed to the `question-answering` pipeline as the `context` parameter. The question is passed as the `question` parameter.

**Exercise example — Building a QA Pipeline:**

```python
# Load the question-answering pipeline
qa_pipeline = pipeline(
    task="question-answering",
    model="distilbert-base-cased-distilled-squad"
)

question = "What is the notice period for resignation?"

# Get the answer from the QA pipeline
result = qa_pipeline(question=question, context=document_text)

# Print the answer
print(f"Answer: {result['answer']}")
```

The output is a dictionary. The extracted answer text is stored under the `'answer'` key.

The `distilbert-base-cased-distilled-squad` model is the specific model used in the exercise — it is a lightweight, efficient model well-suited for extractive QA tasks.

### 4.5 Full End-to-End Document QA Pipeline

Combining the PDF extraction and QA pipeline gives a complete system. The course recommends wrapping this into a reusable function so that users can submit any question without modifying the code:

```python
from pypdf import PdfReader
from transformers import pipeline

# Step 1: Extract text from the PDF
reader = PdfReader("US_Employee_Policy.pdf")
document_text = ""
for page in reader.pages:
    document_text += page.extract_text()

# Step 2: Set up the QA pipeline
qa_pipeline = pipeline(
    task="question-answering",
    model="distilbert-base-cased-distilled-squad"
)

# Step 3: Ask a question
question = "How many volunteer days does the policy allow per year?"
result = qa_pipeline(question=question, context=document_text)
print(f"Answer: {result['answer']}")
# Returns: Answer: 1
```

The answer `1` is a direct extraction from the policy document — the pipeline found and returned the specific value mentioned in the relevant passage.

---

## 5. Choosing the Right Task and Approach

### 5.1 Matching Real-World Scenarios to Tasks

The course tests this via a drag-and-drop exercise. Understanding which task is appropriate for which scenario is a core competency.

| Scenario | Correct Task |
|:---|:---|
| Evaluate social media posts for positivity or negativity | Text Classification |
| Label news articles as Politics, Sports, or Technology | Text Classification |
| Turn a detailed contract into a short list of key clauses for client understanding | Summarization |
| Create a brief overview of a 10-page financial report for busy executives | Summarization |
| Locate the total revenue for Q3 from a financial report | Question Answering |
| Find the maternity leave policy details from a company document | Question Answering |

**The distinguishing logic:**

- **Text Classification** → you want a *label* applied to a piece of text.
- **Summarization** → you want a *condensed version* of a long text.
- **Question Answering** → you want a *specific fact or value* extracted from a document in response to a direct question.

### 5.2 Matching Scenarios to Pipelines vs. Auto Classes

The course also tests when to use pipelines versus Auto classes:

| Scenario | Correct Approach |
|:---|:---|
| Quickly compare multiple models for text generation tasks | Pipelines |
| Simple text summarization for news articles | Pipelines |
| Quick way to classify customer reviews as positive or negative | Pipelines |
| Customer support model should prioritize 'Urgent' category more often | Auto Classes |
| Task requires tokenizing financial reports with custom tokens like 'EBITDA' or 'ROI' | Auto Classes |

---

## 6. Practical Code Patterns

### Pattern 1: Sentiment Analysis Pipeline

```python
from transformers import pipeline

sentiment_pipeline = pipeline(task="text-classification", model="<sentiment-model>")
output = sentiment_pipeline("I love pineapple on pizza")
print(output)  # [{'label': 'POSITIVE', 'score': 0.99}]
```

### Pattern 2: Grammar Checking Pipeline

```python
from transformers import pipeline

grammar_checker = pipeline(
    task="text-classification",
    model="abdulmatinomotoso/English_Grammar_Checker"
)
output = grammar_checker("I will walk dog")
print(output)
```

### Pattern 3: QNLI Pipeline

```python
from transformers import pipeline

classifier = pipeline(
    task="text-classification",
    model="cross-encoder/qnli-electra-base"
)
# Question and premise passed as a single comma-separated string
output = classifier("Where is the capital of France?, Brittany is known for its stunning coastline.")
print(output)
```

### Pattern 4: Zero-Shot Classification Pipeline

```python
from transformers import pipeline

text = "AI-powered robots assist in complex brain surgeries with precision."

classifier = pipeline(
    task="zero-shot-classification",
    model="facebook/bart-large-mnli"
)

categories = ["politics", "science", "sports"]
output = classifier(text, categories)

print(f"Top Label: {output['labels'][0]} with score: {output['scores'][0]}")
```

### Pattern 5: Abstractive Summarization Pipeline

```python
from transformers import pipeline

summarizer = pipeline(
    task="summarization",
    model="cnicu/t5-small-booksum"
)

summary_text = summarizer(original_text)
print(f"Original text length: {len(original_text)}")
print(f"Summary length: {len(summary_text[0]['summary_text'])}")
```

### Pattern 6: Summarization with Length Control

```python
from transformers import pipeline

# Short summary: 1 to 10 tokens
short_summarizer = pipeline(
    task="summarization",
    model="cnicu/t5-small-booksum",
    min_new_tokens=1,
    max_new_tokens=10
)
print(short_summarizer(original_text)[0]["summary_text"])

# Long summary: 50 to 150 tokens
long_summarizer = pipeline(
    task="summarization",
    model="cnicu/t5-small-booksum",
    min_new_tokens=50,
    max_new_tokens=150
)
print(long_summarizer(original_text)[0]["summary_text"])
```

### Pattern 7: Tokenizing Text with AutoTokenizer

```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(
    "distilbert-base-uncased-finetuned-sst-2-english"
)
tokens = tokenizer.tokenize("AI: Making robots smarter and humans lazier!")
print(f"Tokenized output: {tokens}")
```

### Pattern 8: Custom Pipeline with Auto Classes

```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

my_model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased-finetuned-sst-2-english"
)
my_tokenizer = AutoTokenizer.from_pretrained(
    "distilbert-base-uncased-finetuned-sst-2-english"
)

my_pipeline = pipeline(
    task="sentiment-analysis",
    model=my_model,
    tokenizer=my_tokenizer
)

output = my_pipeline("This course is pretty good, I guess.")
print(f"Sentiment using AutoClasses: {output[0]['label']}")
```

### Pattern 9: PDF Text Extraction with pypdf

```python
from pypdf import PdfReader

reader = PdfReader("US_Employee_Policy.pdf")
document_text = ""
for page in reader.pages:
    document_text += page.extract_text()
print(document_text)
```

### Pattern 10: Document QA Pipeline (End-to-End)

```python
from pypdf import PdfReader
from transformers import pipeline

# Extract text
reader = PdfReader("US_Employee_Policy.pdf")
document_text = ""
for page in reader.pages:
    document_text += page.extract_text()

# Build QA pipeline
qa_pipeline = pipeline(
    task="question-answering",
    model="distilbert-base-cased-distilled-squad"
)

# Ask a question
question = "What is the notice period for resignation?"
result = qa_pipeline(question=question, context=document_text)
print(f"Answer: {result['answer']}")
```

---

## 7. Summary Cheat Sheet

### 7.1 Pipeline Task Reference

| Task | Pipeline Task String | Output Key | Notes |
|:---|:---|:---|:---|
| Sentiment analysis | `"text-classification"` | `output[0]['label']`, `output[0]['score']` | Model determines labels (POSITIVE/NEGATIVE) |
| Grammar checking | `"text-classification"` | `output[0]['label']`, `output[0]['score']` | LABEL_0 = incorrect, LABEL_1 = correct (model-dependent) |
| QNLI | `"text-classification"` | `output[0]['label']`, `output[0]['score']` | Pass question + premise as one comma-separated string |
| Zero-shot classification | `"zero-shot-classification"` | `output['labels'][0]`, `output['scores'][0]` | Custom categories passed as a list at runtime |
| Summarization | `"summarization"` | `output[0]['summary_text']` | Use `min_new_tokens` and `max_new_tokens` for length control |
| Question answering | `"question-answering"` | `result['answer']` | Pass `question=` and `context=` as keyword arguments |

### 7.2 Extractive vs. Abstractive Summarization

| Property | Extractive | Abstractive |
|:---|:---|:---|
| Copies original sentences | Yes | No |
| Generates new sentences | No | Yes |
| Risk of fabrication | None | Present |
| Readability | Lower | Higher |
| Resource cost | Lower | Higher |
| Best for | Legal, financial (accuracy first) | News, content (readability first) |

### 7.3 Key Output Structures to Know

| Pipeline | Output Type | How to Access Result |
|:---|:---|:---|
| Text classification | `list` of `dict` | `output[0]['label']`, `output[0]['score']` |
| Zero-shot classification | `dict` with ranked lists | `output['labels'][0]`, `output['scores'][0]` |
| Summarization | `list` of `dict` | `output[0]['summary_text']` |
| Question answering | `dict` | `result['answer']` |

### 7.4 Common Mistakes to Avoid

| Mistake | Better Approach |
|:---|:---|
| Using the same task string for zero-shot classification | Zero-shot uses `"zero-shot-classification"`, not `"text-classification"` |
| Passing question and premise separately for QNLI | Pass them as a single comma-separated string: `"Question?, Premise."` |
| Accessing summarization output directly without indexing | Use `output[0]['summary_text']` — the result is always a list |
| Mixing up extractive and abstractive just by task name | The task string is the same; the model choice determines the method |
| Using the wrong tokenizer with a model | Always use `AutoTokenizer.from_pretrained(model_name)` with the exact same `model_name` as the model |
| Forgetting to loop through PDF pages during text extraction | Always iterate over `reader.pages` and call `.extract_text()` on each page |
| Assuming zero-shot classification is always accurate | The model generalizes from training data; results for niche categories may not match intuition |
| Using pipelines when custom category weights are needed | Use Auto Classes when you need thresholding or customization |

---

*End of Revision Guide — Segment 2: Building Pipelines with Hugging Face*
