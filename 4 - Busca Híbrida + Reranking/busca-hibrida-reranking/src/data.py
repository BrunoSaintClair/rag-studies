"""
Definições e Parâmetros do Dataset:
- Quantidade total: 50 textos.
- Domínio: Engenharia de Software, Cloud, Infraestrutura, CI/CD, Contêineres e Observabilidade.
- Objetivo do Benchmark: Demonstrar o valor combinado de Busca Híbrida + Reranking.
  * O Target Gold (chunk 0) contém a solução específica para 'Docker BuildKit com cache remoto inline em CI/CD'.
  * Armadilhas léxicas (chunks 1, 2, 5) têm termos literais coincidentes ('BuildKit', 'cache remoto inline', 'banda', 'builds'), mas contextos errados (cache local efêmero, web CSS/CDN ou hardware de CPU).
  * Armadilhas semânticas (chunks 3, 4, 6, 10) discutem aceleração de builds, imagens leves, CI/CD e caching, mas não respondem à pergunta sobre BuildKit com cache remoto inline.
  * Chunks 7 a 49 compõem um corpus realista de infraestrutura corporativa (K8s, Kafka, PostgreSQL, eBPF, Vault, etc.).
"""

chunks = [
    # Chunk 0: Target Gold (Aceleração de build e redução de banda em CI/CD com Docker BuildKit e cache remoto inline)
    "Para acelerar builds e minimizar o consumo de banda em pipelines CI/CD efêmeros, o Docker BuildKit permite embutir metadados de cache diretamente na imagem final exportada com a flag --build-arg BUILDKIT_INLINE_CACHE=1 ou usando o exportador --cache-to type=inline. Durante execuções subsequentes do pipeline, o comando docker build consome o cache com a diretiva --cache-from referenciando a imagem no registry, dispensando o upload ou download redundante de camadas separadas de cache e reaproveitando camadas inalteradas.",

    # Chunk 1: Armadilha léxica (Tem 'Docker BuildKit' e 'builds', mas fala de cache local que se perde no CI efêmero)
    "O motor Docker BuildKit fornece uma opção de exportação de cache local através do argumento --cache-to type=local,dest=/var/cache/buildkit. Essa abordagem armazena camadas compiladas no disco local do executor, acelerando compilações em máquinas de desenvolvedores ou runners dedicados permanentes. Entretanto, em agentes efêmeros de CI/CD que são destruídos ao final do job, esse cache em disco local é completamente descartado e não proporciona nenhum reaproveitamento compartilhado.",

    # Chunk 2: Armadilha léxica (Tem as palavras exatas 'cache remoto inline' e 'banda', mas sobre CSS, HTML e CDN)
    "Na otimização de front-end para aplicações web, a inclusão de folhas de estilo com cache remoto inline através de tags de link pré-carregadas reduz a quantidade de requisições paralelas feitas pelo navegador. A combinação dessa técnica com cabeçalhos HTTP Cache-Control em uma CDN global diminui drasticamente o consumo de banda dos servidores de origem e viabiliza um tempo de carregamento de página ultraveloz.",

    # Chunk 3: Armadilha semântica (Otimização de tempo e tamanho de imagens em CI/CD, mas focado em multi-stage e Alpine)
    "A otimização do tempo de empacotamento e a redução drástica do tamanho de imagens de contêineres em fluxos de entrega contínua são alcançadas através de Dockerfiles multi-stage com imagens base enxutas como Alpine Linux ou Google Distroless. Separar os estágios de compilação dos artefatos finais de execução remove compiladores, gerenciadores de pacotes e ferramentas de teste da imagem distribuída, reduzindo o tráfego de rede ao subir a imagem.",

    # Chunk 4: Armadilha conceitual de cache em CI/CD (GitHub Actions actions/cache)
    "Em fluxos de automação do GitHub Actions, a utilização da action oficial actions/cache permite persistir e restaurar dependências de bibliotecas de código-fonte entre execuções de pipelines, tais como a pasta node_modules no ecossistema Node.js ou o diretório .m2 no Java Maven. O cache é indexado por meio do hash dos arquivos de lock e reduz significativamente o tempo de resolução de dependências no início de cada job.",

    # Chunk 5: Armadilha léxica (Termos 'cache', 'inline' e 'latência', mas em microarquitetura de processadores e CPU)
    "Em microarquitetura de computadores, a memória cache L1, L2 e L3 armazena cópias temporárias de dados e blocos de código para mitigar a latência de acesso à memória principal DRAM. O uso de diretivas de pré-busca de instruções e a expansão de funções inline pelo compilador evitam penalidades de desvios condicionais e preservam o fluxo contínuo de execução nos pipelines de superescalaridade da CPU.",

    # Chunk 6: Docker layer caching tradicional e ordenação de instruções no Dockerfile
    "O mecanismo padrão de layer caching do Docker baseia-se na reutilização de camadas intermediárias calculadas a partir do hash do comando executado e do conteúdo dos arquivos copiados. Para maximizar o acerto de cache durante o build, recomenda-se posicionar diretivas que mudam com menor frequência (como instalação de pacotes do sistema) antes de instruções que se alteram a cada commit (como a cópia do código-fonte da aplicação).",

    # Chunk 7: Podman e Buildah para compilação sem daemon no Linux
    "As ferramentas Podman e Buildah permitem compilar e executar contêineres compatíveis com o padrão OCI de maneira daemonless e rootless no Linux. Elas eliminam a dependência de um serviço central como o dockerd, possibilitando a criação segura de imagens de contêineres em ambientes restritos de Kubernetes sem a necessidade de conceder privilégios de root aos pods de compilação.",

    # Chunk 8: Kaniko para build de contêineres dentro de pods Kubernetes
    "O Kaniko é uma ferramenta desenvolvida pelo Google projetada especificamente para compilar imagens de contêineres a partir de um Dockerfile dentro de um cluster Kubernetes, sem depender de um daemon Docker ou de permissões privilegiadas. O Kaniko executa cada comando do Dockerfile inteiramente no espaço de usuário e extrai o sistema de arquivos diretamente para empacotar e publicar a imagem no registry.",

    # Chunk 9: Cloud Native Buildpacks (CNB) para criação automática de imagens OCI
    "A especificação Cloud Native Buildpacks transforma código-fonte de aplicações em imagens OCI prontas para produção sem a necessidade de escrever ou gerenciar Dockerfiles. Detectando a linguagem e dependências automaticamente, os buildpacks criam camadas padronizadas e seguras, simplificando auditorias de segurança e atualizações de vulnerabilidades em sistemas corporativos.",

    # Chunk 10: Docker Buildx com cache externo dedicado no Registry (type=registry)
    "Com o Docker Buildx, equipes de engenharia podem configurar cache de compilação distribuído utilizando o exportador avançado --cache-to type=registry,mode=max. Diferente do modo inline que inclui metadados na imagem da aplicação, o backend dedicado de registry armazena todas as camadas intermediárias de estágios multi-stage em uma tag de imagem separada, otimizando o reuso mesmo para estágios descartados.",

    # Chunk 11: Kubernetes Horizontal Pod Autoscaler (HPA)
    "O Horizontal Pod Autoscaler (HPA) do Kubernetes ajusta dinamicamente a quantidade de réplicas de pods em execução com base no consumo observado de CPU, memória ou métricas customizadas coletadas via Prometheus Adapter. Esse mecanismo assegura elasticidade automática e estabilidade da aplicação diante de variações imprevisíveis na carga de tráfego de requisições.",

    # Chunk 12: Kubernetes Event-driven Autoscaling (KEDA)
    "O KEDA (Kubernetes Event-driven Autoscaling) é um componente que estende o escalonador do Kubernetes para permitir que workloads escalem de 0 a N instâncias em resposta direta a eventos externos, como a profundidade de filas no RabbitMQ, partições com lag no Apache Kafka ou mensagens pendentes em filas AWS SQS.",

    # Chunk 13: Ingress Controllers no Kubernetes
    "Um Ingress Controller no Kubernetes opera como um ponto centralizado de entrada e roteamento de tráfego HTTP e HTTPS externo para serviços internos do cluster. Implementações baseadas em NGINX, Traefik ou HAProxy oferecem recursos de terminação TLS, regras de roteamento baseadas em URI e controle de tráfego com autenticação em camada de borda.",

    # Chunk 14: Service Mesh com Istio e Proxy Envoy
    "O Istio é uma malha de serviços (service mesh) que automatiza a segurança, observabilidade e gerenciamento de tráfego entre microsserviços por meio da injeção de sidecars baseados no proxy Envoy. A solução viabiliza criptografia mTLS ponta a ponta sem modificação do código da aplicação, além de controle granular para lançamentos canário.",

    # Chunk 15: OpenTelemetry Collector para telemetria de microsserviços
    "O OpenTelemetry Collector atua como um intermediário agnóstico de fornecedor para receber, processar e exportar dados de telemetria (rastros distribuídos, métricas e registros de log). Ele suporta o protocolo padrão OTLP e permite aplicar amostragem, mascaramento de informações sensíveis e roteamento de telemetria para múltiplos backends.",

    # Chunk 16: Tracing distribuído e amostragem com Jaeger
    "Em arquiteturas de microsserviços com alto volume de tráfego, sistemas de rastreamento distribuído como o Jaeger empregam estratégias de amostragem (sampling) para conter custos de rede e armazenamento. A amostragem baseada em cauda (tail-based sampling) permite avaliar o rastreamento completo antes de decidir se o rastro com erro ou latência anormal deve ser persistido.",

    # Chunk 17: Coleta de métricas com Prometheus e Alertmanager
    "O Prometheus monitora serviços distribuídos através de um modelo de coleta pull via endpoints HTTP de métricas. Utilizando a linguagem de consulta PromQL, engenheiros definem regras de alerta que disparam notificações para o Alertmanager, o qual gerencia silenciamento, deduplicação e envio de alertas para canais como Slack e PagerDuty.",

    # Chunk 18: Centralização de logs com Grafana Loki
    "O Grafana Loki adota uma arquitetura de agregação de logs inspirada no Prometheus, indexando unicamente os metadados dos fluxos de logs (labels) em vez de indexar o texto completo das mensagens. Essa abordagem reduz drasticamente os requisitos de hardware e custos operacionais se comparada a soluções tradicionais de busca textual como Elasticsearch.",

    # Chunk 19: Apache Kafka e partição de tópicos
    "O Apache Kafka distribui mensagens através de tópicos particionados, permitindo paralelismo horizontal de consumo entre membros de um mesmo consumer group. O algoritmo de particionamento garante ordenação estrita das mensagens que compartilham a mesma chave de particionamento, suportando garantias de entrega com semântica at-least-once ou exactly-once.",

    # Chunk 20: RabbitMQ e roteamento com Dead-Letter Exchanges
    "O RabbitMQ gerencia filas de mensagens assíncronas utilizando o protocolo AMQP com suporte a exchanges do tipo direct, fanout e topic. Mensagens não processadas com sucesso após múltiplas retentativas podem ser roteadas para Dead-Letter Exchanges (DLX), prevenindo o travamento das filas principais e permitindo análise isolada de payloads malformados.",

    # Chunk 21: Redis e estruturas de dados em memória
    "O Redis é um armazenamento de chave-valor em memória que fornece estruturas complexas como Hashes, Sets, Sorted Sets e Streams. Devido ao processamento single-threaded orientado a eventos, ele oferece latências submilisegundas, sendo amplamente adotado como cache de alta velocidade, bloqueador distribuído (Redlock) e gerenciador de sessões de usuário.",

    # Chunk 22: PostgreSQL e índices de busca vetorial pgvector
    "O PostgreSQL estende sua capacidade analítica e relacional por meio de extensões como a pgvector, que permite armazenar e consultar representações densas de embeddings em alta dimensão. Com suporte aos algoritmos de indexação HNSW e IVFFlat, o banco viabiliza buscas semânticas aproximadas por k-vizinhos mais próximos com integridade transacional ACID.",

    # Chunk 23: Mitigação de deadlocks no PostgreSQL com lock_timeout
    "Em ambientes com alta concorrência de escrita no PostgreSQL, deadlocks podem ocorrer quando transações simultâneas tentam adquirir travas exclusivas em linhas compartilhadas em ordens conflitantes. Definir parâmetros como lock_timeout e deadlock_timeout no arquivo postgresql.conf garante que transações bloqueadas sofram aborto controlado, prevenindo filas de contenção de conexões.",

    # Chunk 24: MySQL e mecanismo de armazenamento InnoDB
    "O motor InnoDB é o mecanismo de armazenamento transacional padrão do MySQL, projetado para alta confiabilidade com suporte a integridade referencial e chaves estrangeiras. A persistência é assegurada por mecanismos de buffer pool e escrita em redo logs para garantir durabilidade (crash recovery), enquanto o MVCC permite leituras não bloqueantes de registros.",

    # Chunk 25: MongoDB e modelo orientado a documentos BSON
    "O MongoDB organiza dados semiestruturados em coleções de documentos no formato BSON, proporcionando esquemas flexíveis e suporte a índices secundários compostos. Para alta disponibilidade, utiliza replica sets com eleição automática do nó primário, e para escalabilidade horizontal em petabytes, particiona coleções em shards distribuídos.",

    # Chunk 26: Elasticsearch e busca textual invertida
    "O Elasticsearch implementa um mecanismo distribuído de busca e análise em tempo real sobre o Apache Lucene. Utilizando estruturas de índices invertidos, analisadores léxicos e o algoritmo BM25, a plataforma oferece recuperação de textos em frações de segundo para pesquisas de catálogo e análise de grandes volumes de logs empresariais.",

    # Chunk 27: Apache Cassandra e consistência ajustável
    "O Apache Cassandra adota um modelo descentralizado peer-to-peer sem nós mestres baseado na arquitetura Amazon Dynamo e Google Bigtable. Ele permite que aplicações ajustem o nível de consistência das leituras e escritas por consulta (como ONE, QUORUM ou ALL), viabilizando alta disponibilidade contínua mesmo durante falhas severas de rede entre data centers.",

    # Chunk 28: Terraform e estado distribuído com DynamoDB
    "O HashiCorp Terraform automatiza o provisionamento declarativo de infraestrutura em nuvem através de arquivos de configuração em HCL. Para viabilizar a colaboração entre equipes e impedir modificações concorrentes que corrompam o estado da infraestrutura, utiliza-se backend remoto como AWS S3 associado a bloqueio com tabela no DynamoDB (State Locking).",

    # Chunk 29: OpenTofu como alternativa open-source de IaC
    "O OpenTofu surgiu como um fork comunitário e open-source do Terraform sob licença Mozilla Public License 2.0, garantindo compatibilidade reversa com providers e módulos existentes. A ferramenta mantém a proposta de infraestrutura como código declarativa com governança comunitária aberta e suporte contínuo a múltiplos provedores de nuvem.",

    # Chunk 30: Ansible e automação idempotente sem agentes
    "O Ansible realiza automação de configuração e orquestração de servidores por meio de conexões SSH padronizadas sem a necessidade de agentes residentes nas máquinas gerenciadas. Seus playbooks em YAML são concebidos com foco em idempotência, assegurando que a execução repetida de uma receita mantenha o sistema no estado desejado sem efeitos colaterais indesejados.",

    # Chunk 31: ArgoCD e GitOps no Kubernetes
    "O ArgoCD implementa o modelo operacional GitOps para Kubernetes, monitorando continuamente repositórios Git que contêm manifestos declarativos e sincronizando o estado real do cluster com a definição versionada. O operador detecta desvios de configuração (drift) e pode acionar autorreconciliação imediata para manter a conformidade do ambiente.",

    # Chunk 32: FluxCD para entrega contínua nativa do Kubernetes
    "O FluxCD é um conjunto de controladores e APIs que fornecem automação GitOps progressiva e segura diretamente integrada aos recursos nativos do Kubernetes. Suporta reconciliação de Helm releases, kustomizations e verificação de assinaturas criptográficas de artefatos antes da aplicação em produção.",

    # Chunk 33: HashiCorp Vault e segredos dinâmicos
    "O HashiCorp Vault centraliza a custódia e o controle de acesso a segredos, chaves de API e credenciais de bancos de dados. Seu diferencial reside na emissão de credenciais dinâmicas com tempo de vida curto (TTL) e revogação automática, minimizando o impacto de vazamentos acidentais e facilitando a rotação de senhas em larga escala.",

    # Chunk 34: AWS IAM e privilégio mínimo com IAM Roles para Service Accounts
    "Em clusters Kubernetes na AWS (EKS), a integração de IAM Roles for Service Accounts (IRSA) vincula identidades de pods a credenciais transitórias via OpenID Connect (OIDC). Esse padrão elimina o armazenamento de chaves de acesso estáticas em código ou variáveis de ambiente, assegurando o princípio de menor privilégio de acesso aos recursos de nuvem.",

    # Chunk 35: Cilium e observabilidade com eBPF
    "O Cilium substitui o iptables tradicional no Kubernetes por programas eBPF carregados diretamente no kernel do Linux. Essa arquitetura proporciona roteamento de rede de altíssima performance, balanceamento de carga sem perda de pacotes e aplicação de políticas de segurança e observabilidade em camada 7 com sobrecarga computacional mínima.",

    # Chunk 36: Proxy Envoy e balanceamento de tráfego L7
    "O Envoy é um proxy de serviço e borda de alto desempenho desenvolvido em C++ para arquiteturas orientadas a microsserviços. Implementa modelo de I/O assíncrono baseado em loops de eventos, suporte nativo a HTTP/2 e gRPC, balanceamento de carga com detecção de hosts lentos (outlier detection) e recarregamento dinâmico de configuração via APIs xDS.",

    # Chunk 37: Comunicação entre serviços com gRPC e Protocol Buffers
    "O framework gRPC utiliza o Protocol Buffers como linguagem de definição de interface e mecanismo de serialização binária compacta. Operando sobre o transporte multiplexado do HTTP/2, ele permite chamadas remotas de procedimento (RPC) com tipagem estrita, baixa latência e suporte a streaming bidirecional de mensagens entre microsserviços.",

    # Chunk 38: Padrão Circuit Breaker com Resilience4j
    "A biblioteca Java Resilience4j disponibiliza implementações leves e funcionais do padrão Circuit Breaker para mitigar falhas em cascata em arquiteturas de microsserviços. Ao monitorar a taxa de erros e o tempo limite de chamadas a serviços terceiros, o circuito transiciona para o estado aberto, interrompendo chamadas subsequentes e retornando respostas de fallback pré-definidas.",

    # Chunk 39: Padrão Saga para transações distribuídas em microsserviços
    "O padrão Saga orquestra transações que abrangem múltiplos microsserviços por meio de uma sequência de etapas locais independentes. Caso alguma operação falhe no meio do fluxo, o sistema executa ações compensatórias reversas para restaurar a consistência dos dados, contornando a complexidade e os bloqueios de protocolos de two-phase commit (2PC).",

    # Chunk 40: CQRS (Command Query Responsibility Segregation)
    "O padrão arquitetural CQRS segrega as operações de escrita e mutação de estado (Commands) das operações de leitura e apresentação de dados (Queries). Essa separação permite otimizar modelos de dados e bancos de dados distintos para cada finalidade, como utilizar um banco relacional normalizado para escritas e um cache desnormalizado para consultas de alta performance.",

    # Chunk 41: Cloudflare CDN e mitigação de ataques DDoS na borda
    "A rede de distribuição de conteúdo (CDN) da Cloudflare dispersa o tráfego de requisições por centenas de data centers mundiais por meio de roteamento Anycast. Esse posicionamento permite absorver e neutralizar ataques DDoS volumétricos diretamente na borda da rede antes que o tráfego atinja os servidores de aplicação da empresa.",

    # Chunk 42: WebSockets e Server-Sent Events (SSE)
    "Para cenários que exigem transmissão de dados em tempo real do servidor para o cliente, Server-Sent Events (SSE) oferece um canal unidirecional leve baseado no protocolo HTTP padrão. Já os WebSockets fornecem um canal full-duplex bidirecional sobre uma única conexão TCP persistente, ideal para jogos online, chats e dashboards financeiros instantâneos.",

    # Chunk 43: NGINX como reverse proxy e terminação SSL/TLS
    "O servidor web NGINX é frequentemente posicionado como reverse proxy à frente de aplicações web para gerenciar balanceamento de carga, compressão gzip e terminação segura de conexões TLS/SSL. Delegar a descriptografia criptográfica ao NGINX alivia o processamento das instâncias de aplicação e possibilita cache de respostas estáticas na borda interna.",

    # Chunk 44: Análise estática de código com SonarQube em CI/CD
    "A integração do SonarQube nos pipelines de integração contínua avalia automaticamente o código-fonte em busca de vulnerabilidades de segurança, bugs em potencial e violações de padrões arquiteturais (code smells). Critérios rigorosos de Quality Gate bloqueiam o merge de pull requests que não atinjam metas mínimas de cobertura de testes ou confiabilidade.",

    # Chunk 45: Varredura de vulnerabilidades em contêineres com Trivy
    "O Trivy é um scanner de segurança abrangente para contêineres e imagens OCI capaz de detectar vulnerabilidades conhecidas (CVEs) em pacotes de sistema operacional e dependências de linguagem em segundos. Integrado ao pipeline de CI/CD, impede que imagens contendo falhas críticas sejam publicadas em registries de produção.",

    # Chunk 46: Assinatura de imagens e proveniência de software com Cosign e Sigstore
    "O projeto Sigstore e a ferramenta Cosign facilitam a assinatura criptográfica e verificação de integridade de imagens de contêineres sem necessidade de gerenciar pares de chaves estáticas locais. Utilizando identidades OpenID e registros de transparência Rekor, assegura que apenas artefatos auditados e legítimos sejam executados pelos nós do cluster Kubernetes.",

    # Chunk 47: Linux Cgroups v2 para limites de recursos em contêineres
    "O subsistema cgroups v2 (control groups) do kernel Linux fornece gerenciamento unificado de alocação de recursos de hardware para processos. No contexto de contêineres, ele impõe limites máximos de consumo de CPU, pressão de memória (Memory OOM) e largura de banda de I/O em disco, impedindo que um único contêiner degrade o desempenho de todo o nó hospedeiro.",

    # Chunk 48: Namespaces do kernel Linux para isolamento de contêineres
    "Os namespaces do Linux são a base fundamental da virtualização leve em contêineres, particionando recursos globais do sistema de modo que cada grupo de processos veja uma visão isolada do ambiente. Namespaces de PID, Network, Mount, IPC e UTS impedem que um processo em um contêiner interfira ou inspecione recursos de outros contêineres no mesmo sistema.",

    # Chunk 49: Gerenciamento de serviços e logs de sistema com Systemd e Journalctl
    "O Systemd é o sistema de inicialização e gerenciador de serviços padrão na maioria das distribuições Linux modernas. Ele gerencia dependências de inicialização de daemons em paralelo através de cgroups e centraliza registros de logs estruturados e binários acessíveis via utilitário journalctl, substituindo com maior confiabilidade daemons tradicionais como SysVinit.",
]
