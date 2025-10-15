# AI Agents for Data Science: How To and Should We?

```yaml slide-metadata
slide-type: title
subtitle: Flatiron-Wide Autumn Meeting, October 2025
author: Jeremy Magland, Center for Computational Mathematics, Flatiron Institute
```

---

# Outline and Spoilers

```yaml section-metadata
font: medium-large
```
* What are AI agents?
* How do they work? How to build one?
* **Spoiler 1**: Great for certain tasks
    - Assisting with software tools
    - Exploring datasets and generating visualizations
* **Spoiler 2**: They struggle with *real* data analysis
    - Spurious discoveries
    - Wrong conclusions
* Caveats
    - AI is a fast-moving field
    - This is my personal perspective based on the fields I have experience in

* * *

<div style="text-align: center;">
<img src="https://upload.wikimedia.org/wikipedia/commons/6/64/Dall-e_3_%28jan_%2724%29_artificial_intelligence_icon.png" alt="AI brain" height="300px"></img>
</div>
<div style="text-align: center;">
<img src="https://upload.wikimedia.org/wikipedia/commons/3/38/Data_Science.png" alt="Data Science" height="300px"></img>
</div>

---

# What is a Software Agent?

A software agent is a system that can:
* **Perceive** its environment
* **Reason** about goals
* **Act** autonomously (or semi-autonomously)

**Example: Thermostat**
* Perceives temperature
* Has goal temperature
* Acts by turning heating/cooling on or off

* * *

![Thermostat](https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Thermostat_science_photo.jpg/1200px-Thermostat_science_photo.jpg)

---

# What is an AI Agent?

An AI agent is a software agent that uses artificial intelligence to perceive, reason, and act.

**Example: Self-driving car**
* Perceives the world (cameras, LIDAR, etc.)
* Plans a safe and efficient route
* Acts by steering, accelerating, braking, etc.

* * *

![Waymo Self-Driving Car](https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Waymo_self-driving_car_front_view.gk.jpg/1200px-Waymo_self-driving_car_front_view.gk.jpg)

---

# Data Exploration Agent

An **AI agent for data science** that explores datasets and generates insights.

**Example: Visualizing a dataset**
* **Perceives** a dataset (e.g., CSV file)
* **Aims** to find patterns and relationships
* **Acts** by generating and running analysis code

**Reasoning loop:**
* Summarize the data
* Find interesting features
* Create visualizations
* Iterate as needed
* Produce a final report

**Output**: An exploratory report with plots, summaries, and insights

* * *

![example data exploration plot](./images/example_data_exploration_plot.png)

---

# Hypothesis Testing Agent

**Goal**: Generate/Test a hypotheses, beyond just exploration

**Example hypothesis**: Higher synchrony between brain regions predicts better attention performance

**Example dataset:**
* Thousands of neural recordings across many subjects
* Millions of time points
* Dozens of brain regions

**Agent's open-ended reasoning:**

1. Read background literature
2. Load and explore data
3. Formulate and test hypotheses
4. Generate visualizations and statistics
5. Repeat as needed
6. Produce a final report

* * *

![Hypothesis Testing](./images/hypothesis-testing-plot.png)

---

# Why use AI agents?

```yaml section-metadata
font: large
```

**Potential benefits:**
* Productivity: Automate repetitive tasks, accelerate analysis
* Discovery: Reveal hidden patterns, suggest new hypotheses
* Accessibility: Lower barrier for non-experts

Overall, they can make science faster, more open, and sometimes more creative.

* * *

![fastest animal](https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Fastest_animal.jpg/1200px-Fastest_animal.jpg?20210526203921)

---

# Why be cautious?

```yaml section-metadata
font: large
```

**Key risks:**
* Reliability: Confident but wrong results
* Ethics: Bias, plagiarism, environmental cost
* Over-reliance: Erosion of critical thinking, scientific expertise
* Accountability: Who is responsible when AI gets it wrong?

What aspects of data science can be delegated to AI? What should be reserved for human judgment?

* * *

![cautious animal](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Culpeo_MC.jpg/640px-Culpeo_MC.jpg)

---

# Why build our own AI agents?

```yaml section-metadata
font: medium-large
```

