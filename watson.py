import streamlit as st
import time
import json
from prompt import Prompt
from auth import get_access_token

PROJECT_ID = st.secrets["WATSONX_PROJECT_ID"]
MODEL_ID = "google/flan-ul2"
parameters = {
    "decoding_method": "sample",
    "max_new_tokens": 100,
    "min_new_tokens": 5,
    # "random_seed": 123,
    "temperature": 0.8,
    "top_k": 50,
    "top_p": 1,
    "repetition_penalty": 1.2
}


def query_to_watson(prompt_input):
    access_token = get_access_token()
    watson_prompt = Prompt(access_token, PROJECT_ID)
    response = watson_prompt.generate(prompt_input, MODEL_ID, parameters)
    return response


st.title("My WatsonX Text Generator")
st.markdown(f"This Chatbot uses the following parameters along with `{MODEL_ID}`")
st.code(f"{json.dumps(parameters, indent=2)}")
st.markdown("As the models are not for a conversation completion, the prompt would take each input as a new inquery.")
st.divider()


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        query_input = f"{st.session_state.messages[-1]['content']}"
        assistant_response = query_to_watson(query_input)

        if assistant_response:
            for chunk in assistant_response["generated_text"].split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌ ")
            message_placeholder.markdown(full_response)
        else:
            message_placeholder.markdown("Could not respond")

    st.session_state.messages.append({"role": "assistant", "content": full_response})
