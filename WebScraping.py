import os
import time
import re
import json
import requests
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from collections import Counter as cnt
from bs4 import BeautifulSoup as bs

def ignorar_caracteres_cercados(texto, char_abertura, char_fechamento):
    #print("entrou")
    profundidade = 0
    novo_texto = ''

    for c in texto:
        if c == char_abertura:
            profundidade += 1
        elif c == char_fechamento:
            profundidade -= 1
            if profundidade < 0:
                raise Exception('Cercamento não balanceado')
        elif profundidade == 0:
            novo_texto += c

    if profundidade > 0:
        raise Exception('Cercamento não balanceado')

    return novo_texto

i = 0

chromedriver = "chromedriver.exe"
driver = webdriver.Chrome(chromedriver)
#chama login google
driver.get("https://accounts.google.com/signin/v2/identifier?hl=pt-BR&passive=true&continue=https%3A%2F%2Fwww.google.com%2F%3Fgws_rd%3Dssl&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
#time.sleep(2)
#driver.find_element_by_xpath('//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]').click()
#time.sleep(1)
#driver.find_element_by_xpath('//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]').send_keys(email)
print("")
print("")
ID_Reuniao = input("Quando terminar de fazer o login insira o ID da reunião Ex.(tnh-znvk-vrn): ")
print("")
print("")
print("")
print("Aguarde...")
time.sleep(2)

#Abre reunião
driver.get("https://meet.google.com/" + ID_Reuniao)
#print("Aguarde mais uns instantes...")
#time.sleep(15)
#driver.find_element_by_xpath('//*[@id="yDmH0d"]/div[3]/div/div[2]/div[3]/div/span').click()
print("")
print("")
print("")
bloquear = input("Pressione em bloquear microfone e vídeo, em seguida pressione enter para continuar.")
print("")
print("")
print("")
#Entra na reunião
driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[4]/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/span').click()
print("")
print("")
print("Entrando na reunião")

time.sleep(7)
driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[4]/div[3]/div[6]/div[3]/div/div[2]/div[1]/span').click()
print("Procurando por participantes")

time.sleep(5)

#Armazenar html onde todos os nomes estão
element = driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[4]/div[3]/div[3]/div/div[2]/div[2]/div[2]/span[1]/div[2]')
html_content = element.get_attribute('outerHTML')

#Tratar o html
soup = bs(html_content, 'html.parser')
table = str(soup.find_all(class_="cS7aqe NkoVdd"))

pessoas = ignorar_caracteres_cercados(table, '<' , '>' )

nome = []
nome = pessoas.replace('[',' ')
nome = nome.replace(']','')
nome = nome.split(',')
print("")
print("Presentes")
print("")

for i in nome:
    print(i)

print("")
print(pessoas)
print("")

#print("")
#print(table)
#print("")

time.sleep(2)
print("Saindo da reunião")
driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[4]/div[3]/div[9]/div[2]/div[2]/div').click()
print("Salvando nomes em txt")
driver.quit()

datt = datetime.now().date().strftime("%Y-%m-%d")
nomeArquivo = input("Digite o nome do arquivo: ")
arquivo = open(nomeArquivo + "_" + datt + '.txt', 'a')

for i in nome:
    arquivo.write( i + '\n')

print("Nomes salvos")
arquivo.close()
