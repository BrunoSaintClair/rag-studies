# Configuração de Ambiente

import os
from typing import Any
from dotenv import load_dotenv
from langchain_core.documents import Document

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")


# Coleta e separação dos dados

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from data import raw_data  # Arquivo auxiliar contendo os textos usados nas buscas


text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)  # Os textos que temos seriam mais ou menos o tamanho de um chunk gerado a partir de um processamento, então, para não prejudicarmos muito a qualidade do resultado, vamos deixar o tamanho dos chunks maior que os dos textos em si, para salvarmos eles inteiros.

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


# Geração das respostas

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
    question = "Como alimentar e cuidar de uma python em cativeiro?"

    # --- Pipeline Sem Rankeamento ---
    without_rerank_docs = base_retriever.invoke(question)
    context_text_without_ranking = "\n\n".join(doc.page_content for doc in without_rerank_docs)
    answer_1 = chain.invoke({"context": context_text_without_ranking, "question": question})

    exibir_resultado(
        titulo="Sem Rankeamento",
        pergunta=question,
        docs=without_rerank_docs,
        resposta=answer_1,
    )

    # --- Pipeline Com Rankeamento ---
    raw_reranked_docs = compressor.compress_documents(documents=without_rerank_docs, query=question)
    reranked_docs = [
        doc for doc in raw_reranked_docs
        if (doc.metadata.get("relevance_score") or 0.0) >= SCORE_THRESHOLD
    ]
    context_text_with_ranking = "\n\n".join(doc.page_content for doc in reranked_docs)
    answer_2 = chain.invoke({"context": context_text_with_ranking, "question": question})

    exibir_resultado(
        titulo="Com Rankeamento",
        pergunta=question,
        docs=reranked_docs,
        resposta=answer_2,
    )
