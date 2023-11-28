import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Function to load IIP data
def load_iip_data(file_path):
    iip_data = pd.read_excel(file_path)
    return iip_data

# Function to load stock data
def load_stock_data(stock_folder):
    stock_files = [f for f in os.listdir(stock_folder) if f.endswith('.xlsx')]
    stock_data = pd.DataFrame()

    for file in stock_files:
        file_path = os.path.join(stock_folder, file)
        stock = pd.read_excel(file_path)
        stock_data = pd.concat([stock_data, stock], ignore_index=True)

    return stock_data

# Function to filter data based on selected dates
def filter_data(data, start_date, end_date):
    mask = (data['Date'] >= start_date) & (data['Date'] <= end_date)
    return data.loc[mask]

# Function to plot industry and stock graphs
def plot_graphs(iip_data, stock_data, industry_column, stock_column):
    fig = px.line(iip_data, x='Date', y=industry_column, title='IIP Industry Growth')
    fig.update_layout(xaxis_title='Date', yaxis_title='Industry Growth')

    fig_stock = px.line(stock_data, x='Date', y=stock_column, title='Stock Price Movement')
    fig_stock.update_layout(xaxis_title='Date', yaxis_title='Stock Price')

    return fig, fig_stock

# Function to calculate correlation
def calculate_correlation(iip_data, stock_data, industry_column, stock_column):
    merged_data = pd.merge(iip_data, stock_data, on='Date', how='inner')
    correlation = merged_data[industry_column].corr(merged_data[stock_column])
    return correlation

# Streamlit app
def main():
    st.title("Industry and Stock Analysis")

    # Sidebar - IIP data
    st.sidebar.header("IIP Data")
    iip_file = st.sidebar.file_uploader("Upload IIP Data (Excel file)", type=["xlsx"])
    if iip_file is not None:
        iip_data = load_iip_data(iip_file)

        st.sidebar.subheader("Select Date Range for IIP Data")
        iip_start_date = st.sidebar.date_input("Start Date", min_value=iip_data['Date'].min(), max_value=iip_data['Date'].max())
        iip_end_date = st.sidebar.date_input("End Date", min_value=iip_data['Date'].min(), max_value=iip_data['Date'].max())

        iip_data_filtered = filter_data(iip_data, iip_start_date, iip_end_date)

    # Sidebar - Stock data
    st.sidebar.header("Stock Data")
    stock_folder = st.sidebar.folder_uploader("Select Stock Data Folder")
    if stock_folder is not None:
        stock_data = load_stock_data(stock_folder)

        st.sidebar.subheader("Select Date Range for Stock Data")
        stock_start_date = st.sidebar.date_input("Start Date", min_value=stock_data['Date'].min(), max_value=stock_data['Date'].max())
        stock_end_date = st.sidebar.date_input("End Date", min_value=stock_data['Date'].min(), max_value=stock_data['Date'].max())

        stock_data_filtered = filter_data(stock_data, stock_start_date, stock_end_date)

    # Main content
    if 'iip_data_filtered' in locals() and 'stock_data_filtered' in locals():
        st.header("Industry and Stock Analysis")

        industry_column = st.selectbox("Select Industry Column", options=iip_data_filtered.columns[1:])
        stock_column = st.selectbox("Select Stock Column", options=stock_data_filtered.columns[1:])

        # Plot graphs
        industry_fig, stock_fig = plot_graphs(iip_data_filtered, stock_data_filtered, industry_column, stock_column)
        st.plotly_chart(industry_fig)
        st.plotly_chart(stock_fig)

        # Calculate and display correlation
        correlation = calculate_correlation(iip_data_filtered, stock_data_filtered, industry_column, stock_column)
        st.subheader(f"Correlation between {industry_column} and {stock_column}: {correlation:.2f}")

if __name__ == "__main__":
    main()
