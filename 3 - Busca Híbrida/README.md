# Busca Híbrida 

A busca vetorial possui alguns "blind spots" pelo fato de se basear na semântica e no contexto, isso pode causar uma perda de algumas palavras-chave que o usuário menciona no input. Com a busca híbrida, nós realizamos uma busca vetorial e uma busca por match exato de palavras. 


## Algoritmo de Match BM25

O algoritmo `Best Matching 25` é o mais relevante para a busca por palavras exatas. Ele rankeia chunks baseado em dois fatores:

    1. Frequência que o termo aparece -> Term Frequency (TF).
    2. Quão raro o termo é ao longo de toda a coleção de chunks -> Inverse Document Frequency (IDF).


Exemplo do TF: 

    - Chunk A: "O crescimento de receita da Tesla é gigante. A Tesla registrou lucro."
    - Chunk B: "Tesla reportou resultados ótimos."

Uma busca realizada apenas com o termo 'Tesla' retornaria o chunk A, pois lá ele foi repetido mais vezes.


Exemplo do IDF: 

    - Se 'Tesla' aparece em 100 chunks mas 'Cybertruck' aparece em apenas 5, para a query 'Tesla Cybertruck' os 5 chunks ganham um maior IDF score por que é mais raro.



Combinando ambos: Para a consulta 'Tesla Cybertruck', um chunk com 'Tesla Cybertruck production' é melhor pontuado do que um chunk com 'Tesla Tesla Tesla financial reports', por que o termo raro Cybertruck é mais valioso que termos comuns sendo repetidos.


## Conclusão

Na busca vetorial é capturada as relações semânticas e contextuais, na busca por palavra exata captura-se matches exatos. A busca híbrida cobre as falhas de cada uma. 