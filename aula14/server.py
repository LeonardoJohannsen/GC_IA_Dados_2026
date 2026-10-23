from flask import Flask, jsonify, request
import requests

BASE_URL_FRUITYVICE = 'https://www.fruityvice.com/api/fruit'
app = Flask(__name__)
sucos = []
sucos.append({
        "id": 1,
        "nome": "Tuti-Fruti",  
        "frutas_ids": [67, 15, 23, 40, 12, 5],  
        "preco": 12.50,
        "volume_ml": 500,
        "descricao": "Um suco refrescante com uma mistura de frutas tropicais."
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



@app.route('/sucos', methods=['GET'])
def listar_sucos():
    return jsonify(sucos), 200


@app.route('/sucos', methods=['POST'])
def inserir_suco():
    response = request.get_json()
    if not response.get("nome") or not response.get("frutas_ids") or not response.get("preco") or not response.get("volume_ml"):
        return jsonify({"error": "Dados incompletos. Certifique-se de fornecer 'nome', 'frutas_ids', 'preco' e 'volume_ml'."}), 400
    else:
        sucos.append({
            "id": len(sucos) + 1,
            "nome": response.get("nome"),
            "frutas_ids": response.get("frutas_ids"),
            "preco": response.get("preco"),
            "volume_ml": response.get("volume_ml"),
            "descricao": response.get("descricao", "")
        })
        print(sucos)
        return jsonify({"message":"Suco criado com sucesso!"}), 201
    

if __name__ == '__main__':
    app.run(debug=True)