**General commercial models (ChatGPT, Calude, Gemini)**:
* Broad, powerful, but opaque
* Limited access to tools and data
* Can't run code on our own compute resources / environments
* Difficult to integrate into custom workflows

**Custom agents**:
* Transparent
* Tuned for specific tasks
* Access to local data and compute
* Open source

Note: Custom agents can use commercial models as components.

---

# How to build an AI Agent?

```yaml section-metadata
font: large
```

**Key components:**
* LLM (e.g., GPT-4, Claude, Open Source)
* Toolset (e.g., Python, shell commands, APIs)
* Reasoning framework: Loop / logic that connects them

* * *

![How to build an AI Agent](./images/how-to-build-ai-agent-diagram.png)

---

# How a homemade AI agent "thinks"

```yaml section-metadata
font: large
```

1. Receive a goal or question
2. Ask the LLM for next action
3. Parse the response for tool calls
4. Execute tools (locally) and collect outputs
5. Append outputs to conversation history and go back to step 2
6. Stop when the LLM indicates the task is complete

* * *

![Agent flow diagram](./images/agent-flow-diagram.png)

---

# Inside the agent: The system prompt

```yaml section-metadata
font: large
```

The agent starts with a **system prompt** that defines its role and capabilities.

* * *

```yaml section-metadata
font: medium-small
```

**Sample system prompt**:
You are an expert data scientist. Your task is to explore a dataset and generate visualizations. You have access to Python and common data science libraries (pandas, matplotlib, seaborn, etc.). You can also use shell commands to manage files.

In your response you can respond with tools calls in the following format:

```xml
<tool name="execute_python">
# Python code here
</tool>

<tool name="read_file">
Path to file here
</tool>

<tool name="write_file">
Path to file here
</tool>

<tool name="execute_shell">
# Shell command here
</tool>

<tool name="end">
The task is complete. Here is the summary of findings...
</tool>

etc.
```

Do not hallucinate, etc., etc.

---

# Example: Agent Reasoning in Action

```yaml section-metadata
font: small
```

**System prompt**: **As in previous slide**

**User**: Please analyze the dataset `data.csv` and generate visualizations.

**Agent**: Sure! I will start by loading and summarizing the dataset.

```xml
<tool name="execute_python">
import pandas as pd
df = pd.read_csv('data.csv')
summary = df.describe()
summary.to_csv('summary.csv')
</tool>
```

**Tool response**: Executed Python code. No console output.

**Agent**: I've generated a summary. I will now read it.

```xml
<tool name="read_file">
summary.csv
</tool>
```

**Tool response**: (Contents of summary.csv)

**Agent**: I have read the summary of the dataset. Next, I will generate a plot depicting the distribution of a key variable.

```xml
<tool name="execute_python">
import matplotlib.pyplot as plt
...
plt.savefig('plot.png')
</tool>
```

* * *

```yaml section-metadata
font: small
```

Tool response: Executed Python code. No console output.

**Assistant**: I have generated a plot and saved it as `plot.png`.

```xml
<tool name="end">
The analysis is complete. The summary is in `summary.csv` and the plot is in `plot.png`.
</tool>
```

![distribution-of-key-variable](./images/distribution-of-key-variable.png)

---

# Accessing the LLM

```yaml slide-metadata
slide-type: tabs-on-right
```

```yaml section-metadata
font: large
```

**How the agent talks to the model:**
* Send conversation history to API call (e.g, OpenAI, Anthropic)
* Receive text and tool calls as response
* Loop until task is complete

**Minicline**: Full, open source Python implementation of an agent (see tab on right)

* * *

```yaml section-metadata
font: small
```

### What does an API call look like?

```yaml section-metadata
tab-label: OpenAI API
```

```python
import openai

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant... etc."},
        {"role": "user", "content": "Please analyze the dataset `data.csv` and generate visualizations."}
    ],
    temperature=0.7
)

tool_calls = response.get("tool_calls", [])
text_response = response.get("choices", [])[0]["content"]

print("LLM response:", text_response)
if tool_calls:
    for tool_call in tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call.get("arguments", "")
        # Execute the tool call
        print(f"Executing tool: {tool_name} with args: {tool_args}")
```

