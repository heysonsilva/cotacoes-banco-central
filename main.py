import requests
from datetime import date

strURL = 'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata'
strURL += '/Moedas?$top=100&$format=json'
dictMoedas = requests.get(strURL).json()

strURL = 'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/'
strURL += 'CotacaoMoedaPeriodo(moeda=@moeda,dataInicial='
strURL += '@dataInicial,dataFinalCotacao=@dataFinalCotacao)?'
strURL += '@moeda=%27USD%27&@dataInicial=%2701-01-2023%27&'
strURL += '@dataFinalCotacao=%2712-31-2023%27&$top=100&$format=json'
dictCotacoes = requests.get(strURL).json()

# Esta Variável armazena a data atual para ser utiilizada nas requisições
data_atual = date.today().strftime("%d/%m/%Y")

try:
    # solicitando as informações ao úsuario, que serão usadas posteriormente.
    ano = int(input("DIGITE O ANO: "))
    moeda = input("DIGITE A MOEDA (Ex: USD):")
    def validando_Busca(year, moeda): 
            # usei este WHILE para impossibilitar a utilização de um ano superior ao atual
            while year > int(data_atual[6:9+1]) or len(year) != 4 : print("DIGITE UM ANO VÁLIDO") ; year = int(input("DIGITE O ANO: "))

             # criando lista com as siglas das moedas
            moedas_validas = []
            moedas_validas_siglas = []
            for i in dictMoedas['value']: moedas_validas.append(i)
            for i in moedas_validas: moedas_validas_siglas.append(i['simbolo'])

            # este WHILE é utilizado para impossibilitar o úsuario de inserir uma moeda inválida
            while moeda not in moedas_validas_siglas: print(f"A Moeda Inválida"); moeda = input("DIGITE A MOEDA (Ex: USD):")

            return ano, moeda

    print(validando_Busca(ano, moeda))
                 

except:
    print("TRATAMENTO DE ERRO")


