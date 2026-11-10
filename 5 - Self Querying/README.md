# Busca por Metadados / Self Querying

O **Self Querying** é uma técnica de RAG que utiliza um modelo de linguagem (LLM) antes da etapa de recuperação vetorial para transformar uma pergunta em linguagem natural em duas partes fundamentais:

1. **Consulta Semântica (Semantic Query):** O texto limpo para ser comparado via similaridade vetorial (embeddings).
2. **Filtros Estruturados de Metadados (Metadata Filters):** Expressões lógicas (ex: `ano >= 2023`, `avaliacao > 4.5`, `categoria == 'Cloud & DevOps'`) aplicadas diretamente no banco vetorial.


## O Problema que Resolvemos

1. **Limitação da Busca Vetorial Pura:**
   - Modelos de embedding são excelentes para similaridade semântica de conceitos, mas são notoriamente ruins para lidar com restrições lógicas, numéricas e temporais (ex: "apenas após 2023", "avaliação acima de 4.8", "somente cursos gratuitos").
   - Em buscas convencionais com filtros no prompt, chunks antigos ou não gratuitos com alta proximidade semântica acabam ocupando o Top-K, descartando os resultados corretos.

2. **Limitação de Filtros Manuais Rígidos:**
   - Criar filtros manuais via código exige prever todas as possíveis variações e intenções da consulta do usuário.

3. **A Solução com Self Querying:**
   - O LLM analisa a pergunta do usuário e o schema de metadados disponíveis na coleção.
   - Ele extrai a intenção conceitual para o vetor e traduz as restrições explícitas ou implícitas em operadores de filtro nativos do banco de dados (ex: Chroma, Qdrant, Pinecone).
   - O banco vetorial executa uma busca híbrida real de **similaridade semântica restrita aos documentos que satisfazem o filtro**, garantindo precisão absoluta.


## Fluxo da Execução

```
                    [Pergunta do Usuário em Linguagem Natural]
             ("Artigos avançados de Cloud pós-2023 gratuitos com nota >= 4.8")
                                        │
                                        ▼
                             [LLM Query Constructor]
                                        │
                   ┌────────────────────┴────────────────────┐
                   ▼                                         ▼
         [Query Semântica Limpa]                  [Filtro Estruturado]
         "Cloud infraestrutura"          AND(ano >= 2023, nivel == 'avançado',
                                             gratuito == True, avaliacao >= 4.8)
                   │                                         │
                   └────────────────────┬────────────────────┘
                                        ▼
                   [Vector Store (ex: Chroma Filtered Search)]
                                        │
                                        ▼
                     [Documentos Recuperados Estritamente Válidos]
                                        │
                                        ▼
                           [LLM Geração de Resposta]
```


## Trade-offs

- **Vantagens:**
  - Elimina falsos positivos semânticos que violam regras lógicas, datas ou categorias.
  - Otimiza o contexto fornecido para o gerador, economizando tokens e reduzindo alucinações.
  - Alta flexibilidade para o usuário interagir usando linguagem natural sem formulários de busca complexos.

- **Desvantagens:**
  - Adiciona uma chamada preliminar de LLM para estruturar a query (latência e custo de tokens de input/output).
  - Depende da qualidade do prompt e da capacidade do LLM em gerar o filtro correto no dialeto do banco vetorial.
