import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="CSV Visualizer", layout="wide")
st.title("📊 CSV Visualizer Tool")

# Upload CSV
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("CSV Loaded Successfully!")
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    # Display data preview
    if st.checkbox("Show Data Preview"):
        st.dataframe(df)

    # Select chart type
    chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Line Chart", "Pie Chart"])

    # Select column(s) based on chart type
    if chart_type in ["Bar Chart", "Line Chart"]:
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if not numeric_cols:
            st.warning("No numeric columns available for plotting.")
        else:
            x_col = st.selectbox("X-axis", df.columns)
            y_col = st.selectbox("Y-axis (numeric only)", numeric_cols)

            if st.button("Generate Chart"):
                fig, ax = plt.subplots()
                if chart_type == "Bar Chart":
                    ax.bar(df[x_col], df[y_col])
                    ax.set_xlabel(x_col)
                    ax.set_ylabel(y_col)
                elif chart_type == "Line Chart":
                    ax.plot(df[x_col], df[y_col], marker='o')
                    ax.set_xlabel(x_col)
                    ax.set_ylabel(y_col)
                plt.xticks(rotation=45)
                st.pyplot(fig)

    elif chart_type == "Pie Chart":
        pie_col = st.selectbox("Select Column for Pie Chart (categorical)", df.columns)
        agg_col = st.selectbox("Values Column (numeric)", df.select_dtypes(include='number').columns)

        pie_data = df.groupby(pie_col)[agg_col].sum()

        if st.button("Generate Pie Chart"):
            fig, ax = plt.subplots()
            ax.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%", startangle=90)
            ax.axis('equal')
            st.pyplot(fig)
else:
    st.info("Please upload a CSV file to begin.")
