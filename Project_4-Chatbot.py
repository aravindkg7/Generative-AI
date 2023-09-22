#This code is based on an online course by Andrei Dumitrescu (Crystal Mind Academy

from langchain.chat_models import ChatOpenAI
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)

import streamlit as st
from streamlit_chat import message

#Load the OpenAI api keys
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv(), override=True)

st.set_page_config(page_title="Chat Assistant", page_icon='🤖')

st.subheader('Private Chat Assistant 🤠')

chat = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.3)

#Creating the messages (chat history)
if 'messages' not in st.session_state:
    st.session_state.messages = []

#Creating the sidebar
with st.sidebar:
    #Text input for the System role
    system_message = st.text_input(label='System role:')

    #Text input for user question
    human_message = st.text_input(label="Ask a question:")

    #When user entered a system message
    if system_message:
        if not any(isinstance(x, SystemMessage) for x in st.session_state.messages):
            st.session_state.messages.append(SystemMessage(content=system_message))

    #When user entered a question
    if human_message:
        st.session_state.messages.append(HumanMessage(content=human_message))

        with st.spinner("Generating response ..."):
            #Generating response
            response = chat(st.session_state.messages)

        #Adding the response to session state
        st.session_state.messages.append(AIMessage(content=response.content))

#Adding a default SystemMessage if the user hasn't entered one
if len(st.session_state.messages) >=1:
    if not isinstance(st.session_state.messages[0], SystemMessage):
        st.session_state.messages.insert(0, SystemMessage(content="You are a helpful assistant"))

#Displaying the chat history
for i, msg in enumerate(st.session_state.messages[1:]):
    if i%2 == 0:
        message(msg.content, is_user=True, key=f'{i} + 🤓') #User Question
    else:
        message(msg.content, is_user=False, key=f'{i} + 🤖') #Response from GPT
