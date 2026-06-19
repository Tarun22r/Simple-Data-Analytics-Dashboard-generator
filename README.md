Simple Data Analytics Dashboard (Streamlit)

An interactive data analytics web application built using Streamlit, Pandas, Plotly, and Python that allows users to upload datasets, automatically clean data, generate insights, and visualize patterns with smart, dynamic charts.

Live Features

Data Upload

Supports CSV and Excel (.xlsx) files
Instant dataset preview after upload

🧹 Automated Data Cleaning

Standardizes column names
Removes duplicate records
Handles missing values intelligently:
Numeric → Median Imputation
Categorical → Mode / “Unknown”
Generates a detailed cleaning report
📈 Smart Data Insights
Dataset shape summary
Numeric & categorical column detection
Mean, min, max for numeric fields
Most frequent values in categorical columns
📊 Automatic Visualizations

The app intelligently generates charts based on dataset structure:

 Top category distribution (Bar Chart)
 Category vs Numeric comparison (Grouped analysis)
 Numerical distribution (Box Plot)
Trend analysis for sequential data (Line Chart)
 Correlation scatter plot (Best variable pair)
 Correlation heatmap
 Donut chart for categorical contribution
Export Feature
Download cleaned dataset as Excel (.xlsx)
🛠️ Tech Stack
Frontend/UI: Streamlit
Backend Logic: Python
Data Processing: Pandas, NumPy
Visualization: Plotly Express
File Handling: openpyxl, BytesIO

🎯 How It Works
Upload dataset (CSV or Excel)
Click "Process Dataset"
View:
Cleaning report
Automated insights
Smart visualizations
Download cleaned dataset

💡 Key Highlights
No manual coding required for analysis
Automatically adapts to any dataset structure
Beginner-friendly UI
Business-ready data insights in seconds

📌 Future Improvements
Machine learning prediction module
Auto report generation (PDF)
Advanced filtering dashboard
Multi-sheet Excel support
Real-time data streaming

👨‍💻 Author

Tarun R
Aspiring Data Analyst | Full-Stack Developer
Focused on building real-world AI + Data solutions
