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


## Diferenças: Self-Querying vs. Query Expansion vs. Query Rewriting

Embora todas essas técnicas utilizem um LLM na etapa de **pré-recuperação (pre-retrieval)** para melhorar a qualidade dos documentos recuperados, cada uma atua em uma dimensão diferente do problema:

| Técnica | Objetivo Principal | O que o LLM gera (Saída) | Problema que Resolve |
| :--- | :--- | :--- | :--- |
| **Self-Querying** | Separar intenção semântica de restrições determinísticas. | **Query textual limpa + Filtro estruturado de metadados** (ex: JSON, sintaxe SQL/Chroma). | Falha da similaridade vetorial em respeitar regras lógicas, datas, categorias e limites numéricos. |
| **Query Expansion** | Aumentar a abrangência (recall) da busca trazendo múltiplos pontos de vista ou termos correlatos. | **Múltiplas variações textuais** da pergunta (Multi-Query, Sub-queries) ou **documento hipotético** (HyDE). | Vocabulário descompassado (palavras diferentes com mesmo sentido) e perguntas complexas multifacetadas. |
| **Query Rewriting** | Corrigir, desambiguar e contextualizar a pergunta original em uma versão única mais clara. | **Uma única query textual reescrita**, auto-contida e sem ruídos. | Perguntas ambíguas, cheias de jargão conversacional ou dependentes do histórico de chat (resolução de anáforas/co-referências). |

---

### Detalhamento das Abordagens

#### 1. Self-Querying (Busca Estruturada por Metadados)
- **Foco:** Tradução da linguagem natural em **filtros determinísticos de banco de dados**.
- **Exemplo:**
  - *Entrada:* "Quero cursos gratuitos de Python lançados em 2024 com nota maior que 4.5"
  - *Saída:*
    - **Query semântica:** `"cursos Python"`
    - **Filtro estruturado:** `AND(gratuito == True, ano == 2024, nota > 4.5)`
- **Uso ideal:** Coleções com metadados bem estruturados onde o usuário costuma impor condições explícitas ou implícitas de filtragem.

#### 2. Query Expansion (Expansão de Consulta)
- **Foco:** Diversificar a busca para **maximizar a taxa de recuperação (recall)**.
- **Abordagens comuns:**
  - **Multi-Query:** O LLM gera 3 a 5 reformulações da pergunta sob diferentes perspectivas, buscando vetores para cada uma e unificando os resultados.
  - **Sub-Question Decomposition:** Uma pergunta ampla é quebrada em sub-perguntas menores e mais fáceis de responder.
  - **HyDE (Hypothetical Document Embeddings):** O LLM gera uma resposta hipotética provável, e o vetor dessa resposta é usado para buscar trechos parecidos na base.
- **Exemplo:**
  - *Entrada:* "Como tratar erros de concorrência em Go?"
  - *Saída:*
    - Query 1: `"tratamento de race conditions em Golang"`
    - Query 2: `"uso de sync.Mutex e channels para concorrência em Go"`
    - Query 3: `"boas práticas de deadlocks e atomicidade em Go"`
- **Uso ideal:** Casos em que a pergunta do usuário é vaga, muito curta ou pode ter termos e sinônimos variados nos documentos.

#### 3. Query Rewriting (Reescrita / Reformulação de Consulta)
- **Foco:** Tornar a pergunta **auto-contida e sem ruído**, especialmente em interfaces conversacionais (chatbots).
- **Abordagens comuns:**
  - **Resolução de Co-referência / Anáforas:** Substituir pronomes e termos ambíguos pelo contexto do histórico prévio (ex: "E como eu instalo *ele*?" $\rightarrow$ "Como instalar o *Docker*?").
  - **Remoção de ruído conversacional:** Eliminar saudações e rodeios ("Olá, você poderia por gentileza me explicar...").
- **Exemplo:**
  - *Histórico:* "Qual é a diferença entre CPU e GPU?" $\rightarrow$ *Resposta do bot*
  - *Pergunta atual do usuário:* "Qual deles é melhor para treinar LLMs?"
  - *Saída Reescrita:* `"Comparativo entre CPU e GPU para treinamento de Large Language Models"`
- **Uso ideal:** Aplicações de chat multi-turn onde consultas subsequentes dependem criticamente do contexto anterior.

---

### Podem ser combinadas?
**Sim.** Em pipelines RAG avançados, essas técnicas frequentemente trabalham juntas em cascata:
1. **Query Rewriting:** Resolve pronomes e histórico de chat, gerando uma consulta clara.
2. **Self-Querying:** Analisa a consulta reescrita, extrai os filtros de metadados e isola a query semântica.
3. **Query Expansion (opcional):** Gera variações da query semântica para buscar no banco vetorial mantendo o mesmo filtro estruturado aplicado.
