# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 11:31:50 2026

@author: Manna
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="Kärna Service Logic", layout="wide")

# --- BACKGROUND SYNC SIMULATION (The 24h Cycle) ---
@st.cache_data(ttl=86400) # This forces a 24-hour refresh cycle
def sync_fortnox_data():
    dates = pd.date_range(end=datetime.today(), periods=90, freq='D')
    # Logic: Input Waste (Ingredients) vs Output Waste (Sales/Plate)
    data = {
        'date': dates,
        'supplier_spend': np.random.uniform(10000, 15000, size=90),
        'ingredient_waste': np.random.uniform(5, 15, size=90), # INPUT
        'plate_waste': np.random.uniform(2, 8, size=90),      # OUTPUT
        'contract_hrs': [160] * 90,
        'actual_hrs': np.random.uniform(160, 185, size=90),
        'burnout_max': np.random.uniform(4, 15, size=90)
    }
    return pd.DataFrame(data)

df = sync_fortnox_data()

# --- HEADER & COMPLIANCE ---
st.title(" Kärna Service Logic")
st.info(" Last sync with Fortnox: Today at 02:00 AM (24h Cycle)")

# THE COMPLIANCE TABLE (Visible Audit Logic)
st.subheader(" Compliance: ESRS Mapping")
map_col1, map_col2 = st.columns([2, 1])

with map_col1:
    mapping = {
        "Data Source": ["Acc 4010 (Invoices)", "Sales/POS Data", "Fortnox Time"],
        "Waste Category": ["Input (Ingredients)", "Output (Ready-made)", "Social (S1)"],
        "ESRS Code": ["E5: Resource Use", "E5: Waste Management", "S1: Workforce"]
    }
    st.table(pd.DataFrame(mapping))

with map_col2:
    st.write("**Audit Ready**")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(" EXPORT AUDIT REPORT", csv, "Karna_Audit.csv", "text/csv", use_container_width=True)

st.divider()

# --- ANALYTICS ---
view = st.radio("Switch View", ["Sustainability (E5)", "Workforce (S1)"], horizontal=True)

if view == "Sustainability (E5)":
    st.subheader("Waste Analysis: Ingredients vs. Ready-made")
    # This chart explicitly shows Input vs Output
    st.area_chart(df.set_index('date')[['ingredient_waste', 'plate_waste']])
    st.caption("Lower area: Ingredient Spoilage (Input) | Upper area: Unsold Ready-made/Plate Waste (Output)")
else:
    st.subheader("Labor Intensity: Contract vs. Actual")
    st.line_chart(df.set_index('date')[['actual_hrs', 'contract_hrs']])
    st.caption("Monitoring the delta to identify S1 Burnout risks.")

st.success(f"Potential recovery identified: **{(df['supplier_spend'].sum()*0.12):,.0f} SEK**")
