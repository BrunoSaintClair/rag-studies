# Configuração de Ambiente

import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")


# Coleta e separação dos dados

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from data import raw_data # Arquivo auxiliar contendo os textos usados nas buscas


text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50) # Os textos que temos seriam mais ou menos o tamanho de um chunk gerado a partir de um processamento, então, para não prejudicarmos muito a qualidade do resultado, vamos deixar o tamanho dos chunks maior que os dos textos em si, para salvarmos eles inteiros.

splits = text_splitter.create_documents(raw_data)

embedding_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2", google_api_key=GEMINI_API_KEY)
vector_store = Chroma.from_documents(documents=splits, embedding=embedding_model)
base_retriever = vector_store.as_retriever(search_kwargs={"k": 8})


# Configura Retriever de Rankeamento

from langchain_cohere import CohereRerank
from langchain_classic.retrievers import ContextualCompressionRetriever

SCORE_THRESHOLD = 0.5  # Limiar mínimo de relevância

compressor = CohereRerank(
    cohere_api_key=COHERE_API_KEY,
    model="rerank-multilingual-v3.0",
    top_n=3
)

rerank_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=base_retriever
)


# Realiza busca, rankeamento dos dados e coleta de dados temporais para análise

import time
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

question = "Como alimentar e cuidar de uma python em cativeiro?"

# --- Pipeline Sem Rankeamento ---
t0_retrieval = time.perf_counter()
without_rerank_docs = base_retriever.invoke(question)
latency_retrieval = time.perf_counter() - t0_retrieval

# --- Pipeline Com Rankeamento  ---
t0_rerank = time.perf_counter()
raw_reranked_docs = compressor.compress_documents(documents=without_rerank_docs, query=question)
reranked_docs = [
    doc for doc in raw_reranked_docs
    if (doc.metadata.get("relevance_score") or 0.0) >= SCORE_THRESHOLD
]
latency_rerank = time.perf_counter() - t0_rerank


# Geração das respostas

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

context_text_without_ranking = "\n\n".join(doc.page_content for doc in without_rerank_docs)
context_text_with_ranking = "\n\n".join(doc.page_content for doc in reranked_docs)

# Se quisesse apenas gerar as respostas, bastava fazer aqui algo como `answer_= chain.invoke({"context": context, "question": question})`
# O excesso de código escrito abaixo foi escrito para permitir uma análise de tempo e tokens gastos, além de uma bela formatação visual


# LLM Generation 1 (Sem rankeamento)
t0_llm_1 = time.perf_counter()
answer_1 = chain.invoke({"context": context_text_without_ranking, "question": question})
latency_llm_1 = time.perf_counter() - t0_llm_1
total_latency_1 = latency_retrieval + latency_llm_1

# LLM Generation 2 (Com rankeamento)
t0_llm_2 = time.perf_counter()
answer_2 = chain.invoke({"context": context_text_with_ranking, "question": question})
latency_llm_2 = time.perf_counter() - t0_llm_2
total_latency_2 = latency_retrieval + latency_rerank + latency_llm_2

from output_formatter import format_output

format_output(
    "Sem Rankeamento",
    answer_1,
    len(without_rerank_docs),
    {
        "total": total_latency_1,
        "etapas": {
            "Retrieval (Vetorial)": latency_retrieval,
            "Geração LLM": latency_llm_1,
        },
    },
)

format_output(
    "Com Rankeamento",
    answer_2,
    len(reranked_docs),
    {
        "total": total_latency_2,
        "etapas": {
            "Retrieval (Vetorial)": latency_retrieval,
            "Reranking (Cohere)": latency_rerank,
            "Geração LLM": latency_llm_2,
        },
    },
)
