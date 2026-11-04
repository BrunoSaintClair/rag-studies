"""
Definições e Parâmetros do Dataset:
- Quantidade total: 30 textos.
- Tamanho por texto: 500 caracteres cada.
- Estrutura temática: Organizado em grupos propositalmente muito parecidos entre si,
  abrangendo pares ou trios com sobreposição de vocabulário e palavras-chave idênticas.
- Pegadinhas semânticas (Homônimos / Polissemia):
    * Python (Linguagem de programação/IA vs. Serpente píton/biologia/cativeiro)
    * Banco (Instituição financeira/Banco Central vs. Banco de dados SQL/NoSQL vs. Mobiliário urbano de praça)
    * Vírus (Patógeno biológico/gripe vs. Malware computacional/trojan/ransomware)
    * Redes Neurais (Biológica/sinapses cerebrais vs. Inteligência Artificial/CNN/Transformers)
    * Cookies (Sessões HTTP/privacidade LGPD na web vs. Biscoitos caseiros/culinária)
    * Maçã / Apple (Fruta/pomicultura vs. Empresa de tecnologia de hardware e serviços)
    * Nuvem (Fenômeno meteorológico/troposfera vs. Computação em nuvem/cloud AWS/GCP)
    * Reranking (Fundamento teórico sobre reordenação de documentos em pipelines RAG)
"""

