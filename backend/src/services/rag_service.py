import os
try:
    from langchain_community.vectorstores import Chroma
    from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
from dotenv import load_dotenv

load_dotenv()

class RAGService:
    def __init__(self, persist_directory="./db"):
        self.persist_directory = persist_directory
        self.db = None
        self.chain = None
        
        if not LANGCHAIN_AVAILABLE:
            print("⚠️ LangChain dependencies missing. RAG service disabled.")
            return

        try:
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=os.getenv("GOOGLE_API_KEY")
            )
            if os.path.exists(persist_directory):
                self.load_db()
        except Exception as e:
            print(f"⚠️ RAG Init failed: {e}")

    def load_db(self):
        if not LANGCHAIN_AVAILABLE: return
        try:
            self.db = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )

            retriever = self.db.as_retriever(search_kwargs={"k": 3})

            template = """Answer based on this context:

Context: {context}

Question: {question}

Answer as a Physical AI Professor:"""

            prompt = PromptTemplate.from_template(template)
            
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash-latest",
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                temperature=0
            )

            def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)

            self.chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
            )
            
            self.retriever = retriever
            print("✅ RAG with Gemini loaded!")
        except Exception as e:
            print(f"⚠️ Failed: {e}")

    def query(self, question: str):
        if not self.chain:
            return {"response": "KB initializing.", "sources": []}

        try:
            response = self.chain.invoke(question)
            docs = self.retriever.invoke(question)
            sources = [doc.metadata.get("source", "textbook") for doc in docs]
            return {"response": response, "sources": sources}
        except Exception as e:
            return {"response": f"Error: {str(e)}", "sources": []}

rag_service = RAGService()
