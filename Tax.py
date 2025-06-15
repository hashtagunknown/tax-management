import streamlit as st
import mysql.connector
import pandas as pd


# Function to connect to the MySQL database
def connect_to_db():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="tax_new1"
        )
        return mydb
    except mysql.connector.Error as err:
        st.error(f"Error connecting to MySQL database: {err}")
        return None

def update_tax_payer_details(cursor, username, legalname, panno, adhaar, user_address, phoneno):
    try:
        # Update details in the tax_payer_details table
        update_query = f"UPDATE tax_payer_details SET legalname = '{legalname}', panno = '{panno}', adhaar = '{adhaar}', user_address = '{user_address}', phoneno = '{phoneno}' WHERE username = '{username}'"
        cursor.execute(update_query)
        cursor._connection.commit()
        st.success("Tax Payer Details Updated Successfully!")
    except mysql.connector.Error as err:
        st.error(f"Error updating tax payer details: {err}")

# Function to delete tax payer details from the database
def delete_tax_payer_details(cursor, username):
    try:
        # Delete details from the tax_payer_details table
        delete_query = f"DELETE FROM tax_payer_details WHERE username = '{username}'"
        cursor.execute(delete_query)
        cursor._connection.commit()
        st.success("Tax Payer Details Deleted Successfully!")
    except mysql.connector.Error as err:
        st.error(f"Error deleting tax payer details: {err}")


# Function to fetch tax payer details by user ID
def fetch_tax_payer_by_id(cursor, username):
    cursor.execute(f"SELECT * FROM tax_payer_details WHERE username= {username}")
    return cursor.fetchone()

# Function to fetch tax payer details by PAN number
def fetch_tax_payer_by_pan(cursor, panno):
    cursor.execute(f"SELECT * FROM tax_payer_details WHERE panno = '{panno}'")
    return cursor.fetchone()

# Function to fetch tax payer details by Aadhaar number
def fetch_tax_payer_by_aadhaar(cursor, adhaar):
    cursor.execute(f"SELECT * FROM tax_payer_details WHERE adhaar = '{adhaar}'")
    return cursor.fetchone()









def fetch_all_tables(cursor):
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    return tables

