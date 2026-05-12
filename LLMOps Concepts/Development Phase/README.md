# Comprehensive Study Guide: LLMOps Concepts — Segment 2: Development Phase

---

## 1. Overview of the Development Phase

The development phase is a **cyclic process** of building and improving the LLM application, known as the **development cycle**. It begins after the ideation phase (data sourcing and base model selection are complete) and consists of four major activities:

1. **Prompt Engineering**
2. **Chain and Agent Development**
3. **RAG and/or Fine-Tuning**
4. **Testing**

The phase is cyclic — if tests fail, you return to earlier activities to revise and improve. Only when tests pass does the application transition to the **operational phase**.

---

## 2. Prompt Engineering

### 2.1 What Is Prompt Engineering?
Prompt engineering is the practice of **crafting and refining prompts** to instruct the LLM to generate desired outputs. It is at the **heart of every LLM application** and is the first activity in the development cycle.

### 2.2 Why Is Prompt Engineering Important?
Prompt engineering enhances prompts in **three key ways**:

| Benefit | Description |
|---|---|
| **Improved performance** | Clear instructions lead to more accurate and helpful responses from LLMs |
| **Greater control** | Well-crafted prompts steer LLMs to generate the desired content |
| **Reduced bias and hallucinations** | Thoughtful prompts help avoid incorrect or irrelevant information |

> **Note:** Prompt engineering does **not** aim to completely eliminate randomness — it manages and guides output quality while tolerating some degree of model variability.

### 2.3 Elements of a Prompt
A typical prompt includes up to **four elements**:

| Element | Description | Example (Calorie Prediction) |
|---|---|---|
| **Instruction** | Specifies the task and desired format | "Predict the calories of this dish." |
| **Examples** | Provides sample input-output pairs for in-context learning | Other dishes and their calorie counts |
| **Input data** | The actual data to be processed | The specific dish to predict |
| **Output indicator** | Guides what the model should produce | "Calories:" or a format specification |

### 2.4 Finding the Perfect Prompt
When testing prompts, consider adjusting:
- **Temperature** — controls randomness in the output
- **Max tokens** — controls output length

Additional techniques:
- **In-context learning** — show the model examples of inputs and outputs within the prompt itself (zero-shot, one-shot, few-shot)
- **Online prompt design patterns** — numerous resources offer prompt templates and frameworks
- **Playground environments** — useful for trying various models and settings interactively

> **Mindset:** Each prompt acts like a **mini-experiment**. At this stage, you evaluate prompt quality using your own judgment before formal testing.

### 2.5 Prompt Management
**Prompt management** is the practice of systematically tracking prompts and their results. It is crucial for:
- **Efficiency** — quickly build on what's already been tried
- **Reproducibility** — re-run and verify past results
- **Collaboration** — team members can reference and reuse past work

#### What to Track:
- The prompt itself
- The model's output
- Details about the model and settings used (temperature, max tokens, model version)

#### Tools:
- Dedicated prompt management tools
- Preferred version control systems (e.g., Git)

> **Important side activity:** During prompt engineering, begin generating a **collection of good input-output pairs** — these will be used to evaluate the application during testing later.

### 2.6 Prompt Templates
Once a collection of promising prompts is gathered, the next step is building **prompt templates**:
- Templates use **placeholders** for input data
- They function like **recipes for different tasks** — applicable to any kind of input data
- They are **reusable** and make the application more flexible and efficient

**Example — Calorie Prediction Template:**
```
Determine the calories for the following dish.
Examples: {examples}
Input: {dish_description}
Calories:
```
This template can be reused for any dish by swapping out `{examples}` and `{dish_description}`.

---

## 3. Chains and Agents

### 3.1 From Prompts to Applications
A prompt alone isn't enough to build a full application. Real applications require a **flow and structure** to process inputs and produce useful outputs. This is where **chains** and **agents** come in.

**Example (Calorie Prediction Application):**
Steps needed:
1. Receive dish description (input)
2. Search a database for similar dish examples
3. Create the prompt using the template + examples + input
4. Send prompt to the LLM
5. Extract a number from the output (output parsing)

