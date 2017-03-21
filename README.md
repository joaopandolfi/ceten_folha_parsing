# CETEN Folha Parser
Ferramenta para separar o conteúdo em arquivos

## Base de dados
O arquivo da base dados pode ser encontrado em: http://www.linguateca.pt/cetenfolha/index_info.html

## Requisitos
 >Python 3.X

## Utilização
 >Navegue até a pasta raiz do projeto
 >Execute
```
python3 lib_processa_ceten.py <arquivoEntrada>

ou

python3 lib_processa_ceten.py <arquivoEntrada> <codificacao>

Exemplo

python3 lib_processa_ceten.py ceten.txt

ou

python3 lib_processa_ceten.py ceten.txt utf-8

```

 >Os arquivos de saída serão gerados na pasta data dentro do projeto