import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for visualizations
sns.set_theme(style="whitegrid", palette="muted")

# Define the 10 competency dimensions
COMPETENCY_MAP = {
    'EE': 'Executing with Excellence',
    'ST': 'Strategic Thinking',
    'LA': 'Learning Agility',
    'CI': 'Collaboration & Influence',
    'PS': 'Problem Solving & Decision Making',
    'DI': 'Drive & Initiative',
    'PL': 'People Leadership',
    'CM': 'Communication',
    'RE': 'Resilience',
    'CO': 'Customer/Stakeholder Orientation'
}

# Mapping of survey item IDs to competencies (same mapping across levels)
ITEM_COMPETENCY_MAPPING = {
    'A01': 'EE', 'A02': 'EE',
    'A03': 'ST', 'A04': 'ST',
    'A05': 'LA', 'A06': 'LA',
    'A07': 'CI', 'A08': 'CI',
    'A09': 'PS', 'A10': 'PS',
    'A11': 'DI', 'A12': 'DI',
    'A13': 'PL', 'A14': 'PL',
    'A15': 'CM', 'A16': 'CM',
    'A17': 'RE', 'A18': 'RE',
    'A19': 'CO', 'A20': 'CO'
}

# Even-numbered items are reverse-scored (indicated by R in survey design)
REVERSE_SCORED_ITEMS = ['A02', 'A04', 'A06', 'A08', 'A10', 'A12', 'A14', 'A16', 'A18', 'A20']

def load_data(survey_path, olp_path):
    """
    Loads the survey responses Excel and the OLP Scored Master Excel.
    """
    print(f"📂 Loading survey responses from: {survey_path}")
    df_survey = pd.read_excel(survey_path)
    
    print(f"📂 Loading OLP scored data from: {olp_path}")
    df_olp = pd.read_excel(olp_path)
    
    return df_survey, df_olp

def preprocess_survey(df_survey):
    """
    Preprocesses survey results, applying reverse scoring and calculating competency averages.
    
    Expected survey columns naming convention (change mapping if Forms exports differently):
    - 'Email' or 'Employee ID' as matching key
    - 'Job Level' to identify junior, manager, leader
    - 'AC1' (Attention Check 1): expected response = 4
    - 'AC2' (Attention Check 2): expected response = 1
    - Likert columns: 'A01', 'A02', ..., 'A20' (scaled 1-5)
    """
    # 1. Filter out failed attention checks to guarantee data quality
    initial_rows = len(df_survey)
    
    # Check if attention check columns exist, filter if they do
    ac_cols = [c for c in df_survey.columns if 'AC1' in str(c) or 'AC2' in str(c)]
    if len(ac_cols) >= 2:
        ac1_col = [c for c in ac_cols if 'AC1' in str(c)][0]
        ac2_col = [c for c in ac_cols if 'AC2' in str(c)][0]
        
        # Keep only respondents passing both attention checks
        df_survey = df_survey[(df_survey[ac1_col] == 4) & (df_survey[ac2_col] == 1)]
        cleaned_rows = len(df_survey)
        print(f"🧹 Attention Checks Filter: Removed {initial_rows - cleaned_rows} rows (Initial: {initial_rows}, Cleaned: {cleaned_rows})")
    else:
        print("⚠️ Warning: Attention check columns (AC1/AC2) not found. Skipping data quality filter.")

    # 2. Extract Likert responses and calculate competency scores
    # We look for columns matching A01-A20 pattern
    likert_cols = {}
    for col in df_survey.columns:
        match = [item_id for item_id in ITEM_COMPETENCY_MAPPING.keys() if item_id in str(col)]
        if match:
            likert_cols[col] = match[0] # maps excel column name to short ID (e.g. 'A01')

    if not likert_cols:
        raise ValueError("❌ Error: Could not find Likert columns matching A01-A20 pattern in the survey file. Please verify headers.")

    processed_records = []
    
    # Process row-by-row
    for idx, row in df_survey.iterrows():
        record = {
            'Employee ID': row.get('Employee ID') or row.get('Employee Code') or row.get('Emp.Code'),
            'Full Name': row.get('Full Name') or row.get('Name'),
            'Job Level': row.get('Job Level') or row.get('Band')
        }
        
        # Calculate competency-level sums/counts
        comp_scores = {c: [] for c in COMPETENCY_MAP.keys()}
        
        for col_name, item_id in likert_cols.items():
            val = row[col_name]
            if pd.isna(val):
                continue
                
            # Parse to numeric if string
            try:
                val = float(val)
            except:
                continue
                
            # Apply reverse scoring for even-numbered items: Scored = 6 - Response
            if item_id in REVERSE_SCORED_ITEMS:
                val = 6.0 - val
                
            comp_id = ITEM_COMPETENCY_MAPPING[item_id]
            comp_scores[comp_id].append(val)
            
        # Average the items for each competency
        for comp_id, scores in comp_scores.items():
            record[f"Score_{comp_id}"] = np.mean(scores) if scores else np.nan
            
        processed_records.append(record)
        
    df_processed = pd.DataFrame(processed_records)
    print("✅ Completed reverse-scoring and competency aggregation.")
    return df_processed

