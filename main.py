import os
import streamlit as st
from dotenv import load_dotenv
import cohere

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Chat with Command R+!",
    page_icon="🧠",
    layout="wide",
)

# Load Cohere API key
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not COHERE_API_KEY:
    st.error("🚨 COHERE_API_KEY is not set. Please check your .env file.")
    st.stop()

# Initialize Cohere client
co = cohere.Client(COHERE_API_KEY)

# Session state for chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# App title
st.title("🤖 Wiskey Pro - Powered by Cohere Command R+")

# Display chat history
for role, text in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(text)

# Chat input
user_input = st.chat_input("Ask Wiskey anything...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append(("user", user_input))

    try:
        response = co.chat(
            model="command-r-plus",
            message=user_input,
            chat_history=[
                {"role": role, "message": msg} for role, msg in st.session_state.chat_history
            ],
        )
        reply = response.text
        st.chat_message("assistant").markdown(reply)
        st.session_state.chat_history.append(("assistant", reply))
    except Exception as e:
        st.error(f"❌ Cohere API call failed: {e}")
