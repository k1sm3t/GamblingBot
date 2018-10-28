#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 18:49:06 2018

@author: root
"""
import sqlite3

class GamblingCRUD(object):

    c_create_table = '''
                            
        CREATE TABLE {table_name} (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                numero_concurso TEXT NOT NULL,
                resultado TEXT NOT NULL
        );
                
                '''

    c_insert_record = 'INSERT INTO {table_name} (numero_concurso, resultado) VALUES ("{a}","{b}")'

    c_retrieve_record = 'SELECT resultado FROM resultados_{game} WHERE numero_concurso = ?'
    
    def connectDB(self):
        self.conn = sqlite3.connect('Gambling.db')    
        self.cursor = self.conn.cursor()
        if (self.check_table('resultados_megasena') == None):
            self.cria_tabelas('resultados_megasena')
            self.cria_tabelas('resultados_lotofacil')
    
    def cria_tabelas(self, table):
        self.cursor.execute(self.c_create_table.format(table_name=table))
        
        
    def insere_registro(self, tipo_jogo, concurso, resultado):
        separador = '-'
        resultado_joinado = separador.join(resultado)
        self.cursor.execute(self.c_insert_record.format(table_name=tipo_jogo.lower(), a=concurso, b=resultado_joinado))            
        self.conn.commit()

    def check_table(self, table):
        self.cursor.execute('SELECT name FROM sqlite_master WHERE type = "table" AND name = "{table_name}"'.format(table_name=table))
        return self.cursor.fetchone()

            
    def consulta_registro(self, tipo_jogo, concurso):
        sql = self.c_retrieve_record.format(game=tipo_jogo.lower())            
        self.cursor.execute(sql, [(concurso)])        
        return self.cursor.fetchone()
    
    def close_connection(self):
        self.conn.close()