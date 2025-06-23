# 📊 Universal EDA App
The Universal EDA App is a Streamlit-powered tool for performing automated Exploratory Data Analysis (EDA) on any dataset. It intelligently detects the problem type (classification or regression), generates insights, highlights trends, identifies best- and worst-case scenarios, and creates downloadable reports in both Markdown and PDF formats.

# 🚀 Features
- 📁 Upload .csv or .xlsx dataset
- 🎯 Select your target column
- 🧠 Automatically detects whether task is classification or regression

# 📈 Provides:
- EDA takeaways
- Trend insights
- Best- and worst-case scenarios in human-readable language
- 📄 Downloadable report in Markdown & PDF
- 🖼️ Auto-generated bar plots for categorical features

# 📦 How It Works
- Upload Dataset
- Upload any .csv or .xlsx file from your system.
- Target Column Selection
- Choose the column you want to analyze (e.g., Survived, Price, Tip).
- Run EDA
- Click "Run EDA" to launch the analysis:
- The app preprocesses the data (label encoding, redundancy removal).
- It detects task type (classification if target has ≤20 unique values).
- A decision tree is trained to extract the best and worst profiles.
- Visualizations are created for interpretable features.

# Results
- A detailed report is generated and saved as eda_summary.md and eda_summary.pdf.
- Visuals are displayed and downloadable.
- Insightful, natural-language output is shown for quick understanding.

# ☁️ Deployment
- To deploy on Streamlit Community Cloud:
- Push code to GitHub.
- Go to streamlit.io/cloud → Sign in with GitHub.
- Click "New App", select your repo & branch, and set eda_app.py as the entry point.
- Deploy!

# 🧠 Technologies Used
- Streamlit
- pandas, numpy
- scikit-learn
- seaborn, matplotlib
- fpdf / markdown
- DecisionTreeClassifier / Regressor
