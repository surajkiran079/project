import streamlit as st
import sqlite3
from sqlite3 import Error
import subprocess

# Function to create a database connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        st.error(e)
    return conn

# Function to create a new user
def create_user(conn, user):
    sql = ''' INSERT INTO users(username, email, password)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid

# Function to check if a user exists
def user_exists(conn, email):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    rows = cur.fetchall()
    return len(rows) > 0

# Function to retrieve a user's password
def get_user_password(conn, email):
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE email=?", (email,))
    rows = cur.fetchall()
    if len(rows) > 0:
        return rows[0][0]
    else:
        return None



# Main function
def main():
    st.title("Registration and Login Page")

    # Create a database connection
    conn = create_connection("users.db")

    # Create users table if it doesn't exist
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')

    # Sidebar selection
    page = st.sidebar.radio("Select Page", ["Login", "Register"])

    # Login page
    if page == "Login":
        st.subheader("Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            # Check if user exists
            if user_exists(conn, email):
                # Check if password matches
                stored_password = get_user_password(conn, email)
                if password == stored_password:
                    st.success("Login successful!")
                    subprocess.run(["streamlit", "run", "candle.py"])


                else:
                    st.error("Incorrect email or password.")
            else:
                st.error("User does not exist. Please register.")


    # Registration page
    elif page == "Register":
        st.subheader("Register")
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("Register"):
            if password == confirm_password:
                # Check if user already exists
                if user_exists(conn, email):
                    st.error("User with this email already exists.")
                else:
                    # Add user to database
                    user = (username, email, password)
                    create_user(conn, user)
                    st.success("Registration successful! Please login.")
            else:
                st.error("Passwords do not match.")


if __name__ == "__main__":
    main()










