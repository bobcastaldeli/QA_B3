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
        return message(result)
    else:
        return None


def input():
    """
    This function is responsible for taking the user input.
    """
    prompt_text = st.text_input("Type your question here")
    return prompt_text


if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []


user_input = input()


if user_input:
    output = generate_response(user_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state["generated"]:
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(
            st.session_state["past"][i], is_user=True, key=str(i) + "_user"
        )
