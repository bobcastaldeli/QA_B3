"""
This is the main file for the Streamlit frontend.
"""

import requests
import streamlit as st
from streamlit_chat import message


st.title("Chatbot sobre produtos e serviços da B3")
st.write("Pergunte sua dúvida sobre produtos e serviços da B3")


API_URL = "http://localhost:8000/query"


def main():
    """
    This function is responsible for displaying the Streamlit frontend.
    """
    query = st.text_input("Enter your question:", "")
    if st.button("Submit"):
        # Make GET request to the API endpoint
        response = requests.get(API_URL, params={"query": query})
        if response.status_code == 200:
            result = response.json()
            # Process the result and display it in Streamlit
            # You can access the relevant information from the response JSON
            # For example, if the response JSON has a 'answer' field, you can display it like this:
            st.success(f"Answer: {result}")
        else:
            st.error("Failed to get answer. Please try again.")


if __name__ == "__main__":
    main()
