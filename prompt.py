
from llama_index.llms import LangChainLLM
from langchain.llms import Clarifai
from llama_index import VectorStoreIndex
from llama_index import ServiceContext
from llama_index import Document
from llama_index import SimpleDirectoryReader
from llama_index.prompts  import PromptTemplate
from llama_index.chat_engine.simple import SimpleChatEngine
from llama_index import LLMPredictor

import streamlit as st

# Your PAT (Personal Access Token) can be found in the portal under Authentification
PAT = st.secrets.cf_pat
# Specify the correct user_id/app_id pairings
# Since you're making inferences outside your app's scope
USER_ID = 'openai'
APP_ID = 'chat-completion'
# Change these to whatever model and text URL you want to use
MODEL_ID = 'GPT-4'
MODEL_VERSION_ID = 'ad16eda6ac054796bf9f348ab6733c72'

class LLM_Hander:
    def __init__(self):
        Cfllm = LangChainLLM(llm = Clarifai(
        pat=PAT, user_id=USER_ID, app_id=APP_ID, model_id=MODEL_ID
    ))
        #st.write(type(Cfllm))
        
        self.index = None
        self.documents = []
        self.query_engine = None
        # self.chat_template = """
        #     I want to act as a teacher's assistant. Your task is to help teachers in cutting down their boring tasks.
        #     Follow the instructions given by the teacher and produce the outputs that the teacher is requesting.
        #     You are allowed to ask follow-up questions to better understand the task if the provided instruction is not clear.
        #     Also follow the below rules when you respond.
        #         1. Avoid generating single quotes in your response.
        #         2. DONOT return JSON response.
        #         2. Use easy to understand english.
        #         5. Use the information only in the context to answer your response
        #         """
        self.chat_template = """
            I want to act as a teacher's assistant. Your task is to help teachers in cutting down their boring tasks.
            Follow the instructions given by the teacher and produce the outputs that the teacher is requesting.
            Retrieve information from the vector index about current input within the service context.
            Also follow the below rules when you respond.
            1. Avoid generating single quotes in your response.
            2. DONOT return JSON response.
            3. Use easy to understand english.
            """
        self.service_context = ServiceContext.from_defaults(llm_predictor=LLMPredictor(llm=Cfllm), system_prompt=self.chat_template)
        
    def loadData(self, files):
        for f in files:
            with open('data.pdf', 'wb') as w:
                w.write(f.getvalue())
        reader = SimpleDirectoryReader(
             input_files=["./data.pdf"]
             )
        self.documents = reader.load_data()
        self.index = VectorStoreIndex.from_documents(self.documents, service_context=self.service_context)
        #self.query_engine = self.index.as_query_engine(service_context=self.service_context)
        #print(self)
        #print(self.index)
    
    def firePrompt(self, role, prompt):
        if role == 'student':
            query_engine = self.index.as_query_engine(service_context=self.service_context,
                                                      system_prompt='''
Use only the information in service context. Quote the page number in the reference. Use bullet points. 
                                                      ''')
            return query_engine.query(prompt)
        if role == 'teacher':
            chat_engine = self.index.as_chat_engine(chat_mode='simple')
            return chat_engine.chat(prompt)

    


    
