import streamlit as st
import pandas as pd
import os
from universal_eda_module import universal_eda_best_worst

st.set_page_config(page_title="Universal EDA Tool", layout="centered")
st.title("\U0001F50D Universal EDA Report Generator")

# Upload CSV or Excel
uploaded_file = st.file_uploader("\U0001F4C1 Upload your dataset (.csv or .xlsx)", type=["csv", "xlsx"])

if uploaded_file:
    # Read dataset
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file, engine="openpyxl")
    st.success("✅ File uploaded successfully!")
    st.write("\U0001F4CA Preview of Data:")
    st.dataframe(df.head())

    # Select target column
    target_col = st.selectbox("🎯 Select the target column for analysis:", df.columns)

    # Run EDA
    if st.button("\U0001F680 Run EDA"):
        temp_path = "temp_uploaded_file.csv"
        df.to_csv(temp_path, index=False)

        # Run universal EDA
        universal_eda_best_worst(temp_path, target_col)
        st.success("✅ EDA Completed Successfully!")

        # Download Buttons
        if os.path.exists("eda_summary.md"):
            st.download_button("📄 Download Markdown Report", open("eda_summary.md", "rb"), "eda_summary.md")

        if os.path.exists("eda_summary.pdf"):
            st.download_button("📄 Download PDF Report", open("eda_summary.pdf", "rb"), "eda_summary.pdf")

        # Show visualizations
        st.subheader("\U0001F4CA Visualizations")
        for col in df.columns:
            img_file = f"{col}_barplot.png"
            if os.path.exists(img_file):
                st.image(img_file, caption=f"{col} vs {target_col}", use_container_width=True)