import pandas as pd
from datetime import datetime
import streamlit as st

def run_alert_logic(df):
    # Match your real database column names (UPPERCASE)
    date_col = 'ENTRY_DATE'
    status_col = 'PROPOSAL_STATUS'
    
    if date_col not in df.columns:
        st.error(f"Column {date_col} not found in database!")
        return

    # Convert to datetime safely
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    today = datetime.now()

    # Filter for Pending cases only
    pending_df = df[df[status_col].str.contains('Pending', case=False, na=False)].copy()
    
    # Calculate days passed
    pending_df['days_passed'] = (today - pending_df[date_col]).dt.days
    
    # Identify 3rd and 7th day cases
    day3 = pending_df[pending_df['days_passed'] == 3]
    day7 = pending_df[pending_df['days_passed'] >= 7]

    # Professional UI Output
    st.write(f"### 📢 Alert Processing Results")
    col1, col2 = st.columns(2)
    col1.metric("3-Day Follow-up", len(day3))
    col2.metric("7-Day Critical", len(day7))

    if len(day7) > 0:
        st.warning(f"🚨 Found {len(day7)} cases pending for over a week!")
        st.dataframe(day7[['AGENT_NAME', 'PROPOSALNO', 'days_passed']])
    else:
        st.success("✅ No critical 7-day delays found.")