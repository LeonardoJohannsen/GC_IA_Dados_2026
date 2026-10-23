from flask import Flask, jsonify, requests

BASE_URL_FRUITYVICE = 'https://www.fruityvice.com/api/fruit'
app = Flask(__name__)
sucos = {
        "id": 1,
        "nome": "Tuti-Fruti",  
        "frutas_ids": [67, 15, 23, 40, 12, 5],  
        "preco": 12.50,
        "volume_ml": 500
    }

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


if __name__ == '__main__':
    app.run(debug=True)