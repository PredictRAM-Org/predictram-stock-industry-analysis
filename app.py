import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Load industry growth data
industry_data = pd.read_excel("IIP_Data.xlsx")

# Load initial stock revenue and net income growth data
stock_data_file_path = "stock_revenue.xlsx"
stock_data = pd.read_excel(stock_data_file_path)

# Load stock price movement data
stock_folder_path = "Stock_Data"
# Assuming stock files are named as per stock symbols (e.g., AAPL.xlsx, GOOGL.xlsx)
stock_files = [f"{stock_folder_path}/{file}" for file in os.listdir(stock_folder_path) if file.endswith(".xlsx")]

# Function to calculate correlation and trendline analysis
def calculate_correlation_and_trend(stock_data, industry_data, selected_stock, selected_industry):
    # Filter selected stock and industry data
    selected_stock_data = stock_data[stock_data["Stock Symbol"] == selected_stock]
    selected_industry_data = industry_data[selected_industry]

    # Merge stock and industry data on the "Date" column
    merged_data = pd.merge(selected_stock_data, selected_industry_data, on="Date")

    # Calculate correlation between stock revenue and industry growth
    correlation = merged_data["Total Revenue/Income"].corr(merged_data[selected_industry])

    # Prepare data for trendline analysis
    X = merged_data["Total Revenue/Income"].values.reshape(-1, 1)
    y = merged_data[selected_industry].values.reshape(-1, 1)

    # Fit a linear regression model
    model = LinearRegression()
    model.fit(X, y)
    trendline = model.predict(X)

    return correlation, trendline

# Streamlit app
def main():
    st.title("Stock and Industry Analysis App")

    # Upload stock revenue file
    uploaded_file = st.file_uploader("Upload Stock Revenue File (in xlsx format)", type="xlsx")

    if uploaded_file is not None:
        stock_data = pd.read_excel(uploaded_file)

    # Select industry and stock
    selected_industry = st.selectbox("Select Industry", industry_data.columns[1:])
    selected_stock = st.selectbox("Select Stock", [file.split("/")[1].split(".")[0] for file in stock_files])

    # Calculate correlation and trendline
    correlation, trendline = calculate_correlation_and_trend(stock_data, industry_data, selected_stock, selected_industry)

    # Plotting
    plt.figure(figsize=(10, 6))

    # Plot stock revenue and industry growth
    plt.scatter(stock_data["Total Revenue/Income"], industry_data[selected_industry], label="Data points")
    plt.plot(stock_data["Total Revenue/Income"], trendline, color='red', label="Trendline")

    plt.title(f"Correlation: {correlation:.2f} | Trendline Analysis")
    plt.xlabel("Total Revenue/Income")
    plt.ylabel(f"{selected_industry} (Industry Growth)")
    plt.legend()
    st.pyplot()

if __name__ == "__main__":
    main()
