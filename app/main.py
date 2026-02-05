import streamlit as st
from app.database import init_db, load_all_data
from app.excel_bot import process_report_316
from app.contests import get_rankings
from app.alerts import run_alert_logic

# Page Config
st.set_page_config(page_title="SuperAchiever Portal", layout="wide")
init_db()

st.title("🚀 SuperAchiever Digitalization Portal")

# Sidebar - Admin Upload
st.sidebar.header("Admin Tools")
uploaded_file = st.sidebar.file_uploader("Upload Report 316", type="xlsx")

if uploaded_file:
    if st.sidebar.button("Process & Automate"):
        # Fixed: Catching both return values from the bot
        count, file_path = process_report_316(uploaded_file)
        st.sidebar.success(f"Processed {count} records!")
        st.sidebar.info(f"File saved in: {file_path}")

# Load Data
df = load_all_data()

if not df.empty:
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "⚠️ Pending Alerts", "🏆 Contest Rankings"])

    with tab1:
        st.subheader("Daily Submissions Overview")
        st.dataframe(df, use_container_width=True)

        # Download Button inside the tab
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Daily Submissions (CSV)",
            data=csv,
            file_name='Daily_Submissions.csv',
            mime='text/csv',
        )

    with tab2:
        st.subheader("⚠️ 3-Day & 7-Day Pending Cases")
        if st.button("Run Alert Bot"):
            run_alert_logic(df)
            st.success("Alerts sent to Admin email!")

    with tab3:
        st.subheader("🏆 Leaderboard")
        c_type = st.selectbox("Select Contest", ["General", "NAIS", "Etiqa Bonus"])
        ranks = get_rankings(df, c_type)
        
        # This shows the bar chart
        st.bar_chart(ranks)
        
        # --- ADD THE NEW LINES HERE ---
        st.subheader("📋 Detailed Ranking Table")
        st.table(ranks.rename("Total AFY (RM)"))
        # ------------------------------
else:
    st.info("No data found. Please upload 'Report 316' in the sidebar.")