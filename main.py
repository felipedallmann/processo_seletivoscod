import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json


def obter_valor(detalhes, i):
    caminho = "/html/body/div[3]/div/div[2]/table/tbody/tr[" + \
        str(2+i) + "]/td[1]/form/input[3]"

    # clica no botão "detalhes" para abrir a página contendo o valor
    driver.find_element_by_xpath(caminho).click()
    driver.current_url
    element = driver.find_element_by_xpath(
        "/html/body/div[3]/div/div[2]/table/tbody/tr[2]/td[4]")
    html_content = element.get_attribute('outerHTML')
    soup = BeautifulSoup(html_content, 'html.parser')
    detalhes[i] = soup.find(text=True)
    url = "https://scodbrasil.com/teste"
    driver.get(url)


# url da página sendo "raspada"
url = "https://scodbrasil.com/teste"

option = Options()

# faz com que o navegador não abra, faz tudo em background
option.headless = True
driver = webdriver.Firefox(options=option)

driver.get(url)
# obter o html para obter as informações da página
element = driver.find_element_by_xpath("/html/body/div[3]/div/div[1]")
html_content = element.get_attribute('outerHTML')
soup = BeautifulSoup(html_content, 'html.parser')
contatos = soup.find()

# manipular as strings obtidas no html da página
string = " ".join(contatos.text.split())
aux_string = list(string)
aux_string[27] = '\n'
aux_string[75] = '\n'
aux_string[128] = '\n'
new_string = "".join(aux_string)
email = new_string[8:27]
telefones = new_string[39:75]
endereco = new_string[86: 128]
cidade = new_string[137:]


# obtém o html que contém dados de débito
element = driver.find_element_by_xpath("/html/body/div[3]/div/div[2]")
html_content = element.get_attribute('outerHTML')
soup = BeautifulSoup(html_content, 'html.parser')
list_item_dados = soup.find()

# são criadas listas para armazenar futuramente os dados de débito
ano = []
parcela = []
vencimento = []
detalhes = []
valor = []

# itera entre as colunas e linhas obtendo as informações de débito e adicionado-as na lista criada
for row in list_item_dados.findAll("tr"):
    cells = row.findAll('td')
    if len(cells) == 4:
        detalhes.append(cells[0].find('input'))
        ano.append(cells[1].find(text=True))
        parcela.append(cells[2].find(text=True))
        vencimento.append(cells[3].find(text=True))

# itera na lista de detalhes para obter o valor das parcelas
for i in range(0, len(detalhes)):
    if detalhes[i] != None:
        obter_valor(detalhes, i)

# Criação dos dicionários utilizados para armazenar as informações em um JSON
contato = {
    "Email": str(email),
    "Telefone": str(telefones),
    "Endereco": str(endereco),
    "Cidade": str(cidade)
}

debitos = {}
for i in range(0, 4):
    debitos['Debito-' + str(i)] = {
        "Ano": str(ano[i]),
        "Parcela(s)": str(parcela[i]),
        "Vencimento": str(vencimento[i]),
        "Valor": str(detalhes[i])
    }

info = {
    "Contato": contato,
    "Informações de débito": debitos
}

# escrevendo as informações no JSON
js = json.dumps(info)
fp = open('dados.json', 'w')
fp.write(js)
fp.close


driver.quit()
