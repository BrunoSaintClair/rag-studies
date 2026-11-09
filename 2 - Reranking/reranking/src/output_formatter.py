from typing import Any
from langchain_core.documents import Document


def exibir_resultado(titulo: str, pergunta: str, docs: list[Document], resposta: Any) -> None:
    """Exibe no terminal de forma padronizada a pergunta, chunks usados e resposta final."""
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
