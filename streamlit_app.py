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

st.markdown("### 📋 Multi-Product Production Plan")

# Editable product plan
st.subheader("📥 Enter Target Products")
product_plan = st.data_editor(pd.DataFrame({
    "Product": ["Bobolo (Abunde Foods)", "CDC Palm Oil (20L)"],
    "Target Quantity": [60, 40],
    "Days Available": [7, 5]
}), num_rows="dynamic")

results = []

for _, row in product_plan.iterrows():
    product = row["Product"]
    target_qty = row["Target Quantity"]
    days_available = row["Days Available"]

    try:
        bom_row = bom_df[bom_df["Product"] == product].iloc[0]
        prod_row = prod_df[prod_df["Product"] == product].iloc[0]

        raw_material_name = bom_row["Raw Material"]
        price_match = price_df[price_df["Raw Material"] == raw_material_name]

        if price_match.empty:
    st.warning(f"No price found for raw material: {raw_material_name}")
    price_value = 0
        else:
            price_row = price_match.iloc[0]
            price_value = price_row["Avg Unit Price (FCFA)"]

        raw_needed = bom_row["Raw Material Qty per Output Unit"] * target_qty
        material_cost = raw_needed * price_value
        total_worker_days = target_qty / prod_row["Units per Worker per Day"]
        required_workers = math.ceil(total_worker_days / days_available)
        labor_cost = required_workers * pay_rate * days_available
        total_cost = material_cost + labor_cost

        results.append({
            "Product": product,
            "Target Quantity": target_qty,
            "Days Available": days_available,
            "Raw Material": raw_material_name,
            "Total Raw Material (kg)": raw_needed,
            "Material Cost (FCFA)": material_cost,
            "Required Workers": required_workers,
            "Labor Cost (FCFA)": labor_cost,
            "Total Production Cost (FCFA)": total_cost
        })
    except Exception as e:
        st.error(f"Error processing {product}: {e}")
            price_value = 0
        else:
            price_row = price_match.iloc[0]
            price_value = price_row["Avg Unit Price (FCFA)"]

        raw_needed = bom_row["Raw Material Qty per Output Unit"] * target_qty
        material_cost = raw_needed * price_value
        total_worker_days = target_qty / prod_row["Units per Worker per Day"]
        required_workers = math.ceil(total_worker_days / days_available)
        labor_cost = required_workers * pay_rate * days_available
        total_cost = material_cost + labor_cost
        st.error(f"Error processing {product}: {e}")

if results:
    st.markdown("---")
    st.subheader("📊 Batch Production Plan Summary")
    result_df = pd.DataFrame(results)
    result_df["Material Cost (FCFA)"] = pd.to_numeric(result_df["Material Cost (FCFA)"], errors="coerce")
    result_df["Labor Cost (FCFA)"] = pd.to_numeric(result_df["Labor Cost (FCFA)"], errors="coerce")
    result_df["Total Production Cost (FCFA)"] = pd.to_numeric(result_df["Total Production Cost (FCFA)"], errors="coerce")
    st.dataframe(result_df.style.format({
        "Material Cost (FCFA)": "{:,}",
        "Labor Cost (FCFA)": "{:,}",
        "Total Production Cost (FCFA)": "{:,}"
    }))

    st.success("✅ Batch plan generated. Adjust any product rows above to update.")
