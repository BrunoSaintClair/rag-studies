# Arquivo 100% gerado por IA

def format_output(title: str, answer, doc_count: int, latencies: dict) -> None:
    """Formata e exibe no terminal a resposta, contagem de documentos, latências e tokens."""
    usage = getattr(answer, "usage_metadata", {}) or {}
    input_tokens = usage.get("input_tokens", 0) if isinstance(usage, dict) else getattr(usage, "input_tokens", 0)
    output_tokens = usage.get("output_tokens", 0) if isinstance(usage, dict) else getattr(usage, "output_tokens", 0)
    total_tokens = usage.get("total_tokens", 0) if isinstance(usage, dict) else getattr(usage, "total_tokens", 0)

    print("=" * 80)
    print(f"📌 {title.upper()}")
    print("=" * 80)
    print("\n💬 Resposta:")
    print(getattr(answer, "text", str(answer)).strip())
    print("\n📊 Métricas:")
    print(f"  • Documentos:      {doc_count}")
    print(f"  • Latência Total:  {latencies['total']:.2f}s")
    for step_name, step_latency in latencies.get("etapas", {}).items():
        print(f"      ↳ {step_name}: {step_latency:.2f}s")
    print(f"  • Tokens Input:    {input_tokens}")
    print(f"  • Tokens Output:   {output_tokens}")
    print(f"  • Tokens Total:    {total_tokens}")
    print("=" * 80 + "\n")
