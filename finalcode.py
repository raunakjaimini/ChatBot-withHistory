import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="ChatBot",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Custom CSS for grey tone theme and additional styling
st.markdown("""
    <style>
    body {
        background-color: #2E2E2E;
        color: #E0E0E0;
    }
    .chat-message {
        padding: 12px;
        border-radius: 10px;
        margin: 5px 0;
        max-width: 80%;
        word-wrap: break-word;
        animation: fadeIn 0.5s ease-in-out;
    }
    .user-message {
        background-color: #6c757d; /* Grey color for user messages */
        color: #ffffff;
        text-align: right;
    }
    .assistant-message {
        background-color: #4a4a4a; /* Dark grey for assistant messages */
        color: #ffffff;
        text-align: left;
    }
    .stTextInput input {
        background-color: #3c3c3c;
        color: #ffffff;
        border: 1px solid #555555;
        border-radius: 8px;
        padding: 10px;
    }
    .stTextInput input::placeholder {
        color: #888888;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    </style>
""", unsafe_allow_html=True)

# Display the chatbot's title on the page
st.title("Chat-Mate...Lets Chat Brother")

# Create a container for the chat messages
chat_container = st.container()

# Display the chat history
with chat_container:
    for message in st.session_state.chat_session.history:
        message_class = 'assistant-message' if message.role == "model" else 'user-message'
        st.markdown(
            f'<div class="chat-message {message_class}">{message.parts[0].text}</div>',
            unsafe_allow_html=True
        )

# Input field for user's message
user_prompt = st.chat_input("Ask....")
if user_prompt:
    # Add user's message to chat and display it
    st.markdown(
        f'<div class="chat-message user-message">{user_prompt}</div>',
        unsafe_allow_html=True
    )

    # Show loading spinner while waiting for the chatbot's response
    with st.spinner("Generating response..."):
        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Display Gemini-Pro's response
        st.markdown(
            f'<div class="chat-message assistant-message">{gemini_response.text}</div>',
            unsafe_allow_html=True
        )
