# JioCX Performance Predictor & Success Profile Analysis

An HR Analytics modeling framework designed to analyze historical performance and predict success profiles for HR Manager and HRBP roles in the **JioCX Business Unit (Jio Platforms Limited)**.

---

## 📌 Project Overview

Traditional talent management relies heavily on subjective performance reviews and manager bias. This project addresses these pain points by constructing:
1. **A Success Profile Framework:** Defining core competencies, leadership behaviors, and skills that drive performance using structured literature (Iceberg, Lominger, SHL Great Eight).
2. **A Performance Predictor Model:** A weighted, recency-weighted, and consistency-aware scoring matrix that aggregates 5 years of historical performance data (OLP).
3. **An Interactive HR Dashboard:** A tool for HR leaders and sponsors (e.g., Mr. Bharat Bhushan, HR Head) to filter talent pools, simulate performance scenarios, and identify star performers.

---

## 📁 Repository Structure & File Index

The repository contains files organized alphabetically/chronologically (**A** to **N**) representing the development timeline:

*   **`README.md`** - This documentation guide.
*   **`.gitignore`** - Git configuration to ignore system and IDE caches.
*   **`survey_analysis_utility.py`** - Python automation utility script to clean, reverse-score, and merge survey responses with OLP performance profiles.
*   **`(A) Project Charter Day1.pdf`** - Scope, sponsor alignment, and project timeline specification.
*   **`(D) Employee Data and Performance History (by anisha)/`** - Original HR data sheets, including `OLP Data.xlsx` (920 employee records) and `Stay and Exit Data - Latest.xlsx`.
*   **`(E) OLP_Analysis_Teaching_Notebook.ipynb`** - Step-by-step Jupyter Notebook explaining clean-up, normalization, and scoring of OLP performance data.
*   **`(E) Stay_Exit_and_Merged_Analysis.ipynb`** - Jupyter Notebook mapping Stay/Exit qualitative coding and matching.
*   **`(G) Matrice Explainer.html`** - Web explainer detailing mathematical logic, normalization formulas, and interactive tier thresholds.
*   **`(G) Performer Dashboard.html`** - Dynamic spreadsheet-style performer dashboard built with Chart.js and SheetJS.
*   **`(K) Project/`** - Consolidated production assets (Dashboards, explainer pages, survey formats, and reports).
*   **`(M) (J) Third Demo Survey for all JIOCX Emp 20Q.html`** - Shortened, 20-question survey designed to be copy-pasted directly into Microsoft Forms.
*   **`(M) 25th June Meeting Correction Note 1-4.jpg`** - Handwritten meeting notes summarizing mentor and sponsor reviews.
*   **`(N) Framework Methodology Behind Survey-1.html & Survey-2.html`** - Theoretical and academic reviews (Spencer & Spencer, Bartram, Lominger) supporting the survey design.

---

## 🚀 How to Run the Deliverables

### 1. Interactive Performer Dashboard & Explainer
*   Navigate to the `(K) Project/` folder.
*   Double-click and open **`performer-dashboard.html`** in any modern web browser.
*   Upload the master Excel file (`Employee Rating Analysis.xlsx` or `OLP Data.xlsx`) to see real-time statistics, distributions, and top performer lists.
*   Use **`matrice-explainer.html`** to trace calculations for specific employees step-by-step.

### 2. Microsoft Forms Survey Branching
*   Open the survey specification sheet: **`(M) (J) Third Demo Survey for all JIOCX Emp 20Q.html`**.
*   Select the Job Level tab (Junior, Manager, Leader).
*   Click **"Copy Section"** to copy formatted question blocks for direct paste into Microsoft Forms.
*   Use MS Forms branching rules to redirect respondents to their level-specific sections based on their "Job Level" response.

### 3. Processing Survey Response Data
Once survey collection is complete:
1. Export responses from Microsoft Forms as an Excel sheet and place it in the data folder as `Survey_Responses_Demo.xlsx`.
2. Run the processing script:
   ```bash
   python survey_analysis_utility.py
   ```
3. This creates **`JioCX_Predictor_Master_Dataset.xlsx`** and reports statistical correlation graphs for your presentation.

---

## 👥 Collaboration & Version Control

To initialize this project for Git collaboration, execute the following commands in your terminal:
1. Initialize local repository:
   ```bash
   git init
   ```
2. Add files:
   ```bash
   git add .
   ```
3. Commit progress:
   ```bash
   git commit -m "Initial commit - JioCX Performance Predictor project"
   ```
4. Connect to remote repository:
   ```bash
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```
