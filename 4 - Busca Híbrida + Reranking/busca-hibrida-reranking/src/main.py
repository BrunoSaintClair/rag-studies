# Configuração de Ambiente

import os
from typing import Any
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")


# Coleta e separação dos dados

from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from data import chunks  # Base com 50 textos de engenharia, cloud e infraestrutura

documents = [
    Document(page_content=chunk, metadata={"source": f"chunk_{i}"})
    for i, chunk in enumerate(chunks)
]

# 1. Retriever Vetorial (Semântico)
embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2",
    google_api_key=GEMINI_API_KEY
)
vector_store = Chroma.from_documents(documents=documents, embedding=embedding_model)
vector_retriever = vector_store.as_retriever(search_kwargs={"k": 4})


# 2. Retriever Léxico (BM25 - Match de Palavras-Chave Exatas)

from langchain_community.retrievers import BM25Retriever

bm25_retriever = BM25Retriever.from_documents(documents=documents, k=4)


# 3. Retriever Híbrido (Ensemble: Combina Vetorial + BM25)

from langchain_classic.retrievers import EnsembleRetriever

hybrid_retriever = EnsembleRetriever(
    retrievers=[vector_retriever, bm25_retriever],
    weights=[0.5, 0.5]
)


# 4. Compressor de Reranking (Cohere)

from langchain_cohere import CohereRerank

SCORE_THRESHOLD = 0.5  # Limiar mínimo de relevância do cross-encoder

compressor = CohereRerank(
    cohere_api_key=COHERE_API_KEY,
    model="rerank-multilingual-v3.0",
    top_n=3
)


# Configuração do Prompt e Modelo de Geração (LLM)

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


# Execução Comparativa das 4 Abordagens de RAG

if __name__ == "__main__":
    pergunta = (
        "Como acelerar builds e minimizar o consumo de banda em pipelines CI/CD "
        "utilizando Docker BuildKit com cache remoto inline?"
    )

    # 1. Pipeline: Busca Vetorial Pura (Chroma)
    vector_docs = vector_retriever.invoke(pergunta)
    context_v = "\n\n".join(doc.page_content for doc in vector_docs)
    answer_v = chain.invoke({"context": context_v, "question": pergunta})

    exibir_resultado(
        titulo="1. Busca Vetorial Pura (Chroma)",
        pergunta=pergunta,
        docs=vector_docs,
        resposta=answer_v,
    )

    # 2. Pipeline: Busca por Palavra Exata (BM25)
    bm25_docs = bm25_retriever.invoke(pergunta)
    context_bm = "\n\n".join(doc.page_content for doc in bm25_docs)
    answer_bm = chain.invoke({"context": context_bm, "question": pergunta})

    exibir_resultado(
        titulo="2. Busca por Palavra Exata (BM25)",
        pergunta=pergunta,
        docs=bm25_docs,
        resposta=answer_bm,
    )

    # 3. Pipeline: Busca Híbrida (Ensemble: Vetorial + BM25)
    hybrid_docs = hybrid_retriever.invoke(pergunta)
    context_h = "\n\n".join(doc.page_content for doc in hybrid_docs)
    answer_h = chain.invoke({"context": context_h, "question": pergunta})

    exibir_resultado(
        titulo="3. Busca Híbrida (Ensemble: Vetorial + BM25)",
        pergunta=pergunta,
        docs=hybrid_docs,
        resposta=answer_h,
    )

    # 4. Pipeline: Busca Híbrida + Reranking (Cohere)
    initial_hybrid_docs = hybrid_retriever.invoke(pergunta)
    raw_reranked_docs = compressor.compress_documents(
        documents=initial_hybrid_docs,
        query=pergunta
    )
    final_reranked_docs = [
        doc for doc in raw_reranked_docs
        if (doc.metadata.get("relevance_score") or 0.0) >= SCORE_THRESHOLD
    ]
    context_hr = "\n\n".join(doc.page_content for doc in final_reranked_docs)
    answer_hr = chain.invoke({"context": context_hr, "question": pergunta})

    exibir_resultado(
        titulo="4. Busca Híbrida + Reranking (Cohere)",
        pergunta=pergunta,
        docs=final_reranked_docs,
        resposta=answer_hr,
    )