def fetch_table_data(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    return data



def view_all_tables():
    st.title("View All Tables")

    mydb = connect_to_db()
    if not mydb:
        return

    cursor = mydb.cursor()

    tables = fetch_all_tables(cursor)

    if tables:
        for table in tables:
            table_name = table[0]
            st.subheader(f"Table: {table_name}")
            data = fetch_table_data(cursor, table_name)
            df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
            st.dataframe(df)

    cursor.close()
    mydb.close()



def fetch_tax_slabs(cursor):
    cursor.execute("SELECT * FROM admin_settings")
    return cursor.fetchone()

# Function to update tax slabs in the database
def update_tax_slabs(cursor, tax_rate, tax_range):
    cursor.execute(f"UPDATE admin_settings SET tax_rate = {tax_rate}, tax_range = {tax_range}")
    cursor._connection.commit()

# Function to insert tax payer income details into the database
def insert_income_details(cursor, username, job_earnings, business_earnings, property_earnings, total_earning):
    try:
        # Insert all details into the tax_payer_income_details table
        insert_query = f"INSERT INTO tax_payer_income_details (username, job_earning, business_earning, property_earning, total_earning) VALUES ('{username}', {job_earnings}, {business_earnings}, {property_earnings}, {total_earning})"
        cursor.execute(insert_query)
        cursor._connection.commit()
        st.success("Income Details Saved Successfully!")
    except mysql.connector.Error as err:
        st.error(f"Error inserting income details: {err}")

# Function to insert tax payer investments details into the database
def insert_loan_details(cursor, username, housing_loans, other_loans, rent, provided_funds, policies):
    try:
        # Insert all details into the tax_payer_investments table
        insert_query = f"INSERT INTO tax_payer_loans_details (username, housing_loans, other_loans, rent, provided_funds, policies) VALUES ('{username}', {housing_loans}, {other_loans}, {rent}, {provided_funds}, {policies})"
        cursor.execute(insert_query)
        cursor._connection.commit()
        st.success("Investments Details Saved Successfully!")
    except mysql.connector.Error as err:
        st.error(f"Error inserting investments details: {err}")

# Function to insert tax payer details into the database
def insert_tax_payer_details(cursor, legalname, panno, adhaar, user_address, phoneno):
    
    mydb = connect_to_db()
    if not mydb:
        return

    cursor = mydb.cursor()

    try:
        # Insert all details into the tax_payer_details table
        insert_query = f"INSERT INTO tax_payer_details (legalname, panno, adhaar, user_address, phoneno) VALUES ('{legalname}', '{panno}', '{adhaar}', '{user_address}', '{phoneno}')"
        cursor.execute(insert_query)
        cursor._connection.commit()
        st.success("Tax Payer Details Saved Successfully!")
    except mysql.connector.Error as err:
        st.error(f"Error inserting tax payer details: {err}")
    
    cursor.close()

# Function to fetch user details from the database for login
def fetch_user(cursor, username, password, tax_officer_id):
    query = f"SELECT * FROM users WHERE username = '{username}' AND user_password = '{password}' AND tax_officer_id = '{tax_officer_id}'"
    cursor.execute(query)
    return cursor.fetchone()

# Admin panel page
def admin_panel():
    st.title("Admin Panel")
    
    mydb = connect_to_db()
    if not mydb:
        return
    
    cursor = mydb.cursor()

    # Fetch existing tax slab details
    current_tax_slabs = fetch_tax_slabs(cursor)

    if current_tax_slabs:
        st.subheader("Current Tax Slab Details")
        st.write(f"Tax Rate: {current_tax_slabs[1]}")
        st.write(f"Tax Range: {current_tax_slabs[2]}")

        # Update tax slabs form
        st.subheader("Update Tax Slabs")
        new_tax_rate = st.number_input("New Tax Rate", value=current_tax_slabs[1])
        new_tax_range = st.number_input("New Tax Range", value=current_tax_slabs[2])

        if st.button("Update Tax Slabs"):
            update_tax_slabs(cursor, new_tax_rate, new_tax_range)
            st.success("Tax Slabs Updated Successfully!")

    cursor.close()
    mydb.close()

# Registration page
def register():
    mydb = connect_to_db()
    if not mydb:
        return

    cursor = mydb.cursor()

    st.title("Registration Page")

    # Create Streamlit input fields for registration
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    tax_officer_id = st.text_input("Tax Officer ID")

    # Handle register button click
    if st.button("Register"):
        # Check if the username already exists
        check_query = f"SELECT * FROM users WHERE username = '{username}'"
        cursor.execute(check_query)
        existing_user = cursor.fetchone()

        if existing_user:
            st.error("Username already exists. Please choose a different username.")
        else:
            # Insert new user data into the Users table
            insert_query = f"INSERT INTO users (username, user_password, tax_officer_id) VALUES ('{username}', '{password}', '{tax_officer_id}')"
            cursor.execute(insert_query)
            mydb.commit()  # Commit the transaction
            st.success("Registration successful!")

    cursor.close()
    mydb.close()

# Login page
def login():
    mydb = connect_to_db()
    if not mydb:
        return

    cursor = mydb.cursor()

    st.title("Login Page")

    # Create Streamlit input fields
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    tax_officer_id = st.text_input("Tax Officer ID")

    # Handle login button click
    if st.button("Login"):
        user = fetch_user(cursor, username, password, tax_officer_id)

        if user:
            if user[0] == 'admin':
                st.success("Admin login successful!")
                st.write("Go to Admin Panel")
            else:
                st.success("Login successful!")
                st.write("Go to Tax payer details")
        else:
            st.error("Invalid credentials. Please try again.")

    cursor.close()
    mydb.close()

# Tax payer details page
def tax_payer_details_page():
    st.title("Tax Payer Details")

    mydb = connect_to_db()
    if not mydb:
        return

    cursor = mydb.cursor()

    # Create Streamlit input fields for tax payer details
    username = st.text_input("Username")
    legalname = st.text_input("Legal Name")
    panno = st.text_input("PAN Number")
    adhaar = st.text_input("Aadhaar Number")
    user_address = st.text_area("Address")
    phoneno = st.text_input("Phone Number")

    # Handle save button click
    if st.button("Save"):
        insert_tax_payer_details(cursor, legalname, panno, adhaar, user_address, phoneno)

    if st.button("Fetch Details"):
        tax_payer = fetch_tax_payer_by_id(cursor, username)
        if tax_payer:
            st.subheader("Existing Details")
            df = pd.DataFrame([tax_payer], columns=['Username', 'Legal Name', 'PAN Number', 'Aadhaar Number', 'Address', 'Phone Number'])
            st.dataframe(df)
        else:
            st.error("Tax Payer not found")

    # Handle update button click
    if st.button("Update"):
        update_tax_payer_details(cursor, username, legalname, panno, adhaar, user_address, phoneno)

    # Handle delete button click
    if st.button("Delete"):
        delete_tax_payer_details(cursor, username)    

    cursor.close()
    mydb.close()

# Tax payer income details page
def tax_payer_income_details_page():
    st.title("Tax Payer Income Details")

    mydb = connect_to_db()
    if not mydb:
        return

    cursor = mydb.cursor()

    # Create Streamlit input fields for income details
    username = st.text_input("Username")
    job_earnings = st.number_input("Job Earnings")
    business_earnings = st.number_input("Business Earnings")
    property_earnings = st.number_input("Property Earnings")
    total_earning = st.number_input("Total Earnings")

    # Handle save button click
    if st.button("Save"):
        insert_income_details(cursor, username, job_earnings, business_earnings, property_earnings, total_earning)
        st.success("Income Details Saved Successfully!")

    cursor.close()
    mydb.close()

# Tax payer investments page
def tax_payer_loan_page():
    st.title("Tax Payer Loan Page")

    mydb = connect_to_db()
    if not mydb:
        return

    cursor = mydb.cursor()

    # Create Streamlit input fields for investments details
    username = st.text_input("Username")
    housing_loans = st.number_input("Housing Loans")
    other_loans = st.number_input("Other Loans")
    rent = st.number_input("Rent")
    provided_funds = st.number_input("Provided Funds")
    policies = st.number_input("Policies")

    # Handle save button click
    if st.button("Save"):
        insert_loan_details(cursor, username, housing_loans, other_loans, rent, provided_funds, policies)

    cursor.close()
    mydb.close()

# Main function to select pages based on user input
def main():
    page = st.sidebar.selectbox("Select Page", ["Login", "Register", "Tax Payer Details", "Admin Panel", "Tax Payer Income Details", "Tax Payer loan Page", "View All Tables"])
    if page == "Login":
        login()
    elif page == "Register":
        register()
    elif page == "Tax Payer Details":
        tax_payer_details_page()
    elif page == "Admin Panel":
        admin_panel()
    elif page == "Tax Payer Income Details":
        tax_payer_income_details_page()
    elif page == "Tax Payer loan Page":
        tax_payer_loan_page()
    elif page == "View All Tables":
        view_all_tables()

if __name__ == "__main__":
    main()
