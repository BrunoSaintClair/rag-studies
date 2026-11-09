# Busca Híbrida + Reranking

Esta etapa combina o melhor dos dois mundos: a abrangência de recuperação da **Busca Híbrida** com a precisão do **Reranking**.


## O Problema que Resolvemos

1. **Busca Vetorial Isolada:** Excelente para capturar significado semântico e paráfrases, mas vulnerável a termos técnicos específicos, siglas, códigos e flags exatas.
2. **Busca por Palavra Exata (BM25) Isolada:** Ótima para palavras raras e literais, porém cega a contexto e sinônimos, frequentemente trazendo "armadilhas léxicas" (documentos que repetem palavras-chave em contextos irrelevantes).
3. **Busca Híbrida Isolada:** Maximiza a revocação (recall) unindo candidatos semânticos e léxicos, mas pode poluir o prompt com chunks distratores que tiveram match superficial.
4. **Busca Híbrida + Reranking:** A busca híbrida atua como uma rede ampla para recuperar os melhores candidatos potenciais, e o modelo de Reranking reavalia a interação cruzada entre a pergunta e cada texto, descartando ruídos e entregando apenas o contexto mais relevante para a LLM.


## Fluxo da Execução

```
[Pergunta do Usuário]
         │
         ├───► [Chroma (Busca Vetorial - k=4)] ──┐
         │                                        ├─► [Ensemble Retriever (~6-8 candidatos)]
         └───► [BM25 (Palavra Exata - k=4)]    ──┘
                                                              │
                                                              ▼
                                               [Cohere Rerank (Top 3, Score >= 0.5)]
                                                              │
                                                              ▼
                                              [Contexto Filtrado de Alta Relevância]
                                                              │
                                                              ▼
                                                   [Gemini LLM (Resposta Direta)]
```


## Trade-offs

- **Vantagens:** 
  - Máxima precisão e relevância nas respostas.
  - Eliminação de alucinações causadas por falsos positivos léxicos ou semânticos.
  - Economia de tokens de contexto na geração final pela LLM.
- **Desvantagens:**
  - Adiciona uma etapa extra de processamento (chamada à API do modelo de Reranking), aumentando a latência total em relação à busca pura.
