# Task 4: Appify the Visualization

## 1. Directions for Extension & Improvement

Based on the current static visualization (which includes **Overall Performance Comparison** and **Error Type Distribution**), the following interactive features are proposed to enhance usability, especially for remote colleagues:

### A. Dynamic Filtering & Segmentation

The static chart forces users to consider all models and error types at once. The proposed app will include sidebar controls for personalized exploration:

- **Model Selector:**  
  A multi-select dropdown that allows users to choose which chatbot models to display (e.g., compare only _gemini_, _claude_, and _chatgpt_), reducing visual clutter.

- **Error Type Toggle:**  
  Checkboxes to show/hide specific error categories. For instance, a user may hide "Rounding / Formatting" errors to focus on more critical issues like "Fiscal vs Calendar Period Confusion."

### B. Interactive Drill-Downs

- **Hover Tooltips:**  
  Interactive charts (built with Plotly or Altair) will display precise counts and percentage contributions when hovering over chart segments, such as the "Ambiguous Interpretation" block for _claude_.

- **Outlier Management ("Claude_DLP" Isolation):**  
  Since `claude_dlp` is a significant outlier (5.8% error rate vs. ~88% for _Gemini_), the scaling in the charts muddles smaller error bars. The app will offer an "exclude outliers" option to rescale axes, improving readability for other models.

### C. Raw Data Inspection

- **Data Table View:**  
  An expandable section below the charts will display the underlying DataFrame. Colleagues can search, filter, or export the data (e.g., to CSV) for their own analysis and reporting.

---

## 2. Tech Stack Selection

### Core Framework: **Streamlit**

**Rationale:**  
Streamlit enables rapid development of interactive Python apps using dataframes. It requires no HTML/CSS/JS knowledge, supports simple user controls natively, and integrates seamlessly with charting libraries.

### Visualization Library: **Plotly Express**

**Rationale:**  
Plotly provides rich interactivity (zoom, pan, tooltips) not available in static charts (e.g., Matplotlib). It integrates directly into Streamlit, producing interactive web visualizations with minimal code change.

---

## 3. Sharing & Deployment Strategy

To ensure easy access for remote users (without VPNs or complex authentication), the app will be deployed via the Hugging Face Hub.

### Deployment Architecture

- **Host:** Hugging Face Spaces  
- **SDK:** Streamlit (natively supported in HF Spaces)  
- **Profile:** [https://huggingface.co/ruanchaves](https://huggingface.co/ruanchaves)

#### Deployment Workflow

1. **Repository Setup:**  
   Create a new Space on Hugging Face using the Streamlit template.

2. **Dependency Management:**  
   Create a `requirements.txt` file:
   ```
   streamlit
   pandas
   plotly
   ```

3. **Application Logic:**  
   Write the interactive app in `app.py`, encapsulating all visualization and UI logic.

4. **CI/CD:**  
   Push files to the Hugging Face Git repository. Spaces will automatically build and launch the app.

### Access & Collaboration

- The app will be accessible from a public URL  
  _e.g._: `https://huggingface.co/spaces/ruanchaves/chatbot-error-analysis`
- If the dataset is sensitive, set Space visibility to **Private** and add remote colleagues as collaborators to the organization or repo.
