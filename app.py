import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="Ollama AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Title
st.title("🤖 Ollama AI Chatbot")
st.write("Chat with an AI using Streamlit and Ollama")

# Create chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# Chat input box
user_input = st.chat_input("Type your message here...")

# When the user sends a message
if user_input:

    # Display user message
    with st.chat_message("user"):
        st.write(user_input)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    try:

        # Send message to Ollama
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": user_input,
                "stream": False
            }
        )

        # Check if request was successful
        response.raise_for_status()

        # Convert response to JSON
        data = response.json()

        # Get AI response
        ai_response = data.get(
            "response",
            "Ollama did not return a response."
        )

    except requests.exceptions.ConnectionError:

        ai_response = (
            "❌ Ollama is not running. "
            "Please start Ollama and try again."
        )

    except requests.exceptions.RequestException as error:

        ai_response = f"❌ Error connecting to Ollama: {error}"

    # Display AI response
    with st.chat_message("assistant"):
        st.write(ai_response)

    # Save AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_response
    })