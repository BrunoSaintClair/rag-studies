from langchain_core.documents import Document

documents = [
    Document(
        page_content=(
            "### Seção 1: Resiliência e Idempotência na API de Pagamentos e Checkout\n\n"
            "Em chamadas síncronas à API de Checkout que resultem em erro HTTP 504 Gateway Timeout "
            "ou HTTP 502 Bad Gateway, o cliente HTTP deve aplicar política de retentativa com no máximo "
            "3 tentativas e backoff exponencial com jitter (intervalos base de 1s, 2s e 4s).\n\n"
            "Para qualquer retentativa de pagamento, é estritamente obrigatório o envio do cabeçalho "
            "HTTP 'X-Idempotency-Key' contendo um identificador UUIDv4 único gerado na requisição inicial. "
            "O gateway de pagamento e os microsserviços utilizam essa chave armazenada em Redis Cluster com "
            "TTL de 24 horas para garantir que transações já processadas não sejam cobradas em duplicidade.\n\n"
            "Caso todas as 3 tentativas de retentativa se esgotem persistindo o código HTTP 504, o cliente "
            "não deve descartar a transação nem retornar falha genérica ao usuário. O payload completo da "
            "operação deve ser encaminhado para a Dead Letter Queue (DLQ) 'payment-failures-dlq' e acionada "
            "imediatamente a saga de compensação contábil via orquestrador de transações (Temporal/Camunda) "
            "para estornar a reserva de limite do cliente no Ledger Financeiro e emitir evento de alerta de infraestrutura."
        ),
        metadata={
            "modulo": "pagamentos",
            "dominio": "checkout-resilience",
            "versao": "2.4",
            "tipo_documento": "manual_arquitetura",
            "autor": "Equipe de Arquitetura Transacional",
        },
    ),
    Document(
        page_content=(
            "### Seção 2: Governança de Tráfego e Rate Limiting no API Gateway\n\n"
            "O API Gateway corporativo aplica controle de fluxo baseado no algoritmo Token Bucket para proteger "
            "os microsserviços contra sobrecarga e ataques de negação de serviço distribuídos (DDoS).\n\n"
            "Os limites operacionais são definidos por categorias de clientes: Tier Gold possui cota de 5.000 req/min "
            "com burst máximo de 10.000 requisições; Tier Silver possui cota de 1.000 req/min com burst de 2.000 requisições; "
            "e Tier Bronze possui limite rígido de 200 req/min sem capacidade de burst permitida.\n\n"
            "Todas as respostas HTTP do gateway incluem obrigatoriamente os headers 'X-RateLimit-Limit', "
            "'X-RateLimit-Remaining' e 'X-RateLimit-Reset'. Ao exceder a cota contratada, o gateway responde com o "
            "código HTTP 429 Too Many Requests acompanhado do cabeçalho 'Retry-After' em segundos. Clientes que violarem "
            "o limite de 429 por mais de 5 janelas consecutivas sofrem bloqueio temporário (quarentena) de 15 minutos via IP."
        ),
        metadata={
            "modulo": "gateway",
            "dominio": "traffic-management",
            "versao": "1.9",
            "tipo_documento": "manual_arquitetura",
            "autor": "Equipe de Plataforma e Gateway",
        },
    ),
    Document(
        page_content=(
            "### Seção 3: Padrões de Mensageria Event-Driven com Apache Kafka e Outbox\n\n"
            "Para assegurar consistência eventual entre bancos relacionais e brokers de mensagens, todos os serviços "
            "produtores devem implementar o padrão Transactional Outbox com captura de dados via Debezium CDC no PostgreSQL.\n\n"
            "A publicação direta de eventos a partir da camada de aplicação sem transação com o banco de dados é proibida. "
            "As mensagens devem ser particionadas estritamente pela chave de negócio 'order_id' ou 'customer_id', garantindo "
            "que todos os eventos de um mesmo ciclo de vida sejam consumidos em ordem cronológica estrita pela partição correspondente.\n\n"
            "Os tópicos críticos devem ser configurados com fator de replicação mínimo de 3 réplicas e parâmetro de produtor "
            "'acks=all' combinado com 'min.insync.replicas=2'. Em caso de mensagens malformadas que provoquem exceção de desserialização "
            "(poison pills), o consumidor deve rotear o registro para o Dead Letter Topic 'orders-poison-pill-dlt' após 3 falhas, "
            "evitando o travamento do consumer group e registrando o erro no APM."
        ),
        metadata={
            "modulo": "mensageria",
            "dominio": "event-driven",
            "versao": "3.1",
            "tipo_documento": "manual_arquitetura",
            "autor": "Equipe de Engenharia de Dados e Mensageria",
        },
    ),
    Document(
        page_content=(
            "### Seção 4: Segurança Zero-Trust e Autenticação Inter-Microsserviços\n\n"
            "Toda comunicação inter-serviços na malha (Service Mesh) utiliza criptografia mTLS obrigatória com certificados "
            "X.509 de curta duração (validade máxima de 12 horas) gerados e rotacionados automaticamente pelo SPIFFE/SPIRE.\n\n"
            "Além da camada de transporte mTLS, cada requisição HTTP/gRPC deve carregar no header 'Authorization' um Bearer Token "
            "JWT assinado com algoritmo assimétrico Ed25519 pela autoridade central de identidade do cluster. "
            "As claims obrigatórias do token incluem 'iss' (emissor), 'sub' (identidade da conta de serviço) e 'scope' (permissões granularizadas).\n\n"
            "A propagação de contexto de rastreabilidade distribuída deve seguir o padrão W3C TraceContext com os cabeçalhos "
            "'traceparent' e 'tracestate'. É terminantemente vetada a gravação de dados pessoais sensíveis (PII) e dados de cartão "
            "(PCI-DSS) nos logs ou headers de rastreio, aplicando-se obrigatoriamente filtros de máscara antes da ingestão no OpenSearch."
        ),
        metadata={
            "modulo": "seguranca",
            "dominio": "zero-trust",
            "versao": "2.0",
            "tipo_documento": "manual_arquitetura",
            "autor": "Equipe de Segurança da Informação",
        },
    ),
    Document(
        page_content=(
            "### Seção 5: Resiliência de Comunicação com Circuit Breaker e Fallback\n\n"
            "Chamadas síncronas para dependências externas ou microsserviços legados devem ser encapsuladas pelo padrão "
            "Circuit Breaker (implementado via biblioteca Resilience4j ou proxy sidecar Envoy).\n\n"
            "O disjuntor opera com base em uma janela deslizante baseada em contagem configurada para as últimas 100 requisições. "
            "Se a taxa de erros (HTTP 5xx ou timeouts superiores a 2.500ms) ultrapassar o limiar de tolerância de 50%, "
            "o circuito transiciona imediatamente do estado CLOSED para o estado OPEN.\n\n"
            "Durante o estado OPEN, todas as chamadas recebem rejeição imediata com exceção 'CallNotPermittedException' sem onerar "
            "o serviço de destino, e o sistema deve invocar a rotina de fallback retornando resposta degradada pré-computada "
            "armazenada em cache local em memória (Caffeine). O tempo de permanência no estado OPEN é de 30 segundos, após o qual o "
            "circuito entra no estado HALF-OPEN permitindo 10 chamadas de sondagem para testar a recuperação do serviço dependente."
        ),
        metadata={
            "modulo": "resiliencia",
            "dominio": "circuit-breaker",
            "versao": "1.7",
            "tipo_documento": "manual_arquitetura",
            "autor": "Equipe de Arquitetura e SRE",
        },
    ),
    Document(
        page_content=(
            "### Seção 6: Cache Distribuído Multi-Camadas e Mitigação de Stampede\n\n"
            "A estratégia de aceleração de leitura em microsserviços com alto volume de consultas adota arquitetura de cache em "
            "duas camadas: Camada L1 em memória no processo da aplicação (Caffeine) com TTL de 60 segundos, e Camada L2 compartilhada "
            "em cluster Redis com TTL padrão de 30 minutos.\n\n"
            "Para evitar o fenômeno de Cache Stampede (degradação massiva causada pela expiração simultânea de chaves de altíssimo acesso), "
            "a aplicação implementa o algoritmo probabilístico XFetch para recomputação em background antes do vencimento real da chave, "
            "além de utilizar locks distribuídos com Redlock no Redis para garantir que apenas uma réplica recarregue a fonte de dados primária.\n\n"
            "A sincronização e invalidação do cache em caso de escrita ou mutação de dados é disparada de forma orientada a eventos "
            "através de mensagens de invalidação publicadas no tópico Kafka 'cache-invalidation-events', garantindo que todos os pods "
            "descartem seus registros locais L1 em menos de 200 milissegundos após o commit no banco relacional."
        ),
        metadata={
            "modulo": "caching",
            "dominio": "distributed-cache",
            "versao": "2.2",
            "tipo_documento": "manual_arquitetura",
            "autor": "Equipe de Performance e Escalabilidade",
        },
    ),
]
