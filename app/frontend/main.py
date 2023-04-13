"""
This is the main file for the Streamlit frontend.
"""

import requests
import streamlit as st
from streamlit_chat import message


st.title("Chatbot sobre produtos e serviços da B3")
st.write("Pergunte sua dúvida sobre produtos e serviços da B3")


def generate_response(query):
    """
    This function is responsible for making a GET request to the API endpoint.
    """
    # Replace the API_URL with the URL of your deployed API endpoint
    API_URL = "http://localhost:8000/query"
    response = requests.get(API_URL, params={"query": query}, timeout=15)
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        return None


if "history" not in st.session_state:
    st.session_state.history = []


def generate_answer():
    user_input = st.session_state.input_text
    output = generate_response(user_input)
    st.session_state.history.append({"message": user_input, "is_user": True})
    st.session_state.history.append({"message": output, "is_user": False})


st.text_input("Talk to the bot", key="input_text", on_change=generate_answer)


for i, chat in enumerate(st.session_state.history):
    message(**chat, key=str(i))
