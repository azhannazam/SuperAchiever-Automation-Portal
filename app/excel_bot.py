import pandas as pd
import os
from datetime import datetime
from app.database import save_to_db

def process_report_316(file_path):
    # 1. Load the file
    df = pd.read_excel(file_path)
    
    # 2. Filter by GAM_NAME (Exactly matching 'SuperAchiever')
    # This catches 'superachiever', 'SUPERACHIEVER', and handles spaces
    filtered_df = df[df['GAM_NAME'].str.strip().str.contains('SuperAchiever', case=False, na=False)].copy()
    
    # 3. Select only the 14 required columns
    required_columns = [
        "PROPOSAL_STATUS", "ENTRY_DATE", "PROPOSALNO", 
        "RISK_COMMENCEMENT_DATE", "AM_NAME", "AGENT_NAME", 
        "AGENT_CODE", "PAYMENT_METHOD", "AFYC", "Factor", 
        "TOTAL_EXPECTED_DUE", "POLY_STATUS", "POLICYNO", "PRODUCT_NAME", "PAYMENT_FREQUENCY"
    ]
    
    # Check if columns exist to avoid errors
    existing_cols = [col for col in required_columns if col in filtered_df.columns]
    final_df = filtered_df[existing_cols].copy()

    # 4. Data Cleaning: Ensure numeric columns are actually numbers
    numeric_cols = ["AFYC", "Factor", "TOTAL_EXPECTED_DUE"]
    for col in numeric_cols:
        if col in final_df.columns:
            final_df[col] = pd.to_numeric(final_df[col], errors='coerce').fillna(0)
    
    # 5. Save to Database
    save_to_db(final_df)
    
    # 6. Create the "Daily Submission" Excel file for the Admin
    output_folder = "data/daily_submissions"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_filename = f"{output_folder}/Daily_Submissions_{timestamp}.xlsx"
    
    final_df.to_excel(output_filename, index=False)
    
    return len(final_df), output_filename