# Configuração de Ambiente

import os
import warnings
from dotenv import load_dotenv

# Silencia avisos de depreciação do ecossistema LangChain
warnings.filterwarnings("ignore", category=DeprecationWarning)

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# Coleta e Separação dos Dados

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.stores import InMemoryStore
from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_core.prompts import ChatPromptTemplate
from data import documents
from output_formatter import exibir_resultado


# Configuração dos Modelos e Splitters

embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2",
    google_api_key=GEMINI_API_KEY
)

# Chunks Pais: Preservam o contexto macro da seção técnica com regras, exceções e governança
parent_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=150
)

# Chunks Filhos: Trechos pequenos e especializados para indexação vetorial de alta precisão semântica
child_splitter = RecursiveCharacterTextSplitter(
    chunk_size=250,
    chunk_overlap=40
)


# 1. Pipeline RAG Convencional (Baseline: Indexação e Recuperação de Chunks Pequenos)
# O modelo vetorial busca e entrega apenas os fragmentos curtos para o gerador

small_chunks = child_splitter.split_documents(documents)
vector_store_convencional = Chroma.from_documents(
    documents=small_chunks,
    embedding=embedding_model,
    collection_name="convencional_small_chunks"
)
convencional_retriever = vector_store_convencional.as_retriever(search_kwargs={"k": 2})


# 2. Pipeline Parent Document Retriever (Hierárquico: Vetores em Chunks Filhos + Armazenamento de Chunks Pais)
# A busca vetorial localiza os fragmentos filhos específicos, mas o retriever devolve o bloco pai integral do Docstore

docstore = InMemoryStore()
vector_store_parent = Chroma(
    collection_name="parent_child_chunks",
    embedding_function=embedding_model
)

parent_retriever = ParentDocumentRetriever(
    vectorstore=vector_store_parent,
    docstore=docstore,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
    search_kwargs={"k": 2}
)

# Ingestão hierárquica dos manuais no docstore e no vectorstore
parent_retriever.add_documents(documents, ids=None)


# Configuração do Prompt e Modelo de Geração (LLM)

template = """
Responda a pergunta baseado EXCLUSIVAMENTE no contexto a seguir:
{context}

Na resposta, não diga frases genéricas como "Com base no contexto fornecido...", apenas responda de maneira direta e completa destacando os requisitos técnicos, regras obrigatórias e procedimentos operacionais necessários.

Pergunta:
{question}
"""

prompt = ChatPromptTemplate.from_template(template=template)
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", google_api_key=GEMINI_API_KEY)
chain = prompt | llm


def formatar_contexto(docs: list[Document]) -> str:
    """Formata os documentos recuperados incluindo metadados e conteúdo para a LLM."""
    blocos = []
    for doc in docs:
        meta = doc.metadata
        bloco = (
            f"Módulo: {meta.get('modulo', 'N/A')} | Domínio: {meta.get('dominio', 'N/A')} | "
            f"Versão: {meta.get('versao', 'N/A')} | Tipo: {meta.get('tipo_documento', 'N/A')}\n"
            f"Conteúdo:\n{doc.page_content}"
        )
        blocos.append(bloco)
    return "\n\n---\n\n".join(blocos)


# Execução Comparativa das Abordagens de RAG

if __name__ == "__main__":
    pergunta = (
        "Em caso de erro HTTP 504 Gateway Timeout na API de pagamentos, quais são as regras de retentativa, "
        "que cabeçalho obrigatório deve ser enviado para garantir consistência e qual o procedimento completo "
        "caso as tentativas se esgotem?"
    )

    # 1. Pipeline: RAG Convencional (Chunks Pequenos)
    # Recupera apenas os trechos curtos correspondentes ao match vetorial.
    docs_convencional = convencional_retriever.invoke(pergunta)
    context_convencional = formatar_contexto(docs_convencional)
    resposta_convencional = chain.invoke({"context": context_convencional, "question": pergunta})

    exibir_resultado(
        titulo="1. RAG Convencional (Chunks Pequenos - Perda de Contexto Amplo)",
        pergunta=pergunta,
        docs=docs_convencional,
        resposta=resposta_convencional,
    )

    # 2. Pipeline: Parent Document Retriever (Hierárquico)
    # Busca com granularidade fina via chunks filhos, mas recupera o bloco pai completo do InMemoryStore.
    docs_parent = parent_retriever.invoke(pergunta)
    context_parent = formatar_contexto(docs_parent)
    resposta_parent = chain.invoke({"context": context_parent, "question": pergunta})

    exibir_resultado(
        titulo="2. Parent Document Retriever (Busca em Filhos + Contexto Completo dos Pais)",
        pergunta=pergunta,
        docs=docs_parent,
        resposta=resposta_parent,
    )
