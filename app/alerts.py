import pandas as pd
from datetime import datetime
import smtplib
from email.message import EmailMessage
from config import EMAIL_USER, EMAIL_PASS, RECEIVER_ADMIN

def run_alert_logic(df):
    """
    Main logic to calculate pending days and trigger emails.
    Called by main.py
    """
    if df.empty:
        return 0

    # 1. Convert Entry_Date to datetime objects for calculation
    df['Entry_Date'] = pd.to_datetime(df['Entry_Date'], errors='coerce')
    today = datetime.now()
    
    # 2. Filter for 'Pending' cases only
    # Note: Using .str.contains to catch 'Pending - Payment', 'Pending - Docs', etc.
    pending = df[df['Proposal_Status'].str.contains('Pending', case=False, na=False)].copy()
    
    # 3. Calculate age of the case
    pending['days_old'] = (today - pending['Entry_Date']).dt.days
    
    alerts_triggered = 0
    
    for _, row in pending.iterrows():
        days = int(row['days_old'])
        
        # Trigger alert only on exactly the 3rd or 7th day
        if days == 3 or days == 7:
            send_email(row, days)
            alerts_triggered += 1
            
    return alerts_triggered

def send_email(row, days):
    # Determine priority based on days
    priority = "NORMAL" if days == 3 else "HIGH ALERT"
    
    # Create a WhatsApp link for the admin to 'nudge' the agent immediately
    # Assuming the Excel has an 'Agent_phone' column; if not, this link stays generic
    agent_contact = getattr(row, 'Agent_phone', '601XXXXXXXXX') # Default MY number format
    wa_link = f"https://wa.me/{agent_contact}?text=Reminder: Case {row['ProposalNo']} is still pending for {days} days."

    msg = EmailMessage()
    msg['Subject'] = f"[{priority}] {days}-Day Pending: {row['ProposalNo']} ({row['Agent_name']})"
    msg['From'] = EMAIL_USER
    msg['To'] = RECEIVER_ADMIN
    
    body = f"""
    SuperAchiever Admin Notification:
    
    Case ID: {row['ProposalNo']}
    Agent: {row['Agent_name']}
    Product: {row['Product_name']}
    Days Pending: {days}
    
    Action Required:
    - On Day 3: Normal follow-up.
    - On Day 7: Admin to contact agent immediately to settle the case.
    
    Quick WhatsApp Agent: {wa_link}
    """
    msg.set_content(body)
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)
    except Exception as e:
        print(f"SMTP Error: {e}")