import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Load industry growth data
industry_data_path = "IIP_Data.xlsx"
industry_df = pd.read_excel(industry_data_path, parse_dates=["Date"])

# Load initial stock revenue data
stock_revenue_path = "stock_revenue.xlsx"
stock_revenue_df = pd.read_excel(stock_revenue_path, parse_dates=["Date"])

# Load stock data
stock_data_folder = "Stock_Data"

# Function to get stock list
def get_stock_list():
    stock_files = [f for f in os.listdir(stock_data_folder) if f.endswith('.xlsx')]
    return stock_files

# Function to get stock data
def get_stock_data(stock_file):
    stock_path = os.path.join(stock_data_folder, stock_file)
    stock_df = pd.read_excel(stock_path, parse_dates=["Date"])
    return stock_df

# Function to calculate correlation and plot trendline
def plot_correlation_trendline(stock_revenue_df, industry_df, stock_df, selected_industry):
    # Filter industry data based on selection
    selected_industry_data = industry_df[["Date", selected_industry]]
    
    # Merge dataframes based on Date
    merged_df = pd.merge(stock_revenue_df, selected_industry_data, on="Date", how="inner")
    merged_df = pd.merge(merged_df, stock_df[["Date", "Close"]], on="Date", how="inner")
    
    # Calculate correlation
    correlation_matrix = merged_df.corr()
    
    # Plot correlation matrix heatmap
    st.subheader("Correlation Matrix Heatmap")
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=.5)
    st.pyplot()

    # Plot trendline
    st.subheader("Trendline Analysis")
    plt.figure(figsize=(10, 6))
    sns.regplot(x="Total Revenue/Income", y=selected_industry, data=merged_df, label="Total Revenue/Income")
    sns.regplot(x="Total Operating Expense", y=selected_industry, data=merged_df, label="Total Operating Expense")
    sns.regplot(x="Net Income", y=selected_industry, data=merged_df, label="Net Income")
    sns.regplot(x="Close", y=selected_industry, data=merged_df, label="Stock Price (Close)")
    plt.legend()
    st.pyplot()

# Streamlit app
st.title("Stock Analysis App")

# Upload stock revenue file
uploaded_stock_revenue_file = st.file_uploader("Upload Stock Revenue File (xlsx)", type=["xlsx"])
if uploaded_stock_revenue_file is not None:
    stock_revenue_df = pd.read_excel(uploaded_stock_revenue_file, parse_dates=["Date"])

# Select industry
selected_industry = st.selectbox("Select Industry", industry_df.columns[1:])

# Select stock
selected_stock = st.selectbox("Select Stock", get_stock_list())
selected_stock_df = get_stock_data(selected_stock)

# Display selected industry and stock data
st.write("Selected Industry Data:")
st.write(industry_df[["Date", selected_industry]])

st.write("Selected Stock Data:")
st.write(selected_stock_df)

# Plot correlation and trendline analysis
plot_correlation_trendline(stock_revenue_df, industry_df, selected_stock_df, selected_industry)
