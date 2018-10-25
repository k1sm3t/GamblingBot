#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 18:49:06 2018

@author: root
"""
import sqlite3

class GamblingCRUD(object):
    
    def connectDB(self):
        self.conn = sqlite3.connect('Gambling.db')    
        self.cursor = self.conn.cursor()
        if (1 == 1):
            self.cria_tabelas()
    
    def cria_tabelas(self):
        self.cursor.execute('''
                            
        CREATE TABLE resultados_megasena (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                numero_concurso TEXT NOT NULL,
                resultado TEXT NOT NULL
        );
                
                ''')
        
        self.cursor.execute('''
                            
        CREATE TABLE resultados_lotofacil (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                numero_concurso TEXT NOT NULL,
                resultado TEXT NOT NULL
        );
                
                ''')
        
        self.cursor.execute('''
                            
        CREATE TABLE resultados_lotomania (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                numero_concurso TEXT NOT NULL,
                resultado TEXT NOT NULL
        );
                
                ''')
        
        self.cursor.execute('''
                            
        CREATE TABLE resultados_duplasena (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                numero_concurso TEXT NOT NULL,
                resultado TEXT NOT NULL
        );
                
                ''')
        
    def insere_registro(self, tipo_jogo, concurso, resultado):        
        if (tipo_jogo.lower() == 'megasena'):
            self.cursor.execute('INSERT INTO resultados_megasena VALUES ({a},{b})'.format(a=concurso, b=resultado))
        elif (tipo_jogo.lower() == 'lotofacil'):
            self.cursor.execute('INSERT INTO resultados_lotofacil VALUES ({a},{b})'.format(a=concurso, b=resultado))
        elif (tipo_jogo.lower() == 'lotomania'):
            self.cursor.execute('INSERT INTO resultados_lotomania VALUES ({a},{b})'.format(a=concurso, b=resultado))
        elif (tipo_jogo.lower() == 'duplasena'):
            self.cursor.execute('INSERT INTO resultados_duplasena VALUES ({a},{b})'.format(a=concurso, b=resultado))
            
        self.conn.commit()
            
    def consulta_registro(self, tipo_jogo, concurso):
        if (tipo_jogo.lower() == 'megasena'):
            sql = 'SELECT resultado FROM resultados_megasena WHERE concurso = ?'
        elif (tipo_jogo.lower() == 'lotofacil'):
            sql = 'SELECT resultado FROM resultados_lotofacil WHERE concurso = ?'
        elif (tipo_jogo.lower() == 'lotomania'):
            sql = 'SELECT resultado FROM resultados_lotomania WHERE concurso = ?'
            
        self.cursor.execute(sql, [(concurso)])
        
        return self.cursor.fetchone()
    
    def close_connection(self):
        self.conn.close()