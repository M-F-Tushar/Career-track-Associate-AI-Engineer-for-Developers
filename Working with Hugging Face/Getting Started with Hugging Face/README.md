# Working with Hugging Face
## Segment 1 — Getting Started with Hugging Face

*Comprehensive Revision Guide*

---

## Table of Contents

1. [What is Hugging Face?](#1-what-is-hugging-face)
2. [The Hugging Face Hub](#2-the-hugging-face-hub)
3. [Running Hugging Face Models](#3-running-hugging-face-models)
4. [The Transformers Library and the Pipeline](#4-the-transformers-library-and-the-pipeline)
5. [Inference Providers](#5-inference-providers)
6. [Hugging Face Datasets](#6-hugging-face-datasets)
7. [The Datasets Library](#7-the-datasets-library)
8. [Practical Code Patterns](#8-practical-code-patterns)
9. [Summary Cheat Sheet](#9-summary-cheat-sheet)

---

## 1. What is Hugging Face?

### 1.1 The Core Definition

Hugging Face is a platform where the AI community can **access, collaborate, and stay informed** on the latest open-source models, datasets, and applications. Crucially, you do not need to be a Machine Learning Engineer to use it — the platform is designed to be accessible to a wide range of users and skill levels.

### 1.2 What Hugging Face Provides

Hugging Face offers three interconnected things:

**Models** — Pre-trained and fine-tuned machine learning models covering an enormous range of tasks (text generation, image classification, audio processing, and more), uploaded and maintained by both community members and major AI organizations.

**Datasets** — A large collection of community-curated datasets across a variety of tasks, domains, languages, and modalities, used for training, fine-tuning, and evaluating models.

**Applications** — Spaces on the Hub where developers share interactive demos and deployed AI applications built on top of models and datasets.

### 1.3 The Community Behind It

Hugging Face is sustained by a thriving open-source community. Both individual practitioners and major AI organizations — including Google, Meta, and DeepSeek — openly share their latest models and research on the platform. If you compile a dataset, fine-tune a model, or build an application, the course encourages sharing it on Hugging Face so the wider community can benefit.

### 1.4 What This Course Covers

This course covers navigating the Hub to explore models and datasets — both through the browser interface and through Hugging Face's Python libraries — and performing common natural language tasks such as summarization, classification, and document question-answering. It is the first in a series that also covers Hugging Face for LLMs, other modalities (images, audio, video), and efficient model training.

### 1.5 What Hugging Face Does NOT Guarantee

An important concept tested in the exercises: Hugging Face does **not** guarantee model performance across all tasks. Every model has its own strengths, limitations, and evaluation results that must be checked individually on the model card. "Guaranteed model performance across all tasks" is explicitly identified in the exercises as something Hugging Face does *not* provide.

---

## 2. The Hugging Face Hub

### 2.1 Overview

The Hugging Face Hub is the central, browser-accessible place where everything is hosted. From the Hub you can browse models, datasets, and applications; filter by task, modality, language, or license; and begin using or downloading any resource without writing a single line of code.

### 2.2 Finding the Right Model

To find a model on the Hub, navigate to the **Models** section and apply the relevant **task filter** (e.g., Text Generation, Image Classification, Question Answering). Results can be sorted by newest, most downloaded, or trending. You can also search by keyword within the filtered results.

### 2.3 The Model Card

Each model on the Hub has a **model card** — a standardized information page that helps you evaluate whether the model is right for your use case. A model card typically contains:

| Section | What It Tells You |
|:---|:---|
| Model name | The identifier used to load the model in code |
| Uploader | The user or organization that published it |
| Tasks | The tasks the model is designed to perform |
| Modalities | The input/output types the model works with (text, image, audio, etc.) |
| Languages | The natural languages the model was trained on |
| License | How the model can be used commercially and legally |
| Intended use and limitations | The recommended use cases and known failure modes |
| Training parameters | Architecture and hyperparameter details |
| Training datasets | What data was used to train the model |
| Evaluation results | Benchmark metrics for comparing models |
| Research paper | A link to the publication if one exists |

The evaluation results section is particularly important: it allows you to compare a model against others before committing to it.

### 2.4 Running a Model from the Hub

Once you have identified a suitable model, clicking **"Use this model"** presents several options:

**Transformers Python code** — automatically generated code for loading the model using the `pipeline` class for inference, or for training.

**Pre-populated notebooks** — a notebook environment with the transformers code already filled in, ready to run.

**vLLM** — an option to load and serve the model using vLLM, a popular production-grade tool for serving AI models in a fast and memory-efficient way. This is particularly relevant for application developers.

> **Inference** means prediction — for a text generation model, inference is the process of predicting which words should follow an input prompt.

### 2.5 Task Categories on the Hub

The Hub organizes models into task categories across different domains. Examples visible on the Hub interface include:

- **Multimodal:** Audio-Text-to-Text, Image-Text-to-Text, Visual Question Answering, Document Question Answering, Video-Text-to-Text, Any-to-Any
- **Computer Vision:** Depth Estimation, Image Classification, Object Detection, Image Segmentation, Text-to-Image, Image-to-Text, Image-to-Video, Unconditional Image Generation, Video Classification, Text-to-Video, Zero-Shot Image Classification, Mask Generation, Zero-Shot Object Detection, Text-to-3D, Image-to-3D, Image Feature Extraction, Keypoint Detection
- **Natural Language Processing:** Text Generation, Text Classification, Token Classification, Question Answering, Summarization, Translation, and more

### 2.6 Reading a Model Card — Exercise Example

The course uses the `lxyuan/vit-xray-pneumonia-classification` model card as a reading exercise. Key facts from that card: the model supports Image Classification (not image generation), it was uploaded by the user `lxyuan`, it is available under the apache-2.0 license, and it is a fine-tuned version of `google/vit-base-patch16-224-in21k`. The false statement tested was that "the model can also be used for image generation" — the card does not support this claim.

---

## 3. Running Hugging Face Models

### 3.1 The Two Inference Options

When using a Hugging Face model to make predictions (i.e., running inference), there are two main routes:

**Local Inference** — running the computation on your own hardware, whether a physical computer, laptop, or cloud-based development environment. This is free and convenient, but consumer-grade hardware is often too slow for large-parameter LLMs and image/video generation models, which require GPUs that most consumer systems do not have.

**Inference Providers** — sending requests to partner organizations that provide remote access to high-performance machines with powerful GPUs. You send the model name and inputs, the provider runs the computation, and the result is returned to you. This offloads the hardware burden entirely.

### 3.2 Inference Providers: Key Facts

Inference providers are partner organizations connected to Hugging Face's API. Key points:

- It is **free to get started** — Hugging Face provides some inference credits to new users.
- There are **multiple providers** to choose from. The course uses `Together.ai` as the example provider.
- Providers are accessed via the `InferenceClient` from the `huggingface_hub` library.
- Your **Hugging Face API key** (`HF_TOKEN`) is used to authenticate and consume inference credits.
- The correct order to use an inference provider is: import `InferenceClient` → create the client with provider and API key → call `client.chat.completions.create()` with model and messages → print the result. This order is tested directly in the drag-and-drop exercise.

---

## 4. The Transformers Library and the Pipeline

### 4.1 What is the Transformers Library?

The Hugging Face **Transformers** library is a Python package that simplifies working with pre-trained models for both inference and training. It provides a unified interface for loading and using the thousands of models available on the Hub.

### 4.2 The `pipeline` Class

The `pipeline` class is the most convenient way to perform **local inference** with any model on the Hub. It abstracts away the complexity of loading model weights, tokenizers, and pre/post-processing into a single, easy-to-use object.

**Basic usage:**

```python
from transformers import pipeline

# Instantiate the pipeline with a task and a model
gpt2_pipeline = pipeline(task="text-generation", model="openai-community/gpt2")

# Run inference on an input string
result = gpt2_pipeline("What if AI")
# Returns: [{'generated_text': 'What if AI ...'}]
```

Two things must be specified when creating a pipeline: the **task** (e.g., `"text-generation"`) and the **model** (found on the model card on the Hub, e.g., `"openai-community/gpt2"`).

The output is a **list of dictionaries**. For text generation, the generated text is found under the `'generated_text'` key.

### 4.3 Tokens

The course introduces the concept of **tokens**: groups of characters that language models process as their basic unit of input and output. Tokens are not the same as words — a word may be one or more tokens depending on its length and frequency. Token limits are used to control output length.

### 4.4 Adjusting Pipeline Parameters

The pipeline accepts additional keyword arguments to customize output:

**Exercise example — Building a Text Generation Pipeline:**

```python
from transformers import pipeline

gpt2_pipeline = pipeline(task="text-generation", model="openai-community/gpt2")

# Generate 2 sequences, each limited to 10 new tokens
results = gpt2_pipeline("Make AI", max_new_tokens=10, num_return_sequences=2)

for result in results:
    print(result['generated_text'])
```

Key parameters:

| Parameter | Effect |
|:---|:---|
| `max_new_tokens` | Limits the number of new tokens generated (prevents very long outputs) |
| `num_return_sequences` | Requests multiple generated sequences in one call |

When `num_return_sequences > 1`, the output is a list of dictionaries, so you must loop over it to print each generated text individually.

---

## 5. Inference Providers

### 5.1 Setting Up the Inference Client

To use an inference provider, import `InferenceClient` from `huggingface_hub` and create a client object specifying the provider name and your API key.

```python
from huggingface_hub import InferenceClient
import os

client = InferenceClient(
    provider="together",
    api_key=os.environ["HF_TOKEN"]
)
```

The API key is read from an environment variable (`HF_TOKEN`) rather than hard-coded — a standard security best practice.

### 5.2 Running Inference via a Provider

Most modern text generation models accept input as **messages**, using the same role-based conversational interface you may recognize from the OpenAI API. For model inputs, the `user` role is used.

```python
completion = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V3",
    messages=[
        {
            "role": "user",
            "content": "What is the capital of Belgium?"
        }
    ],
)

print(completion.choices[0].message)
```

The response is accessed via `completion.choices[0].message`. This structure is identical to the OpenAI API response format, making it easy for developers already familiar with that API to switch.

### 5.3 Correct Order of Inference Provider Code

The drag-and-drop exercise tests whether you understand the correct sequence of steps:

1. `from huggingface_hub import InferenceClient`
2. `client = InferenceClient(provider="together", api_key=os.environ["HF_TOKEN"])`
3. `completion = client.chat.completions.create(model=..., messages=[...])`
4. `print(completion.choices[0].message)`

---

## 6. Hugging Face Datasets

### 6.1 What Are Hugging Face Datasets?

The Datasets section of the Hub provides a collection of community-curated datasets covering a wide variety of tasks, domains, languages, and modalities. Like models, datasets can be filtered by task, modality, language, format, size, and license.

### 6.2 The Dataset Card

Each dataset on the Hub has a **dataset card** analogous to a model card. It contains:

- How the dataset was compiled and its provenance
- The license it is available under
- The number of rows and size
- The available splits (train, validation, test)
- Metadata tags (task, modality, format, libraries)

### 6.3 The Dataset Viewer and Data Studio

The **Dataset Viewer** allows you to preview the actual rows of a dataset directly in the browser without downloading it, giving you a feel for the data structure and content. The **Data Studio** provides a more detailed exploration interface.

A particularly useful feature is the ability to run **SQL queries** directly on the dataset in the browser. For example, using a `WHERE` clause with the `LIKE` keyword to filter rows containing a specific string is demonstrated in the course. This lets you explore large datasets before deciding to download them.

### 6.4 Reading a Dataset Card — Exercise Example

The course uses the `XenArcAI/MathX-5M` dataset as a reading exercise. Key facts from that card: it contains more than 4 million rows (~4.32M estimated), it is available under the MIT license, it contains only Text modality (not images), and it is called MathX-5M. The dataset has three columns: `problem`, `expected_answer`, and `generated_solution`, and it is designed to help LLMs reason about math problems.

---

## 7. The Datasets Library

### 7.1 What is the Datasets Library?

Hugging Face developed a dedicated Python package called **`datasets`** specifically for interacting with Hub datasets. It allows you to access, download, manipulate, and share datasets with minimal code.

### 7.2 Downloading a Dataset

The `load_dataset()` function downloads a dataset by its Hub path. You can optionally specify a `split` to download only a specific partition.

**Exercise example — Loading Datasets:**

```python
from datasets import load_dataset

# Load the "validation" split of the TIGER-Lab/MMLU-Pro dataset
my_dataset = load_dataset("TIGER-Lab/MMLU-Pro", split="validation")

# Display dataset details
print(my_dataset)
```

Key points about `load_dataset()`:

- The first argument is the **dataset path** — the `owner/dataset-name` string from the Hub URL.
- The `split` parameter accepts `"train"`, `"test"`, or `"validation"` (check the dataset card to see which splits are available for any given dataset).
- Omitting `split` downloads all available splits.

### 7.3 Apache Arrow Format

Most datasets on Hugging Face use **Apache Arrow** as their underlying storage format. Arrow uses **columnar storage** rather than the traditional row-based storage used by formats like CSV. This makes querying and filtering significantly faster, especially for large datasets.

The practical implication is that manipulating Arrow datasets requires different methods than those used with pandas DataFrames.

### 7.4 Filtering Datasets

To filter rows in an Arrow dataset, use the `.filter()` method with a **lambda function** that defines the filtering criterion. The lambda is applied to each row individually and returns `True` for rows that should be kept.

```python
# Filter for rows where the "text" column contains the word "football"
filtered = wikipedia.filter(lambda row: "football" in row["text"])
```

### 7.5 Selecting Rows by Index

To select specific rows by index, use the `.select()` method. Pass a range or list of indices.

```python
# Select the first row from the filtered dataset
example = filtered.select(range(1))
```

To access the content of a specific cell, pass the row index and the column name:

```python
# Access the "text" column of the first row
print(example[0]["text"])
```

**Exercise example — Manipulating Datasets:**

```python
# Filter the dataset for rows with "football" in the text column
filtered = wikipedia.filter(lambda row: "football" in row["text"])

# Create a sample dataset with one example
example = filtered.select(range(1))

# Print the text of the first (and only) result
print(example[0]["text"])
```

### 7.6 Dataset Splits Explained

Datasets are commonly divided into **splits** for use in the machine learning development process:

| Split | Purpose |
|:---|:---|
| `train` | Used to train the model — the largest portion of data |
| `validation` | Used during development to tune hyperparameters and monitor performance |
| `test` | Used for final evaluation — held out until the very end to give an unbiased measure of performance |

Not every dataset includes all three splits. Always check the dataset card to confirm which splits are available.

---

## 8. Practical Code Patterns

### Pattern 1: Local Inference with the Transformers Pipeline

```python
from transformers import pipeline

# Create a text generation pipeline with GPT-2
gpt2_pipeline = pipeline(task="text-generation", model="openai-community/gpt2")

# Generate a single completion
result = gpt2_pipeline("What if AI")
print(result[0]['generated_text'])
```

### Pattern 2: Pipeline with Custom Parameters

```python
from transformers import pipeline

gpt2_pipeline = pipeline(task="text-generation", model="openai-community/gpt2")

# Generate 2 sequences, each limited to 10 new tokens
results = gpt2_pipeline("Make AI", max_new_tokens=10, num_return_sequences=2)

for result in results:
    print(result['generated_text'])
```

### Pattern 3: Inference via an Inference Provider

```python
from huggingface_hub import InferenceClient
import os

# Create the inference client
client = InferenceClient(
    provider="together",
    api_key=os.environ["HF_TOKEN"]
)

# Send a message to the model
completion = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V3",
    messages=[
        {
            "role": "user",
            "content": "What is the capital of Belgium?"
        }
    ],
)

# Access and print the response
print(completion.choices[0].message)
```

### Pattern 4: Loading a Dataset with a Specific Split

```python
from datasets import load_dataset

# Load only the validation split
my_dataset = load_dataset("TIGER-Lab/MMLU-Pro", split="validation")
print(my_dataset)
```

### Pattern 5: Filtering and Selecting from a Dataset

```python
# Filter for rows containing "football" in the "text" column
filtered = wikipedia.filter(lambda row: "football" in row["text"])

# Select the first result
example = filtered.select(range(1))

# Print the text content of that row
print(example[0]["text"])
```

---

## 9. Summary Cheat Sheet

### 9.1 Key Concepts at a Glance

| Concept | Definition |
|:---|:---|
| Hugging Face Hub | Central browser-based platform for models, datasets, and applications |
| Model card | Information page for a model: tasks, license, training data, evaluation results |
| Dataset card | Information page for a dataset: provenance, license, splits, row count |
| Inference | Running a model to make predictions (not training) |
| Token | The basic unit of text processed by a language model; not equivalent to a word |
| Local inference | Running model computation on your own hardware using the Transformers library |
| Inference provider | A third-party partner that provides GPU hardware for running inference via an API |
| `pipeline` | A Transformers class that wraps model loading and inference into a simple interface |
| `InferenceClient` | A class from `huggingface_hub` for communicating with inference providers |
| Apache Arrow | The columnar storage format used by most Hugging Face datasets |
| `load_dataset()` | The `datasets` library function for downloading Hub datasets |
| `.filter()` | Arrow dataset method for retaining rows matching a lambda condition |
| `.select()` | Arrow dataset method for selecting rows by index |
| Dataset split | A partition of a dataset: `train`, `validation`, or `test` |
| vLLM | A production-grade tool for serving AI models efficiently (available from model card) |

### 9.2 Local Inference vs. Inference Providers

| Dimension | Local Inference | Inference Providers |
|:---|:---|:---|
| Cost | Free | Free credits provided; pay-as-you-go beyond that |
| Hardware requirement | Your own CPU/GPU | Provider's remote GPUs |
| Speed | Slow for large models on consumer hardware | Fast — high-performance machines |
| Best for | Small models, development, experimentation | Large LLMs, image/video generation |
| Library used | `transformers` (`pipeline`) | `huggingface_hub` (`InferenceClient`) |
| Example provider | — | Together.ai |

### 9.3 Checklist: Choosing Between Local and Provider Inference

- [ ] Is the model small enough to run efficiently on local hardware? → **Use local inference with `pipeline`**
- [ ] Does the model require a GPU for reasonable speed? → **Use an inference provider**
- [ ] Is the model a large-parameter LLM or an image/video generation model? → **Use an inference provider**
- [ ] Do you want to avoid any API costs during development? → **Use local inference with a smaller model**

### 9.4 Common Mistakes to Avoid

| Mistake | Better Approach |
|:---|:---|
| Assuming Hugging Face guarantees model performance | Always check the evaluation results on the model card before selecting a model |
| Confusing `max_new_tokens` with total output length | `max_new_tokens` limits the number of *new* tokens added, not the total sequence length |
| Forgetting to loop over results when `num_return_sequences > 1` | The pipeline always returns a list; loop over it to access each `'generated_text'` |
| Hard-coding the API key in code | Store the API key in an environment variable and read it with `os.environ["HF_TOKEN"]` |
| Using pandas DataFrame methods on Arrow datasets | Use `.filter()` with a lambda and `.select()` with a range — not `.loc[]` or boolean indexing |
| Downloading an entire dataset when only one split is needed | Pass the `split` parameter to `load_dataset()` to download only what you need |
| Trying to run large LLMs locally on a laptop | Switch to an inference provider for large models; local hardware will be too slow |

---

*End of Revision Guide — Segment 1: Getting Started with Hugging Face*
