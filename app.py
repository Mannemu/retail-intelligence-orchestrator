# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 11:31:50 2026

@author: Manna
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# 1. PAGE CONFIG
st.set_page_config(page_title="Kärna Service Logic | CSRD", layout="wide")

# 2. DATA ENGINE
@st.cache_data
def generate_granular_data(sector):
    dates = pd.date_range(end=datetime.today(), periods=90, freq='D')
    multipliers = {
        "Event Center": {"waste": 45, "overtime_max": 12, "vol": 20000, "staff_base": 160},
        "Hotel (F&B)": {"waste": 30, "overtime_max": 8, "vol": 15000, "staff_base": 160},
        "Restaurant": {"waste": 20, "overtime_max": 5, "vol": 10000, "staff_base": 160},
        "Café/Bistro": {"waste": 10, "overtime_max": 2, "vol": 5000, "staff_base": 160},
        "Fast Food": {"waste": 15, "overtime_max": 4, "vol": 12000, "staff_base": 160}
    }
    m = multipliers.get(sector, multipliers["Restaurant"])
    data = {
        'date': dates,
        'supplier_invoice_sek': np.random.uniform(m['vol']*0.8, m['vol']*1.2, size=90),
        'waste_kg': np.random.uniform(m['waste']*0.5, m['waste']*1.5, size=90),
        'ingredient_yield_gap': np.random.uniform(0.05, 0.25, size=90),
        'contract_hours': [m['staff_base']] * 90,
        'actual_hours_clocked': np.random.uniform(m['staff_base'], m['staff_base'] + (m['overtime_max']*5), size=90),
        'max_individual_overtime': np.random.uniform(m['overtime_max']*0.8, m['overtime_max']*2, size=90)
    }
    return pd.DataFrame(data)

# 3. SIDEBAR
st.sidebar.title("Kärna Service Logic")
sector = st.sidebar.selectbox("Verksamhet", ["Event Center", "Hotel (F&B)", "Restaurant", "Café/Bistro", "Fast Food"])
view_mode = st.sidebar.radio("Analys", ["Organisatorisk (CSRD)", "Operativ (Duty of Care)"])

# 4. PROCESS
df = generate_granular_data(sector)
financial_leakage = df['supplier_invoice_sek'].sum() * df['ingredient_yield_gap'].mean()
burnout_risk_count = (df['max_individual_overtime'] > 12).sum()
total_overtime = df['actual_hours_clocked'].sum() - df['contract_hours'].sum()

# 5. DASHBOARD HEADER
st.title(f"{sector} Dashboard")

# KPI METRICS
m1, m2, m3, m4 = st.columns(4)
m1.metric("Waste (E5)", f"{df['waste_kg'].sum():,.0f} kg")
m2.metric("Burnout Risk", "CRITICAL" if burnout_risk_count > 10 else "STABLE")
m3.metric("Overtime", f"+{total_overtime:,.0f} hrs")
m4.metric("Leakage (SEK)", f"{financial_leakage:,.0f}")

st.divider()

# 6. MANDATORY COMPLIANCE SECTION (VISIBLE NOW)
st.subheader("📑 Government Compliance & Audit")
col1, col2 = st.columns([1, 1])

with col1:
    st.write("**Fortnox to ESRS Mapping**")
    mapping = {
        "Account": ["4010", "7010", "Tid"],
        "ESRS Code": ["E5 Resource", "S1 Social", "S1 Health"],
        "Status": ["Verified", "Verified", "Verified"]
    }
    st.table(pd.DataFrame(mapping))

with col2:
    st.write("**Audit Export**")
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 DOWNLOAD OFFICIAL CSRD REPORT (CSV)",
        data=csv_data,
        file_name=f"Karna_Compliance_{sector}.csv",
        mime='text/csv',
        use_container_width=True # Makes it a big visible button
    )
    st.info("This file is formatted for Swedish government sustainability reporting standards.")

st.divider()

# 7. VISUALS
if view_mode == "Operativ (Duty of Care)":
    st.subheader("Labor Intensity vs. Contract")
    st.line_chart(df.set_index('date')[['actual_hours_clocked', 'contract_hours']])
else:
    st.subheader("Resource Usage Trends")
    st.area_chart(df.set_index('date')[['waste_kg', 'supplier_invoice_sek']])

st.success(f"Profit Recovery identified: **{financial_leakage*0.6:,.0f} SEK** potential gain.")
