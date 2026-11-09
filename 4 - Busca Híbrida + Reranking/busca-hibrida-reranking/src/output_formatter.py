"""
Formatador de saída para exibição padronizada dos resultados no terminal.
Exibe resposta da IA, chunks selecionados (com ID e score de relevância, se houver)
e métricas de latência e consumo de tokens.
"""

from typing import Any
from langchain_core.documents import Document


def format_output(
    title: str,
    answer: Any,
    docs: list[Document],
    latencies: dict[str, Any],
) -> None:
    """Formata e exibe no terminal os resultados, chunks, latências e tokens."""
    # Extração de tokens de uso
    usage = getattr(answer, "usage_metadata", {}) or {}
    input_tokens = (
        usage.get("input_tokens", 0)
        if isinstance(usage, dict)
        else getattr(usage, "input_tokens", 0)
    )
    output_tokens = (
        usage.get("output_tokens", 0)
        if isinstance(usage, dict)
        else getattr(usage, "output_tokens", 0)
    )
    total_tokens = (
        usage.get("total_tokens", 0)
        if isinstance(usage, dict)
        else getattr(usage, "total_tokens", 0)
    )

    answer_text = getattr(answer, "text", str(answer)).strip()

    print("\n" + "=" * 80)
    print(f"📌 {title.upper()}")
    print("=" * 80)

    print("\n💬 Resposta da IA:")
    print(answer_text)

    print(f"\n📄 Chunks Utilizados como Contexto ({len(docs)}):")
    if not docs:
        print("  Nenhum chunk retornado.")
    else:
        for i, doc in enumerate(docs, start=1):
            origem = doc.metadata.get("source", "N/A")
            score = doc.metadata.get("relevance_score")
            score_info = f" | Relevância: {score:.4f}" if score is not None else ""
            print(f"\n  [{i}] ID: {origem}{score_info}")
            print(f"      Texto: {doc.page_content}")

    print("\n📊 Métricas de Execução:")
    print(f"  • Quantidade de Chunks: {len(docs)}")
    print(f"  • Latência Total:       {latencies.get('total', 0.0):.2f}s")
    for step_name, step_latency in latencies.get("etapas", {}).items():
        print(f"      ↳ {step_name}: {step_latency:.2f}s")
    print(f"  • Tokens Input:         {input_tokens}")
    print(f"  • Tokens Output:        {output_tokens}")
    print(f"  • Tokens Total:         {total_tokens}")
    print("=" * 80)