raw_data = [
    'A linguagem de programação Python se consolidou como uma das ferramentas mais populares no desenvolvimento de software moderno. Com uma sintaxe intuitiva, limpa e de fácil leitura, permite criar desde scripts simples de automação até sistemas web complexos. A rica biblioteca padrão e o ecossistema de módulos comunitários aceleram a entrega de projetos com confiabilidade. Empresas adotam amplamente Python em microsserviços por sua alta produtividade com frameworks ágeis como FastAPI e com Django.',

    'O ecossistema da linguagem Python tornou-se referência global na área de inteligência artificial, análise de dados e aprendizado de máquina. Bibliotecas consagradas como Pandas, NumPy, Scikit-Learn e PyTorch fornecem estruturas de dados velozes e suporte a tensores multidimensionais. Cientistas utilizam Python para manipular grandes volumes de registros e criar modelos preditivos robustos. A comunidade científica impulsiona a evolução dessas ferramentas com algoritmos ágeis e bastante flexíveis.',

    'A serpente Python, popularmente chamada de píton, pertence a uma família de répteis constritores que habitam regiões da África e Ásia. Essas serpentes não produzem veneno; seu método de caça envolve emboscar presas e imobilizá-las através de constrição muscular vigorosa. Capazes de atingir comprimentos extraordinários, as pítons desempenham papel ecológico crucial no controle populacional de mamíferos. Seu habitat natural engloba florestas tropicais úmidas, pântanos densos e savanas preservadas.',

    'O manejo da serpente Python em cativeiro exige recintos com controle rigoroso de umidade, temperatura e espaço físico útil ao réptil. Por serem animais ectotérmicos, as pítons dependem do aquecimento ambiental externo para manter a digestão e o metabolismo em equilíbrio. Biólogos alertam contra o comércio ilegal dessa espécie de réptil, enfatizando que sua soltura acidental pode provocar desastres em biomas. Em cativeiro responsável, monitora-se a troca de pele, hidratação constante e boa saúde.',

    'Um banco comercial opera como intermediário financeiro captando depósitos e concedendo empréstimos a pessoas físicas e corporações. Os correntistas utilizam contas bancárias para movimentar saldos, pagar boletos, realizar transferências e solicitar linhas de crédito. A rentabilidade das instituições de crédito decorre do spread bancário entre as taxas captadas e cobradas em financiamentos de longo prazo. Ademais, a transformação digital modernizou o atendimento via novos aplicativos bem seguros.',

    'A regulação do sistema bancário cabe ao banco central, autoridade responsável por formular a política monetária e manter a estabilidade. Definindo metas para as taxas básicas de juros, o banco busca conter a inflação e assegurar a solidez das reservas internacionais do país. Adicionalmente, auditorias permanentes nas instituições financeiras previnem crises sistêmicas e garantem a liquidez do mercado de capitais. Decisões sobre compulsórios bancários modulam o volume de crédito para as empresas.',

    'O gerenciamento de um banco de dados relacional requer esquemas estruturados baseados em tabelas conectadas por chaves estrangeiras. Sistemas como PostgreSQL e MySQL executam consultas em SQL garantindo propriedades ACID para preservar a integridade das transações. Administradores de bancos monitoram índices, planos de execução e bloqueios concorrentes para otimizar operações de leitura e gravação pesadas. O particionamento de tabelas melhora a performance de relatórios analíticos bem volumosos.',

    'Projetado para escalabilidade horizontal, o banco de dados NoSQL armazena registros não estruturados em formato de documentos ou grafos. Soluções como MongoDB e Cassandra flexibilizam modelos de dados ao dispensar esquemas rígidos previamente declarados em tabelas relacionais. A distribuição de partições por múltiplos nós garante alta disponibilidade mesmo diante de falhas de hardware em grande escala na rede. A consistência eventual prioriza a latência reduzida em aplicações modernas e globais.',

    'O banco de madeira posicionado no centro da praça arborizada oferece repouso e contemplação aos transeuntes que caminham pelo parque. Construído com ripas de carvalho envernizadas e pés de ferro fundido, o banco resiste às intempéries do tempo e ao uso contínuo da cidade. Idosos e crianças sentam-se para conversar à sombra das árvores, transformando o mobiliário urbano em ponto de convívio social acolhedor. A prefeitura realiza manutenções periódicas na pintura e na fixação firme do bom assento.',

    'Um vírus biológico consiste em material genético envolvido por uma cápsula proteica incapaz de reprodução metabólica independente. Ao parasitar células hospedeiras sadias, o patógeno sequestra a maquinaria molecular celular para fabricar novas cópias de si mesmo. A resposta imune do organismo produz anticorpos específicos para neutralizar as partículas virais circulantes no tecido infectado. Mutações frequentes no genoma viral desafiam a imunidade celular e a boa eficácia de terapias antivirais.',

    'O vírus da gripe sazonal acomete o trato respiratório superior provocando febre alta, dores musculares e fadiga generalizada no corpo. Campanhas públicas de imunização disponibilizam vacinas anuais formuladas com cepas inativadas do vírus Influenza em circulação global. A imunização coletiva diminui drasticamente hospitalizações de idosos e indivíduos vulneráveis a complicações pulmonares severas. Práticas simples de higiene das mãos reduzem bastante o contágio direto em ambientes mais fechados.',

    'No ambiente digital, um vírus de computador propaga código malicioso infiltrando arquivos executáveis e os sistemas operacionais alheios. Cavalos de Troia disfarçados de softwares legítimos abrem portas de comunicação clandestinas para cibercriminosos controlarem o terminal. Mecanismos de detecção heurística em antivírus examinam padrões anômalos na memória RAM para mitigar os ataques invasores no PC. A atualização constante de patches de segurança previne invasões que exploram brechas zero-day.',

    'O ransomware é uma categoria agressiva de vírus computacional que criptografa partições inteiras de arquivos vitais corporativos. Os atacantes exigem resgates financeiros pagos em criptomoedas para fornecer a chave criptográfica que restaura o acesso aos dados. Empresas reforçam políticas de backup imutável e autenticação multifator para neutralizar a chantagem imposta por invasores virtuais. Segmentação rigorosa de redes corporativas impede a propagação lateral veloz deste malware muito nocivo.',

    'A rede neural biológica no cérebro humano é formada por bilhões de neurônios interconectados por complexas sinapses eletroquímicas. Dendritos recebem potenciais de ação que estimulam a liberação de neurotransmissores na fenda sináptica para conduzir impulsos nervosos. Esse arranjo de conexões viabiliza a formação de memórias duradouras, o raciocínio dedutivo e a percepção sensorial do ambiente externo. Circuitos neurais refinam respostas comportamentais através de aprendizado biológico contínuo.',

    'A neuroplasticidade permite que a rede neural biológica reorganize caminhos anatômicos em resposta a lesões ou novos aprendizados diários. Neurônios fortalecem ou enfraquecem a eficácia de suas sinapses conforme o estímulo repetido, processo chamado potenciação de longo prazo. Essa maleabilidade estrutural do córtex cerebral sustenta a recuperação motora e a real consolidação de hábitos ao longo da vida. Exercícios cognitivos e sono de qualidade preservam a saúde das sinapses e a memória lúcida.',

    'A rede neural artificial convolucional processa matrizes de pixels para identificar padrões visuais em fotografias digitais detalhadas. Camadas intermediárias aplicam filtros matemáticos capazes de detectar bordas, texturas geométricas e formas anatômicas progressivas. Esse modelo computacional viabilizou avanços históricos no diagnóstico por imagem médica, direção autônoma e biometria facial confiável. Treinamentos com placas aceleradoras gráficas ajustam pesos matemáticos em lotes mais densos.',

    'Modelos de rede neural artificial baseados em Transformers utilizam mecanismos de autoatenção para processar texto e linguagem natural. Diferente de arquiteturas recorrentes, calculam relações semânticas entre todos os termos da sentença simultaneamente em paralelo. Essa formulação matemática permitiu a criação de grandes modelos de linguagem capazes de tradução precisa e geração fluente de respostas. O ajuste fino supervisionado alinha as previsões estatísticas aos objetivos do próprio usuário.',

    'No desenvolvimento web, cookies representam pequenos arquivos de texto enviados pelo servidor HTTP e gravados no navegador do cliente. Eles armazenam identificadores únicos de sessão permitindo que a aplicação reconheça um usuário autenticado em requisições posteriores. Atributos de segurança como HttpOnly e SameSite protegem seus dados contra roubo de credenciais via ataques de scripts maliciosos. A expiração programada garante que tokens temporários não permaneçam válidos por tempo indefinido.',

    'O rastreamento de navegação através de cookies de terceiros tem sido alvo de rígidas restrições legais impostas por leis de privacidade. Empresas de publicidade monitoram páginas visitadas para traçar perfis comportamentais e veicular anúncios personalizados a internautas. Regulamentações como a LGPD exigem o consentimento prévio para que os usuários possam bloquear ou aprovar rastreadores na internet. Navegadores modernos começaram a eliminar cookies externos para proteger a identidade digital.',

    'Preparar deliciosos cookies caseiros com gotas de chocolate requer manteiga cremosa, açúcar mascavo, farinha de trigo e essência de baunilha. A massa batida descansa na geladeira antes de ser modelada em pequenas porções esféricas distribuídas sobre a assadeira untada e fria. Assados em forno moderado, os biscoitos ganham bordas douradas e crocantes mantendo o centro bem macio e bastante achocolatado. Servidos ainda mornos com leite fresco, encantam o paladar em qualquer lanche da tarde festivo.',

    'Para uma opção mais nutritiva, cookies integrais de aveia e mel combinam textura rústica com equilíbrio no teor de açúcar refinado. A adição de sementes de chia, canela em pó e castanhas picadas confere crocância extra a cada mordida deste quitute assado no forno. Nutricionistas recomendam essa receita como lanche prático e rico em fibras solúveis benéficas ao trânsito intestinal e digestão diária. Armazenados em potes herméticos de vidro, esses biscoitos conservam frescor por dez dias seguidos.',

    'A maçã é uma fruta pomácea amplamente apreciada por suas qualidades nutricionais, refrescância natural e baixo teor de calorias totais. Rica em antioxidantes, vitamina C e pectina, auxilia no controle dos níveis de colesterol sanguíneo e na saciedade da alimentação diária. Variedades como Gala e Fuji possuem casca avermelhada e polpa adocicada suculenta perfeita para consumo in natura ou em saladas. O consumo regular da fruta fresca fortalece a imunidade e favorece a hidratação matinal saudável.',

    'A pomicultura voltada à produção de maçã prospera em climas temperados com invernos rigorosos que proporcionam horas de frio necessárias. No sul brasileiro, produtores realizam podas minuciosas nos ramos da macieira para garantir aeração e insolação sobre os frutos jovens. Durante o período de colheita, os frutos são apanhados manualmente para evitar escoriações na casca antes da seleção em câmaras frias. Técnicas bem sustentáveis combatem pragas sem comprometer a integridade do pomar frutífero.',

    'A empresa Apple tornou-se uma gigante da indústria de tecnologia com sua linha inovadora de computadores pessoais e smartphones. Seus aparelhos combinam acabamento de alumínio refinado, telas de alta definição e processadores velozes com arquitetura ARM proprietária. O ecossistema integrado atrai consumidores que valorizam consistência operacional, suporte técnico e valorização de revenda no mercado. Lançamentos anuais de produtos mobilizam filas globais em lojas e grandes eventos dos parceiros.',

    'Além da fabricação de aparelhos, a Apple expandiu operações para o fornecimento de serviços digitais em sua plataforma unificada online. Soluções como armazenamento em nuvem no iCloud, streaming de música e a loja App Store geram receitas recorrentes com alta margem líquida. A rígida moderação de aplicativos garante segurança a milhões de proprietários de dispositivos conectados aos serviços online. A convergência entre hardware e software garante retenção incomparável na base de usuários fiéis.',

    "Na meteorologia, a nuvem cumulonimbus ergue-se verticalmente na atmosfera como uma imensa montanha de vapor d'água e cristais de gelo. Correntes térmicas ascendentes vigorosas sustentam a condensação contínua da umidade, gerando relâmpagos, trovoadas e chuvas torrenciais. Pilotos de aviões evitam cruzar o interior dessas nuvens devido à severa turbulência e risco iminente de congelamento nas asas do avião. Radares meteorológicos monitoram a densidade de gotas no interior da grande massa nublada.",

    'A condensação de vapor na troposfera origina diferentes tipos de nuvem, desde os tênues cirros brancos até espessos estratos cinzentos. Essas formações aéreas desempenham papel determinante no balanço radiativo do planeta ao refletir a radiação solar incidente para o espaço. Meteorologistas classificam a nebulosidade conforme altitude e formato para prever a chegada de frentes frias ou dias ensolarados. O orvalho e a névoa matinal formam-se em noites serenas quando a temperatura cai bruscamente.',

    'A computação em nuvem permite provisionar poder computacional, armazenamento e redes virtuais sob demanda sem manter datacenters. Grandes provedores como Amazon Web Services e Google Cloud operam servidores espalhados por zonas geográficas com plena redundância. Arquiteturas modernas recorrem a contêineres e funções serverless para obter elasticidade instantânea diante das oscilações de tráfego web. A cobrança baseada no consumo real otimiza custos operacionais em comparação a servidores locais.',

    'Estratégias de nuvem híbrida combinam a flexibilidade de provedores públicos com o isolamento rígido de datacenters privados corporativos. Setores regulados mantêm bases confidenciais sob controle interno enquanto escalam cargas analíticas em nuvens públicas do setor. Criptografia ponta a ponta e gestão rigorosa de identidades corporativas garantem a integridade das transferências de dados na internet. Políticas de governança em nuvem estabelecem conformidade contínua com marcos legais do setor.',

    'Em arquiteturas de busca semântica e RAG, a etapa de reranking atua reordenando os documentos recuperados por modelos de primeira fase. Enquanto métodos iniciais de busca vetorial priorizam velocidade computacional, o reranker analisa a correspondência cruzada profunda. Essa avaliação refinada elimina ambiguidades e seleciona os trechos com maior densidade informacional para o prompt do modelo final. O reranker reduz alucinações ao entregar ricas evidências contextuais com muita precisão lógica.',

]

