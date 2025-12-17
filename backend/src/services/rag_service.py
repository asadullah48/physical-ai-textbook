import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

class RAGService:
    def __init__(self, persist_directory="./db"):
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings()
        self.db = None
        self.qa_chain = None
        
        # Initialize if DB exists, otherwise wait for ingestion
        if os.path.exists(persist_directory):
            self.load_db()

    def load_db(self):
        """Loads the ChromaDB and sets up the QA chain."""
        try:
            self.db = Chroma(
                persist_directory=self.persist_directory, 
                embedding_function=self.embeddings
            )
            
            retriever = self.db.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 3}
            )

            # Custom prompt for "Professor" persona
            prompt_template = """Use the following pieces of context to answer the question at the end. 
            If you don't know the answer, just say that you don't know, don't try to make up an answer.
            
            Context: {context}
            
            Question: {question}
            
            Answer as a Physical AI & Robotics Professor. Be technical but accessible. Include code snippets if relevant:"""
            
            PROMPT = PromptTemplate(
                template=prompt_template, input_variables=["context", "question"]
            )

            llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
            
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever,
                chain_type_kwargs={"prompt": PROMPT},
                return_source_documents=True
            )
            print("✅ RAG Database loaded successfully.")
        except Exception as e:
            print(f"⚠️ Failed to load RAG Database: {e}")

    def query(self, question: str):
        if not self.qa_chain:
            return {"response": "The knowledge base is currently offline or initializing.", "sources": []}
        
        result = self.qa_chain({"query": question})
        answer = result["result"]
        source_docs = result["source_documents"]
        
        # Format sources
        sources = [doc.metadata.get("source", "Unknown") for doc in source_docs]
        
        return {"response": answer, "sources": sources}

# Global Instance
rag_service = RAGService()
