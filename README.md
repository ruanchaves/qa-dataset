# qa-dataset

This repository consists of 5 tasks related to analyzing a financial retrieval QA dataset.

## 📋 Task Overview

### Task 0: Repo Setup
- **README.md** - This file (repository documentation)

### Task 1: Error Rate Per Chatbot
**Objective:** Calculate and summarize error rates for each chatbot in the dataset.

**Files:**
- `error_rate_analysis.py` - Script that calculates error rates for each chatbot
- `error_rate_report.json` - Output report containing error rate summary per chatbot
- `train.csv` - Input dataset (financial retrieval QA dataset)

### Task 2: Data Sampling for Quality Review
**Objective:** Extract a random sample of 50 Q&A pairs balanced across the top 25 most common categories.

**Files:**
- `data_sampling.py` - Script that extracts balanced Q&A samples across categories
- `qa_sample.json` - Output file containing 50 sampled Q&A pairs for manual review

### Task 3: Visualization of Error Rates
**Objective:** Create a visualization based on Task 1 error rate analysis.

**Files:**
- `visualize_error_rates.py` - Script that generates error rate visualizations
- `error_rate_visualization.png` - Output visualization showing error rates by chatbot

### Task 4: Appify the Visualization
**Objective:** Propose directions for extending the visualization into an interactive web app.

**Files:**
- `task4.md` - Documentation containing:
  - Directions for extension and improvement
  - Tech stack selection (Streamlit + Plotly)
  - Deployment strategy (Hugging Face Spaces)

### Task 5: Share an AI Article
**Objective:** Write a Slack-ready message to share an Anthropic article about measuring political bias in models.

**Files:**
- `task5.md` - Slack-ready message for #research channel

## 📊 Dataset

The dataset used in this project is the **Financial Retrieval QA Dataset** from Hugging Face:
- Source: https://huggingface.co/datasets/daloopa/financial-retrieval
- Main dataset file: `train.csv`

## 🚀 Usage

### Task 1: Run Error Rate Analysis
```bash
python error_rate_analysis.py
```
This generates `error_rate_report.json` with error rate summaries per chatbot.

### Task 2: Generate Q&A Sample
```bash
python data_sampling.py
```
This generates `qa_sample.json` with 50 balanced Q&A pairs for quality review.

### Task 3: Create Visualization
```bash
python visualize_error_rates.py
```
This generates `error_rate_visualization.png` with error rate visualizations.

## 📝 Notes

- All tasks have been committed and pushed to this repository
- Each task builds upon previous work (e.g., Task 3 uses output from Task 1)
- The visualization in Task 3 can be extended into an interactive app as described in Task 4