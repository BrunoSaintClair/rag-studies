# Configuração de Ambiente

import os
import time
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
from output_formatter import format_output

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


# Execução Comparativa das 4 Abordagens de RAG

if __name__ == "__main__":
    pergunta = (
        "Como acelerar builds e minimizar o consumo de banda em pipelines CI/CD "
        "utilizando Docker BuildKit com cache remoto inline?"
    )

    print("\n" + "#" * 80)
    print(f"❓ PERGUNTA DE TESTE:\n\"{pergunta}\"")
    print("#" * 80)

    # -------------------------------------------------------------
    # 1. Pipeline: Busca Vetorial Pura (Chroma)
    # -------------------------------------------------------------
    t0_retrieval_v = time.perf_counter()
    vector_docs = vector_retriever.invoke(pergunta)
    latency_retrieval_v = time.perf_counter() - t0_retrieval_v

    context_v = "\n\n".join(doc.page_content for doc in vector_docs)
    t0_llm_v = time.perf_counter()
    answer_v = chain.invoke({"context": context_v, "question": pergunta})
    latency_llm_v = time.perf_counter() - t0_llm_v

    format_output(
        title="1. Busca Vetorial Pura (Chroma)",
        answer=answer_v,
        docs=vector_docs,
        latencies={
            "total": latency_retrieval_v + latency_llm_v,
            "etapas": {
                "Retrieval Vetorial": latency_retrieval_v,
                "Geração LLM": latency_llm_v,
            },
        },
    )

    # -------------------------------------------------------------
    # 2. Pipeline: Busca por Palavra Exata (BM25)
    # -------------------------------------------------------------
    t0_retrieval_bm = time.perf_counter()
    bm25_docs = bm25_retriever.invoke(pergunta)
    latency_retrieval_bm = time.perf_counter() - t0_retrieval_bm

    context_bm = "\n\n".join(doc.page_content for doc in bm25_docs)
    t0_llm_bm = time.perf_counter()
    answer_bm = chain.invoke({"context": context_bm, "question": pergunta})
    latency_llm_bm = time.perf_counter() - t0_llm_bm

    format_output(
        title="2. Busca por Palavra Exata (BM25)",
        answer=answer_bm,
        docs=bm25_docs,
        latencies={
            "total": latency_retrieval_bm + latency_llm_bm,
            "etapas": {
                "Retrieval BM25": latency_retrieval_bm,
                "Geração LLM": latency_llm_bm,
            },
        },
    )

    # -------------------------------------------------------------
    # 3. Pipeline: Busca Híbrida (Ensemble: Vetorial + BM25)
    # -------------------------------------------------------------
    t0_retrieval_h = time.perf_counter()
    hybrid_docs = hybrid_retriever.invoke(pergunta)
    latency_retrieval_h = time.perf_counter() - t0_retrieval_h

    context_h = "\n\n".join(doc.page_content for doc in hybrid_docs)
    t0_llm_h = time.perf_counter()
    answer_h = chain.invoke({"context": context_h, "question": pergunta})
    latency_llm_h = time.perf_counter() - t0_llm_h

    format_output(
        title="3. Busca Híbrida (Ensemble: Vetorial + BM25)",
        answer=answer_h,
        docs=hybrid_docs,
        latencies={
            "total": latency_retrieval_h + latency_llm_h,
            "etapas": {
                "Retrieval Híbrido (Ensemble)": latency_retrieval_h,
                "Geração LLM": latency_llm_h,
            },
        },
    )

    # -------------------------------------------------------------
    # 4. Pipeline: Busca Híbrida + Reranking (Cohere)
    # -------------------------------------------------------------
    t0_retrieval_hr = time.perf_counter()
    initial_hybrid_docs = hybrid_retriever.invoke(pergunta)
    latency_retrieval_hr = time.perf_counter() - t0_retrieval_hr

    t0_rerank = time.perf_counter()
    raw_reranked_docs = compressor.compress_documents(
        documents=initial_hybrid_docs,
        query=pergunta
    )
    final_reranked_docs = [
        doc for doc in raw_reranked_docs
        if (doc.metadata.get("relevance_score") or 0.0) >= SCORE_THRESHOLD
    ]
    latency_rerank = time.perf_counter() - t0_rerank

    context_hr = "\n\n".join(doc.page_content for doc in final_reranked_docs)
    t0_llm_hr = time.perf_counter()
    answer_hr = chain.invoke({"context": context_hr, "question": pergunta})
    latency_llm_hr = time.perf_counter() - t0_llm_hr

    total_latency_hr = latency_retrieval_hr + latency_rerank + latency_llm_hr

    format_output(
        title="4. Busca Híbrida + Reranking (Cohere)",
        answer=answer_hr,
        docs=final_reranked_docs,
        latencies={
            "total": total_latency_hr,
            "etapas": {
                "Retrieval Híbrido (Ensemble)": latency_retrieval_hr,
                "Reranking (Cohere)": latency_rerank,
                "Geração LLM": latency_llm_hr,
            },
        },
    )

    print("\n" + "#" * 80 + "\n")
