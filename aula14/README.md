# API de Sucos

Aplicação web desenvolvida em Python com Flask. A API permite consultar informações nutricionais de frutas utilizando o serviço externo [Fruityvice](https://www.fruityvice.com/), além de cadastrar, listar e atualizar sucos.

Os outros arquivos exceto o new_server.py ultilizei apenas para aprendizado. Unico arquivo relevante para a entrega é o new_server.py

## Funcionalidades

- Consultar uma fruta e obter seu nome, quantidade de calorias e açúcar.
- Cadastrar sucos informando nome, frutas e descrição do sabor.
- Calcular automaticamente o total de calorias e açúcar de cada suco a partir das informações retornadas pelo Fruityvice.
- Listar os sucos cadastrados.
- Atualizar um suco existente, substituindo seus dados e recalculando os valores nutricionais.
- Validar os dados recebidos com Pydantic e retornar respostas de erro apropriadas quando os dados forem inválidos, uma fruta não for encontrada ou a API externa estiver indisponível.

> **Observação sobre os cálculos:** a aplicação soma os valores nutricionais informados pelo Fruityvice para cada fruta, considerando a referência de 100 g por fruta. O código não recebe nem calcula quantidades personalizadas.

## Tecnologias e dependências

- Python 3.9 ou superior
- Flask
- Requests
- Pydantic 2
- typing-extensions
- API externa: Fruityvice

## Como executar

### 1. Clonar ou baixar o projeto

Coloque o arquivo Python da aplicação e o `requirements.txt` na mesma pasta. Neste README, considera-se que o arquivo Python se chama `app.py`.

### 2. Criar e ativar um ambiente virtual

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux ou macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 4. Iniciar o servidor

Na pasta do projeto, execute:

```bash
python -m flask --app app run --debug
```

A API ficará disponível em:

```text
http://127.0.0.1:5000
```

Se o arquivo Python tiver outro nome, substitua `app` no comando pelo nome do arquivo, sem a extensão `.py`. Por exemplo, para `server.py`, use `python -m flask --app server run --debug`.

## Endpoints

### Consultar uma fruta

**GET** `/frutas/<fruta>`

Consulta o Fruityvice e retorna o nome, as calorias e o açúcar da fruta.

Exemplo:

```http
GET http://127.0.0.1:5000/frutas/apple
```

Resposta de sucesso (`200 OK`):

```json
{
  "nome": "Apple",
  "calorias": 52,
  "acucar": 10.3
}
```

Caso a fruta não seja encontrada, a API retorna `404 Not Found`.

### Cadastrar um suco

**POST** `/sucos`

Recebe um objeto JSON com `nome`, `frutas` e `tem_gosto_de`. Os nomes das frutas devem ter pelo menos três caracteres e a lista deve conter ao menos uma fruta.

Exemplo de corpo da requisição:

```json
{
  "nome": "Suco tropical",
  "frutas": ["apple", "banana"],
  "tem_gosto_de": "doce e refrescante"
}
```

Resposta de sucesso (`201 Created`):

```json
{
  "message": "Suco criado com sucesso!",
  "suco": {
    "id": 1,
    "nome": "Suco tropical",
    "frutas": ["apple", "banana"],
    "tem_gosto_de": "doce e refrescante",
    "total_calorias": 141,
    "total_acucar": 20.59
  }
}
```

Os valores numéricos acima são apenas ilustrativos; os valores efetivos dependem da resposta do Fruityvice.

Possíveis respostas de erro:

- `400 Bad Request`: dados recebidos não passaram pela validação.
- `404 Not Found`: uma das frutas informadas não foi encontrada.
- `502 Bad Gateway`: não foi possível consultar a API externa.

### Listar os sucos

**GET** `/sucos`

Retorna uma lista com todos os sucos cadastrados em memória.

Exemplo:

```http
GET http://127.0.0.1:5000/sucos
```

### Atualizar um suco

**PUT** `/sucos/<suco_id>`

Substitui os dados do suco identificado pelo ID. O corpo deve conter os mesmos campos exigidos no cadastro (`nome`, `frutas` e `tem_gosto_de`). Os valores nutricionais são consultados e calculados novamente.

Exemplo:

```http
PUT http://127.0.0.1:5000/sucos/1
```

Corpo da requisição:

```json
{
  "nome": "Suco energético",
  "frutas": ["banana", "orange"],
  "tem_gosto_de": "doce e cítrico"
}
```

Respostas possíveis:

- `200 OK`: suco atualizado com sucesso.
- `400 Bad Request`: dados inválidos.
- `404 Not Found`: suco ou fruta não encontrada.
- `502 Bad Gateway`: não foi possível consultar a API externa.

## Testando com Postman

Para testar a API pelo Postman:

1. Inicie o servidor seguindo as instruções acima.
2. Crie uma requisição e use `http://127.0.0.1:5000` como endereço base.
3. Para cadastrar ou atualizar um suco, selecione **Body → raw → JSON** e envie um dos exemplos apresentados neste README.
4. Para as requisições GET, não é necessário enviar um corpo.

## Limitações conhecidas

- Os sucos são armazenados em um dicionário Python na memória. Portanto, os cadastros são perdidos quando o servidor é encerrado ou reiniciado.
- A consulta nutricional depende da disponibilidade e dos dados fornecidos pelo Fruityvice.
- O cálculo considera os valores nutricionais retornados pela API para cada fruta, sem permitir informar pesos ou porções diferentes.
