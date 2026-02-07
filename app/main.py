import streamlit as st
import pandas as pd
from app.database import init_db, load_all_data
from app.excel_bot import process_report_316
from app.contests import get_rankings
from app.alerts import run_alert_logic

# Page Config
st.set_page_config(page_title="SuperAchiever Portal", layout="wide", page_icon="🚀")
init_db()

# Aesthetic CSS Overhaul
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    /* Metric Box Styling */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    /* Metric Value Styling (Smaller font to prevent truncation) */
    div[data-testid="stMetricValue"] {
        color: #1f2937 !important;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
    }
    /* Metric Label Styling */
    div[data-testid="stMetricLabel"] {
        color: #6b7280 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 SuperAchiever Digitalization Portal")
st.markdown("---")

# --- 📂 Sidebar: Two-Button Workflow ---
st.sidebar.header("⚙️ Admin Tools")
uploaded_file = st.sidebar.file_uploader("1. Upload Report 316", type="xlsx")

if uploaded_file:
    if st.sidebar.button("🚀 Process Bot"):
        with st.spinner("Processing..."):
            count, file_path = process_report_316(uploaded_file)
            st.sidebar.success(f"Successfully processed {count} records!")
            st.rerun()

df = load_all_data()

if not df.empty:
    # Sidebar Download Button (Step 2)
    st.sidebar.markdown("---")
    csv = df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="📥 Download Daily Submission",
        data=csv,
        file_name='Daily_Submission.csv',
        mime='text/csv',
        use_container_width=True
    )

    # --- KPI SECTION (Professional Titles) ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_afyc = df['AFYC'].sum() if 'AFYC' in df.columns else 0
        st.metric("Total Agency Revenue", f"RM {total_afyc:,.2f}")
    with col2:
        st.metric("New Submissions", f"{len(df)} Cases")
    with col3:
        # Match your UPPERCASE database column
        p_col = 'PROPOSAL_STATUS'
        pending = len(df[df[p_col].str.contains('Pending', case=False, na=False)]) if p_col in df.columns else 0
        st.metric("Cases Awaiting Action", pending)
    with col4:
        a_col = 'AGENT_NAME'
        top_agent = df.groupby(a_col)['AFYC'].sum().idxmax() if a_col in df.columns else "N/A"
        # Truncate long names gracefully
        display_name = (top_agent[:18] + '..') if len(top_agent) > 18 else top_agent
        st.metric("Current Top Agent", display_name)
    
    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["📊 Submissions Overview", "⚠️ Alert Center", "🏆 Contest Leaderboard"])

    with tab1:
        st.subheader("📋 Filtered Submission Data")
        st.dataframe(df, use_container_width=True, height=450)

    with tab2:
        st.subheader("⚠️ Pending Case Alerts")
        st.info("The system automatically scans for cases pending for 3 or 7 days.")
        if st.button("🔍 Run Alert Analysis"):
            run_alert_logic(df)

    with tab3:
        st.subheader("🏆 Contest Rankings")
        c_type = st.selectbox("Contest Type", ["General", "NAIS", "Etiqa Bonus"])
        ranks = get_rankings(df, c_type)
        if not ranks.empty:
            st.bar_chart(ranks, color="#29b5e8")
            st.table(ranks.rename("Total AFYC (RM)"))
else:
    st.info("👋 Welcome! Please upload 'Report 316' in the sidebar to populate the dashboard.")