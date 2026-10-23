import requests

BASE_URL = 'https://www.fruityvice.com/api/fruit'

def consultar_frutas(id_fruta):
    resposta = requests.get(f'{BASE_URL}/{id_fruta}')
    return resposta.json()

def exibir_fruta(resposta):
    if "error" in resposta:
        print(f"Erro: {resposta.get('error')}")
        return

    nome = resposta.get("name")
    id_fruta = resposta.get("id")
    familia = resposta.get("family")
    nutricao = resposta.get("nutritions", {})

    print(f"=== {nome} ===")
    print(f"ID: {id_fruta}")
    print(f"Família: {familia}")
    print("Nutrição:")
    print(f" • Açúcar: {nutricao.get('sugar')}g")
    print(f" • Proteínas: {nutricao.get('protein')}g")
    print(f" • Calorias: {nutricao.get('calories')}g")

def executar_exemplos():
    try:
        test = input("Digite o ID ou Nome da fruta que deseja consultar: ")
        exibir_fruta(consultar_frutas(test))
        
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code
        
        if status == 404:
            print("Fruta não encontrada. Verifique o ID ou Nome digitado.")
        elif status == 400:
            print("Requisição inválida (Bad Request).")
        else:
            print(f"Erro HTTP {status}: {e}")

    except Exception as e:
        print(f"Erro inesperado: {e}")



if __name__ == '__main__':
    executar_exemplos()