---

### 3.2 Chains

#### What Is a Chain?
A **chain** (also called a **pipeline** or **flow**) is a sequence of **connected steps** that take inputs and produce outputs. Each step feeds into the next in a **fixed, predetermined order**.

#### Example Chain (Calorie Prediction):
```
Dish description
       ↓
Find similar dishes in database
       ↓
Combine with prompt template
       ↓
Send to LLM
       ↓
Extract number from output
       ↓
Final calorie output
```

#### Why Use Chains?
- Enable **sophisticated applications** that interface with your own systems and databases
- Establish **modular design**, enhancing scalability and operational efficiency as the system grows
- Unlock **endless possibilities for customization**

---

### 3.3 Agents

#### What Is an Agent?
An **agent** is an LLM-powered system where the **LLM itself decides which action to take** from a set of available actions (also called **tools**). Unlike chains, agents are **adaptive** rather than deterministic.

#### Key Properties of Agents:
- Each **action** functions as a **standalone chain** that generates output
- The LLM chooses the best action based on the current situation
- Actions can happen **any number of times**, in any order
- The number of times each action is triggered is **unknown in advance**
- Backward arrows in agent diagrams indicate that actions provide **additional context** that feeds back into the decision loop

#### When Should You Use an Agent?
Agents are ideal when:
- There are **many possible actions** and the optimal sequence is unknown
- You are **uncertain about the inputs** you will receive
- The application needs to handle **diverse and unpredictable scenarios**

#### Example Agent (Enhanced Calorie Prediction):
The dish description alone may lack sufficient details (ingredients, quantities). Two actions are available:
1. **Fetch more dish information** (ingredients, preparation method)
2. **Find more related dishes** (more examples from the database)

The LLM agent decides which action to take — or whether to take both — based on the query at hand.

---

### 3.4 Chains vs. Agents — Detailed Comparison

| Dimension | Chain | Agent |
|---|---|---|
| **Decision-making** | Deterministic — fixed sequence of steps | Adaptive — LLM decides which action to take |
| **Complexity** | Simpler behavior | More complex behavior due to adaptability |
| **Flexibility** | Less flexible — fixed flow | More flexible — adjusts to diverse inputs |
| **Risk** | Lower risk due to predictability | Higher risk — may execute unpredictable actions |
| **Best for** | Known, well-defined processes | Scenarios with many actions and uncertain inputs |

> **Architecture decision:** Choosing between an agent and a chain is **always a trade-off** between complexity, flexibility, and risk. Neither is always better — it depends on the specific application requirements.

---

## 4. RAG vs. Fine-Tuning

Both RAG and fine-tuning are techniques used to **incorporate proprietary data and external knowledge** into an LLM application during development.

---

### 4.1 Retrieval Augmented Generation (RAG)

#### What Is RAG?
RAG is a common LLM design pattern that **combines the model's reasoning abilities with external factual knowledge**. It is implemented as a chain with three steps:

```
1. RETRIEVE → 2. AUGMENT → 3. GENERATE
```

#### The RAG Workflow in Detail (with Vector Database):

**Step 1 — Retrieve:**
1. User inputs a query
2. **Embed the query** — convert it into a numerical representation called an **embedding**, which captures its meaning
   - Similar meanings yield similar embeddings
   - Embeddings are created using **pre-trained embedding models**
3. **Search the vector database** — compare the query embedding with stored document embeddings using similarity calculations
4. **Retrieve the most similar documents** (top matches)

**Step 2 — Augment:**
5. Combine the original query with the retrieved documents to create the **final enriched prompt**

**Step 3 — Generate:**
6. Send the augmented prompt to the LLM to generate the output
7. Return the response to the user

#### Correct RAG Workflow Order:
1. User inputs a query
2. Embed the query
3. Search vector database using embedded query, and retrieve top matches
4. Augment original query with additional context retrieved from the database
5. Retrieve response from LLM using the augmented query, and return this to user

