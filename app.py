import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Load industry growth data
industry_data = pd.read_excel("IIP_Data.xlsx")

# Function to load stock data
def load_stock_data(file_path):
    try:
        stock_data = pd.read_excel(file_path)
        return stock_data
    except Exception as e:
        st.error(f"Error loading stock data: {e}")
        return None

# Function to calculate correlation and trendline analysis
def calculate_correlation_and_trend(stock_data, industry_data, selected_stock, selected_industry):
    # ... (same as before)

# Streamlit app
def main():
    st.title("Stock and Industry Analysis App")

    # Upload stock revenue file
    uploaded_file = st.file_uploader("Upload Stock Revenue File (in xlsx format)", type="xlsx")

    stock_data = None
    if uploaded_file is not None:
        stock_data = load_stock_data(uploaded_file)

    if stock_data is None:
        # If there's an issue loading stock data, exit the function
        return

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
