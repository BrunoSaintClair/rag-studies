from typing import Any
from langchain_core.documents import Document


def exibir_resultado(titulo: str, pergunta: str, docs: list[Document], resposta: Any = None) -> None:
    """Exibe no terminal de forma padronizada a pergunta, metadados dos chunks e resposta final."""
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
            metadados_str = ", ".join(f"{k}={v}" for k, v in doc.metadata.items())
            print(f"\n  [{i}] Metadados: {{{metadados_str}}}")
            print(f"      Texto ({len(doc.page_content)} caracteres):")
            print(f"      {doc.page_content}")

    if resposta is not None:
        resposta_texto = getattr(resposta, "text", str(resposta)).strip()
        print("\n💬 Resposta Final:")
        print(resposta_texto)

    print("=" * 80)
