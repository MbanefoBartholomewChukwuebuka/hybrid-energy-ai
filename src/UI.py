import streamlit as st
import pandas as pd

from agent import EnergyMonitoringAgent
from database import create_table, log_energy, get_energy_history

# INIT
create_table()
agent = EnergyMonitoringAgent()

# PAGE CONFIG (must be first)
st.set_page_config(
    page_title="AI Energy Dashboard",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ AI Energy Monitoring Dashboard")

# SIDEBAR INPUT
st.sidebar.header("Log Energy Usage")

user_id = st.sidebar.text_input("User ID", value="user_123")
energy_kwh = st.sidebar.number_input("Energy Usage (kWh)", min_value=0.0, step=0.1)

if st.sidebar.button("Analyze Energy"):

    result = agent.analyze_energy(user_id, energy_kwh)

    st.success(f"Logged {energy_kwh} kWh for {user_id}")

    col1, col2 = st.columns(2)

    with col1:
        if result["ml_prediction"] is not None:
            st.metric("Predicted Usage", round(result["ml_prediction"], 2))
        else:
            st.warning("Need at least 2 records for prediction")

    with col2:
        st.metric("Current Usage", energy_kwh)

    st.subheader("AI Analysis")
    st.write(result["llm_analysis"])


st.divider()

# HISTORY SECTION
st.subheader("📊 Energy History")

history = get_energy_history(user_id)

if history and len(history) > 0:

    df = pd.DataFrame(history, columns=["Energy Usage (kWh)", "Date"])
    df = df[["Date", "Energy Usage (kWh)"]]

    st.dataframe(df, use_container_width=True)

    st.line_chart(df.set_index("Date"))

    st.subheader("📌 Insights")
    st.metric("Total Usage", df["Energy Usage (kWh)"].sum())
    st.metric("Average Usage", df["Energy Usage (kWh)"].mean())

else:
    st.info("No energy data found. Start logging usage from the sidebar.")