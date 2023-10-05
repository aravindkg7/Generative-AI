#This is a simple question and answering appication based on Streamlit and OpenAI

#Import the necessary libraries
import streamlit as st
from langchain.llms import OpenAI
from dotenv import load_dotenv, find_dotenv   


#Load the OpenAI model
llm = OpenAI(model='text-davinci-003', temperature=0.5)

if __name__ == "__main__":

    #Load API keys from .env
    load_dotenv(find_dotenv(), override=True)

    #Set the page title
    st.set_page_config("Question Answering Application")
    st.title("Question Answering Application")

    #Ask a question
    input = st.text_input("Please ask a question:")

    submit = st.button("Submit")
    if submit:
        with st.spinner("Generating response..."):
            #Generate response
            answer = llm(input)

            #Display the response in a text area
            st.text_area('Answer:', value=answer)