* * *

```yaml section-metadata
tab-label: OpenRouter Models
```

./markdown_files/snapshot-table-of-openrouter-models.md

* * *

```yaml section-metadata
tab-label: Minicline
```

<iframe src="https://magland.github.io/minicline/"></iframe>

---

# Application: Tool Assistant

```yaml slide-metadata
slide-type: tabs-on-right
```

An AI agent that helps users get started using a software tool.

For example, **Stan Assistant** is a web-based AI agent that helps users learn about [Stan](https://mc-stan.org/) (probabilistic programming language) and build models.

Tools available to the agent:
* Access parts of the [Stan User's Guide](https://mc-stan.org/docs/stan-users-guide/index.html)
* Embed Stan Playground for interactive coding
* Apply strict anti-hallucination rules

Better than general chat agents (e.g., ChatGPT) on a focused scientific task.

* * *

```yaml section-metadata
tab-label: Live Chat
```

<iframe src="https://stan-assistant.vercel.app"></iframe>

* * *

```yaml section-metadata
tab-label: Demo Video
```

<iframe src="https://users.flatironinstitute.org/~magland/screencasts/presentations/ai-agents-for-data-science-how-to-and-should-we/stan-assistant-demo.webm"></iframe>

* * *

```yaml section-metadata
tab-label: System Prompt
```

./markdown_files/stan-assistant-system-prompt.md

---

# Application: Dataset Assistant (Dandiset Explorer)

```yaml slide-metadata
slide-type: tabs-on-right
```

The DANDI Archive is a platform for sharing large-scale neurophysiology datasets.

**It enables**
* Open, reproducible research
* Standardized data (NWB format)
* Rich metadata and search

**Example: Dandiset 001174**
* 45 files, 680 GB, NWB format

**How can a scientist start exploring a dataset this large and complex?**

* * *

```yaml section-metadata
tab-label: DANDI Archive
```

![DANDI Archive](./images/dandi-archive.png)

* * *

```yaml section-metadata
tab-label: Example Dataset
```

![Dandiset 001174](./images/dandiset-001174.png)

* * *

```yaml section-metadata
tab-label: Example Dataset Files
```

![Dandiset 001174 Files](./images/dandiset-001174-files.png)

---

# Application: Dataset Assistant (Dandiset Explorer)

```yaml section-metadata
font: large
```

**Dandiset Explorer** is an AI Agent that helps scientists begin exploring complex datasets.

**Tools and capabilities**
* DANDI API: fetch metadata and file listings
* Python environment with specialized libraries for NWB
* Specialized knowledge about NWB files
* Can view text and image outputs
* Can iteratively refine analyses


* * *

<iframe src="https://dandiset-explorer.vercel.app/chat/de_1759960923445?dandisetId=001174&dandisetVersion=draft"></iframe>

---

# Application: Generating Introductory Notebooks

```yaml section-metadata
font: large
```

* * *

![dandi-notebooks-overview](./images/dandi-notebooks-overview.png)

---

# Pushing the Limits: Hypothesis-Testing Agents

```yaml section-metadata
font: large
```

AI agents can explore data, but can they **generate and test scientific hypotheses**?

This is where trust really matters.

---

# What could possibly go wrong?

```yaml section-metadata
font: large
```

Potential failure modes:

* **False confidence**: plausible but wrong results
* **Spurious patterns**: seeing structure in random data
* **Compounding errors**: small mistakes amplified by loops
* **Missing context**: missing domain knowledge/expertise

<div style="text-align: center;">
<img src="https://upload.wikimedia.org/wikipedia/commons/6/64/Dall-e_3_%28jan_%2724%29_artificial_intelligence_icon.png" alt="AI brain" height="200px"></img>
</div>

---

# What I Found Exploring the DANDI Archive

```yaml section-metadata
font: large
```

AI agents did well at first...
* Wrote boilerplate code
* Summarized datasets
* Identified files of interest
* Produced attractive and helpful visualizations

But deeper analysis went wrong...
* A mix of correct and incorrect conclusions
* Long, impressive notebooks with sloppy science when you checked the details.

* * *

<iframe src="https://nbfiddle.app/?url=https://github.com/dandi-ai-notebooks/001363/blob/main/2025-04-18-claude-3.7-sonnet-prompt-b-5/001363.ipynb"></iframe>

---

# Spurious Discovery Tests

```yaml slide-metadata
slide-type: tabs-on-right
```


```yaml section-metadata
font: medium-large
```

**Goal**: Test whether AI agents can **avoid finding patterns that don't exist**.

**Approach**:
* Created **synthetic datasets** with **no real underlying signal**.
* Asked multiple AI agents to analyze them.
* Clearly instructed that if there is no signal, they should conclude that.
* Evaluated whether they correctly found *nothing*.

https://github.com/magland/spurious-discovery-tests

* * *

```yaml section-metadata
tab-label: Overview
```

## Spurious discovery tests

Question: Can large language models be trusted to test hypotheses in data science?

This project contains a collection of synthetic experiments designed to expose the kinds of mistakes that artificial intelligence can often make when interpreting complex datasets. Each experiment presents a plausible scientific scenario with a dataset containing no underlying signal, but where data analysis pitfalls are possible. Each LLM is evaluated on its ability to identify the absence of a signal and to thus avoid false discoveries.

* * *

```yaml section-metadata
tab-label: multiple_comparisons_01
```

### multiple_comparisons_01

**Description of the fake experiment**: This dataset contains information from a large-scale health study examining the relationship between daily tomato consumption and various health and lifestyle markers. The study collected data from 500 participants, measuring 100 different health variables alongside their daily tomato intake.

**Dataset**: The dataset was generated with no underlying signal. The goal of the experiment is to see if the LLMs will do the proper correction and identify that the correlations are not significant.

* * *

```yaml section-metadata
tab-label: temporal_autocorrelation_01
```

### temporal_autocorrelation_01

**Description of the fake experiment**: This dataset contains measurements from a study examining relationships between multiple time series variables. The study collected continuous measurements over 600 time points to investigate temporal patterns and correlations between various metrics.

**Dataset**: The dataset was generated with no underlying signal. However, there were temporal autocorrelations in the data. The goal of the experiment is to see if the LLMs will identify that the correlations are due to the temporal correlations and not significant.

* * *

```yaml section-metadata
tab-label: temporal_autocorrelation_02
```

### temporal_autocorrelation_02

**Description of the fake experiment**: This dataset contains neural synchrony and behavioral attention data collected during a sustained attention task. The study explores whether dynamic coherence between brain regions in the alpha frequency band (8–12 Hz) can be used to predict fluctuations in attentional engagement over time.

**Dataset**: The dataset was generated with no association. However, there were temporal autocorrelations in the data. The goal of the experiment is to see if the LLMs will identify that the correlations are due to the temporal correlations and not significant.

* * *

```yaml section-metadata
tab-label: data_artifacts_01
```

### data_artifacts_01

**Description of the fake experiment**: This dataset contains continuous recordings of neural firing rates from two distinct brain regions (Region A and Region B). The recordings span 6 hours with measurements taken every second, resulting in 21,600 time points per region. There researchers reported some problems with data acquisition. There may be periods during the recording where the data is corrupted.

**Dataset**: The dataset was generated with no underlying signal. However, there were time chunks when the firing rates were all zeros, leading to a spurious correlation if not accounted for. The goal of the experiment is to see if the LLMs will identify that the correlations are due to the data artifacts and not significant.

---

# Spurious Discovery Tests Prompt

```yaml section-metadata
font: medium-large
```

Included in prompt:
* Your task is to **create and execute scripts that explore this dataset** and then summarize your findings in a new file report.md.
* Be sure to **justify any conclusions** using statistical tests.
* **Do not invent results**. If nothing of significance is found, say so.
```

---

# Test: temporal_autocorrelation_01

```yaml slide-metadata
slide-type: tabs-on-right
```

Study: relationship between multiple time series variables
* 600 time points
* No underlying correlations between variables
* But: strong temporal autocorrelations in each variable

Results:
* **Passed**: None
* **Borderline**: gemini-2.5-flash
* **Failed**: chatgpt-4o-latest, claude-3.5-sonnet, claude-sonnet-4, deepseek-chat-v3, gemini-2.5-pro, ChatGPT 5 online

See the lengthy (incorrect) reports in the tabs to the right

* * *

```yaml section-metadata
tab-label: claude-sonnet-4
```

<iframe src="https://magland.github.io/spurious-discovery-tests/examples/temporal_autocorrelation_01/tests/claude-sonnet-4/working/report"></iframe>


* * *

```yaml section-metadata
tab-label: claude-3.5-sonnet
```

<iframe src="https://magland.github.io/spurious-discovery-tests/examples/temporal_autocorrelation_01/tests/claude-3.5-sonnet/working/report"></iframe>

* * *

```yaml section-metadata
tab-label: chatgpt-4o-latest
```

<iframe src="https://magland.github.io/spurious-discovery-tests/examples/temporal_autocorrelation_01/tests/chatgpt-4o-latest/working/report"></iframe>

* * *

```yaml section-metadata
tab-label: gemini-2.5-flash-preview
```

<iframe src="https://magland.github.io/spurious-discovery-tests/examples/temporal_autocorrelation_01/tests/gemini-2.5-flash-preview/working/report"></iframe>

* * *

```yaml section-metadata
tab-label: gemini-2.5-pro-preview
```

<iframe src="https://magland.github.io/spurious-discovery-tests/examples/temporal_autocorrelation_01/tests/gemini-2.5-pro-preview/working/report"></iframe>

* * *

```yaml section-metadata
tab-label: ChatGPT 5 online
```

<iframe src="https://magland.github.io/spurious-discovery-tests/examples/temporal_autocorrelation_01/tests/chatgpt-5-online/timeseries_analysis_narrative/report_narrative.md"></iframe>

---

# Test: data_artifacts_01

```yaml slide-metadata
slide-type: tabs-on-right
```

Study: continuous recordings of neural firing rates from two brain regions

* 6 hours of data, 21600 time points
* No underlying correlations between regions
* But: Periods of corrupted data with all zeros

Results:
* **Passed**: None
* **Borderline**: None
**Failed**: chatgpt-4o-latest, claude-3.5-sonnet, claude-sonnet-4, deepseek-chat-v3, gemini-2.5-flash, gemini-2.5-pro, ChatGPT 5 online, ChatGPT 4o online

See the lengthy (incorrect) reports in the tabs to the right

* * *

```yaml section-metadata
tab-label: ChatGPT 5 online
```

<iframe src="https://magland.github.io/spurious-discovery-tests/examples/data_artifacts_01/tests/chatgpt-5-online/neural_activity_analysis/report"></iframe>

* * *

```yaml section-metadata
tab-label: claude-sonnet-4
```

<iframe src="https://magland.github.io/spurious-discovery-tests/examples/data_artifacts_01/tests/claude-sonnet-4/working/report"></iframe>

---

# Results of Spurious Discovery Tests

```yaml section-metadata
font: large
```

**Overall outcome**:
* Most agents "discovered" patterns in random data
* Very few concluded "no effect"
* Many produced confident but incorrect reports

---

# What we learned

**AI can be very helpful for a number of data science tasks:**
* Generating boilerplate code
* Summarizing datasets
* Creating visualizations
* Assisting with software tools

But they struggle at being reliable with deeper data analysis.

**To move forward, we should**:
* Benchmark extensively on spurious discovery tests
* Require transparency and reproducibility
* Integrate expert human oversight in loop
* Develop ethical frameworks for accountability and responsible use

* * *

<div style="text-align: center;">
<img src="https://upload.wikimedia.org/wikipedia/commons/6/64/Dall-e_3_%28jan_%2724%29_artificial_intelligence_icon.png" alt="AI brain" height="300px"></img>
</div>
<div style="text-align: center;">
<img src="https://upload.wikimedia.org/wikipedia/commons/3/38/Data_Science.png" alt="Data Science" height="300px"></img>
</div>

---

# Thank You!

Thanks to all the collaborators who helped with this work!

Neurodata Without Borders Team, DANDI Team, Stan Playground Team

Ryan Ly, Oliver Ruebel, Benjamin Dichter, Satrajit Ghosh, Yaroslav Halchenko, Brian Ward, Jeff Soules
