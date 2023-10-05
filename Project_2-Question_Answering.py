#This code is based on an online course by Andrei Dumitrescu (Crystal Mind Academy)

#This program will be able to read pdf, txt, docx files and will be able to answer questions based on that document
import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import os

#Function to read documents from various sources such as pdf, txt and docx
def read_document(file):
    name, extension = os.path.splitext(file)

    if extension == ".pdf":
        from langchain.document_loaders import PyPDFLoader
        print(f'Reading {file} ...')
        loader = PyPDFLoader(file)
    elif extension == ".txt":
        from langchain.document_loaders import TextLoader
        print(f'Reading {file} ...')
        loader = TextLoader(file)
    elif extension == ".docx":
        from langchain.document_loaders import Docx2txtLoader
        print(f'Reading {file} ...')
        loader = Docx2txtLoader(file)
    else:
        print('Document is not in one of the specified formats')
        return None
    
    data = loader.load()
    return(data)

#Function to chunk data
def chunk_data(data, chunk_size=256, chunk_overlap=2):
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(data)
    return(chunks)

#Function to create embeddings using OpenAI and storing them in Chroma vector store
def create_embeddings(chunks):
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma.from_documents(chunks, embeddings)
    return(vector_store)

def question_answer(vector_store, query, k=3):
    from langchain.chains import RetrievalQA
    from langchain.chat_models import ChatOpenAI

    llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=1)
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={'k': k})
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type='stuff', retriever=retriever)

    answer = chain.run(query)
    return(answer)

#Function to clear chat history from streamlit session 
def clear_history():
    if 'history' in st.session_state:
        del st.session_state['history']


if __name__ == "__main__":

    #Load API keys from .env
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv(), override=True)

    st.image('img.png')
    st.subheader('LLM Question and Answering Application :sparkler:')
    with st.sidebar:
        #Upload file
        uploaded_file = st.file_uploader('Upload a file:', type=['.pdf','.docx','.txt'], on_change=clear_history)

        #Chunk size widget
        chunk_size = st.number_input('Chunk Size:', min_value=100, max_value=2048, value=1024, step=200,on_change=clear_history)

        # k number input widget
        k = st.number_input('k', min_value=1, max_value=20, value=3, on_change=clear_history)

        #Add data button widgets
        add_data = st.button('Add Data', on_click=clear_history)

        if uploaded_file and add_data:
            with st.spinner('Reading, chunking and embedding file ...'):

                #Writing the file from RAM to current directory on disk
                bytes_data = uploaded_file.read()
                file_name = os.path.join('./', uploaded_file.name)
                with open(file_name, 'wb') as f:
                    f.write(bytes_data)

                data = read_document(file_name)
                chunks = chunk_data(data, chunk_size=chunk_size)
                st.write(f'Chunk size: {chunk_size}, Chunks: {len(chunks)}')

                #Creating embedding and returning chroma vector store
                vector_store = create_embeddings(chunks)

                #Saving the vector store in the streamlit session state to be persistent between runs
                st.session_state.vs = vector_store
                st.success('File read, chunked and embedded successfully.')

    #User's question text input widget
    q = st.text_input('Ask a question on the content of the file:')
    if q:
        if 'vs' in st.session_state:
            vector_store = st.session_state.vs 
            st.write(f'k: {k}')
            answer = question_answer(vector_store=vector_store, query=q,k=k)
            
            #Text area widget for the answer
            st.text_area("LLM Answer: ", value= answer)

            st.divider()

            #Create chat history, if there is none
            if 'history' not in st.session_state:
                st.session_state.history = ''

            value = f'Q: {q} \nA: {answer}'

            st.session_state.history = f'{value} \n {"-" * 50} \n {st.session_state.history}'
            h = st.session_state.history

            #Text area widget for the chat history
            st.text_area(label='Chat History', value=h, key="history", height=300)







 