
import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Production Planner", layout="wide")
st.title("📦 Time-Bound Production Planning Tool")

st.markdown("---")

# Editable tables
st.sidebar.header("🔧 Edit Planning Tables")
with st.sidebar.expander("Bill of Materials (BOM)"):
    bom_df = st.data_editor(pd.DataFrame({
        "Product": ["Bobolo (Abunde Foods)", "CDC Palm Oil (20L)", "Ekwang"],
        "Output Unit Description": ["Box of 25 packs (3 x 1kg)", "20L Container", "Box of 36 packs (1kg)"],
        "Raw Material": ["Cassava", "Palm nuts", "Cocoyam tubers"],
        "Raw Material Qty per Output Unit": [75, 20, 36],
        "Raw Material Unit": ["kg", "kg", "kg"]
    }), num_rows="dynamic")

with st.sidebar.expander("Productivity Rates"):
    prod_df = st.data_editor(pd.DataFrame({
        "Product": ["Bobolo (Abunde Foods)", "CDC Palm Oil (20L)", "Ekwang"],
        "Units per Worker per Day": [30, 40, 25]
    }), num_rows="dynamic")

with st.sidebar.expander("Raw Material Prices"):
    price_df = st.data_editor(pd.DataFrame({
        "Raw Material": ["Cassava", "Palm nuts", "Cocoyam tubers"],
        "Avg Unit Price (FCFA)": [300, 500, 400],
        "Unit": ["kg", "kg", "kg"]
    }), num_rows="dynamic")

with st.sidebar.expander("Labor Rates"):
    pay_rate = st.number_input("Daily Pay Rate (FCFA)", value=3000)

st.markdown("### 📋 Enter Production Plan")
product_choice = st.selectbox("Select Product", bom_df["Product"].unique())
target_qty = st.number_input("Target Quantity (units or boxes)", min_value=1, value=50)
days_available = st.number_input("Days Available", min_value=1, value=7)

# Get matching rows
bom_row = bom_df[bom_df["Product"] == product_choice].iloc[0]
prod_row = prod_df[prod_df["Product"] == product_choice].iloc[0]
price_row = price_df[price_df["Raw Material"] == bom_row["Raw Material"]].iloc[0]

# Calculations
raw_needed = bom_row["Raw Material Qty per Output Unit"] * target_qty
material_cost = raw_needed * price_row["Avg Unit Price (FCFA)"]
total_worker_days = target_qty / prod_row["Units per Worker per Day"]
required_workers = math.ceil(total_worker_days / days_available)
labor_cost = required_workers * pay_rate * days_available
total_cost = material_cost + labor_cost

st.markdown("---")
st.subheader("📊 Production Plan Summary")
col1, col2, col3 = st.columns(3)
col1.metric("🔧 Raw Material Needed", f"{raw_needed:.1f} {bom_row['Raw Material Unit']}")
col2.metric("👷 Required Workers", f"{required_workers} workers")
col3.metric("💰 Total Cost", f"{total_cost:,.0f} FCFA")

with st.expander("🔎 Detailed Breakdown"):
    st.write(pd.DataFrame.from_dict({
        "Metric": ["Target Quantity", "Days Available", "Units/Worker/Day", "Total Worker Days", "Raw Material Needed", "Material Cost", "Labor Cost", "Total Cost"],
        "Value": [target_qty, days_available, prod_row["Units per Worker per Day"], f"{total_worker_days:.2f}", f"{raw_needed:.1f} {bom_row['Raw Material Unit']}", f"{material_cost:,.0f} FCFA", f"{labor_cost:,.0f} FCFA", f"{total_cost:,.0f} FCFA"]
    }))

st.success("✅ Plan generated. You can adjust inputs in the sidebar and rerun!")
