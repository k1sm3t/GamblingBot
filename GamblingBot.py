#!/usr/bin/env python
#coding: utf-8
import requests
from optparse import OptionParser
import time
import GamblingConstants as constante
import matplotlib.pyplot as plt
from crud.GamblingCRUD import *

class GamblingBot(object):
    options = ""
    args = ""
    lista_grafico_y = []
    lista_grafico_x = []
    def __init__(self, options, args):
        self.db_crud = GamblingCRUD()
        self.tipo_jogo = options.jogo
        self.concurso = options.concurso
        self.db_crud.connectDB()

    def retorna_url(self, tipo_jogo):
        if self.tipo_jogo.lower() == "megasena":
            return constante.url_megasena_parte1 + constante.lista_concursos[0] + constante.url_megasena_parte2
        elif self.tipo_jogo.lower() == "lotomania":
            return constante.url_lotomania_parte1 + constante.lista_concursos[1] + constante.url_lotomania_parte2
        elif self.tipo_jogo.lower() == "lotofacil":
            return constante.url_lotofacil_parte1 + constante.lista_concursos[2] + constante.url_lotofacil_parte2
        elif self.tipo_jogo.lower() == "duplasena":
            return constante.url_duplasena_parte1 + constante.lista_concursos[3] + constante.url_duplasena_parte2
	
    def realiza_requests(self):
        lista_resultados = []
        lista_resultado_atual = []
        contador = int(self.concurso)
        vezes = 0
        self.string_resultado = lambda x : "resultado" if self.tipo_jogo == "megasena" else ("de_resultado" if self.tipo_jogo == "lotofacil" else None)
        while contador > int(self.concurso) - 100:
            vezes += 1
            resultado = self.db_crud.consulta_registro(self.tipo_jogo, contador)
            if (resultado == None):
                self.processa_resposta(lista_resultados, lista_resultado_atual, contador)
            else:
                lista_resultados += resultado[0].split('-')
                print(resultado)
            contador -= 1
            if (vezes == 5):
                time.sleep(10)
                vezes = 0
                
        self.conta_ocorrencias(lista_resultados)
    
    def processa_resposta(self, lista_resultados, lista_resultado_atual, contador):
        resposta = requests.post(self.retorna_url(self.tipo_jogo) + str(contador))
        resposta = self.parse(resposta)
        lista_resultado_atual = resposta[self.string_resultado(self.tipo_jogo)].split('-')
        self.db_crud.insere_registro(self.tipo_jogo, contador, lista_resultado_atual)
        print(lista_resultado_atual)
        
        lista_resultados += lista_resultado_atual
        
    def conta_ocorrencias(self, lista_resultados):
        limite = 0
        if (self.tipo_jogo == "megasena"):
            limite = 61
        elif (self.tipo_jogo == "lotofacil"):
            limite = 26
        elif (self.tipo_jogo == "lotomania"):
            limite = 101
        elif (self.tipo_jogo == "duplasena"):
            limite = 51
        for i in range(1,limite):
            self.lista_grafico_x.append(i)
            if (i in range(1,10)):
                self.lista_grafico_y.append(lista_resultados.count('0' + str(i)))                
                print(str(i) + ' - ' + str(lista_resultados.count('0' + str(i))))
            else:
                self.lista_grafico_y.append(lista_resultados.count(str(i)))
                print(str(i) + ' - ' + str(lista_resultados.count(str(i))))
        
        self.desenha_grafico()
        
    def desenha_grafico(self):
        self.db_crud.close_connection()
        plt.plot(self.lista_grafico_x, self.lista_grafico_y)
        plt.title(u"Gráfico de números mais sorteados")
        plt.grid(True)
        plt.show()       
    
    def parse(self, resposta_json):
        return resposta_json.json()

parser = OptionParser()
parser.add_option("-j", "--jogo", dest="jogo", help="O tipo do jogo deve ser especificado.")
parser.add_option("-c", "--concurso", dest="concurso", help="O número do concurso deve ser especificado.")
(options, args) = parser.parse_args()

gb = GamblingBot(options, args)

gb.realiza_requests()