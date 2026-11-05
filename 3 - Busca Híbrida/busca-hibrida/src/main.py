# Configuração de Ambiente

import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# Coleta e separação dos dados
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from data import chunks # Arquivo auxiliar contendo os textos usados nas buscas


documents = [Document(page_content=chunk, metadata={"source": f"chunk_{i}"}) for i, chunk in enumerate(chunks)]

embedding_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2", google_api_key=GEMINI_API_KEY)
vector_store = Chroma.from_documents(documents=documents, embedding=embedding_model)
vector_retriever = vector_store.as_retriever(search_kwargs={"k": 2})


# Implementando Retriver de Busca por Palavra Exata
from langchain_community.retrievers import BM25Retriever 

bm25_retriever = BM25Retriever.from_documents(documents=documents, k=2)


# Implementando Retriver de Busca Híbrida
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


# Testes dos Retrievers e Geração com IA
def exibir_resultados(nome_retriever: str, resposta: str, docs: list[Document]) -> None:
    print(f"\n{'=' * 75}")
    print(f"🔹 {nome_retriever}")
    print(f"{'=' * 75}")
    print("\n💬 Resposta da IA:")
    print(resposta.strip())
    print("\n📄 Chunks Utilizados como Contexto:")
    if not docs:
        print("  Nenhum chunk retornado.")
    else:
        for i, doc in enumerate(docs, start=1):
            origem = doc.metadata.get("source", "N/A")
            print(f"\n  [{i}] ID: {origem}")
            print(f"      Texto: {doc.page_content}")


if __name__ == "__main__":
    pergunta = "Como resolver a lentidão e saturação de requisições em microsserviços web e qual biblioteca Java pode ser empregada?"

    print("\n" + "#" * 75)
    print(f"❓ Pergunta de Teste: \"{pergunta}\"")
    print("#" * 75)

    retrievers = {
        "Busca Vetorial (Chroma)": vector_retriever,
        "Busca por Palavra Exata (BM25)": bm25_retriever,
        "Busca Híbrida (Ensemble - Vetorial + BM25)": hybrid_search_retriever,
    }

    for nome, retriever in retrievers.items():
        docs = retriever.invoke(pergunta)
        context_text = "\n\n".join(doc.page_content for doc in docs)
        answer = chain.invoke({"context": context_text, "question": pergunta})
        exibir_resultados(nome, answer.text, docs)

    print("\n" + "#" * 75 + "\n")

