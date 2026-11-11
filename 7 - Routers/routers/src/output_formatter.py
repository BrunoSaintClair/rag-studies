"""Formatador visual para exibição dos resultados de roteamento no terminal."""


def simular_direcionamento(destino: str) -> str:
    """Simula a ação tomada na aplicação conforme a rota escolhida."""
    if destino == "chroma_suporte":
        return "-> Direciona para o Retriever da coleção de Suporte Técnico + Reranker"
    elif destino == "chroma_financeiro":
        return "-> Direciona para o Retriever da coleção de Financeiro/Faturas + Reranker"
    else:
        return "-> Responde direto com Gemini (Sem consulta vetorial / Sem gastar ChromaDB)"


def exibir_cabecalho() -> None:
    """Exibe o cabeçalho inicial do benchmark comparativo."""
    print("\n" + "=" * 80)
    print("      COMPARAÇÃO: SEMANTIC ROUTER vs LLM ROUTER (STRUCTURED OUTPUT)")
    print("=" * 80)


def exibir_resultado_comparativo(
    indice: int,
    pergunta: str,
    rota_semantico: str,
    score_semantico: float,
    tempo_semantico_ms: float,
    rota_llm: str,
    tempo_llm_ms: float,
) -> None:
    """Exibe no terminal a comparação detalhada entre o Roteador Semântico e o Roteador LLM."""
    print(f"\n[{indice}] Pergunta: \"{pergunta}\"")
    print(
        f"  • Roteador Semântico : '{rota_semantico}' "
        f"(Tempo: {tempo_semantico_ms:.1f}ms | Score: {score_semantico:.4f})"
    )
    print(
        f"  • Roteador LLM       : '{rota_llm}' "
        f"(Tempo: {tempo_llm_ms:.1f}ms)"
    )
    print(f"  • Ação no Sistema    : {simular_direcionamento(rota_llm)}")


def exibir_rodape() -> None:
    """Exibe a linha de fechamento da exibição."""
    print("\n" + "=" * 80 + "\n")
