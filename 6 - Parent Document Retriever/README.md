# Parent Document Retriever

O **Parent Document Retriever** é uma estratégia de RAG que desacopla a **unidade de recuperação vetorial (Child Chunk)** da **unidade de contexto entregue ao modelo gerador (Parent Document / Parent Chunk)**.


## O Dilema Fundamental do Tamanho de Chunk no RAG

Em qualquer pipeline de RAG convencional, a escolha do tamanho do chunk (`chunk_size`) impõe um dilema crítico de arquitetura:

| Estratégia Convencional | Comportamento na Busca Vetorial | Comportamento na Geração da LLM |
| :--- | :--- | :--- |
| **Chunks Pequenos** (ex: 150 a 300 caracteres) | **Alta precisão semântica:** o vetor representa um conceito pontual e altamente focado, com altíssima taxa de acerto em palavras-chave e termos técnicos. | **Contexto fragmentado:** a LLM não tem visibilidade das regras de contorno, exceções, cabeçalhos obrigatórios, fluxos de compensação ou parágrafos adjacentes. |
| **Chunks Grandes** (ex: 1.500 a 4.000 caracteres) | **Diluição semântica (Vector Averaging):** o vetor projeta a média de dezenas de tópicos distintos em um único ponto do espaço vetorial, degradando o ranking de similaridade para perguntas específicas. | **Contexto completo:** a LLM recebe o fluxo completo de instruções, mas o chunk frequentemente nem sequer é recuperado no Top-K. |

### A Solução com Parent Document Retriever

O **Parent Document Retriever** soluciona esse trade-off através de uma arquitetura de dois níveis:

1. **Indexação:** Os documentos são divididos em blocos pais (`parent_splitter`, ex: ~1.200 caracteres) e armazenados em um repositório de documentos (**Docstore**, ex: `InMemoryStore`).
2. **Subdivisão:** Cada bloco pai é subdividido em blocos filhos menores (`child_splitter`, ex: ~250 caracteres).
3. **Vetorização:** Apenas os blocos filhos são convertidos em embeddings e indexados no banco vetorial (**Chroma**), carregando um metadado com o ID do bloco pai correspondente.
4. **Recuperação e Resolução:** Quando uma consulta é realizada, a busca por similaridade é executada nos blocos filhos. Os IDs dos pais são extraídos, desduplicados e o retriever busca os blocos pais correspondentes no Docstore, entregando o contexto integral para a LLM.


## Modos de Operação

O LangChain suporta dois modos fundamentais para o `ParentDocumentRetriever`:

1. **Hierárquico / Chunks Maiores como Pais (Adotado neste módulo):**
   - Documentos longos são particionados em blocos pais intermediários (~1.000 a 2.000 caracteres) e cada pai é subdividido em filhos (~200 a 300 caracteres).
   - **Vantagem:** Evita saturar a janela de contexto da LLM e previne ruído ao recuperar apenas a seção ou capítulo relevante de manuais extensos.
2. **Full Documents como Pais:**
   - O documento original completo é mantido íntegro no Docstore (sem particionamento pai) e apenas os chunks filhos são indexados.
   - **Uso ideal:** Artigos curtos, e-mails, notas técnicas ou cards onde todo o documento é necessário sempre que qualquer trecho for mencionado.

