# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 11:31:50 2026

@author: Manna
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

 # PAGE SETUP
st.set_page_config(page_title="Service Logic: CSRD/ESRS Dashboard", layout="wide")

# THE "BRAIN" (Synthetic Data Harvester)
# This simulates the data coming from Fortnox Supplier Invoices & Payroll
@st.cache_data
def harvest_simulated_fortnox_data():
    dates = pd.date_range(end=datetime.today(), periods=120, freq='D')
    data = {
        'date': dates,
        'supplier_invoice_sek': np.random.uniform(8000, 25000, size=120),
        'food_category': np.random.choice(['Meat/Dairy', 'Produce', 'Dry Goods'], size=120),
        'waste_estimate_kg': np.random.uniform(15, 60, size=120),
        'staff_overtime_hours': np.random.uniform(0, 15, size=120),
        'event_tag': np.random.choice(['None', 'Hockey Game', 'Corporate Event', 'Wedding'], p=[0.7, 0.1, 0.1, 0.1], size=120)
    }
    df = pd.DataFrame(data)
    # Inject "spikes" for event days to show predictive capability
    df.loc[df['event_tag'] != 'None', 'waste_estimate_kg'] *= 1.8
    df.loc[df['event_tag'] != 'None', 'staff_overtime_hours'] *= 2.5
    return df

df = harvest_simulated_fortnox_data()

# HEADER & SECTOR SELECTION
st.title(" Service Industry Intelligence: CSRD & ESRS Compliance")
st.markdown("""
**Domain:** Large-Scale Kitchens & Event Management | **Regulation:** ESRS E5 & S1
*Bridging the gap between Fortnox Financials and Sustainability Reporting.*
""")

# TOP LEVEL METRICS (The CFO View)
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_waste = df['waste_kg' if 'waste_kg' in df else 'waste_estimate_kg'].sum()
    st.metric("Total Food Waste (E5)", f"{total_waste:,.0f} kg", delta="-4.2% (Benchmark)")

with col2:
    # Logic: Overtime > 10% of total hours = High Burnout Risk
    burnout_risk = "CRITICAL" if df['staff_overtime_hours'].tail(7).mean() > 8 else "STABLE"
    st.metric("Workforce Stability (S1)", burnout_risk, delta="Burnout Alert" if burnout_risk == "CRITICAL" else "Good")

with col3:
    # Financial Materiality: Waste cost estimate
    waste_cost = (df['supplier_invoice_sek'].sum() * 0.18) # Assuming 18% cost of waste
    st.metric("Financial Leakage (Waste)", f"{waste_cost:,.0f} SEK")

with col4:
    st.metric("CSRD Readiness", "82%", delta="Ready for Audit")

# THE "EVENT SPIKE" ANALYSIS (Social + Logistical Logic)
st.divider()
st.subheader(" Event Impact Analysis: Waste vs. Staff Burnout")
st.write("This chart visualizes how high-pressure events (like Hockey Games) correlate with waste spikes and staff stress.")

chart_data = df.set_index('date')[['waste_estimate_kg', 'staff_overtime_hours']]
st.area_chart(chart_data)

# CONSULTING INSIGHT GENERATOR (The Data Science Piece)
st.sidebar.header("Strategy Controls")
st.sidebar.write("Simulate operational changes:")
reduction_target = st.sidebar.slider("Waste Reduction Target (%)", 0, 50, 15)

predicted_savings = waste_cost * (reduction_target / 100)

st.sidebar.success(f"**Projected Annual Savings:** {predicted_savings:,.0f} SEK")

# MOCK FORTNOX "TRANSLATION" (The Demonstration)
with st.expander(" View Fortnox-to-ESRS Data Mapping"):
    st.info("This section shows how we translate raw financial codes into regulatory metrics.")
    
    mapping_demo = {
        "Fortnox Account": ["4010 (Purchases)", "7010 (Salaries)", "7210 (Overtime)", "5410 (Consumables)"],
        "ESRS Category": ["E5: Resource Inflow", "S1: Workforce Impact", "S1: Working Conditions", "E5: Waste Management"],
        "Derived Metric": ["Food Volume (kg)", "Retention Rate", "Burnout Risk Index", "Packaging Waste (t)"]
    }
    st.table(pd.DataFrame(mapping_demo))

#  MONDAY PREP FOOTER
st.divider()
if st.button("Generate Preliminary ESRS Report (Draft)"):
    st.balloons()
    st.download_button("Download CSV for Auditor", df.to_csv(), "ESRS_Draft_Report.csv")
