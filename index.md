# AI Agents for Data Science: How To and Should We?

layout: title

subtitle: Flatiron-Wide Autumn Meeting, October 2025

author: Jeremy Magland, Center for Computational Mathematics, Flatiron Institute

---

# What is a Software Agent?

A software agent is a system that can:
* Perceive environment
* Reason about goals
* Act autonomously (or semi-autonomously)

**Example: Thermostat**
* Perceives temperature
* Has goal temperature
* Acts by turning heating/cooling on or off

column-break

![Thermostat](https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Thermostat_science_photo.jpg/1200px-Thermostat_science_photo.jpg)

---

# What is an AI Agent?

An AI agent is a software agent that uses artificial intelligence techniques to perform its tasks.

**Example: Self-driving car**
* Perceives environment using sensors (cameras, LIDAR, etc.)
* Has goals (reach destination safely and efficiently)
* Acts by controlling the vehicle (steering, acceleration, braking)

column-break

![Waymo Self-Driving Car](https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Waymo_self-driving_car_front_view.gk.jpg/1200px-Waymo_self-driving_car_front_view.gk.jpg)

---

# Data Exploration Agent

**Example: Visualizing a dataset**
* Perceives: Reads and summarizes a dataset (e.g., CSV file)
* Has goals: Generate informative visualizations
* Acts: Create and execute scripts to produce plots

**Reasoning loop:**
1. Load and summarize the dataset
2. Identify interesting features (e.g., distributions, correlations)
3. Decide which visualizations to create
4. Generate and execute code to create plots
5. Review results and iterate if necessary
6. Produce a final report

**Final output**: An exploratory report showing meaningful patterns discovered automatically

column-break

![example data exploration plot](./images/example_data_exploration_plot.png)

---

# Why use them?

### Potential benefits

* Improved productivity
    - Automate repetitive tasks
    - Accelerate analysis
* Discover new insights
    - Uncover hidden patterns
    - Generate hypotheses that a human might miss
* Democratize data science
    - Make data science accessible to non-experts
    - Lower the barrier to entry

column-break

![fastest animal](https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Fastest_animal.jpg/1200px-Fastest_animal.jpg?20210526203921)

---

# Why be cautious?

### Potential risks

* Reliability concerns
    - LLMs can produce incorrect or misleading results
    - Lack of transparency in decision-making
* Ethical considerations
    - Biases in training data
    - Privacy concerns
    - Environmental impact
* Over-reliance on automation
    - Risk of losing critical thinking skills
    - Importance of human oversight

column-break

![cautious animal](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Culpeo_MC.jpg/640px-Culpeo_MC.jpg)

---

# DANDI Archive

The DANDI Archive allows publishing and sharing neurophysiology data

* Hosts large-scale datasets
* Supports reproducible research
* Provides rich metadata and search capabilities

column-break


![DANDI Archive](./images/dandi-archive.png)

---

# Dandiset 001174

Example dataset: Calcium imaging in SMA and M1 of macaques

* 45 Files
* 680 GB
* Neurodata Without Borders (NWB) format

How does one get started exploring this dataset??

column-break

![Dandiset 001174](./images/dandiset-001174.png)

---

# Dandiset 001174

Example dataset: Calcium imaging in SMA and M1 of macaques

* 45 Files
* 680 GB
* Neurodata Without Borders (NWB) format

How does one get started exploring this dataset??

column-break

![Dandiset 001174 Files](./images//dandiset-001174-files.png)

---

# Chat with an AI Agent for Exploring Dandiset

On the right is an example of using an AI agent to explore a DANDI dataset.

column-break

<iframe src="https://dandiset-explorer.vercel.app/chat/de_1759960923445?dandisetId=001174&dandisetVersion=draft"></iframe>

---

# Explorator Chat for a DANDI Dataset

Here is an example of using an AI agent to explore a DANDI dataset.

column-break

<iframe src="https://dandiset-explorer.vercel.app/chat/de_1759959244459?dandisetId=000537&dandisetVersion=draft"></iframe>

---

# The first slide

This is the first slide.

column-break

This is the right side of the first slide.

* bullet 1
* bullet 2
* bullet 3

---

# The second slide

This is the second slide.

column-break

:::plot-1:::

---

# Test

A test

column-break

./spurious-discovery-tests/examples/temporal_autocorrelation_01/tests/claude-sonnet-4/working/report.md

---
