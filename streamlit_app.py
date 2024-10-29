import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

def main():
    st.set_page_config(page_title="CSV Data Explorer", layout="wide")
    
    st.title("📊 CSV Data Explorer")
    st.write("Upload your CSV file to explore and visualize the data")
    
    # File upload
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            # Basic Info Section
            st.header("📋 Basic Information")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Rows", df.shape[0])
            with col2:
                st.metric("Columns", df.shape[1])
            with col3:
                st.metric("Missing Values", df.isna().sum().sum())
            
            # Data Preview Section
            st.header("🔍 Data Preview")
            with st.expander("Show/Hide Data Preview", expanded=True):
                # Number of rows to display
                n_rows = st.slider("Number of rows to display", 5, 50, 5)
                st.dataframe(df.head(n_rows))
            
            # Column Information
            st.header("📑 Column Information")
            col_info = pd.DataFrame({
                'Data Type': df.dtypes,
                'Non-Null Count': df.count(),
                'Null Count': df.isna().sum(),
                'Unique Values': df.nunique()
            })
            st.dataframe(col_info)
            
            # Basic Statistics
            st.header("📈 Basic Statistics")
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
            if len(numeric_cols) > 0:
                st.write(df[numeric_cols].describe())
            else:
                st.info("No numeric columns found for statistical analysis")
            
            # Data Visualization
            st.header("📊 Data Visualization")
            
            # Only show visualization options if there are numeric columns
            if len(numeric_cols) > 0:
                viz_type = st.selectbox(
                    "Choose visualization type",
                    ["Histogram", "Box Plot", "Scatter Plot", "Correlation Heatmap"]
                )
                
                if viz_type == "Histogram":
                    col = st.selectbox("Select column for histogram", numeric_cols)
                    fig = px.histogram(df, x=col, title=f'Histogram of {col}')
                    st.plotly_chart(fig)
                
                elif viz_type == "Box Plot":
                    col = st.selectbox("Select column for box plot", numeric_cols)
                    fig = px.box(df, y=col, title=f'Box Plot of {col}')
                    st.plotly_chart(fig)
                
                elif viz_type == "Scatter Plot":
                    col_x = st.selectbox("Select X-axis column", numeric_cols, key='x')
                    col_y = st.selectbox("Select Y-axis column", numeric_cols, key='y')
                    fig = px.scatter(df, x=col_x, y=col_y, title=f'Scatter Plot: {col_x} vs {col_y}')
                    st.plotly_chart(fig)
                
                elif viz_type == "Correlation Heatmap":
                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
                    st.pyplot(fig)
            
            # Export options
            st.header("💾 Export Options")
            st.download_button(
                label="Download processed data as CSV",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name="processed_data.csv",
                mime="text/csv"
            )
            
        except Exception as e:
            st.error(f"Error occurred while processing the file: {str(e)}")
            
if __name__ == "__main__":
    main()
