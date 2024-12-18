import os
from langchain_community.document_loaders import DataFrameLoader
#from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.docstore.document import Document
#from langchain import HarmBlockThreshold, HarmCategory
from langchain_community.vectorstores import Chroma
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)

class QASystem:
    def __init__(self, google_api_key):
        os.environ["GOOGLE_API_KEY"] = google_api_key
        self.vectorstore = None
        self.rag_chain = None
    
    def initialize_vectorstore(self, df):
        try:
            loader = DataFrameLoader(df, page_content_column="text")
            documents = loader.load()
            
            gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-pro",
                safety_settings={
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                }
            )
            
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=gemini_embeddings,
                persist_directory="chroma_db"
            )
            
            retriever = self.vectorstore.as_retriever(search_kwargs={"k": 10})
            
            template = """You are an assistant for question-answering tasks.
            Use the following context to answer the question.
            If you don't know the answer, just say that you don't know.
            Keep the answer concise.
            Add the metadata or source of the document where you get the answer.
            
            Question: {question} 
            Context: {context} 
            Answer:"""
            
            prompt = PromptTemplate.from_template(template)
            
            def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)
            
            self.rag_chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
            )
            
            return True
            
        except Exception as e:
            print(f"Error initializing vectorstore: {str(e)}")
            return False
    
    def get_answer(self, question):
        if self.rag_chain is None:
            return "System not initialized. Please initialize first."
        try:
            return self.rag_chain.invoke(question)
        except Exception as e:
            return f"Error generating answer: {str(e)}"