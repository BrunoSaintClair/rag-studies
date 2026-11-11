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
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from data import documents  # Base com 26 documentos técnicos e metadados estruturados
from output_formatter import exibir_resultado


# Configuração dos Embeddings e Vector Store

embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2",
    google_api_key=GEMINI_API_KEY
)

vector_store = Chroma.from_documents(
    documents=documents,
    embedding=embedding_model
)


# 1. Retriever Vetorial Puro (Baseline Semântico sem Filtros)

vector_retriever = vector_store.as_retriever(search_kwargs={"k": 3})


# 2. Retriever Self-Querying (Filtro Estruturado de Metadados via LLM)

from typing import Dict
from langchain_classic.chains.query_constructor.base import AttributeInfo
from langchain_classic.chains.query_constructor.ir import Comparison
from langchain_classic.retrievers import SelfQueryRetriever
from langchain_community.query_constructors.chroma import ChromaTranslator
from langchain_google_genai import ChatGoogleGenerativeAI


class CustomChromaTranslator(ChromaTranslator):
    """Tradutor customizado para garantir coerção correta de tipos primitivos (ex: booleanos) no Chroma."""

    def visit_comparison(self, comparison: Comparison) -> Dict:
        val = comparison.value
        if isinstance(val, str):
            if val.lower() == "true":
                val = True
            elif val.lower() == "false":
                val = False
        return {
            comparison.attribute: {
                self._format_func(comparison.comparator): val
            }
        }


# Especificação dos metadados para que o LLM compreenda o Schema
metadata_field_info = [
    AttributeInfo(
        name="titulo",
        description="O título ou nome do material técnico",
        type="string",
    ),
    AttributeInfo(
        name="ano",
        description="O ano de publicação do material (ex: 2021, 2022, 2023, 2024)",
        type="integer",
    ),
    AttributeInfo(
        name="categoria",
        description="A categoria técnica do conteúdo (ex: 'Cloud & DevOps', 'Banco de Dados', 'Observabilidade', 'Segurança', 'IA & Machine Learning')",
        type="string",
    ),
    AttributeInfo(
        name="avaliacao",
        description="A nota média de avaliação técnica concedida pela comunidade (escala de 1.0 a 5.0)",
        type="float",
    ),
    AttributeInfo(
        name="nivel",
        description="O nível de profundidade técnica: 'iniciante', 'intermediario' ou 'avancado'",
        type="string",
    ),
    AttributeInfo(
        name="gratuito",
        description="Booleano indicando se o material é de acesso livre e gratuito (True) ou pago (False)",
        type="boolean",
    ),
    AttributeInfo(
        name="formato",
        description="O formato da publicação: 'artigo', 'tutorial', 'livro' ou 'curso'",
        type="string",
    ),
]

document_content_description = (
    "Resumos e conteúdos de artigos, tutoriais, livros e cursos sobre engenharia de software, "
    "computação em nuvem, bancos de dados, observabilidade, segurança e inteligência artificial."
)

query_llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=GEMINI_API_KEY
)

self_query_retriever = SelfQueryRetriever.from_llm(
    llm=query_llm,
    vectorstore=vector_store,
    document_contents=document_content_description,
    metadata_field_info=metadata_field_info,
    structured_query_translator=CustomChromaTranslator(),
    search_kwargs={"k": 3}
)


# Configuração do Prompt e Modelo de Geração (LLM)

from langchain_core.prompts import ChatPromptTemplate

template = """
Responda a pergunta baseado EXCLUSIVAMENTE no contexto a seguir:
{context}

Na resposta, não diga frases genéricas como "Com base no contexto fornecido...", apenas responda de maneira direta indicando os materiais recomendados e seus detalhes relevantes.

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
            f"Título: {meta.get('titulo')}\n"
            f"Ano: {meta.get('ano')} | Categoria: {meta.get('categoria')} | "
            f"Nível: {meta.get('nivel')} | Avaliação: {meta.get('avaliacao')} | "
            f"Gratuito: {'Sim' if meta.get('gratuito') else 'Não'} | Formato: {meta.get('formato')}\n"
            f"Resumo: {doc.page_content}"
        )
        blocos.append(bloco)
    return "\n\n---\n\n".join(blocos)


if __name__ == "__main__":
    pergunta = (
        "Recomende artigos avançados sobre otimização e caching em Kubernetes "
        "publicados a partir de 2023, gratuitos e com avaliação superior a 4.7."
    )

    # 1. Pipeline: Busca Vetorial
    # Recupera os textos mais próximos no espaço semântico, ignorando restrições lógicas e de metadados
    vector_docs = vector_retriever.invoke(pergunta)
    context_v = formatar_contexto(vector_docs)
    answer_v = chain.invoke({"context": context_v, "question": pergunta})

    exibir_resultado(
        titulo="1. Busca Vetorial Pura (Baseline - Sem Filtros de Metadados)",
        pergunta=pergunta,
        docs=vector_docs,
        resposta=answer_v,
    )

    # 2. Pipeline: Busca com Self Querying
    # O LLM desconstrói a pergunta em uma busca semântica + filtros booleanos/numéricos/categóricos
    self_query_docs = self_query_retriever.invoke(pergunta)
    context_sq = formatar_contexto(self_query_docs)
    answer_sq = chain.invoke({"context": context_sq, "question": pergunta})

    exibir_resultado(
        titulo="2. Busca com Self Querying (LLM + Filtro Estruturado de Metadados)",
        pergunta=pergunta,
        docs=self_query_docs,
        resposta=answer_sq,
    )
