"""
Simples buscador de receitas para o site https://www.tudoreceitas.com
"""

import sys
import requests
from bs4 import BeautifulSoup
import urllib.parse
from os import system

# Pesquisa
query = input('Que receita gostaria de pesquisar: ')

url = 'https://www.tudoreceitas.com/pesquisa?q=' + urllib.parse.quote(query)
receita, indice = 0, 1

while receita <= 0:
    page = requests.get(url) # Carrega pagina da pesquisa
    soup = BeautifulSoup(page.content, 'html.parser')
    link = soup.select('div.resultado.link a') # Todas tags <a>
    receitas, i = [], 1

    for ite in link:
        print(i,ite.get_text()) # contador e titulo
        receitas.append(link[i - 1]['href']) # Lista de links
        i = i + 1

    receita = int(input('Número da receita(-1 voltar ou 0 para ver mais): '))
    if receita <= 0:
        if receita == -1:
            indice = indice - 1    
        else:
            indice = indice + 1
        url = 'https://www.tudoreceitas.com/pesquisa/q/' + query + '/pag/' + str(indice) # Atualiza url para nova pagina
    system("clear") # Limpa a tela

# Receita encontrada, carrega pagina
page = requests.get(link[receita - 1]['href'])
soup = BeautifulSoup(page.content, 'html.parser')

# Título
titulo = soup.find('h1',class_ = 'titulo titulo--articulo')
print(titulo.text + '\n')
print('*' * 43)
# Descricao
descricao = soup.select('div.intro p')    
for i in descricao:
    print(i.text)
    print('\n')
print('*' * 43)
# Ingredientes
print('Ingredientes:')
ingredientes = soup.select('div.ingredientes ul li.ingrediente')
for i in ingredientes:
    if "titulo" in i.__str__():
        print('------------------------' + i.text)
    else:
        print(list(i)[3].text)    
print('*' * 43)
# Modo de preparo
print('Modo de preparo:')
passos = soup.select('div.apartado div.orden + p')
count = 0
for i in passos:
    if "Dica" in i.get_text():
        count = count - 1
    count = count + 1
    print('{}) {}\n'.format(count, i.text))