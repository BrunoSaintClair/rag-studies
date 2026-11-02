# Configuração de Ambiente

import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# 1 - Separando a base de dados em chunks

from langchain_text_splitters import RecursiveCharacterTextSplitter
from data import raw_data # Arquivo auxiliar contendo os textos usados nas buscas


text_splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=30) # O padrão da indústria costuma ser chunk_size entre 800 e 1200 caracteres (cerca de 150 a 250 tokens) com chunk_overlap de 10% a 15% (100 a 150 caracteres)
splits = text_splitter.create_documents(raw_data)


# 2 - Gerando embeddings e armazenando num banco de dados vetorial

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

embedding_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2", google_api_key=GEMINI_API_KEY)
vector_store = Chroma.from_documents(documents=splits, embedding=embedding_model)


# 3 - Busca dos dados (por padrão, o método abaixo realiza uma busca a partir do cálculo da Distância Euclidiana ao quadrado)

retrieved_docs = vector_store.similarity_search(query="Qual a velocidade da luz?", k=3)


# 4 - Geração da Resposta

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

context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)

answer = chain.invoke({"context": context_text, "question": "Qual a velocidade da luz?"})

print("Resposta para a pergunta 'Qual a velocidade da Luz?': \n\n" + answer.text)
