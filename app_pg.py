import streamlit as st
from dotenv import load_dotenv
from streamlit_feedback import streamlit_feedback
from config_pg import *
from edubot_pg import EduBotCreator
from langfuse.callback import CallbackHandler
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.tracers.context import collect_runs
import uuid
from langfuse import Langfuse

# Set page configuration (must be the first Streamlit command)
st.set_page_config(page_title="FAKE OR REAL", page_icon="🧐", layout="centered")

# Initialize feedback session state
if 'fbk' not in st.session_state:
    st.session_state.fbk = str(uuid.uuid4())

if 'run_id' not in st.session_state:
    st.session_state.run_id = None

# Initialize Langfuse callback handler
langfuse_handler = CallbackHandler(user_id="IBRAHIM")


# EduBot creation
def create_edubot():
    edubotcreator = EduBotCreator()
    edubot = edubotcreator.create_edubot()
    return edubot


# Handles user input, streams the bot's response, and stores the run_id
def handle_userinput(user_input):
    with collect_runs() as cb:
        for chunk in st.session_state.chain_with_history.stream(
                {"input": user_input},
                config={"configurable": {"session_id": "any"}, "callbacks": [langfuse_handler]}
        ):
            yield chunk
        st.session_state.run_id = cb.traced_runs[0].id  # Track the run ID for feedback scoring


# Feedback callback to Langfuse and updating the state
def fbcb(feedback):
    score_mappings = {
        "thumbs": {"👍": 1, "👎": 0},
    }
    score = score_mappings["thumbs"].get(feedback["score"])

    # Send the feedback score and comment to Langfuse
    langfuse_client = Langfuse()
    langfuse_client.score(
        trace_id=str(st.session_state.run_id),
        name="user-explicit-feedback",
        value=score,
        comment=feedback.get("text")  # Optional text feedback
    )

    # Display a thank you message after submission
    st.success("Thank you for your feedback!", icon="✅")

    # Generate a new feedback key to reset the form for the next input
    st.session_state.fbk = str(uuid.uuid4())


# Custom styling for better layout and design
def custom_css():
    st.markdown("""
        <style>
            /* Background */
            .stApp {
                background: linear-gradient(135deg, #343a40 10%, #495057 100%);
                color: #f8f9fa;
            }

            /* Chat and feedback containers */
            .feedback-container, .chat-container {
                background-color: #212529;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
                margin-bottom: 20px;
                color: #f8f9fa;
            }

            /* Chat input styling */
            .stTextInput {
                padding: 12px;
                border-radius: 8px;
                border: 1px solid #ced4da;
                box-shadow: 0 1px 6px rgba(0, 0, 0, 0.2);
                background-color: #495057;
                color: #ffffff;
            }

            /* Title Styling */
            h1 {
                font-family: 'Roboto', sans-serif;
                font-size: 2.5rem;
                color: #17a2b8;
                text-align: center;
                margin-bottom: 30px;
            }

            /* Feedback section */
            .feedback-container h3 {
                color: #f8f9fa;
                text-align: center;
                font-weight: 500;
            }

            /* Feedback button */
            .stButton>button {
                background-color: #17a2b8 !important;
                color: white !important;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                padding: 10px 20px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            .stButton>button:hover {
                background-color: #138496 !important;
            }

            /* Assistant and user message styles */
            .stChatMessage {
                border: none;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 10px;
                font-size: 1rem;
            }
            .stChatMessage-user {
                background-color: #f1f3f5;
                color: #212529;
            }
            .stChatMessage-assistant {
                background-color: #17a2b8;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)


# Main Streamlit app logic
def main():
    # Load environment variables (e.g., LangFuse keys)
    load_dotenv()

    # Apply custom CSS styling
    custom_css()

    # Set up page title
    st.title("Misinfo Detector")

    # Initialize chat message history using Streamlit's session management
    msgs = StreamlitChatMessageHistory(key="session_key")

    # Initialize chatbot with history if not already in session state
    if "chain_with_history" not in st.session_state:
        edubot = create_edubot()
        st.session_state.chain_with_history = RunnableWithMessageHistory(
            edubot,
            lambda session_id: msgs,  # Fetch chat history for the session
            input_messages_key="input",
            history_messages_key="chat_history",
        )

    # Display the chat history (previous user and bot messages)
    for msg in msgs.messages:
        with st.chat_message(msg.type):
            st.markdown(msg.content)

    # Input field for the user to enter a question
    user_input = st.chat_input("Enter your query here")

    # If a user input is provided, process it with the chatbot
    if user_input and st.session_state.chain_with_history:
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            st.write_stream(handle_userinput(user_input))

    # If a run_id is generated (indicating that the bot has responded), show the feedback form
    if st.session_state.run_id:
        with st.container():
            st.markdown('<div class="feedback-container">', unsafe_allow_html=True)
            st.markdown("### We value your feedback! 💬")

            # Feedback Form with optional comments
            feedback_col, comment_col = st.columns([1, 2])
            with feedback_col:
                feedback = streamlit_feedback(
                    feedback_type="thumbs",
                    optional_text_label="comments!",
                    key=st.session_state.fbk,  # Ensure the form is reset after each submission
                    on_submit=fbcb  # Callback function to handle the feedback submission
                )

            st.markdown('</div>', unsafe_allow_html=True)


# Run the app
if __name__ == "__main__":
    main()
