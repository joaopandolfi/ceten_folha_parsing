#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  lib_processa_ceten.py
#  
#  Biblioteca para processamento do CETENFolha
#  
#  como usar: >>python3.2 lib_processa_ceten.py <arquivoEntrada>
#  
#  Retorna os dados na pasta data/
#  Contendo os aquivos de separação
#  
############################

# ============== FUNÇÕES DE PARSIING ===========
#Recupera os valores de dentro da tag

def removeTags(baseDados,encode):
	#variaveis de arquivo
	arquivo = ""
	arq = arq_open(baseDados,encode)
	#variaveis de conteudo
	conteudo = ""
	result = ""
	buff = ""
	tagContainer = ""
	#variaveis de controle
	i = 0
	intags = False 
	contTag = False
	conteudo = arq_nextLine(arq)
	while(conteudo != ""):
		tam = len(conteudo)
		i = 0
		#percorre o conteudo
		while(i<tam):
			#procura tags
			if(conteudo[i] == '<' and not(contTag)):
				intags = True
				contTag = True
			elif(conteudo[i] == '<' and contTag):
				intags = True
				contTag = False
				if(buff != "" and buff != "\n"):
					#conteudo entre as tags
					result = result + buff + "\n"
					#escrevo no arquivo
					write_arq("data/"+arquivo,buff,"a+")
				buff = ""
			elif(intags and conteudo[i] == '>'):
				#Processo conteudo da tag e retorno o arquivo a ser gravado
				arquivo = processaTags(tagContainer,arquivo)
				tagContainer = ""
				intags = False
			elif(contTag and not(intags)):
				buff = buff + conteudo[i]
			else:
				#conteudo da tag
				tagContainer = tagContainer + conteudo[i]
			i = i+1
		conteudo = arq_nextLine(arq)
	arq_close(arq)
	return result

#Processa conteudo das TAGS
def processaTags(conteudo,arquivo):
	#variaveis
	arqFinal = ""
	result = ""
	stops = ["'",'"']
	inTag = False
	if(conteudo.find("ext") >= 0): #se for um titulo
		#recupero o inico da string cad
		i = conteudo.find("cad") +4 # cad= (deslocamento 4)
		tam = len(conteudo)
		#percorro a string e salvo
		while(i < tam):
			if((conteudo[i] in stops) and not(inTag)):
				inTag = True
			elif((conteudo[i] in stops) and inTag):
				break
			else:
				result = result + conteudo[i]
			i = i+1

		arqFinal = result
		
		#reinicializo variaveis
		inTag = False
		result = ""
		#recupero o inico da string sec
		i = conteudo.find("sec") +4 # sec= (deslocamento 4)
		tam = len(conteudo)
		#percorro a string e salvo
		while(i < tam):
			if((conteudo[i] in stops) and not(inTag)):
				inTag = True
			elif((conteudo[i] in stops) and inTag):
				break
			else:
				result = result + conteudo[i]
			i = i+1
		
		#monto String
		arqFinal = result+"_"+arqFinal+".data"
		return arqFinal	
		
	return arquivo



#Recupero links das TAGS
def getLinks(conteudo):
	#variaveis
	result = ""
	stops = ["'",'"']
	inTag = False
	if(conteudo.find("href") >= 0): #se for um link
		#recupero o inico da string
		i = conteudo.find("href") +5 # href= (deslocamento 5)
		tam = len(conteudo)
		#percorro a string e salvo
		while(i < tam):
			if((conteudo[i] in stops) and not(inTag)):
				inTag = True
			elif((conteudo[i] in stops) and inTag):
				break
			else:
				result = result + conteudo[i]
			i = i+1
	return result

# ================ FUNÇÔES ARQUIVO ==================

#escreve string no arquivo	, a+ (concatena), w (substitui)
def write_arq(arquivo,string,modo):
	arq = open("./"+arquivo,modo)
	arq.write(string+"\n")
	arq.close()

#funções segmentadas
def arq_open(arquivo,encode):
	if(encode != ""):
		arq = open('./'+arquivo , 'rt',encoding=encode)
	else:
		arq = open('./'+arquivo , 'rt',encoding='ISO-8859-1')			
	return arq

def arq_nextLine(arq):
	conteudo = ""
	conteudo = arq.readline()
	if(conteudo == ""):
		return ""
	if(conteudo[-1] =='\n'):
		conteudo = conteudo[:-1] 
	return conteudo

def arq_close(arq):
	arq.close()
	return

#le arquivo completo => Retorna lista de linhas
def read_arq(arquivo,ext):
	conteudo =""
	lista= []
	arq = open('./'+arquivo+ext , 'rt',encoding='utf-8')
	conteudo = arq.readline()
	while conteudo != '':
		if(conteudo[-1] =='\n'):
			conteudo = conteudo[:-1] 
		lista.append(conteudo)
		conteudo = arq.readline()
	arq.close()
	return lista


# ================== MAIN =================

def main():
	import sys
	argumento = sys.argv[1:] #site	
	if(len(argumento)<1):
		print("\nArgumento invalido")
		print("-------------------------------")
		print("Forma correta: ")
		print("Arquivo.py <DatabaseCetenFolha>")
		print("Ou")
		print("Arquivo.py <DatabaseCetenFolha> <codificacao>")
		print("")
		print("Codificação padrao: ISO-8869-1")
		print("-------------------------------")
		return
	print("Processando...")
	if(len(argumento) == 1):
		removeTags(argumento[0],"")
	else:
		removeTags(argumento[0],argumento[1])
	return 0

main()
