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
from streamlit_feedback import streamlit_feedback

if 'fbk' not in st.session_state:
        st.session_state.fbk = str(uuid.uuid4())

run_id = uuid.uuid4()

langfuse_handler = CallbackHandler()

def create_edubot():
    edubotcreator = EduBotCreator()
    edubot = edubotcreator.create_edubot()
    return edubot

def handle_userinput(input):
    with collect_runs() as cb:
        for chunk in st.session_state.chain_with_history.stream({"input": input}, config = {"configurable": {"session_id": "any"}, "callbacks":[langfuse_handler]}):
            yield chunk
        st.session_state.run_id = cb.traced_runs[0].id


def fbcb(feedback):
    # st.write(feedback)
   
    score_mappings = {
        "thumbs": {"👍": 1, "👎": 0},
    }
    scores = score_mappings["thumbs"]
    score = scores.get(feedback["score"])

    langfuse_client = Langfuse()
    langfuse_client.score(
        trace_id=str(st.session_state.run_id),
        name="user-explicit-feedback",
        value=score,
        comment=feedback.get("text")
    )
    st.session_state.fbk = str(uuid.uuid4())

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
    
    streamlit_feedback(
        feedback_type="thumbs",
        optional_text_label="[Optional]",
        key=st.session_state.fbk,
        on_submit=fbcb
    )


        
        
        
if __name__ == "__main__":
    main()
    
    