from datetime import datetime
import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('data/finance.db')
    return conn

# Retirement Planning
def investment_portfolio():
    st.title("Investment Portfolio Management")
    st.write("Manage and analyze your investment portfolio:")

    conn = get_db_connection()
    c = conn.cursor()

    with st.form(key='investment_form'):
        investment_type = st.selectbox("Investment Type", ["Stocks", "Bonds", "Mutual Funds", "Real Estate", "Other"])
        amount_invested = st.number_input("Amount Invested", min_value=0.0, format="%.2f")
        date = st.date_input("Date of Investment", datetime.now())
        submit_button = st.form_submit_button(label='Add Investment')

        if submit_button:
            user_id = 1  # Assuming user_id is 1 for demonstration purposes
            c.execute(
                "INSERT INTO investments (user_id, type, amount_invested, date) VALUES (?, ?, ?, ?)",
                (user_id, investment_type, amount_invested, str(date))
            )
            conn.commit()
            st.success("Investment added successfully")

    conn.close()

    # Display existing investments
    conn = get_db_connection()
    c = conn.cursor()

    # Query the database to fetch investment data
    c.execute("SELECT type, amount_invested, date FROM investments")
    investments_data = c.fetchall()

    # Close the database connection
    conn.close()

    # Create a DataFrame from the fetched data
    investment_df = pd.DataFrame(investments_data, columns=["Type", "Amount Invested", "Date"])

    st.write("### Your Investment Plans")
    st.write(investment_df)

    # Query the database to fetch investment data for chart
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT type, SUM(amount_invested) FROM investments GROUP BY type")
    investment_data = c.fetchall()
    conn.close()

    # Extract investment types and total amounts from the fetched investment data
    investment_types = [data[0] for data in investment_data]
    investment_amounts = [data[1] for data in investment_data]

    # Bar chart for distribution of investments by type
    st.write("### Investments - Distribution by Type")
    fig, ax = plt.subplots()
    ax.barh(investment_types, investment_amounts, color='skyblue')
    ax.set_xlabel('Amount Invested')
    ax.set_ylabel('Investment Type')
    ax.set_title('Distribution of Investments by Type')
    st.pyplot(fig)

    # Uncomment to export the DataFrame to an Excel sheet
    # excel_file_path = "investment_data.xlsx"
    # investment_df.to_excel(excel_file_path, index=False)
    # st.write(f"Exported investment data to {excel_file_path}")

if __name__ == "__main__":
    investment_portfolio()
