import pandas as pd
import numpy as np
import os
import random

def generate_mock_survey_data():
    print("🚀 Starting Mock Survey Response Generator...")
    
    # 1. Paths configuration
    olp_path = r"C:\Users\Vivek267.Kumar\Desktop\Performance Predictor Project\(K) Project\Employee Rating Analysis.xlsx"
    if not os.path.exists(olp_path):
        olp_path = r"C:\Users\Vivek267.Kumar\Desktop\Performance Predictor Project\(D) Employee Data and Performance History (by anisha)\OLP Data.xlsx"
        
    output_dir = r"C:\Users\Vivek267.Kumar\Desktop\Performance Predictor Project\(D) Employee Data and Performance History (by anisha)"
    output_path = os.path.join(output_dir, "Survey_Responses_Demo.xlsx")
    
    if not os.path.exists(olp_path):
        print(f"❌ Error: OLP performance file not found at {olp_path}. Cannot align mock Employee IDs.")
        return
        
    # 2. Load OLP data to get valid employee codes and grades
    print(f"📂 Loading OLP data from {olp_path} to match Employee Codes...")
    df_olp = pd.read_excel(olp_path)
    
    # Standardize column names
    code_col = 'Emp.Code' if 'Emp.Code' in df_olp.columns else 'Employee Code'
    name_col = 'Name' if 'Name' in df_olp.columns else 'Full Name'
    grade_col = 'Current Grade' if 'Current Grade' in df_olp.columns else 'Grade'
    
    # Drop rows with missing code/name
    df_valid_employees = df_olp.dropna(subset=[code_col, name_col])
    
    # We will sample 150 employees to generate survey responses for
    sample_size = min(150, len(df_valid_employees))
    df_sample = df_valid_employees.sample(n=sample_size, random_state=42)
    
    # 3. Generate responses
    mock_records = []
    
    # Competency mapping to simulate correlation:
    # High-performer OLP ratings (A*, A+) map to high Likert values (4, 5).
    # Low-performer ratings (B, C) map to average/low Likert values (1, 2, 3).
    # We will compute a mock performance value based on recent OLP rating columns.
    rtg_cols = [c for c in df_olp.columns if 'RTG' in str(c)]
    
    for idx, row in df_sample.iterrows():
        emp_code = str(row[code_col]).strip()
        emp_name = row[name_col]
        grade = str(row[grade_col])
        
        # Determine job level based on grade
        if any(term in grade.lower() for term in ['president', 'vp', 'director', 'general manager', 'leader']):
            level = 'Leader / VP+'
        elif any(term in grade.lower() for term in ['manager', 'lead', 'head']):
            level = 'Manager / Team Lead'
        else:
            level = 'Junior / Executive'
            
        # Determine OLP performance rating (A*=4, A+=3, A=2, B=1)
        # We look at the latest rating column or average it
        ratings_numeric = []
        for r_col in rtg_cols:
            val = str(row[r_col]).strip()
            if 'A*' in val: ratings_numeric.append(4.0)
            elif 'A+' in val: ratings_numeric.append(3.5)
            elif 'A' in val: ratings_numeric.append(3.0)
            elif 'B' in val: ratings_numeric.append(2.0)
            elif 'C' in val: ratings_numeric.append(1.0)
            
        avg_perf = np.mean(ratings_numeric) if ratings_numeric else 2.5
        
        # 4. Generate Likert questions A01-A20 (base score scales with OLP performance)
        record = {
            'Employee ID': emp_code,
            'Full Name': emp_name,
            'Job Level': level,
        }
        
        # Add Demographics
        record['Average Weekly Work Hours'] = random.choice(['40–45', '46–50', '51–55', 'More than 55'])
        record['Number of Direct Reports'] = '0 (Individual Contributor)' if level == 'Junior / Executive' else random.choice(['1–3', '4–7', '8–12'])
        record['Cross‑Functional Project Involvement'] = random.choice(['Sometimes (20–40%)', 'Often (40–60%)', 'Very often (more than 60%)'])
        
        # Add Attention Checks
        # 92% pass rate, 8% fail rate
        if random.random() > 0.08:
            record['AC1'] = 4  # Pass value
            record['AC2'] = 1  # Pass value
        else:
            record['AC1'] = random.choice([1, 2, 3, 5])
            record['AC2'] = random.choice([2, 3, 4, 5])
            
        # Generate Likert scores
        # We introduce correlation by setting base probability distributions shifted by avg_perf
        for i in range(1, 21):
            col_id = f"A{i:02d}"
            
            # Base response from 1 to 5
            # Shift mean higher for top performers, lower for low performers
            mean_val = 2.2 + (avg_perf / 4.0) * 1.8 # Ranges from ~3.1 to ~4.0
            
            # Even items are reverse-scored (so their raw responses should be INVERTED to preserve correlation)
            if i in [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]:
                mean_val = 6.0 - mean_val # e.g. ranges from ~2.9 to ~2.0
                
            # Sample value using normal distribution and clip to 1-5
            val = int(np.clip(np.round(np.random.normal(mean_val, 0.8)), 1, 5))
            record[col_id] = val
            
        # Add Section D narrative lengths (character length to simulate word count limit validation)
        record['D1. Professional Achievement'] = "This is a detailed description of my achievement which has more than fifty words in total to pass the minimum validation requirements set by the survey."
        record['D2. Navigating Ambiguity'] = "I faced an ambiguous scenario where requirements were changing rapidly, so I structured the problem into small sprints and delivered successfully."
        record['D3. Your Distinct Value'] = "My colleagues appreciate my learning agility and collaboration, enabling me to bridge gaps between tech and business."
        record['D4. Area for Growth'] = "I want to improve my delegation skills to empower team members and focus more on strategic leadership tasks."
        record['D5. What It Takes to Excel Here'] = "To excel here you need deep customer orientation, persistence, and proactive communication across departments."
        
        mock_records.append(record)
        
    df_mock = pd.DataFrame(mock_records)
    
    # 5. Save responses to file
    df_mock.to_excel(output_path, index=False)
    print(f"🎉 Success! Mock Survey Response file generated at: {output_path}")
    print(f"📊 Total Records: {len(df_mock)} (Juniors: {len(df_mock[df_mock['Job Level'] == 'Junior / Executive'])}, Managers: {len(df_mock[df_mock['Job Level'] == 'Manager / Team Lead'])}, Leaders: {len(df_mock[df_mock['Job Level'] == 'Leader / VP+'])})")
    
if __name__ == "__main__":
    generate_mock_survey_data()
