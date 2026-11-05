chunks = [
    # Chunk 0: Semântico puro (Explica Circuit Breaker contra degradação de resposta e sobrecarga em microsserviços web, sem citar a palavra Resilience4j nem lentidão/saturação)
    "Em microsserviços web, a contenção de panes provocadas por sobrecarga extrema e degradação de resposta é assegurada pelo padrão Circuit Breaker, que isola temporariamente instâncias instáveis e bloqueia novas chamadas.",

    # Chunk 1: Armadilha léxica BM25 (Tem as palavras literais 'lentidão', 'saturação', 'requisições', mas sobre telefonia analógica antiga)
    "Relatório operacional de telefonia comutada: histórico de lentidão crônica e saturação de requisições em centrais telefônicas analógicas e linhas de discagem de pulsos por relés.",

    # Chunk 2: Léxico exato da biblioteca (Cita a biblioteca Java Resilience4j e Circuit Breaker)
    "A biblioteca Java Resilience4j disponibiliza implementações modulares de Circuit Breaker, rate limiter e retentativas exponenciais para proteção de código corporativo na JVM.",

    # Chunks adicionais de ecossistema de tecnologia, nuvem, IA e infraestrutura
    "O Kubernetes é a plataforma padrão da indústria para orquestração declarativa, escalabilidade automática e gerenciamento do ciclo de vida de contêineres.",
    "A Datadog centraliza observabilidade em nuvem através de métricas de infraestrutura, ingestão de logs e rastreamento distribuído de traces para microsserviços.",
    "O PostgreSQL moderno suporta busca semântica vetorial e armazenamento de representações densas em larga escala com a extensão pgvector e indexação HNSW.",
    "A OpenAI é pioneira em pesquisa de inteligência artificial generativa, desenvolvendo os modelos da família GPT, ChatGPT e APIs para geração multimodal.",
    "A Google é referência global em buscas na internet, publicidade digital e sistemas operacionais com o Android, além de atuar em nuvem com o Google Cloud e IA com a família Gemini.",
    "A Microsoft desenvolve soluções de software e nuvem corporativa com o Azure, criadora do Windows e Microsoft 365, com recursos de IA integrados à OpenAI.",
    "A Apple projeta dispositivos e hardware de consumo premium como iPhone, Mac e Apple Watch, integrados aos sistemas iOS e macOS com foco estrito em privacidade.",
    "A Amazon Web Services (AWS) é líder pioneira em infraestrutura de computação em nuvem distribuída, oferecendo instâncias escaláveis EC2 e armazenamento S3.",
    "A NVIDIA domina a fabricação de unidades de processamento gráfico (GPUs) como as arquiteturas Hopper e Blackwell, essenciais para treinamento e inferência de redes neurais.",
    "A Anthropic desenvolve os modelos Claude com foco prioritário em alinhamento constitucional, segurança de IA e processamento de contextos extremamente longos.",
    "A Meta lidera redes sociais globais como Instagram e WhatsApp, e fomenta o ecossistema de software de código aberto com a família de modelos de fundação Llama.",
    "O MongoDB é um banco de dados NoSQL orientado a documentos BSON, oferecendo esquema flexível, replicação por replica sets e particionamento horizontal via sharding.",
    "O Redis é um armazenamento de dados em memória de altíssimo desempenho, frequentemente utilizado para cache de baixa latência, filas de mensagens e sessões efêmeras.",
    "A Snowflake fornece uma plataforma de Data Cloud na nuvem com desacoplamento total entre armazenamento e computação para análise em larga escala com SQL.",
    "A Docker revolucionou a virtualização no nível do sistema operacional ao popularizar contêineres de software leves e reprodutíveis entre ambientes.",
    "O GitHub é a principal plataforma de desenvolvimento colaborativo e hospedagem de repositórios Git, integrando automação com GitHub Actions e CI/CD.",
    "A Cloudflare fornece proteção contra ataques DDoS, rede de entrega de conteúdo (CDN) distribuída globalmente e computação serverless na borda.",
    "A CrowdStrike protege endpoints empresariais e detecta invasões em tempo real aplicando inteligência artificial e telemetria na plataforma Falcon.",
    "O Stripe fornece APIs e infraestrutura financeira para pagamentos na internet, incluindo processamento de cartões de crédito, faturamento recorrente e prevenção a fraudes.",
    "O Spotify utiliza análise em tempo real de grandes volumes de dados de escuta e sistemas de recomendação baseados em filtragem colaborativa e aprendizado de máquina.",
    "O Apache Kafka implementa streaming de eventos em tempo real com arquitetura pub/sub de alta vazão e tolerância a falhas distribuída em partições e réplicas de tópicos.",
    "O CockroachDB e o TiDB são bancos de dados NewSQL distribuídos que fornecem consistência estrita ACID e tolerância a falhas através do algoritmo Raft."
]
