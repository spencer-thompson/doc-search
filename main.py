'''
Usage via terminal: streamlit run main.py

Haven't tested anything yet at all.
'''


import os
from dotenv import load_dotenv

# Openai
#import openai | probably don't need

# Langchain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import initialize_agent

# Tools
from langchain.agents import Tool

# Streamlit
import streamlit as st







def main():
    load_dotenv()



    st.set_page_config(page_title = "My webpage", page_icon = ":tada:", layout = "wide")
    
    st.header("Ask your PDF 💬")

    pdf = st.file_uploader("Upload your PDF", type="pdf")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    # TODO - Need to test / Too tired
    texts = text_splitter.split_documents(pdf)

    llm = ChatOpenAI(
        openai_api_key = os.getenv("OPENAI_API_KEY"),
        temperature = 0,
        model_name = 'gpt-3.5-turbo'
    )

    embedding = OpenAIEmbeddings()

    persist_directory = 'db'

    vectordb = Chroma.from_documents(
        documents = texts, # TODO - Need to test / Too tired
        embedding = embedding,
        persist_directory = persist_directory
    )

    retriever = RetrievalQA.from_chain_type(
        llm = llm,
        chain_type = "stuff",
        retriever = vectordb.as_retriever()
    )

    tools = [Tool(
        func = retriever.run,
        description = "Use this tool to answer Any question, This tool can also be used for follwo up questions from the user.",
        name = 'Lex Fridman DB'
    )]

    memory = ConversationBufferWindowMemory(
        memory_key = "chat_history",  # important to align with agent prompt (below)
        k = 5,
        return_messages = True
    )
     
    conversational_agent = initialize_agent(
        agent='chat-conversational-react-description', 
        tools=tools, 
        llm=llm,
        verbose=True,
        max_iterations=2,
        early_stopping_method="generate",
        memory=memory,
    )

    sys_msg = """You are a helpful chatbot that answers the user's questions.
    """

    prompt = conversational_agent.agent.create_prompt(
        system_message=sys_msg,
        tools=tools
    )

    conversational_agent.agent.llm_chain.prompt = prompt



if __name__ == "__main__":
    main()