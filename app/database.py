import sqlite3
import pandas as pd
from config import DB_NAME

def get_conn():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_conn()
    # Added PAYMENT_FREQUENCY to match your newest required_columns
    conn.execute('''CREATE TABLE IF NOT EXISTS submissions 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     PROPOSAL_STATUS TEXT, 
                     ENTRY_DATE TEXT, 
                     PROPOSALNO TEXT,
                     RISK_COMMENCEMENT_DATE TEXT, 
                     AM_NAME TEXT, 
                     AGENT_NAME TEXT,
                     AGENT_CODE TEXT, 
                     PAYMENT_METHOD TEXT, 
                     AFYC REAL, 
                     FACTOR REAL,
                     TOTAL_EXPECTED_DUE REAL, 
                     POLY_STATUS TEXT, 
                     POLICYNO TEXT, 
                     PRODUCT_NAME TEXT, 
                     PAYMENT_FREQUENCY TEXT,  -- <--- Added this line
                     processed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.close()

def save_to_db(df):
    conn = get_conn()
    df.to_sql('submissions', conn, if_exists='append', index=False)
    conn.close()

def load_all_data():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM submissions", conn)
    conn.close()
    return df