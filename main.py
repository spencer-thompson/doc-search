'''
Usage via terminal: streamlit run main.py

'''


import os
from dotenv import load_dotenv

# Openai
import openai

# Langchain
from langchain.text_splitter import RecursiveCharacterTextSplitter

import streamlit as st







def main():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    st.set_page_config(page_title = "My webpage", page_icon = ":tada:", layout = "wide")
    
    st.header("Ask your PDF 💬")

    pdf = st.file_uploader("Upload your PDF", type="pdf")

if __name__ == "__main__":
    main()