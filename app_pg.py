import streamlit as st
from dotenv import load_dotenv
from streamlit_feedback import streamlit_feedback
from config_pg import *
from edubot_pg import EduBotCreator
from langfuse.callback import CallbackHandler
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
import uuid
from langfuse import Langfuse
from streamlit_feedback import streamlit_feedback


run_id = uuid.uuid4()

langfuse_handler = CallbackHandler()


def create_edubot():
    edubotcreator = EduBotCreator()
    edubot = edubotcreator.create_edubot()
    return edubot

def handle_userinput(input):
    
    for chunk in st.session_state.chain_with_history.stream({"input": input}, config = {"configurable": {"session_id": "any"}, "callbacks":[langfuse_handler], "run_id": run_id}):
        yield chunk

def main():

    load_dotenv()

    st.set_page_config(page_title="FAKE OR REAL")

    st.title("Misinfo Detector")

    msgs = StreamlitChatMessageHistory(key="session_key")

    if "chain_with_history" not in st.session_state:
        edubot = create_edubot()

        st.session_state.chain_with_history = RunnableWithMessageHistory(
        edubot,
        lambda session_id: msgs,  # Always return the instance created earlier
        input_messages_key="input",
        history_messages_key="chat_history",
        )

    for msg in msgs.messages:
        with st.chat_message(msg.type):
            st.markdown(msg.content)



    input = st.chat_input("Enter the info")

    if input and st.session_state.chain_with_history:
        
        with st.chat_message("user"):
            st.markdown(input)

        with st.chat_message("assistant"):
            st.write_stream(handle_userinput(input))



        
        
        
if __name__ == "__main__":
    main()
    
    