# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 11:31:50 2026

@author: Manna
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# 1. PAGE CONFIG & THEME 
st.set_page_config(page_title="Kärna Service Logic | CSRD Compliance", layout="wide")

# 2. THE BRAIN: 24-HOUR SYNC LOGIC (Option 2)
# The 'ttl' ensures the data is only "fetched" once every 24 hours
@st.cache_data(ttl=86400)
def generate_granular_data(sector):
    dates = pd.date_range(end=datetime.today(), periods=90, freq='D')
    
    multipliers = {
        "Event Center": {"waste": 45, "overtime": 12, "vol": 20000},
        "Hotel (F&B)": {"waste": 30, "overtime": 8, "vol": 15000},
        "Restaurant": {"waste": 20, "overtime": 5, "vol": 10000},
        "Café/Bistro": {"waste": 10, "overtime": 2, "vol": 5000},
        "Fast Food": {"waste": 15, "overtime": 4, "vol": 12000}
    }
    
    m = multipliers.get(sector, multipliers["Restaurant"])
    
    data = {
        'date': dates,
        'supplier_invoice_sek': np.random.uniform(m['vol']*0.8, m['vol']*1.2, size=90),
        # CATEGORIZED WASTE: Input (Ingredients) vs Output (Plate Waste/Ready-made)
        'ingredient_waste_kg': np.random.uniform(m['waste']*0.4, m['waste']*0.8, size=90),
        'plate_waste_kg': np.random.uniform(m['waste']*0.1, m['waste']*0.3, size=90),
        'contract_hours': [160] * 90,
        'actual_hours': np.random.uniform(160, 160 + m['overtime']*4, size=90),
        'max_individual_overtime': np.random.uniform(m['overtime']*0.8, m['overtime']*2, size=90)
    }
    return pd.DataFrame(data)

# 3. SIDEBAR START 
st.sidebar.image("https://img.icons8.com/fluency/96/brain.png", width=50)
st.sidebar.title("Kärna Service Logic")
st.sidebar.info("🔄 Sync Mode: 24-Hour Cycle Active")

sector = st.sidebar.selectbox(
    "Välj verksamhetstyp", 
    ["Event Center", "Hotel (F&B)", "Restaurant", "Café/Bistro", "Fast Food"]
)

view_mode = st.sidebar.radio("Analysnivå", ["Organisatorisk (CSRD)", "Operativ (Duty of Care)"])

st.sidebar.divider()

with st.sidebar.expander("⚖️ Juridiska villkor & Avtal"):
    st.markdown("### ANVÄNDARAVTAL")
    st.markdown("#### KOMPLETTERANDE AVTAL")
    st.info("Pris: 199 SEK/mån. Benchmarking baseras på anonymiserad branschdata.")

# 4. DATA PROCESSING 
df = generate_granular_data(sector)
total_waste = df['ingredient_waste_kg'].sum() + df['plate_waste_kg'].sum()
financial_leakage = df['supplier_invoice_sek'].sum() * 0.12 # Simulated yield gap leakage
burnout_risk_count = (df['max_individual_overtime'] > 12).sum()

# 5. MAIN DASHBOARD 
st.title(f"{sector} | {view_mode}")

# Metrics Row
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Total Waste (E5)", f"{total_waste:,.1f} kg", "-2.4% Benchmark")
with c2:
    risk_status = "CRITICAL" if burnout_risk_count > 10 else "STABLE"
    st.metric("Burnout Risk (S1)", risk_status, f"{burnout_risk_count} incidents")
with c3:
    st.metric("Financial Leakage", f"{financial_leakage:,.0f} SEK")

st.divider()

# 6. VISUALS 
if view_mode == "Operativ (Duty of Care)":
    st.subheader("Labor Intensity: Actual vs. Contract Hours")
    st.line_chart(df.set_index('date')[['actual_hours', 'contract_hours']])
    st.caption("Monitoring the delta between planned hours and actual clock-ins (ESRS S1).")
else:
    st.subheader("E5: Resource Usage (Ingredients vs. Plate Waste)")
    # Stacked chart showing the difference between Input and Output waste
    st.area_chart(df.set_index('date')[['ingredient_waste_kg', 'plate_waste_kg']])
    st.caption("Layer 1 (Bottom): Ingredient Yield Loss | Layer 2 (Top): Unsold Prepared Foods")

st.divider()

# 7. DOWNLOADABLE REPORTS (The section you wanted visible)
st.subheader("Compliance Export")
col_a, col_b = st.columns(2)

with col_a:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"📥 Download {sector} Raw Data (CSV)",
        data=csv,
        file_name=f"Karna_{sector.replace(' ', '_')}_Compliance.csv",
        mime='text/csv',
    )

with col_b:
    st.info("This report is formatted for automated ESRS reporting and auditor verification.")

st.success(f"Strategy: Addressing ingredient yield gaps could recover **{financial_leakage*0.5:,.0f} SEK** this quarter.")