#### Embedding Models:
- Available as both **open-source and proprietary** options
- Vary in **quality, cost, and ease-of-use**
- Certain models work better with **specific text types or languages**
- **Experimentation and testing** are crucial when selecting an embedding model

#### When to Use RAG:
- When you need to include **factual knowledge** from external sources
- When you want to **retain all capabilities** of the original LLM without altering it
- When you need the application to stay **up-to-date** (if the external database is kept current)

#### Downsides of RAG:
- Adds **extra components** to the application (vector database, embedding model), requiring careful engineering

---

### 4.2 Fine-Tuning

#### What Is Fine-Tuning?
Fine-tuning **adjusts the LLM's weights** using your own data, expanding the model's reasoning capabilities to specific tasks and new domains (e.g., different languages, specialized fields like medicine or law).

#### Two Main Approaches:

**Approach 1: Supervised Fine-Tuning (Transfer Learning)**
- Requires **demonstration data** — input prompts paired with desired outputs
- **Retrains parts of the model** using this new data
- A form of transfer learning

**Approach 2: Reinforcement Learning from Human Feedback (RLHF)**
- Typically done **after** supervised fine-tuning
- Requires **human-labeled data** — rankings, quality scores, likes/dislikes
- Trains an extra **reward model** to predict output quality
- Optimizes the original LLM to **maximize the reward**

#### When to Use Fine-Tuning:
- When **specializing in a new domain** where the base model lacks expertise
- When you want **full customizability** over the model
- When no additional components are needed during deployment

#### Downsides of Fine-Tuning:
- Requires **labeled data** — expensive and time-consuming to produce
- Requires **specialized AI engineering knowledge** to implement
- May **worsen the application** and amplify data biases if training data is poor
- Can cause **catastrophic forgetting** — the model forgets previously learned knowledge

---

### 4.3 RAG vs. Fine-Tuning — Full Comparison

| Dimension | RAG | Fine-Tuning |
|---|---|---|
| **Primary use** | Including factual knowledge | Specializing in a new domain |
| **Model alteration** | Does NOT alter the model | Adjusts the model's weights |
| **Original capabilities** | Retains all original LLM capabilities | May alter or reduce original capabilities |
| **Implementation ease** | Easier to implement | Complex — requires specialized knowledge |
| **Data requirements** | Needs a searchable knowledge base | Needs labeled demonstration or feedback data |
| **Up-to-date information** | Easy to keep current (update the database) | Requires retraining to update |
| **Deployment components** | Requires extra components (vector DB, embedding model) | No extra components at deployment |
| **Risk** | Lower — model unchanged | Higher — catastrophic forgetting possible |

---

## 5. Testing

### 5.1 Why Is Testing Critical?
- LLMs **make mistakes**, especially as applications become more complex
- Changes to one part of the application can **affect other parts** and degrade overall performance
- Testing determines the application's **readiness for deployment**
- Testing focuses specifically on **evaluating the quality of the model's output**

### 5.2 LLM Testing vs. Traditional ML Testing

| Dimension | Traditional ML | LLM Applications |
|---|---|---|
| **Data needed** | Labeled training data AND test data | Usually just test data |
| **Evaluation focus** | Accuracy / closeness to a target label | Quality of the model's output |
| **Metrics** | Accuracy, RMSE, F1, etc. | Various — depends on whether a target or reference exists |

### 5.3 Step 1: Building a Test Set

A **comprehensive test set** is essential for effective evaluation. Key considerations:
- Building the test set is a **continuous activity** throughout development but must be **completed** before formal testing
- Test data must **closely resemble real-world scenarios** for accurate assessment
- Can include:
  - **Labeled text data** — for precise evaluation (has a known correct answer)
  - **Unlabeled text data** — to simulate typical inputs

> **Tip:** Various tools, including **other LLMs**, can help generate test data.

### 5.4 Step 2: Choosing the Right Metric

The choice of metric depends on the application. Use this decision flowchart:

#### Decision Framework:

