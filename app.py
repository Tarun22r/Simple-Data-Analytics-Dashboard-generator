import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="Simple Data Analytics Project", layout="wide")

st.title("Simple Data Analytics Project")
st.write("Upload a dataset, clean it, analyze it, and generate valid smart visualizations automatically.")

uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])


def load_dataset(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    return pd.read_excel(file, engine="openpyxl")


def clean_dataset(df):
    df = df.copy()
    report = []

    original_shape = df.shape

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    duplicate_count = df.duplicated().sum()
    df.drop_duplicates(inplace=True)

    report.append(f"Original dataset shape: {original_shape[0]} rows and {original_shape[1]} columns.")
    report.append(f"Duplicate rows removed: {duplicate_count}")

    missing_before = df.isnull().sum().sum()

    for col in df.columns:
        if df[col].isnull().sum() > 0:
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].median())
                report.append(f"Missing values in '{col}' filled using median.")
            else:
                mode_value = df[col].mode()
                if not mode_value.empty:
                    df[col] = df[col].fillna(mode_value[0])
                    report.append(f"Missing values in '{col}' filled using mode.")
                else:
                    df[col] = df[col].fillna("Unknown")
                    report.append(f"Missing values in '{col}' filled using 'Unknown'.")

    missing_after = df.isnull().sum().sum()

    report.append(f"Missing values before cleaning: {missing_before}")
    report.append(f"Missing values after cleaning: {missing_after}")
    report.append(f"Final dataset shape: {df.shape[0]} rows and {df.shape[1]} columns.")

    return df, report


def generate_insights(df):
    insights = []

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    insights.append(f"Total rows: {df.shape[0]}")
    insights.append(f"Total columns: {df.shape[1]}")
    insights.append(f"Numeric columns: {len(numeric_cols)}")
    insights.append(f"Categorical columns: {len(categorical_cols)}")

    if numeric_cols:
        for col in numeric_cols[:3]:
            insights.append(
                f"{col}: average = {df[col].mean():.2f}, minimum = {df[col].min()}, maximum = {df[col].max()}"
            )

    if categorical_cols:
        for col in categorical_cols[:3]:
            top_value = df[col].value_counts().idxmax()
            top_count = df[col].value_counts().max()
            insights.append(f"Most common value in {col}: {top_value} ({top_count} records)")

    return insights, numeric_cols, categorical_cols


def convert_to_excel(df):
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Cleaned Data")

    output.seek(0)
    return output.getvalue()


