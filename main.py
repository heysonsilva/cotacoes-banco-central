import requests
from datetime import date, datetime
import json
import csv
import matplotlib.pyplot as plt


def salvar_arquivo_json(dados, moeda, ano):
    nome_arquivo = f"medias_cotacoes_{moeda}_{ano}.json"
    try:
        with open(nome_arquivo, 'w') as arquivo:
            json.dump(dados, arquivo, indent=4)
        print(f"Arquivo salvo como {nome_arquivo}")
    except IOError as e:
        print(f"Erro ao salvar o arquivo: {e}")

def salvar_resultados_em_csv(moeda, ano, resultado_final):
    nome_arquivo_csv = f"medias_cotacoes_{moeda}_{ano}.csv"
    with open(nome_arquivo_csv, 'w', newline='', encoding='utf-8') as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv, delimiter=';')
        escritor_csv.writerow(['moeda', 'mes', 'media_compra', 'media_venda'])
        
        for resultado in resultado_final:
            escritor_csv.writerow([
                moeda,
                resultado['Mes'],
                f"{resultado['Media de Compra']:.5f}",
                f"{resultado['Media de Venda']:.5f}"
            ])
    print(f"Arquivo CSV salvo como {nome_arquivo_csv}")

def identificar_mes(data_str):
    try:
        data = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        data = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")

    meses = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }
    return meses[data.month]

def validar_moeda(moeda, dictMoedas):
    moedas_validas = {i['simbolo'] for i in dictMoedas['value']}
    
    while moeda not in moedas_validas:
        print(">> MOEDA INVÁLIDA")
        moeda = input("DIGITE A MOEDA (Ex: USD):")
    
    return moeda

def filtro_de_cotacoes_por_tipo_boletim(lista, boletim_type):
    meses_de_referencia = [
        "Janeiro", "Fevereiro", "Marco", "Abril", 
        "Maio", "Junho", "Julho", "Agosto", 
        "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    
    lista_resultado = []
    
    for mes_index in range(1, 13):
        mes = meses_de_referencia[mes_index - 1]
        soma_compra = 0
        soma_venda = 0
        contador_dias = 0
        
        for cotacao in lista:
            if identificar_mes(cotacao['dataHoraCotacao']) == mes and cotacao.get('tipoBoletim') == boletim_type:
                soma_compra += cotacao['cotacaoCompra']
                soma_venda += cotacao['cotacaoVenda']
                contador_dias += 1
        
        if contador_dias > 0:
            media_compra = soma_compra / contador_dias
            media_venda = soma_venda / contador_dias
            
            lista_resultado.append({
                'Mes': mes,
                'Media de Compra': round(media_compra, 5),
                'Media de Venda': round(media_venda, 5)
            })
    
    return lista_resultado

def salvar_arquivo_json(dados, moeda, ano):
    nome_arquivo = f"medias_cotacoes_{moeda}_{ano}.json"
    try:
        with open(nome_arquivo, 'w') as arquivo:
            json.dump(dados, arquivo, indent=4)
        print(f"Arquivo salvo como {nome_arquivo}")
    except IOError as e:
        print(f"Erro ao salvar o arquivo: {e}")

def gerar_grafico(moeda, ano, resultado_final):
    meses_de_referencia = [
        "Janeiro", "Fevereiro", "Março", "Abril", 
        "Maio", "Junho", "Julho", "Agosto", 
        "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    
    meses = [resultado['Mes'] for resultado in resultado_final]
    medias_compra = [resultado['Media de Compra'] for resultado in resultado_final]
    medias_venda = [resultado['Media de Venda'] for resultado in resultado_final]
    
    plt.figure(figsize=(10, 6))
    plt.plot(meses, medias_compra, marker='o', label='Média de Compra')
    plt.plot(meses, medias_venda, marker='o', label='Média de Venda')
    
    plt.xticks(rotation=45)
    plt.xlabel('Mês')
    plt.ylabel('Média')
    plt.title(f'Médias de Compra e Venda ao Longo dos Meses - {moeda} {ano}')
    plt.legend()
    plt.grid(True)
    
    nome_arquivo_grafico = f"medias_cotacoes_{moeda}_{ano}.png"
    plt.savefig(nome_arquivo_grafico)
    plt.show()
    print(f"Gráfico salvo como {nome_arquivo_grafico}")

def main():
    ano_atual = date.today().year
    ano = int(input("DIGITE O ANO: ")) 
    while not str(ano).isdigit() or int(ano) > ano_atual or len(str(ano)) != 4:
        ano = input(">> DIGITE UM ANO VÁLIDO: ")
   
    boletim_type = "Fechamento"

    url_moedas = 'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/Moedas?$top=100&$format=json'
    try:
        response_moedas = requests.get(url_moedas)
        response_moedas.raise_for_status()
        dictMoedas = response_moedas.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição das moedas: {e}")
        return
    except json.JSONDecodeError:
        print("Erro ao decodificar a resposta JSON das moedas.")
        return

    moeda = input("DIGITE A MOEDA (Ex: USD): ")
    moeda = validar_moeda(moeda, dictMoedas)

    resultado_final = []

    for mes_index in range(1, 13):
        mes = f"{mes_index:02d}"
        url_cotacoes = (
            f'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/'
            f'CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)'
            f'?@moeda=%27{moeda}%27&@dataInicial=%27{mes}-01-{ano}%27&@dataFinalCotacao=%2712-31-{ano}%27&$top=100&$format=json'
        )

        try:
            response_cotacoes = requests.get(url_cotacoes)
            response_cotacoes.raise_for_status()
            dictCotacoes = response_cotacoes.json()
            lista_de_cotacoes = dictCotacoes['value']
            resultado_mes = filtro_de_cotacoes_por_tipo_boletim(lista_de_cotacoes, boletim_type)
            resultado_final.extend(resultado_mes)
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição para o mês {mes}: {e}")
        except json.JSONDecodeError:
            print(f"Erro ao decodificar a resposta JSON para o mês {mes}")
    
    salvar_arquivo_json(dictCotacoes, moeda, ano)
    salvar_resultados_em_csv(moeda, ano, resultado_final) 
    print(json.dumps(resultado_final, indent=4))
    gerar_grafico(moeda, ano, resultado_final)



    # Salvar o dicionário dictCotacoes em um arquivo JSON


# Executa o programa
main()