```
Does the output have a correct answer (target label or number)?
    YES → Use ML Metrics (accuracy, RMSE, F1, etc.)
    NO  → Does a reference output exist?
              YES → Use Text Comparison Metrics
              NO  → Is there human feedback available?
                        YES → Use Feedback Score Metrics
                        NO  → Use Unsupervised Metrics
```

#### ML Metrics (Correct Answer Available)
- Use standard machine learning metrics like **accuracy, RMSE, F1 score**
- Best for tasks where there is a known correct numerical or categorical answer
- Example: An LLM application predicting the **calories of food dishes**

#### Text Comparison Metrics (Reference Output Available, No Single Correct Answer)
Two options:
1. **Statistical methods** — compare the overlap between predicted and reference text
2. **Model-based methods** — pre-trained models assess similarity
   - A popular approach: **LLM-judges** — LLMs specifically designed to assess the outputs of other LLMs

- Example: An LLM application **answering frequently asked questions** from a website (where there's a reference answer but wording may vary)
- Example: An LLM application **summarizing chat histories** (where summaries vary but a reference exists)

#### Feedback Score Metrics (Human Feedback Available, No Reference)
Two options:
1. **Human rating** — have humans rate the text on quality, relevance, or coherence (expensive)
2. **Model-based methods** — predict expected ratings based on past feedback, or ask LLM judges whether feedback was incorporated

#### Unsupervised Metrics (No Reference, No Human Feedback)
- Use statistical or model-based techniques to assess:
  - **Text coherence** — does the text make logical sense?
  - **Text fluency** — is the language natural and readable?
  - **Text diversity** — is there appropriate variety in the outputs?

---

### 5.5 Step 3: Optional Secondary Metrics

In addition to the primary metric, it is beneficial to track **secondary metrics** related to:

**Text characteristics:**
- Bias
- Toxicity
- Helpfulness

**Operational characteristics:**
- Latency (response time)
- Total cost incurred
- Memory usage

> This list is **not exhaustive** and is use-case dependent.

### 5.6 What Happens After Testing?

```
Test results
    ↓
PASS → Ready for deployment → Transition to Operational Phase
FAIL → Revisit previous development activities (prompt engineering, chains/agents, RAG/fine-tuning)
```

> Testing should **always be conducted**, regardless of whether a target output is present. Different situations call for different metrics, but testing is never skipped.

---

## 6. The Full Development Cycle (Summary Diagram)

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DEVELOPMENT CYCLE                                │
│                                                                     │
│  Load Base Model                                                    │
│       ↓                                                             │
│  ┌─────────────────┐                                               │
│  │ PROMPT          │ ← Craft prompts, track results,               │
│  │ ENGINEERING     │   build templates                             │
│  └────────┬────────┘                                               │
│           ↓  (Improved prompts)                                    │
│  ┌─────────────────┐                                               │
│  │ CHAIN & AGENT   │ ← Structure the application flow              │
│  │ DEVELOPMENT     │                                               │
│  └────────┬────────┘                                               │
│           ↓                                                         │
│  ┌─────────────────┐                                               │
│  │ RAG /           │ ← Incorporate external data                   │
│  │ FINE-TUNING     │                                               │
│  └────────┬────────┘                                               │
│           ↓                                                         │
│  ┌─────────────────┐                                               │
│  │ TESTING         │ → PASS → Operational Phase                   │
│  │                 │ → FAIL → Return to earlier activities         │
│  └─────────────────┘                                               │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 7. Exercise Walkthroughs & Answers

### Exercise 1: The Importance of Prompt Engineering (Multi-select — Choose 3)

**Question:** Identify three correct reasons why prompt engineering is important.

**Correct Answers:**
- ✅ **"By giving clear instructions, we can get more accurate and helpful responses from LLMs"**
- ✅ **"With well-crafted prompts, we can steer the models to generate the kind of content we want"**
- ✅ **"Prompt engineering helps decrease bias and hallucinations in the output"**

**Why the others are wrong:**
- "Prompt engineering ensures that LLMs get prompts with a higher word count, resulting in better performance" — **False.** Length alone doesn't improve performance; clarity and structure do.
- "Prompt engineering aims to completely eliminate randomness from the model's output" — **False.** It manages and reduces unwanted randomness but does not aim to eliminate it entirely.

---

### Exercise 2: Trying Out Prompt Engineering (MCQ)

**Question:** Which prompt would you prefer for predicting whether a food item will be popular?

**Prompts compared:**
- Prompt 1: `"Determine whether a dish will be popular in my restaurant. Input: 'Pizza Hawaii'"` — no examples, no output format
- Prompt 2: `"Determine whether a dish will be popular in my restaurant. Examples: 'Tropical Pizza': 'Yes'. Input: 'Pizza Hawaii'"` — one example, but no output format constraint
- Prompt 3: `"Determine whether a dish will be popular in my restaurant. Give output as 'Yes' or 'No'. Examples: 'Tropical Pizza', Popular: 'Yes'. Input: 'Pizza Hawaii', Popular:"` — example + strict output format

**Correct Answer:** ✅ **"Prompt 3, since by providing examples and clear output instructions we get an answer in a usable form"**

**Why:** Prompt 3 combines in-context learning (examples) with a clear output indicator (`Popular:` with forced Yes/No format), making the output structured and directly usable by the application.

---

### Exercise 3: Keeping Track of Prompts (MCQ)

**Question:** Why do you want to track prompts when working on prompt engineering?

**Correct Answer:** ✅ **"It helps ensure efficiency, reproducibility, and collaboration within a project"**

**Why the others are wrong:**
- "It's mainly for small projects, allowing quick iteration based on past prompt results" — prompt management is valuable at **all scales**, not just small projects.
- "It's primarily for statistics and visualizations" — this is not the purpose of prompt management.

---

### Exercise 4: The Difference Between Agents and Chains (Categorization)

**Task:** Decide whether each keyword/statement aligns more closely with an Agent or a Chain.

| Statement | Correct Category | Reasoning |
|---|---|---|
| The LLM decides what action to take | **Agent** | Core definition of an agent — adaptive decision-making by the LLM |
| Useful when the optimal sequence of steps is unknown | **Agent** | Agents handle uncertainty and variable inputs |
| Deterministic | **Chain** | Chains follow a fixed, predetermined sequence |
| Lower risk due to predictability | **Chain** | Chains are predictable and therefore lower risk |
| Adaptive | **Agent** | Agents adapt to diverse inputs and situations |

---

### Exercise 5: Choosing the Right Architecture (MCQ)

**Question:** When both agent and chain architecture are possible, what would you choose?

**Correct Answer:** ✅ **"It depends, since the choice between an agent and chain architecture is about balancing trade-offs related to complexity, flexibility and risk"**

**Why the others are wrong:**
- "Choosing an agent is preferable, because it makes the application more flexible" — flexibility alone doesn't make agents always better; the added risk and unpredictability must be considered.
- "Choosing a chain is preferable, because it makes the application more predictable" — predictability alone doesn't make chains always better; sometimes flexibility is necessary.

---

### Exercise 6: The RAG Workflow (Ordering)

**Task:** Arrange the RAG steps in the correct order.

**Correct Order:**
1. **User inputs a query**
2. **Embed the query**
3. **Search vector database using embedded query, and retrieve top matches**
4. **Augment original query with additional context retrieved from the database**
5. **Retrieve response from LLM using the augmented query, and return this to user**

---

### Exercise 7: Compare RAG with Fine-Tuning (Categorization)

**Task:** Classify each statement under RAG or Fine-tuning.

| Statement | Correct Category | Reasoning |
|---|---|---|
| Used for specializing in a new domain | **Fine-tuning** | Fine-tuning expands the model into new domains |
| Guarantees that the LLM retains its original reasoning capabilities | **RAG** | RAG doesn't alter the model — original capabilities preserved |
| Used for including factual knowledge | **RAG** | RAG retrieves external factual knowledge at inference time |
| Requires labeled data | **Fine-tuning** | Fine-tuning needs labeled demonstrations or human feedback |
| Requires extra components like a vector database | **RAG** | RAG adds a vector database and embedding model to the pipeline |

---

### Exercise 8: Choosing the Right Metric (Categorization)

**Task:** Decide which metric type is more suitable for each LLM application.

| Application | Correct Metric Type | Reasoning |
|---|---|---|
| An LLM application predicting the calories of food dishes | **Traditional ML metric** | Calories are a specific numerical target — accuracy/RMSE applies |
| An LLM application summarizing chat histories | **Traditional ML metric** | Wait — summaries are text with reference outputs → **Text comparison metrics** |
| An LLM application answering frequently asked questions from a website | **Text comparison metrics** | Answers vary but reference answers exist — text comparison needed |
| An LLM application classifying whether a forum message is toxic or not | **Text comparison metrics** | Wait — classification with a label → **Traditional ML metric** |

> **Clarification on the exercise layout:** The exercise shows:
> - **Traditional ML metrics:** predicting calories (numerical target ✅) and summarizing chat histories
> - **Text comparison metrics:** answering FAQs (reference text ✅) and classifying toxicity (categorical label)
>
> **Correct classification based on course content:**
> - Predicting calories → **Traditional ML metric** (correct numerical target exists)
> - Classifying toxicity → **Traditional ML metric** (correct categorical label exists)
> - Answering FAQs → **Text comparison metric** (reference answer exists, no single exact answer)
> - Summarizing chat histories → **Text comparison metric** (reference summary exists, variation expected)

---

### Exercise 9: The Importance of Testing (MCQ)

**Question:** What answer best describes *when* you should be testing your application?

**Correct Answer:** ✅ **"LLM application testing should always be conducted, regardless of the presence of a target output"**

**Why the others are wrong:**
- "LLM application testing should only be done when the target output is exact, otherwise it is impossible" — **False.** Multiple metric types exist for situations without exact target outputs.
- "LLM application testing should only be done when there is a reference output" — **False.** Feedback score metrics and unsupervised metrics allow testing even without a reference output.

---

## 8. Key Concepts Summary

| Concept | Summary |
|---|---|
| Development cycle | Cyclic process of building/improving the LLM application — iterates until testing passes |
| Prompt engineering | Crafting and refining prompts to improve LLM performance, control, and reduce hallucinations |
| Prompt elements | Instruction, examples, input data, output indicator |
| In-context learning | Providing examples within the prompt to guide model behavior |
| Prompt management | Tracking prompts, outputs, and settings for efficiency, reproducibility, and collaboration |
| Prompt templates | Reusable prompt structures with placeholders for dynamic input data |
| Chain | A fixed, deterministic sequence of steps — predictable, lower risk, less flexible |
| Agent | An adaptive system where the LLM chooses actions — flexible, higher complexity and risk |
| RAG | Combines LLM reasoning with external factual knowledge via retrieve-augment-generate pipeline |
| Embedding | A numerical representation of text that captures its semantic meaning |
| Vector database | A database storing embeddings, enabling similarity search for document retrieval |
| Fine-tuning | Adjusting LLM weights using new data to specialize in domains or tasks |
| Catastrophic forgetting | A risk of fine-tuning where the model forgets previously learned knowledge |
| RLHF | Reinforcement Learning from Human Feedback — a fine-tuning method using human quality ratings |
| Test set | A representative collection of inputs (labeled or unlabeled) used to evaluate the application |
| ML metrics | Used when a correct target answer exists (accuracy, RMSE, F1) |
| Text comparison metrics | Used when a reference output exists but no single correct answer (statistical or LLM-judge methods) |
| Feedback score metrics | Used when human feedback is available but no reference output |
| Unsupervised metrics | Used when neither reference nor human feedback is available (coherence, fluency, diversity) |
| Secondary metrics | Optional supplementary metrics — bias, toxicity, latency, cost, memory usage |

---

*This guide covers all content from Segment 2 of "LLMOps Concepts," including all four video topics (prompt engineering, chains and agents, RAG vs fine-tuning, and testing) and all nine exercises with correct answers and reasoning.*
