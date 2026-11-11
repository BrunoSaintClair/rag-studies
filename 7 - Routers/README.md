# Routers (Semantic Router vs LLM Router)

O **roteamento de consultas** analisa a intenção da pergunta do usuário antes da busca vetorial, decidindo para qual base de dados direcioná-la ou se responde direto (sem gastar chamadas no ChromaDB).

## Abordagens

- **Semantic Router:** Compara o embedding da pergunta com vetores de frases-âncora pré-indexadas via similaridade de cosseno. Se a similaridade for menor que o limiar, cai no fallback.
- **LLM Router:** Usa a LLM com Structured Output (`Pydantic`) para classificar a rota de forma determinística a partir de um schema de literais.

## Trade-offs

| Roteador | Vantagens | Desvantagens |
| :--- | :--- | :--- |
| **Semantic Router** | Latência muito baixa (~450ms) e custo zero de tokens de geração. | Mais sensível à escolha das âncoras e requer calibração de limiar. |
| **LLM Router** | Alta capacidade de interpretação contextual e desambiguação. | Maior latência (~1s a 2s) e consome tokens de LLM a cada chamada. |
