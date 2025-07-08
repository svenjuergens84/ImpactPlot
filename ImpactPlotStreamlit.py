# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 15:52:13 2025

@author: Sven
"""


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#!python -m streamlit run ImpactPlotStreamlit.py

# App title
st.title("💸 Revenue Impact Calculator")


st.markdown('''
    **This dashboard will help you to figure why your mobile app revenue changes.**

    Last Update: 2025-07-08

    **How it works:**
    
    Type in your KPIs from two timeframes (e.g. last week vs. the week before) and see which had the biggest impact on the revenue change.
    If you do not monetize with ads, leave the impressions at zero.
    
    Made by Sven Jürgens
    
    ✨ I help apps increase their ROAS in 90 days
    
    DM me and say hi 👇
    
    https://www.linkedin.com/in/svenjuergens/  
    http://svenjuergens-consulting.com/
    
    ''')
# Sidebar for inputs
with st.sidebar:
    st.header("Input KPIs - Old Timeframe")
    data_old = {
        "impressions": st.number_input("Impressions (old)", value=200000),
        "cpm": st.number_input("CPM (old)", value=7.0),
        "iap_price": st.number_input("IAP Price (old)", value=4.0),
        "iap_sales": st.number_input("IAP Sales (old)", value=150),
        "iap_refund": st.number_input("IAP Refund (old)", value=-25)
    }

    st.header("Input KPIs - New Timeframe")
    data_new = {
        "impressions": st.number_input("Impressions (new)", value=150000),
        "cpm": st.number_input("CPM (new)", value=1.0),
        "iap_price": st.number_input("IAP Price (new)", value=3.0),
        "iap_sales": st.number_input("IAP Sales (new)", value=200),
        "iap_refund": st.number_input("IAP Refund (new)", value=-60)
    }

# Calculations
def calculate_impacts(data_old, data_new):
    # Revenue calculations
    revenue_old = (data_old["impressions"] * data_old["cpm"] / 1000) + \
                 (data_old["iap_price"] * data_old["iap_sales"] + data_old["iap_refund"])
    revenue_new = (data_new["impressions"] * data_new["cpm"] / 1000) + \
                 (data_new["iap_price"] * data_new["iap_sales"] + data_new["iap_refund"])
    
    # Impact calculations
    impact_imp = ((data_new["cpm"] + data_old["cpm"]) / 2) / 1000 * (data_new["impressions"] - data_old["impressions"])
    impact_cpm = ((data_new["impressions"] + data_old["impressions"]) / 2) / 1000 * (data_new["cpm"] - data_old["cpm"])
    impact_iap_price = ((data_new["iap_sales"] + data_old["iap_sales"]) / 2) * (data_new["iap_price"] - data_old["iap_price"])
    impact_iap_sales = ((data_new["iap_price"] + data_old["iap_price"]) / 2) * (data_new["iap_sales"] - data_old["iap_sales"])
    impact_iap_refund = 1 * (data_new["iap_refund"] - data_old["iap_refund"])
    
    difference_observed = revenue_new - revenue_old
    difference_explained = impact_imp + impact_cpm + impact_iap_price + impact_iap_sales + impact_iap_refund
    model_quality = difference_observed / difference_explained * 100 if difference_explained != 0 else 0
    
    return {
        "revenue_old": revenue_old,
        "revenue_new": revenue_new,
        "difference_observed": difference_observed,
        "difference_explained": difference_explained,
        "model_quality": model_quality,
        "impacts": {
            "Impressions": impact_imp,
            "CPM": impact_cpm,
            "IAP Price": impact_iap_price,
            "IAP Sales": impact_iap_sales,
            "IAP Refund": impact_iap_refund
        }
    }

# Run calculations
results = calculate_impacts(data_old, data_new)

# Display results
st.header("Results")

col1, col2 = st.columns(2)
with col1:
    st.metric("Old Revenue", f"${results['revenue_old']:,.2f}")
with col2:
    st.metric("New Revenue", f"${results['revenue_new']:,.2f}", 
              delta=f"${results['difference_observed']:,.2f}")

st.subheader("Revenue Breakdown")
st.metric("Model Quality", f"{results['model_quality']:.1f}%")

# Impact visualization
st.subheader("Impact by Factor")
impacts_df = pd.DataFrame.from_dict(results["impacts"], orient="index", columns=["Impact"])
impacts_df["Absolute Impact"] = impacts_df["Impact"].abs()
impacts_df = impacts_df.sort_values("Absolute Impact", ascending=False)

fig, ax = plt.subplots()
impacts_df["Impact"].plot(kind="bar", ax=ax, color=["green" if x > 0 else "red" for x in impacts_df["Impact"]])
ax.set_ylabel("Revenue Impact ($)")
ax.set_title("Contribution to Revenue Change")
st.pyplot(fig)

# Detailed results
with st.expander("Detailed Calculations"):
    st.write("### Revenue Calculations")
    st.write(f"Old Revenue: ${results['revenue_old']:,.2f}")
    st.write(f"New Revenue: ${results['revenue_new']:,.2f}")
    st.write(f"Observed Difference: ${results['difference_observed']:,.2f}")
    st.write(f"Explained Difference: ${results['difference_explained']:,.2f}")
    
    st.write("### Impact Breakdown")
    for factor, impact in results["impacts"].items():
        st.write(f"{factor}: ${impact:,.2f}")
