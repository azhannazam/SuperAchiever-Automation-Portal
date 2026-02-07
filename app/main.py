import streamlit as st
import pandas as pd
from app.database import init_db, load_all_data
from app.excel_bot import process_report_316
from app.contests import get_rankings
from app.alerts import run_alert_logic

# Page Config for a professional look
st.set_page_config(page_title="SuperAchiever Portal", layout="wide", page_icon="🚀")
init_db()

# Custom CSS to fix the white boxes and text colors
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    div[data-testid="stMetricValue"] { color: #1f2937 !important; font-size: 1.8rem !important; }
    div[data-testid="stMetricLabel"] { color: #4b5563 !important; font-size: 1rem !important; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e5e7eb; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; border-radius: 8px 8px 0 0; padding: 0 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 SuperAchiever Digitalization Portal")
st.markdown("---")

# --- 📂 Sidebar: Two-Button Workflow ---
st.sidebar.header("⚙️ Admin Tools")
uploaded_file = st.sidebar.file_uploader("1. Upload Report 316", type="xlsx")

if uploaded_file:
    if st.sidebar.button("🚀 Process Bot"):
        count, file_path = process_report_316(uploaded_file)
        st.sidebar.success(f"Processed {count} records!")
        st.rerun() # Refresh to show new data

# Show download button only if data exists
df = load_all_data()
if not df.empty:
    st.sidebar.markdown("---")
    csv = df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="📥 Download Daily Submission",
        data=csv,
        file_name=f'Daily_Submission_{pd.Timestamp.now().strftime("%Y%m%d")}.csv',
        mime='text/csv',
        use_container_width=True
    )

# --- Main Dashboard Content ---
if not df.empty:
    # 🏆 KPI Metrics (Readable Colors)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_afyc = df['AFYC'].sum()
        st.metric("Total AFYC", f"RM {total_afyc:,.2f}")
    with col2:
        st.metric("Total Submissions", len(df))
    with col3:
        pending = len(df[df['PROPOSAL_STATUS'].str.contains('Pending', case=False, na=False)])
        st.metric("Pending Cases", pending)
    with col4:
        top_agent = df.groupby('AGENT_NAME')['AFYC'].sum().idxmax()
        st.metric("Top Performer", f"{top_agent[:15]}...")

    tab1, tab2, tab3 = st.tabs(["📊 Submissions", "⚠️ Alerts", "🏆 Leaderboards"])

    with tab1:
        st.dataframe(df, use_container_width=True, height=500)

    with tab2:
        st.subheader("⚠️ Case Monitoring")
        if st.button("🔍 Run Alert Analysis"):
            run_alert_logic(df)

    with tab3:
        st.subheader("🏆 Contest Rankings")
        c_type = st.selectbox("Select Contest Type", ["General", "NAIS", "Etiqa Bonus"])
        ranks = get_rankings(df, c_type)
        if not ranks.empty:
            st.bar_chart(ranks, color="#29b5e8")
            st.table(ranks.rename("Total AFYC (RM)"))
else:
    st.info("👋 Welcome! Please upload 'Report 316' in the sidebar to begin.")