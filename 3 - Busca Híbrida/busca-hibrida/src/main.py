# Configuração de Ambiente

import os
from typing import Any
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


def exibir_resultado(titulo: str, pergunta: str, docs: list[Document], resposta: Any) -> None:
    resposta_texto = getattr(resposta, "text", str(resposta)).strip()

    print("\n" + "=" * 80)
    print(f"📌 {titulo.upper()}")
    print("=" * 80)

    print("\n❓ Pergunta:")
    print(pergunta)

    print(f"\n📄 Chunks Utilizados como Contexto ({len(docs)}):")
    if not docs:
        print("  Nenhum chunk retornado.")
    else:
        for i, doc in enumerate(docs, start=1):
            detalhes = []
            origem = doc.metadata.get("source")
            if origem:
                detalhes.append(f"ID: {origem}")
            score = doc.metadata.get("relevance_score")
            if score is not None:
                detalhes.append(f"Relevância: {score:.4f}")

            header_info = f" ({' | '.join(detalhes)})" if detalhes else ""
            print(f"\n  [{i}]{header_info}")
            print(f"      Texto: {doc.page_content}")

    print("\n💬 Resposta Final:")
    print(resposta_texto)
    print("=" * 80)


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
