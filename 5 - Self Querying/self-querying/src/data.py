"""
Definições e Parâmetros do Dataset para Self Querying:
- Quantidade total: 26 documentos técnicos estruturados.
- Domínio: Engenharia de Software, Cloud, Bancos de Dados, Observabilidade, Segurança e IA.
- Objetivo do Benchmark de Self Querying:
  Demonstrar a superioridade da busca vetorial filtrada por metadados contra a busca puramente semântica.
  
Campos de Metadados:
  * titulo (str): Nome do material técnico.
  * ano (int): Ano de publicação (2021 a 2024).
  * categoria (str): 'Cloud & DevOps', 'Banco de Dados', 'Observabilidade', 'Segurança', 'IA & Machine Learning'.
  * avaliacao (float): Avaliação da comunidade técnica (escala 1.0 a 5.0).
  * nivel (str): 'iniciante', 'intermediario', 'avancado'.
  * gratuito (bool): Se o material é de acesso livre (True) ou pago (False).
  * formato (str): 'artigo', 'tutorial', 'livro', 'curso'.

Cenário de Teste Típico:
  Pergunta: "Quero recomendações de artigos avançados sobre otimização e caching em Kubernetes publicados a partir de 2023, gratuitos e com avaliação superior a 4.7."
  - Target Gold (Doc 0): Cumpre todos os requisitos semânticos e todos os filtros de metadados.
  - Armadilha Semântica 1 (Doc 1): Idêntico semanticamente (caching e K8s), mas de 2021 (viola filtro ano >= 2023).
  - Armadilha Semântica 2 (Doc 2): Idêntico semanticamente, mas pago (gratuito=False) e avaliação 4.3 (viola filtros).
  - Armadilha de Metadados (Doc 3): Cumpre todos os filtros (2024, avancado, gratuito=True, avaliacao 4.9), mas é sobre Segurança/Criptografia (semântica irrelevante).
  - Documentos 4 a 25: Ampla cobertura técnica com distribuições variadas para testes compostos de AND, OR, >, <, ==.
"""

from langchain_core.documents import Document

