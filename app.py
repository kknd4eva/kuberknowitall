import streamlit as st
import requests
import json
import os 
import random
import string
import uuid

st.set_page_config(page_title="Kuberknowitall")

hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)
st.title("Kuberknowitall")

# Sidebar or another section for instructions or summary information
st.sidebar.title("Sample questions to get started")
st.sidebar.markdown("""
- Show me a simple K8s yaml file
""")
st.sidebar.image("https://i.ibb.co/64WqhVV/kubernetes-logo.png", use_column_width=True)

# Use a hardcoded session ID or generate one as needed
sessionId = "None"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize session id
if 'sessionId' not in st.session_state:
    st.session_state['sessionId'] = sessionId

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("How can I help you?"):
    # Display user input in chat message container
    question = prompt
    st.chat_message("user").markdown(question)

    # Prepare the payload for the HTTP request
    payload = {"question": prompt, "sessionid": st.session_state['sessionId']}
   
    # Specify the function URL
    function_url = os.environ.get('FUNCTION_URL')

    with st.spinner('Kuberknowitall is thinking..shhhh'):  
        response = requests.post(function_url, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()
        print(result)

        answer = result['answer']
        sessionId = result.get('sessionId', 'None')  # Update this line based on the actual key returned for session ID

        st.session_state['sessionId'] = sessionId

        # Add user input to chat history
        st.session_state.messages.append({"role": "user", "content": question})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(answer)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": answer})
    else:
        st.error(response.text)
