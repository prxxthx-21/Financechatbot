import streamlit as st
import requests

st.set_page_config(page_title="Personal Finance Chatbot", page_icon="💰", layout="centered")

st.title("💰 Personal Finance Chatbot")
st.markdown("Get intelligent guidance for savings, taxes, and investments.")

BACKEND_URL = "http://127.0.0.1:8000/chat"

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])

user_input = st.chat_input("Ask about savings, taxes, or investments...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state["messages"].append({"role": "user", "content": user_input})
    try:
        response = requests.post(BACKEND_URL, json={"query": user_input})
        if response.status_code == 200:
            bot_reply = response.json().get("response", "⚠ No reply from backend.")
        else:
            bot_reply = f"⚠ Error: {response.status_code}"
    except Exception as e:
        bot_reply = f"❌ Backend not reachable: {e}"
    st.chat_message("assistant").markdown(bot_reply)
    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
