import os

import streamlit as st
from dotenv import load_dotenv
from langsmith import Client
from streamlit_feedback import streamlit_feedback

from config_pg import *
from edubot_pg import EduBotCreator
load_dotenv()
import uuid
client = Client(api_url=os.getenv("LANGCHAIN_ENDPOINT"), api_key=os.getenv("LANGCHAIN_API_KEY"))

def create_edubot():
    edubotcreator = EduBotCreator()
    edubot = edubotcreator.create_edubot()
    return edubot

def handle_userinput(user_question):
    
    full_response = ""
    
    chat_history_str = EduBotCreator.format_chat_history(st.session_state.chat_history)

    for chunk in st.session_state.edubot.stream({"user_question":user_question, "chat_history": st.session_state.chat_history, "chat_history_str": chat_history_str}):
        full_response += chunk.content
        yield chunk.content

    st.session_state.chat_history.append({"role": "user", "content": user_question})
    st.session_state.chat_history.append({"role": "assistant", "content": full_response})
    


def main():

    load_dotenv()
    st.set_page_config(page_title="FAKE OR REAL")

    st.title("Misinfo Detector")

    if "edubot" not in st.session_state:
        st.session_state.edubot = create_edubot()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "run_id" not in st.session_state:
        st.session_state['run_id'] = ""


    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    user_question = st.chat_input("Enter the info")

    if user_question and st.session_state.edubot:
        
        with st.chat_message("user"):
            st.markdown(user_question)

        with st.chat_message("assistant"):
            st.write_stream(handle_userinput(user_question))
            st.session_state['run_id'] = uuid.uuid4()

            if st.session_state.get("run_id"):
                print(st.session_state.get("run_id"))

                feedback = streamlit_feedback(
                    feedback_type="faces",  # Apply the selected feedback style
                    optional_text_label="[Optional] Please provide an explanation",  # Allow for additional comments
                    key=f"feedback_{st.session_state.run_id}",
                )
                print(feedback)
                







        
        # Keep only the latest 2 sets of conversation in the chat history
        st.session_state.chat_history = st.session_state.chat_history[-6:]



if __name__ == "__main__":
    main()
    
    