import streamlit as st
import mysql.connector
import bcrypt

# Database connection
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="video_gen"
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None

# Password hashing
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Password check
def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# Signup function
def signup(username, password):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            st.success("User signed up successfully!")
            st.session_state.page = "login"
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
        finally:
            cursor.close()
            conn.close()

# Login function
def login(usrmail, password):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT u_pass FROM userregdetails WHERE u_mail = %s", (usrmail,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result and password == result[0]:
            st.session_state.logged_in = True
            st.session_state.page = "chat"
            return True
        else:
            return False

# Chat interface
def chat_interface():
    st.title("imaginator.io")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("What is up?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Generate response (simplified example)
        response = "This is a bot response."
        with st.chat_message("bot"):
            st.markdown(response)
        st.session_state.messages.append({"role": "bot", "content": response})

# Navigation
def navigate():
    if "page" not in st.session_state:
        st.session_state.page = "login"
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "signup":
        signup_page()
    elif st.session_state.page == "chat":
        if st.session_state.get("logged_in"):
            chat_interface()
        else:
            st.error("You must be logged in to access the chat interface.")
            st.session_state.page = "login"
            login_page()

# Login page
def login_page():
    st.header("Login")
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        if login_username and login_password:
            if login(login_username, login_password):
                st.success("Logged in successfully!")
                st.session_state.page = "chat"
            else:
                st.error("Invalid username or password.")
        else:
            st.error("Please provide both username and password.")
    if st.button("New User? Sign Up"):
        st.session_state.page = "signup"
        st.experimental_rerun()

# Signup page
def signup_page():
    st.header("Signup")
    signup_username = st.text_input("Username", key="signup_username")
    signup_password = st.text_input("Password", type="password", key="signup_password")
    if st.button("Signup"):
        if signup_username and signup_password:
            signup(signup_username, signup_password)
        else:
            st.error("Please provide both username and password.")
    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()

# Main app
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

navigate()


# ###
# import mysql.connector
# import streamlit as st
# import random
# import time

# st.title("Simple Chat")

# # Establish database connection
# try:
#     conn = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="",
#         database="video_gen"
#     )
# except mysql.connector.Error as err:
#     st.error(f"Error: {err}")
#     st.stop()

# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # Accept user input
# if prompt := st.chat_input("What is up?"):
#     # Display user message in chat message container
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     # Here you can add logic to fetch a response from the database or generate a response
#     # Example: Fetching a random response from a database table called 'responses'
#     cursor = conn.cursor()
#     cursor.execute("SELECT response FROM responses ORDER BY RAND() LIMIT 1")
#     response = cursor.fetchone()
#     if response:
#         response_content = response[0]
#     else:
#         response_content = "Sorry, I don't have a response for that."

#     # Display the bot's response
#     with st.chat_message("bot"):
#         st.markdown(response_content)
#     # Add bot response to chat history
#     st.session_state.messages.append({"role": "bot", "content": response_content})

# # Close the database connection
# conn.close()
# ###