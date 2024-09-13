import streamlit as st
from dotenv import load_dotenv
from streamlit_feedback import streamlit_feedback
from config_pg import *
from edubot_pg import EduBotCreator
from langfuse.callback import CallbackHandler

langfuse_handler = CallbackHandler()

def create_edubot():
    edubotcreator = EduBotCreator()
    edubot = edubotcreator.create_edubot()
    return edubot

def handle_userinput(input):
    
    full_response = ""
    
    chat_history_str = EduBotCreator.format_chat_history(st.session_state.chat_history)

    for chunk in st.session_state.edubot.stream({"input":input, "chat_history": st.session_state.chat_history, "chat_history_str": chat_history_str},config={"callbacks": [langfuse_handler]}):
        full_response += chunk
        yield chunk

    st.session_state.chat_history.append({"role": "human", "content": input})
    st.session_state.chat_history.append({"role": "assistant", "content": full_response})
    
def storenprintfb(dic):
    st.markdown(dic)

def main():

    load_dotenv()

    st.set_page_config(page_title="FAKE OR REAL")

    st.title("Misinfo Detector")

    if "edubot" not in st.session_state:
        st.session_state.edubot = create_edubot()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    input = st.chat_input("Enter the info")

    if input and st.session_state.edubot:
        
        with st.chat_message("user"):
            st.markdown(input)

        with st.chat_message("assistant"):
            st.write_stream(handle_userinput(input))
        
        
        # Keep only the latest 2 sets of conversation in the chat history
        st.session_state.chat_history = st.session_state.chat_history[-6:]



if __name__ == "__main__":
    main()
    
    