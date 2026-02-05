from app.excel_bot import process_report_316
from app.database import init_db, get_conn
import pandas as pd
import os

def test_run():
    print("--- 🤖 Starting Bot Test Run ---")
    
    # 1. Initialize the database
    print("[1/4] Initializing Database...")
    init_db()
    
    # 2. Path to your test file
    test_file = "Report_316_Actual_Feb.xlsx" 
    
    if not os.path.exists(test_file):
        print(f"❌ Error: Please create {test_file} first!")
        return

    # 3. Run the processing logic
    print(f"[2/4] Processing {test_file}...")
    try:
        count, output_path = process_report_316(test_file)
        print(f"✅ Success! {count} rows filtered for 'SuperAchiever'.")
        print(f"📄 Daily Submission file created at: {output_path}")
    except Exception as e:
        print(f"❌ Processing failed: {e}")
        return

    # 4. Verify Database Entry
    print("[3/4] Verifying Database...")
    conn = get_conn()
    db_df = pd.read_sql("SELECT * FROM submissions", conn)
    conn.close()
    
    if len(db_df) > 0:
        print(f"✅ Database check passed! {len(db_df)} total records in DB.")
        print("\n--- Preview of Filtered Data ---")
        print(db_df[['AGENT_NAME', 'PROPOSALNO', 'TOTAL_EXPECTED_DUE']].head())
    else:
        print("❌ Database is empty. Check if GAM_NAME matches 'SuperAchiever' exactly.")

    print("\n[4/4] Test Complete!")

if __name__ == "__main__":
    test_run()