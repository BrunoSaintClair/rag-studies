import os
import sys
import time
import warnings
from typing import Literal
import numpy as np
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from output_formatter import (
    exibir_cabecalho,
    exibir_resultado_comparativo,
    exibir_rodape,
)

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# ============================================================================
# 1. ROTEADOR COM LLM (Structured Output com Pydantic)
# ============================================================================

class DecisaoRota(BaseModel):
    destino: Literal["chroma_financeiro", "chroma_suporte", "conversa_geral"] = Field(
        description="Escolha a base de dados correta com base na intenção da pergunta, ou 'conversa_geral' para outros assuntos."
    )


llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=GEMINI_API_KEY,
)
roteador_llm = llm.with_structured_output(DecisaoRota)


def executar_roteador_llm(pergunta: str) -> tuple[str, float]:
    """Classifica a consulta usando LLM e Structured Output, medindo o tempo."""
    inicio = time.perf_counter()
    decisao: DecisaoRota = roteador_llm.invoke(
        f"Classifique para qual rota esta mensagem deve ir: {pergunta}"
    )
    latencia_ms = (time.perf_counter() - inicio) * 1000.0
    return decisao.destino, latencia_ms


# ============================================================================
# 2. ROTEADOR SEMÂNTICO (Embeddings + Similaridade de Cosseno)
# ============================================================================

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2",
    google_api_key=GEMINI_API_KEY,
)

# Exemplos representativos (âncoras) de cada rota cadastrados na inicialização
rotas_exemplos = {
    "chroma_financeiro": [
        "Qual a multa de cancelamento do contrato?",
        "Como pedir reembolso ou segunda via de boleto?",
        "Qual o valor da mensalidade do plano Pro?",
        "Minha fatura veio com cobrança indevida",
    ],
    "chroma_suporte": [
        "O sistema está dando erro 500 na tela de login",
        "Como configurar a integração via API e token?",
        "Não consigo redefinir minha senha de acesso",
        "O aplicativo fecha sozinho ao clicar em exportar arquivo",
    ],
}

# Vetoriza os exemplos uma única vez na inicialização do sistema
print("Indexando exemplos das rotas para o Roteador Semântico...")
vetores_rotas = {
    nome: embeddings.embed_documents(frases)
    for nome, frases in rotas_exemplos.items()
}


def executar_roteador_semantico(pergunta: str, limiar: float = 0.65) -> tuple[str, float, float]:
    """Classifica a consulta via produto escalar (cosseno) contra os vetores pré-indexados."""
    inicio = time.perf_counter()
    vetor_pergunta = embeddings.embed_query(pergunta)

    melhor_rota = "conversa_geral"
    maior_score = -1.0

    for nome_rota, matriz_vetores in vetores_rotas.items():
        # Produto escalar entre matriz de vetores normalizados e o vetor da pergunta
        scores = np.dot(matriz_vetores, vetor_pergunta)
        max_score_rota = float(np.max(scores))

        if max_score_rota > maior_score:
            maior_score = max_score_rota
            melhor_rota = nome_rota

    latencia_ms = (time.perf_counter() - inicio) * 1000.0
    destino_final = melhor_rota if maior_score >= limiar else "conversa_geral"
    return destino_final, maior_score, latencia_ms


# ============================================================================
# 3. EXECUÇÃO COMPARATIVA
# ============================================================================

if __name__ == "__main__":
    perguntas_teste = [
        "Meu aplicativo fecha sozinho quando clico em exportar PDF.",
        "Quero a 2ª via da minha fatura que venceu ontem.",
        "Como gerar uma chave de API para integrar com meu sistema?",
        "Qual é a receita tradicional de bolo de cenoura com cobertura de chocolate?",
    ]

    exibir_cabecalho()

    for i, pergunta in enumerate(perguntas_teste, start=1):
        rota_sem, score_sem, tempo_sem = executar_roteador_semantico(pergunta)
        rota_llm, tempo_llm = executar_roteador_llm(pergunta)

        exibir_resultado_comparativo(
            indice=i,
            pergunta=pergunta,
            rota_semantico=rota_sem,
            score_semantico=score_sem,
            tempo_semantico_ms=tempo_sem,
            rota_llm=rota_llm,
            tempo_llm_ms=tempo_llm,
        )

    exibir_rodape()
