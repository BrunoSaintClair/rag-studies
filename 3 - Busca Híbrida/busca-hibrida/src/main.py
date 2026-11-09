# Configuração de Ambiente

import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# Coleta e separação dos dados
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from data import chunks  # Arquivo auxiliar contendo os textos usados nas buscas


documents = [Document(page_content=chunk, metadata={"source": f"chunk_{i}"}) for i, chunk in enumerate(chunks)]

embedding_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2", google_api_key=GEMINI_API_KEY)
vector_store = Chroma.from_documents(documents=documents, embedding=embedding_model)
vector_retriever = vector_store.as_retriever(search_kwargs={"k": 2})


# Implementando Retriever de Busca por Palavra Exata
from langchain_community.retrievers import BM25Retriever

bm25_retriever = BM25Retriever.from_documents(documents=documents, k=2)


# Implementando Retriever de Busca Híbrida
from langchain_classic.retrievers import EnsembleRetriever

hybrid_search_retriever = EnsembleRetriever(
    retrievers=[vector_retriever, bm25_retriever],
    weights=[0.5, 0.5]
)


# Geração da Resposta com IA
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from output_formatter import exibir_resultado

template = """
Responda a pergunta baseado EXCLUSIVAMENTE no contexto a seguir:
{context}

Na resposta, não diga frases genéricas como "Com base no contexto fornecido...", apenas responda de maneira direta.

Pergunta:
{question}
"""

prompt = ChatPromptTemplate.from_template(template=template)
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", google_api_key=GEMINI_API_KEY)
chain = prompt | llm


if __name__ == "__main__":
    pergunta = "Como resolver a lentidão e saturação de requisições em microsserviços web e qual biblioteca Java pode ser empregada?"

    retrievers = {
        "Busca Vetorial (Chroma)": vector_retriever,
        "Busca por Palavra Exata (BM25)": bm25_retriever,
        "Busca Híbrida (Ensemble - Vetorial + BM25)": hybrid_search_retriever,
    }

    for nome, retriever in retrievers.items():
        docs = retriever.invoke(pergunta)
        context_text = "\n\n".join(doc.page_content for doc in docs)
        answer = chain.invoke({"context": context_text, "question": pergunta})
        exibir_resultado(
            titulo=nome,
            pergunta=pergunta,
            docs=docs,
            resposta=answer,
        )
