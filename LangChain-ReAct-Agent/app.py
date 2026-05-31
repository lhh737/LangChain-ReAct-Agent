import streamlit as st
from agent.react_agent import ReactAgent
from langchain_core.messages import HumanMessage, AIMessage


st.set_page_config(page_title="智扫通 · 智能客服", page_icon="🤖")
st.title("🤖 智扫通机器人智能客服")
st.caption("基于 LangChain ReAct Agent + RAG 检索增强")
st.divider()

if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()
if "display_messages" not in st.session_state:
    st.session_state["display_messages"] = []
if "langchain_history" not in st.session_state:
    st.session_state["langchain_history"] = []

with st.sidebar:
    if st.button("🗑️ 新对话", use_container_width=True):
        st.session_state["display_messages"] = []
        st.session_state["langchain_history"] = []
        st.rerun()

for message in st.session_state["display_messages"]:
    st.chat_message(message["role"]).write(message["content"])

MAX_TURNS = 3 

def trim_history(history: list):
    """截断历史，最多保留 MAX_TURNS 轮对话"""
    max_messages = MAX_TURNS * 2
    if len(history) > max_messages:
        return history[-max_messages:]
    return history

prompt = st.chat_input()
if prompt:

    st.chat_message("user").write(prompt)
    st.session_state["display_messages"].append({"role": "user", "content": prompt})

    history_for_agent = trim_history(st.session_state["langchain_history"])

    full_response = ""
    response_placeholder = st.chat_message("assistant").empty()
    with st.spinner("智能客服思考中..."):
        stream = st.session_state["agent"].execute_stream(prompt, chat_history=history_for_agent)
        for chunk in stream:
            full_response += chunk
            response_placeholder.markdown(full_response + "▌")
        response_placeholder.markdown(full_response)

    st.session_state["display_messages"].append({"role": "assistant", "content": full_response})
    st.session_state["langchain_history"].append(HumanMessage(content=prompt))
    st.session_state["langchain_history"].append(AIMessage(content=full_response))
    st.session_state["langchain_history"] = trim_history(st.session_state["langchain_history"])
    st.rerun()