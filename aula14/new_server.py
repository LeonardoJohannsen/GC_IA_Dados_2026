

import requests
from flask import Flask, jsonify, request 
from typing_extensions import Annotated
from pydantic import BaseModel, Field, ValidationError

BASE_URL_FRUITYVICE = 'https://www.fruityvice.com/api/fruit'

app = Flask(__name__)

class SucoEntrada(BaseModel):
    nome: str = Field(min_length=3)
    frutas: list[Annotated[str, Field(min_length=3)]] = Field(min_length=1)
    tem_gosto_de: str = Field(min_length=3)

class Suco(BaseModel):
    id: int
    nome: str
    frutas: list[str]
    tem_gosto_de: str
    total_calorias: float
    total_acucar: float

class FrutaNaoEncontradaError(Exception):
    pass

sucos: dict[int, Suco] = {}

def buscar_dados_fruityvice(fruta: str):
    response = requests.get(
        f"{BASE_URL_FRUITYVICE}/{fruta}",
        timeout=5
    )

    if response.status_code == 404:
        raise FrutaNaoEncontradaError(fruta)

    response.raise_for_status()
    return response.json()
    
def obter_detalhes_frutas(frutas: list[str]):
    resultados = []

    for nome in frutas:
        dados = buscar_dados_fruityvice(nome)
        resultados.append(dados)

    return resultados

def calcular_valores_nutricionais(frutas_detalhes: list[dict]) -> tuple[float, float]:
    total_calorias = 0.0
    total_acucar = 0.0

    for fruta in frutas_detalhes:
        nutritions = fruta["nutritions"]
        total_calorias += nutritions["calories"]
        total_acucar += nutritions["sugar"]

    return total_calorias, total_acucar

@app.get('/frutas/<string:fruta>')
def consultar_fruta(fruta: str):
    try:
        dados = buscar_dados_fruityvice(fruta)
        nutricao = dados.get("nutritions", {})

        return jsonify({
            "nome": dados.get("name"),
            "calorias": nutricao.get("calories"),
            "acucar": nutricao.get("sugar")
        }), 200

    except FrutaNaoEncontradaError:
        return jsonify({
            "erro": f"Fruta '{fruta}' não encontrada."
        }), 404

    except requests.RequestException:
        return jsonify({
            "erro": "Não foi possível consultar a API de frutas."
        }), 502

@app.get('/sucos')
def listar_sucos():
    return jsonify([
        suco.model_dump()
        for suco in sucos.values()
    ]), 200

@app.post('/sucos')
def inserir_suco():
    data = request.get_json()
    try:
        entrada = SucoEntrada.model_validate(data)

    except ValidationError as erro:
        return jsonify({
            "erro": "Dados inválidos",
            "detalhes": erro.errors(
                include_input=False,
                include_context=False,
                include_url=False
            )
        }), 400

    try:
        frutas_detalhes = obter_detalhes_frutas(entrada.frutas)

    except FrutaNaoEncontradaError as erro:
        return jsonify({
            "erro": f"Fruta '{erro}' não encontrada."
        }), 404
    
    except requests.RequestException:
        return jsonify({
            "erro": "Não foi possível consultar a API de frutas."
        }), 502

    total_calorias, total_acucar = calcular_valores_nutricionais(frutas_detalhes)
    novo_id = max(sucos.keys(), default=0) + 1
    novo_suco = Suco(
        id=novo_id,
        nome=entrada.nome,
        frutas=entrada.frutas,
        tem_gosto_de=entrada.tem_gosto_de,
        total_calorias=total_calorias,
        total_acucar=total_acucar
    )

    sucos[novo_id] = novo_suco

    return jsonify({"message": "Suco criado com sucesso!", "suco": novo_suco.model_dump()}), 201

@app.put('/sucos/<int:suco_id>')
def atualizar_suco(suco_id: int):
    data = request.get_json()
    try:
        entrada = SucoEntrada.model_validate(data)

    except ValidationError as erro:
        return jsonify({
            "erro": "Dados inválidos",
            "detalhes": erro.errors(
                include_input=False,
                include_context=False,
                include_url=False
            )
        }), 400

    suco = sucos.get(suco_id)
    if suco is None:
        return jsonify({
            "erro": f"Suco com ID {suco_id} não encontrado."
    }), 404
    
    try:
        frutas_detalhes = obter_detalhes_frutas(entrada.frutas)
    
    except FrutaNaoEncontradaError as erro:
        return jsonify({
            "erro": f"Fruta '{erro}' não encontrada."
        }), 404
        
    except requests.RequestException:
        return jsonify({
            "erro": "Não foi possível consultar a API de frutas."
        }), 502
    
    total_calorias, total_acucar = calcular_valores_nutricionais(frutas_detalhes)


    suco.nome = entrada.nome
    suco.frutas = entrada.frutas
    suco.tem_gosto_de = entrada.tem_gosto_de
    suco.total_calorias = total_calorias
    suco.total_acucar = total_acucar

    return jsonify({"message": "Suco atualizado com sucesso!", "suco": suco.model_dump()}), 200