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




load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")



def main():
    pass


if __name__ == "__main__":
    main()