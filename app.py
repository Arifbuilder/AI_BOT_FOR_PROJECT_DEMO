
import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

st.set_page_config(page_title="Deep Reason", page_icon="🧠")
st.title("🧠 Deep Reason")
st.caption("Stage 1 — Single AI Chatbot")

if not API_KEY:
    st.error("Add OPENROUTER_API_KEY to your .env file.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Enter a problem or ask a question...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("AI is thinking..."):
            try:
                response = requests.post(
                    API_URL,
                    headers={
                        "Authorization": f"Bearer {API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "openrouter/free",
                        "messages": [
                            {
                                "role": "system",
                                "content": (
                                    "You are the initial assistant in "
                                    "the Deep Reason research prototype. "
                                    "Give clear, useful answers."
                                ),
                            },
                            *st.session_state.messages,
                        ],
                    },
                    timeout=90,
                )
                response.raise_for_status()
                answer = response.json()["choices"][0][
                    "message"
                ]["content"]

                st.markdown(answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except requests.RequestException as error:
                st.error(f"AI request failed: {error}")
            except (KeyError, IndexError, TypeError, ValueError):
                st.error("The API returned an unexpected response.")