# Rag com Reranking

Essa versão adiciona um passo a mais no nosso Rag. Consiste em realizarmos um rankeamento dos chunks mais similares com base na relevância de cada um perante a entrada recebida.

## Fluxo da Execução

Sistema recebe a pergunta -> Realiza a busca atrás de chunks similares -> Ordena o resultado com base na relevância de cada um -> Usa os mais bem avaliados para gerar a resposta.

## Trade-off

Enquanto a busca vetorial isolada recupera rapidamente documentos similares, ela frequentemente traz ruídos que poluem o prompt. O **reranking** avalia a relação exata entre a pergunta e cada documento (cross-encoder), descartando trechos irrelevantes.

Como resultado, obtém-se maior precisão na resposta da LLM e menor consumo de tokens. Em contrapartida, adiciona-se uma camada a mais na arquitetura e a latência de rede/processamento do modelo de rankeamento.