def visualize_data(df, numeric_cols, categorical_cols):
    st.subheader("Smart Visualizations")

    chart_count = 0

    bad_keywords = ["id", "rank", "serial", "index", "code", "number"]

    useful_numeric_cols = [
        col for col in numeric_cols
        if not any(word in col.lower() for word in bad_keywords)
    ]

    rank_like_cols = [
        col for col in numeric_cols
        if any(word in col.lower() for word in bad_keywords)
    ]

    valid_cat_cols = [
        col for col in categorical_cols
        if 2 <= df[col].nunique() <= 30
    ]

    # Chart 1: Category Frequency
    if valid_cat_cols:
        cat_col = max(valid_cat_cols, key=lambda col: df[col].nunique())

        count_df = df[cat_col].value_counts().head(10).reset_index()
        count_df.columns = [cat_col, "count"]

        fig = px.bar(
            count_df,
            x=cat_col,
            y="count",
            text="count",
            title=f"Top Category Distribution: {cat_col}",
            template="plotly_white"
        )

        fig.update_traces(textposition="outside")
        fig.update_layout(
            xaxis_title=cat_col,
            yaxis_title="Record Count",
            title_font_size=22
        )

        st.plotly_chart(fig, use_container_width=True)
        chart_count += 1

    # Chart 2: Category vs Numeric
    if valid_cat_cols and useful_numeric_cols:
        cat_col = valid_cat_cols[0]
        num_col = max(useful_numeric_cols, key=lambda col: df[col].mean())

        group_df = (
            df.groupby(cat_col)[num_col]
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig = px.bar(
            group_df,
            x=cat_col,
            y=num_col,
            text=num_col,
            title=f"Category-wise Performance Analysis: Average {num_col} by {cat_col}",
            template="plotly_white"
        )

        fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig.update_layout(
            xaxis_title=cat_col,
            yaxis_title=f"Average {num_col}",
            title_font_size=22
        )

        st.plotly_chart(fig, use_container_width=True)
        chart_count += 1

    # Chart 3: Numeric Box Plot
    if useful_numeric_cols:
        num_col = max(useful_numeric_cols, key=lambda col: df[col].std())

        fig = px.box(
            df,
            y=num_col,
            title=f"Numerical Data Distribution Analysis: {num_col}",
            template="plotly_white"
        )

        fig.update_layout(
            yaxis_title=num_col,
            title_font_size=22
        )

        st.plotly_chart(fig, use_container_width=True)
        chart_count += 1

    # Chart 4: Rank / ID / Ordered Numeric Trend
    if rank_like_cols:
        rank_col = rank_like_cols[0]

        fig = px.line(
            df.reset_index(),
            x="index",
            y=rank_col,
            title=f"Trend Analysis of Sequential Data: {rank_col}",
            template="plotly_white"
        )

        fig.update_layout(
            xaxis_title="Record Index",
            yaxis_title=rank_col,
            title_font_size=22
        )

        st.plotly_chart(fig, use_container_width=True)
        chart_count += 1

    # Chart 5: Scatter Relationship
    if len(useful_numeric_cols) >= 2:
        corr = df[useful_numeric_cols].corr().abs()

        best_pair = None
        best_value = 0

        for i in range(len(useful_numeric_cols)):
            for j in range(i + 1, len(useful_numeric_cols)):
                value = corr.iloc[i, j]

                if pd.notna(value) and value > best_value and value < 1:
                    best_value = value
                    best_pair = (useful_numeric_cols[i], useful_numeric_cols[j])

        if best_pair:
            x_col, y_col = best_pair

            fig = px.scatter(
                df,
                x=x_col,
                y=y_col,
                title=f"Correlation Between Variables: {x_col} vs {y_col}",
                template="plotly_white"
            )

            fig.update_layout(
                xaxis_title=x_col,
                yaxis_title=y_col,
                title_font_size=22
            )

            st.plotly_chart(fig, use_container_width=True)
            chart_count += 1

    # Chart 6: Correlation Heatmap
    if len(useful_numeric_cols) >= 2:
        fig = px.imshow(
            df[useful_numeric_cols].corr(),
            text_auto=True,
            title="Correlation Matrix of Numeric Features",
            template="plotly_white"
        )

        fig.update_layout(title_font_size=22)

        st.plotly_chart(fig, use_container_width=True)
        chart_count += 1

    # Chart 7: Donut Chart
    low_cardinality_cols = [
        col for col in categorical_cols
        if 2 <= df[col].nunique() <= 8
    ]

    if low_cardinality_cols:
        pie_col = low_cardinality_cols[0]

        pie_df = df[pie_col].value_counts().reset_index()
        pie_df.columns = [pie_col, "count"]

        fig = px.pie(
            pie_df,
            names=pie_col,
            values="count",
            hole=0.35,
            title=f"Category Contribution Analysis: {pie_col}",
            template="plotly_white"
        )

        fig.update_layout(title_font_size=22)

        st.plotly_chart(fig, use_container_width=True)
        chart_count += 1

    if chart_count == 0:
        st.warning("Not enough valid columns to generate charts.")
    else:
        st.success(f"{chart_count} charts generated successfully.")


if uploaded_file is not None:
    df = load_dataset(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head(20), use_container_width=True)

    if st.button("Process Dataset"):
        cleaned_df, report = clean_dataset(df)

        st.subheader("Cleaning Report")
        for r in report:
            st.write("-", r)

        st.subheader("Insights")
        insights, num_cols, cat_cols = generate_insights(cleaned_df)
        for ins in insights:
            st.write("-", ins)

        visualize_data(cleaned_df, num_cols, cat_cols)

        excel_file = convert_to_excel(cleaned_df)

        st.download_button(
            label="Download Cleaned Dataset",
            data=excel_file,
            file_name="cleaned_dataset.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

else:
    st.info("Upload a dataset to begin.")