# JioCX Survey Redesign & Analysis Task Context

This document summarizes the current state, modifications, and background context for the **JioCX Workplace Effectiveness Survey** redesign so you can seamlessly continue the task in Claude.

---

## 📌 Project Overview
* **Organization**: Jio Platforms Limited (JioCX Business Unit)
* **Goal**: Build an HR Analytics performance predictor model by correlating behavioral survey scores with historical OLP performance data.
* **Academic/Theoretical Foundation**:
  * **Spencer & Spencer Iceberg Model**: Measures hidden traits, self-concept, and motives.
  * **Lominger Leadership Architect**: Maps to standard behavioral competency definitions.
  * **SHL Great Eight (Bartram)**: Organizes competencies into universal predictors.
  * **Campbell's Tripartite Model**: Covers Task, Contextual, and Adaptive performance.
  * **Classical Test Theory**: Guides reliability, reverse-scoring, and attention checks.

---

## 🛠️ What We Just Accomplished
We shortened and simplified the survey design to prevent survey fatigue and make it compatible with a 4-point rating scale mapping to `-1, 0, 1, 2`.

### 1. Survey HTML File Redesign
* **File Location**: `(M) (J) Shortened Behavioral Survey 12Q.html`
* **Section A (Likert evaluated)**:
  * Reduced from 20 questions to **10 questions** (exactly 1 question per competency) plus **2 attention checks** (AC1 at Q4, AC2 at Q9).
  * Converted the 5-point scale to a **4-point scale** mapping to numerical values `-1, 0, 1, 2`:
    * `-1`: Avoids / Passive (Rarely or never does this; works against it)
    * `0`: Meets Basic (Only does it when requested; minimum reactive effort)
    * `1`: Proactive / Consistent (Regularly and actively does this in daily work)
    * `2`: Role Model / Strategic (Exemplary impact; guides others; designs systems)
  * Level-adapted the 10 competency questions for Junior/Executive, Manager/Team Lead, and Leader/VP+ using simple, everyday English.
  * Embedded **AC1** (A04 - expected answer: `1`) and **AC2** (A09 - expected answer: `-1`) to catch straight-lining.
  * Configured exactly **3 reverse-scored items** per level: `A02` (ST), `A10` (CM), and `A12` (CO).
* **Section B (Competency Priorities)**:
  * Kept the forced ranking of the 10 competencies from 1 to 10 and the Top 3 focus checklist cross-check, simplifying the explanations.
* **Section C (Behavioral Scenarios)**:
  * Simplified the 3 level-adapted scenarios and options using very simple, non-corporate English.
* **Section D (Personal Reflections)**:
  * Redesigned to mitigate survey fatigue. Instead of 5 mandatory long questions, employees use a dropdown to select **only 1 or 2 competencies** where they have strong, real examples. They write a brief STAR-format example of **30 to 50 words**.
* **Microsoft Forms Copy Utility**:
  * Tab toggles let you choose the job level.
  * **"Copy"** buttons let you instantly copy formatted text to your clipboard for quick, structured pasting directly into Microsoft Forms.

### 2. Python Script Update
* **File Location**: `survey_analysis_utility.py`
* **Competency Mapping**:
  * Updated `ITEM_COMPETENCY_MAPPING` to map `A01-A12` keys, excluding `A04` (AC1) and `A09` (AC2) to prevent key errors.
* **Scale and Reverse Scoring**:
  * Adapted reverse-scoring for the `-1 to 2` scale. The formula `reversed_val = 1.0 - val` maps `2 -> -1`, `1 -> 0`, `0 -> 1`, and `-1 -> 2` perfectly.
  * Set `REVERSE_SCORED_ITEMS = ['A02', 'A10', 'A12']` to match the survey specification.
* **Attention Checks Filter**:
  * Updated the filter in `preprocess_survey` to check for expected values of `1` for AC1 (A04) and `-1` for AC2 (A09).
  * Enhanced the column finder to match columns containing `AC1/A04` and `AC2/A09` to handle different Excel header exports.
* **Plot Labels**:
  * Changed the box-plot label from `Aggregated Survey Score (1-5)` to `Aggregated Survey Score (-1 to 2)` to match the new scoring profile.

---

## 🎯 Claude Continuation Prompt
Copy and paste the prompt below into Claude to continue the task in your next session:

```markdown
Hi Claude, I want to continue working on an HR Analytics Performance Predictor model for Jio Platforms Limited (JioCX).

We have just redesigned the survey layout to make it shorter and simpler (reduced to 12 questions in Section A, using a 4-point scale mapping to -1, 0, 1, 2, and adding dynamic qualitative options in Section D).

Here are the key files we are working with:
1. `(M) (J) Shortened Behavioral Survey 12Q.html` - The survey UI layout and text copying utility.
2. `survey_analysis_utility.py` - The script that processes survey responses and correlates them with OLP historical rating data.

Please help me with the following next steps:
1. Review the changes made in `(M) (J) Shortened Behavioral Survey 12Q.html` and `survey_analysis_utility.py` to ensure they are fully aligned.
2. Verify if we need to mock survey response data to test the preprocessing script. If so, write a python utility script to generate mock Excel survey responses for 150 employees with job levels (Junior, Manager, Leader) and ratings in the -1 to 2 scale, including some simulated attention check failures to test the data-cleaning filter.
3. Suggest how we should handle Phase 1, Step 3: "Extract Key Competencies and Map to Lominger Framework" based on the survey analysis results.
```