# Sugestões de perguntas para testar o reranking:
# - "Como alimentar e cuidar de uma python em cativeiro?" (réptil vs linguagem)
# - "Quais bibliotecas de python são usadas em inteligência artificial?" (linguagem vs réptil)
# - "Como o banco garante a consistência das transações com ACID?" (banco de dados vs financeiro)
# - "Qual banco oferece melhor descanso ao ar livre em praças?" (mobiliário vs financeiro/dados)
# - "Como tratar infecções causadas por vírus no corpo?" (biológico vs malware)
# - "Como remover vírus que sequestram arquivos do computador?" (malware vs biológico)
# - "Qual o tempo de forno para assar cookies com gotas de chocolate?" (culinária vs web)
# - "Como desativar cookies no navegador para cumprir a LGPD?" (web vs culinária)
# - "Quais são as propriedades nutritivas da maçã fresca?" (fruta vs tecnologia)
# - "Quais serviços de nuvem e dispositivos são fornecidos pela Apple?" (tecnologia vs fruta)
# - "Que tipo de nuvem provoca tempestades e chuvas fortes?" (clima vs computação)
# - "Como provisionar servidores em nuvem com alta redundância?" (computação vs clima)
# - "Qual a diferença entre banco NoSQL e banco relacional SQL?" (comparação técnica)
# - "Por que utilizar uma etapa de reranking em pipelines de RAG?" (conceito do reranker)