documents = [
    # --- GRUPO 1: Benchmark Core (Target Gold vs Armadilhas Semânticas e de Metadados) ---
    Document(
        page_content=(
            "Guia aprofundado sobre estratégias de caching distribuído e otimização de latência "
            "em clusters Kubernetes de alta densidade. Abrange tuning do CoreDNS, políticas de cache "
            "com Redis Cluster multi-região e ajustes de kernel no nó Linux para mitigar throttling de CPU."
        ),
        metadata={
            "titulo": "Otimização Extrema de Latência e Cache em Kubernetes",
            "ano": 2023,
            "categoria": "Cloud & DevOps",
            "avaliacao": 4.9,
            "nivel": "avancado",
            "gratuito": True,
            "formato": "artigo",
        },
    ),
    Document(
        page_content=(
            "Técnicas de caching e mitigação de gargalos de rede em workloads Kubernetes. Aborda "
            "o uso de proxies sidecar Envoy e cache de DNS local em pods para reduzir a sobrecarga "
            "de resolução de serviços em microsserviços."
        ),
        metadata={
            "titulo": "Práticas de Caching e Otimização em Kubernetes Legado",
            "ano": 2021,  # Armadilha: semântica perfeita, mas publicado antes de 2023
            "categoria": "Cloud & DevOps",
            "avaliacao": 4.8,
            "nivel": "avancado",
            "gratuito": True,
            "formato": "artigo",
        },
    ),
    Document(
        page_content=(
            "Manual corporativo pago sobre escalabilidade, tuning e cache para pods Kubernetes "
            "em ambientes AWS EKS e Google GKE sob tráfego massivo de Black Friday."
        ),
        metadata={
            "titulo": "Masterclass Comercial de Tuning em Kubernetes",
            "ano": 2024,
            "categoria": "Cloud & DevOps",
            "avaliacao": 4.3,  # Armadilha: avaliação inferior a 4.7 e material pago
            "nivel": "avancado",
            "gratuito": False,
            "formato": "artigo",
        },
    ),
    Document(
        page_content=(
            "Fundamentos da criptografia pós-quântica e substituição de algoritmos RSA por "
            "esquemas baseados em reticulados (lattice-based cryptography) para proteção de infraestrutura bancária."
        ),
        metadata={
            "titulo": "Criptografia Pós-Quântica na Prática",
            "ano": 2024,
            "categoria": "Segurança",
            "avaliacao": 4.9,  # Armadilha: metadados idênticos ao filtro alvo, mas semântica totalmente diferente
            "nivel": "avancado",
            "gratuito": True,
            "formato": "artigo",
        },
    ),

    # --- GRUPO 2: Cloud & DevOps ---
    Document(
        page_content=(
            "Introdução prática ao Docker e containers para desenvolvedores iniciantes. "
            "Aprenda comandos básicos, criação de Dockerfile simples e conceitos fundamentais de isolamento de processos."
        ),
        metadata={
            "titulo": "Primeiros Passos com Docker e Contêineres",
            "ano": 2022,
            "categoria": "Cloud & DevOps",
            "avaliacao": 4.5,
            "nivel": "iniciante",
            "gratuito": True,
            "formato": "tutorial",
        },
    ),
    Document(
        page_content=(
            "Arquitetura declarativa de infraestrutura como código utilizando Terraform e OpenTofu. "
            "Gerenciamento de módulos reutilizáveis, backends remotos com state locking no DynamoDB e pipelines CI/CD."
        ),
        metadata={
            "titulo": "Infraestrutura como Código com Terraform Avançado",
            "ano": 2023,
            "categoria": "Cloud & DevOps",
            "avaliacao": 4.7,
            "nivel": "intermediario",
            "gratuito": False,
            "formato": "curso",
        },
    ),
    Document(
        page_content=(
            "Padrões de implantação contínua GitOps utilizando ArgoCD em múltiplos clusters Kubernetes. "
            "Sincronização automatizada, estratégias de rollouts com Canary e testes de regressão automatizados."
        ),
        metadata={
            "titulo": "GitOps em Escala com ArgoCD",
            "ano": 2024,
            "categoria": "Cloud & DevOps",
            "avaliacao": 4.8,
            "nivel": "avancado",
            "gratuito": True,
            "formato": "tutorial",
        },
    ),
    Document(
        page_content=(
            "Guia de bolso sobre automação de tarefas com GitHub Actions para repositórios open-source. "
            "Criação de matrizes de compilação, publicação em registries de pacotes e linting de código."
        ),
        metadata={
            "titulo": "Automação Eficiente com GitHub Actions",
            "ano": 2022,
            "categoria": "Cloud & DevOps",
            "avaliacao": 4.4,
            "nivel": "iniciante",
            "gratuito": True,
            "formato": "artigo",
        },
    ),

    # --- GRUPO 3: Bancos de Dados e Armazenamento ---
    Document(
        page_content=(
            "Tuning avançado de queries SQL e estratégias de indexação profunda no PostgreSQL. "
            "Uso de EXPLAIN ANALYZE, índices parciais, índices BRIN para tabelas bilionárias e particionamento declarativo."
        ),
        metadata={
            "titulo": "Engenharia de Performance com PostgreSQL",
            "ano": 2023,
            "categoria": "Banco de Dados",
            "avaliacao": 4.9,
            "nivel": "avancado",
            "gratuito": True,
            "formato": "artigo",
        },
    ),
    Document(
        page_content=(
            "Introdução aos modelos relacionais e sintaxe fundamental SQL para iniciantes. "
            "Criação de tabelas, consultas SELECT com JOINs simples e garantia de integridade referencial."
        ),
        metadata={
            "titulo": "SQL do Zero ao Primeiro Banco Relacional",
            "ano": 2021,
            "categoria": "Banco de Dados",
            "avaliacao": 4.3,
            "nivel": "iniciante",
            "gratuito": True,
            "formato": "tutorial",
        },
    ),
    Document(
        page_content=(
            "Arquitetura de dados orientada a documentos e modelagem no MongoDB. "
            "Desenho de coleções balanceando embedding vs referencing, estratégias de sharding e replica sets de alta disponibilidade."
        ),
        metadata={
            "titulo": "Modelagem e Escalabilidade no MongoDB",
            "ano": 2022,
            "categoria": "Banco de Dados",
            "avaliacao": 4.6,
            "nivel": "intermediario",
            "gratuito": False,
            "formato": "livro",
        },
    ),
    Document(
        page_content=(
            "Busca semântica vetorial e recuperação em escala no PostgreSQL utilizando a extensão pgvector. "
            "Comparativo de índices HNSW e IVFFlat, dimensionalidade de embeddings e cálculo de similaridade de cosseno."
        ),
        metadata={
            "titulo": "Bancos Vetoriais com PGVector e PostgreSQL",
            "ano": 2024,
            "categoria": "Banco de Dados",
            "avaliacao": 4.8,
            "nivel": "avancado",
            "gratuito": True,
            "formato": "artigo",
        },
    ),

    # --- GRUPO 4: Observabilidade e Monitoramento ---
    Document(
        page_content=(
            "Implementação de tracing distribuído de ponta a ponta em microsserviços com OpenTelemetry e Jaeger. "
            "Propagação de contexto W3C Trace Context, spans manuais e redução de sobrecarga com amostragem baseada em cauda."
        ),
        metadata={
            "titulo": "Tracing Distribuído Corporativo com OpenTelemetry",
            "ano": 2023,
            "categoria": "Observabilidade",
            "avaliacao": 4.8,
            "nivel": "avancado",
            "gratuito": True,
            "formato": "tutorial",
        },
    ),
    Document(
        page_content=(
            "Coleta e consolidação de métricas operacionais com Prometheus e Grafana para iniciantes. "
            "Configuração de exporters de sistema, montagem de dashboards interativos e alertas essenciais de uptime."
        ),
        metadata={
            "titulo": "Monitoramento Essencial com Prometheus e Grafana",
            "ano": 2021,
            "categoria": "Observabilidade",
            "avaliacao": 4.5,
            "nivel": "iniciante",
            "gratuito": True,
            "formato": "tutorial",
        },
    ),
    Document(
        page_content=(
            "Centralização eficiente de logs em Kubernetes utilizando Grafana Loki e Promtail. "
            "Estratégia de indexação por rótulos (labels) reduzindo custos de armazenamento em comparação ao Elasticsearch."
        ),
        metadata={
            "titulo": "Gestão de Logs Econômica com Grafana Loki",
            "ano": 2024,
            "categoria": "Observabilidade",
            "avaliacao": 4.7,
            "nivel": "intermediario",
            "gratuito": False,
            "formato": "curso",
        },
    ),
    Document(
        page_content=(
            "Observabilidade de baixo nível no kernel Linux utilizando eBPF. "
            "Rastreamento de chamadas de sistema, detecção de gargalos de I/O em disco e profiling contínuo sem instrumentação de código."
        ),
        metadata={
            "titulo": "Observabilidade Profunda do Kernel com eBPF",
            "ano": 2024,
            "categoria": "Observabilidade",
            "avaliacao": 4.9,
            "nivel": "avancado",
            "gratuito": True,
            "formato": "artigo",
        },
    ),

    # --- GRUPO 5: Segurança da Informação ---
    Document(
        page_content=(
            "Arquitetura Zero Trust em nuvem e gestão centralizada de segredos com HashiCorp Vault. "
            "Emissão dinâmica de credenciais efêmeras de banco, injeção de secrets em pods e integração com OIDC."
        ),
        metadata={
            "titulo": "Segurança Zero Trust com HashiCorp Vault",
            "ano": 2023,
            "categoria": "Segurança",
            "avaliacao": 4.8,
            "nivel": "avancado",
            "gratuito": False,
            "formato": "livro",
        },
    ),
    Document(
        page_content=(
            "Fundamentos de segurança em aplicações web baseados na lista OWASP Top 10. "
            "Prevenção contra SQL Injection, Cross-Site Scripting (XSS), boas práticas de sanitização e autenticação básica."
        ),
        metadata={
            "titulo": "Guia Defensivo OWASP Top 10 para Iniciantes",
            "ano": 2021,
            "categoria": "Segurança",
            "avaliacao": 4.6,
            "nivel": "iniciante",
            "gratuito": True,
            "formato": "tutorial",
        },
    ),
    Document(
        page_content=(
            "Segurança na esteira de software (DevSecOps): análise estática de código (SAST) "
            "e verificação contínua de vulnerabilidades em imagens de contêineres utilizando Trivy e SonarQube."
        ),
        metadata={
            "titulo": "DevSecOps: Protegendo a Supply Chain de Software",
            "ano": 2022,
            "categoria": "Segurança",
            "avaliacao": 4.4,
            "nivel": "intermediario",
            "gratuito": True,
            "formato": "artigo",
        },
    ),
    Document(
        page_content=(
            "Hardening avançado de nós e clusters Kubernetes em produção. "
            "Políticas de admissão com Kyverno, perfis Seccomp, AppArmor e isolamento de rede com Cilium Network Policies."
        ),
        metadata={
            "titulo": "Hardening Extremo de Segurança em Kubernetes",
            "ano": 2024,
            "categoria": "Segurança",
            "avaliacao": 4.9,
            "nivel": "avancado",
            "gratuito": True,
            "formato": "artigo",
        },
    ),

    # --- GRUPO 6: IA & Machine Learning ---
    Document(
        page_content=(
            "Engenharia de pipelines RAG (Retrieval-Augmented Generation) com modelos generativos. "
            "Estratégias de chunking semântico, modelos de embeddings multilíngues e conexão de bases de conhecimento externas."
        ),
        metadata={
            "titulo": "Construindo Sistemas RAG Corporativos",
            "ano": 2023,
            "categoria": "IA & Machine Learning",
            "avaliacao": 4.8,
            "nivel": "intermediario",
            "gratuito": True,
            "formato": "tutorial",
        },
    ),
    Document(
        page_content=(
            "Introdução aos modelos fundamentais de Deep Learning e visão computacional com PyTorch. "
            "Camadas convolucionais, funções de perda, otimizadores Adam e treino de redes em GPUs."
        ),
        metadata={
            "titulo": "Deep Learning com PyTorch para Iniciantes",
            "ano": 2022,
            "categoria": "IA & Machine Learning",
            "avaliacao": 4.5,
            "nivel": "iniciante",
            "gratuito": False,
            "formato": "curso",
        },
    ),
    Document(
        page_content=(
            "Técnicas de quantização e inferência de baixa latência para Large Language Models (LLMs). "
            "Uso de técnicas de quantização 4-bit (AWQ, GPTQ) e servidores vLLM com PagedAttention para alto throughput."
        ),
        metadata={
            "titulo": "Otimização e Servidão de LLMs em Alta Escala",
            "ano": 2024,
            "categoria": "IA & Machine Learning",
            "avaliacao": 4.9,
            "nivel": "avancado",
            "gratuito": True,
            "formato": "artigo",
        },
    ),
    Document(
        page_content=(
            "Fine-tuning eficiente de parâmetros (PEFT) utilizando LoRA e QLoRA em modelos abertos da família Llama. "
            "Ajuste supervisionado de instruções (SFT) e alinhamento com preferências humanas via DPO."
        ),
        metadata={
            "titulo": "Fine-Tuning com LoRA e DPO para Especialistas",
            "ano": 2023,
            "categoria": "IA & Machine Learning",
            "avaliacao": 4.7,
            "nivel": "avancado",
            "gratuito": False,
            "formato": "livro",
        },
    ),
    Document(
        page_content=(
            "Fundamentos da arquitetura Transformer: autoatenção (Self-Attention), encoders e decoders "
            "explicados passo a passo com intuição matemática e implementações em Python puro."
        ),
        metadata={
            "titulo": "Transformers por Dentro: Teoria e Código",
            "ano": 2022,
            "categoria": "IA & Machine Learning",
            "avaliacao": 4.7,
            "nivel": "intermediario",
            "gratuito": True,
            "formato": "artigo",
        },
    ),
    Document(
        page_content=(
            "Agentes autônomos inteligentes com LangGraph e ferramentas externas (Tool Calling). "
            "Fluxos com grafos de estados cíclicos, persistência de memória em sessões e recuperação de falhas operacionais."
        ),
        metadata={
            "titulo": "Desenvolvimento de Agentes com LangGraph",
            "ano": 2024,
            "categoria": "IA & Machine Learning",
            "avaliacao": 4.8,
            "nivel": "intermediario",
            "gratuito": True,
            "formato": "tutorial",
        },
    ),
]