def merge_and_correlate(df_processed_survey, df_olp, output_dir):
    """
    Merges the processed survey data with the OLP Performance metrics and runs validation.
    """
    # Standardize join key
    # Survey ID column name
    survey_key = 'Employee ID'
    # OLP Code column name (usually 'Emp.Code' or 'Employee Code')
    olp_key = 'Emp.Code' if 'Emp.Code' in df_olp.columns else 'Employee Code'
    
    # Clean keys
    df_processed_survey[survey_key] = df_processed_survey[survey_key].astype(str).str.strip()
    df_olp[olp_key] = df_olp[olp_key].astype(str).str.strip()
    
    # Merge datasets
    df_merged = pd.merge(
        df_processed_survey,
        df_olp,
        left_on=survey_key,
        right_on=olp_key,
        how='inner'
    )
    
    print(f"🔗 Merged Survey and OLP profiles. Match count: {len(df_merged)} rows.")
    if len(df_merged) == 0:
        print("⚠️ Warning: 0 overlapping records matched between Survey and OLP. Double-check employee code formats!")
        return df_merged
        
    # Analyze correlations
    comp_score_cols = [f"Score_{c}" for c in COMPETENCY_MAP.keys()]
    
    # Calculate correlations with OLP Composite Performance Score
    olp_composite_col = 'composite_score' if 'composite_score' in df_olp.columns else 'Composite Score'
    if olp_composite_col in df_merged.columns:
        correlations = {}
        for c_col in comp_score_cols:
            if c_col in df_merged.columns:
                corr = df_merged[c_col].corr(df_merged[olp_composite_col], method='pearson')
                correlations[c_col.replace('Score_', '')] = round(corr, 3)
                
        df_corr = pd.DataFrame(list(correlations.items()), columns=['Competency_ID', 'Correlation_with_OLP'])
        df_corr['Competency_Name'] = df_corr['Competency_ID'].map(COMPETENCY_MAP)
        df_corr = df_corr.sort_values(by='Correlation_with_OLP', ascending=False)
        
        print("\n📈 COMPETENCY CORRELATION WITH OLP PERFORMANCE:")
        print(df_corr.to_string(index=False))
        
        # Save Excel report of correlation results
        df_corr.to_excel(os.path.join(output_dir, 'survey_olp_correlations.xlsx'), index=False)
        print(f"💾 Correlation report saved to {os.path.join(output_dir, 'survey_olp_correlations.xlsx')}")
        
        # Generate Visualization Plots
        generate_plots(df_merged, df_corr, comp_score_cols, olp_composite_col, output_dir)
        
    return df_merged

def generate_plots(df_merged, df_corr, comp_score_cols, olp_composite_col, output_dir):
    """
    Generates analytics visualization figures.
    """
    # 1. Bar plot of correlations
    plt.figure(figsize=(10, 6))
    sns.barplot(
        x='Correlation_with_OLP', 
        y='Competency_Name', 
        data=df_corr, 
        palette='Blues_r'
    )
    plt.title('Predictive Power: Competency Survey Correlation with OLP Composite Score')
    plt.xlabel('Pearson Correlation Coefficient (r)')
    plt.ylabel('Competency Dimension')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'competency_correlations.png'), dpi=300)
    plt.close()
    
    # 2. Box plots of key competencies by Performance Tier
    tier_col = 'performance_tier' if 'performance_tier' in df_merged.columns else 'Performance Tier'
    if tier_col in df_merged.columns:
        # Get top 2 correlated competencies
        top_comps = df_corr['Competency_ID'].head(2).tolist()
        
        for idx, comp in enumerate(top_comps):
            plt.figure(figsize=(8, 5))
            sns.boxplot(
                x=tier_col,
                y=f"Score_{comp}",
                data=df_merged,
                order=['Below Expectation', 'Developing', 'Meets Expectation', 'Exceeds', 'Star Performer'],
                palette='viridis'
            )
            plt.title(f"{COMPETENCY_MAP[comp]} Scores across OLP Performance Tiers")
            plt.xlabel('OLP Performance Tier')
            plt.ylabel('Aggregated Survey Score (1-5)')
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, f'boxplot_tier_{comp}.png'), dpi=300)
            plt.close()
            
    print("🎨 Analytics plots generated and saved as PNG files.")

if __name__ == "__main__":
    # Template paths (adjust to matching folders on run)
    SURVEY_FILE_PATH = r"C:\Users\Vivek267.Kumar\Desktop\Performance Predictor Project\(D) Employee Data and Performance History (by anisha)\Survey_Responses_Demo.xlsx"
    OLP_FILE_PATH = r"C:\Users\Vivek267.Kumar\Desktop\Performance Predictor Project\(K) Project\Employee Rating Analysis.xlsx"
    OUTPUT_DIRECTORY = r"C:\Users\Vivek267.Kumar\Desktop\Performance Predictor Project\(K) Project"
    
    print("🚀 Running JioCX Competency Survey Analysis Utility...")
    
    # Example execution warning
    if not os.path.exists(SURVEY_FILE_PATH):
        print(f"\n💡 Setup Notice: Set SURVEY_FILE_PATH to point to your MS Forms Excel output once data collection is complete.")
        print(f"Example run path assumed: {SURVEY_FILE_PATH}")
    else:
        try:
            survey_data, olp_data = load_data(SURVEY_FILE_PATH, OLP_FILE_PATH)
            processed_survey = preprocess_survey(survey_data)
            merged_master = merge_and_correlate(processed_survey, olp_data, OUTPUT_DIRECTORY)
            
            # Save master dataset with combined profiles
            merged_master.to_excel(os.path.join(OUTPUT_DIRECTORY, 'JioCX_Predictor_Master_Dataset.xlsx'), index=False)
            print(f"🎉 Success! Combined Master Dataset saved to {os.path.join(OUTPUT_DIRECTORY, 'JioCX_Predictor_Master_Dataset.xlsx')}")
        except Exception as e:
            print(f"❌ Error executing script: {e}")
