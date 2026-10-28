from flask import Flask, jsonify, request
import requests

#BASE_URL_FRUITYVICE = 'https://www.fruityvice.com/api/fruit'
BASE_URL_FRUITYVICE =  'http://127.0.0.1:5001/api/fruit'  # URL do servidor fake
app = Flask(__name__)
sucos = []
sucos.append({
        "id": 1,
        "nome": "Tuti-Fruti",  
        "frutas_ids": [67, 15, 23, 40, 12, 5],  
        "preco": 12.50,
        "descricao": "Um suco refrescante com uma mistura de frutas tropicais.",
        "total_calorias": 0,
        "total_acucar": 0,
    })

def obter_detalhes_frutas(frutas_ids):
    frutas_detalhes = []
    
    for fruta_id in frutas_ids:
        try:
            resposta = requests.get(f'{BASE_URL_FRUITYVICE}/{fruta_id}')
            resposta.raise_for_status()
            frutas_detalhes.append(resposta.json())
        except requests.exceptions.RequestException:
            print(f"Erro ao consultar a fruta com ID {fruta_id}. Verifique se o ID é válido.")
            continue
            
    return frutas_detalhes

def calcular_valor_nutricional(suco):
    frutas_detalhes = obter_detalhes_frutas(suco["frutas_ids"])
    total_calorias = 0
    total_acucar = 0
    for fruta in frutas_detalhes:
        total_calorias += fruta.get("nutritions", {}).get("calories", 0)
        total_acucar += fruta.get("nutritions", {}).get("sugar", 0)
    return total_calorias, total_acucar

@app.route('/sucos', methods=['GET'])
def listar_sucos():
    return jsonify(sucos), 200


@app.route('/sucos', methods=['POST'])
def inserir_suco():
    print("Recebendo solicitação para criar um novo suco...")
    response = request.get_json()
    if not response.get("nome") or not response.get("frutas_ids") or  response.get("preco") is None or not response.get("descricao"):
        return jsonify({"error": "Dados incompletos. Certifique-se de fornecer 'nome', 'frutas_ids', 'preco' e 'descricao'."}), 400
    else:
        sucos.append({
            "id": len(sucos) + 1,
            "nome": response.get("nome"),
            "frutas_ids": response.get("frutas_ids"),
            "preco": response.get("preco"),
            "descricao": response.get("descricao"),
            "total_calorias": 0,
            "total_acucar": 0,
        })
        total_calorias, total_acucar = calcular_valor_nutricional(sucos[-1])
        sucos[-1]["total_calorias"] = total_calorias
        sucos[-1]["total_acucar"] = total_acucar
        print(sucos)
        return jsonify({"message":"Suco criado com sucesso!"}), 201


@app.route('/sucos', methods=['PUT'])
def atualizar_suco():
    response = request.get_json()
    if not response.get("id"):
        return jsonify({"error": "ID do suco não fornecido."}), 400
    for suco in sucos:
        if suco["id"] == response.get("id"):
            suco["nome"] = response.get("nome", suco["nome"])
            suco["frutas_ids"] = response.get("frutas_ids", suco["frutas_ids"])
            suco["preco"] = response.get("preco", suco["preco"])
            suco["descricao"] = response.get("descricao", suco["descricao"])
            total_calorias, total_acucar = calcular_valor_nutricional(suco)
            suco["total_calorias"] = total_calorias
            suco["total_acucar"] = total_acucar
            return jsonify({"message": "Suco atualizado com sucesso!"}), 200
    return jsonify({"error": "Suco não encontrado."}), 404    

if __name__ == '__main__':
    app.run(debug=True) 