import requests
from bs4 import BeautifulSoup
from lxml import etree
from lxml import html

#converte string em número e converte para float
def somenteNumeros(string):
    while True:
        var = str(string).strip().replace(',', '.')
        if var in '{[´`^~/?=+-)(*&¨%$#@!"çáÁóÓíÍãÃâÂéÉêÊúÚAaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz;]}':
            for i in range(0,len(var)):
                if var[i] in '{[´`^~/?=+-)(*&¨%$#@!"çáÁóÓíÍãÃâÂéÉêÊúÚAaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz;]}':
                    var[i] = ''
        else:
            var = str(var).strip()
            break
    return float(var)


#Busca valor utilizando parametros x ('Link') e y ('xpath')
def buscaValue(x, y):
    url = x
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
    response = requests.get(url, headers=headers)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    tree = etree.fromstring(soup.prettify(), etree.HTMLParser())
    element = tree.xpath(y)
    return str(element[0].text)

#Verifica se o código inserido existe ou não como ação
def verificaFii(x):
    erros = 1
    while True:
        if erros == 5:
            print('Infelizmente você errou 5 vezes')
            print('Reinicie o código!')
            codigo = False
            break
        urlErro = f"https://www.google.com/finance/quote/{x}:BVMF"
        paginaErro = requests.get(urlErro)
        erroGeral = html.fromstring(paginaErro.content)
        erro = erroGeral.xpath('//*[@id="yDmH0d"]/c-wiz/div/div[4]/div/div/div[2]/text()')
        erro = str(erro).replace('["', '').replace('"]', '')
        erro = str(erro).strip()
        if erro == "We couldn't find any match for your search.":
            print('  Código incorreto! Tente novamente  ')
            x = str(input('Código da ação: ')).strip().upper()
            erros += 1
        else:
            codigo = True
            break
    if codigo == True:
        return True
    else:
        return False


code = str(input('Codigo da ação: ')).strip().upper()
if verificaFii(code) == True:
    value = somenteNumeros(buscaValue(f'https://www.google.com/search?q={code}', '//*[@id="knowledge-finance-wholepage__entity-summary"]/div[3]/g-card-section/div/g-card-section/div[2]/div[1]/span[1]/span/span[1]'))
    print(value)

