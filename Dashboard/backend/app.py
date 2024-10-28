import os
from dotenv import load_dotenv
import requests
from flask import Flask, jsonify, request
import time
from bd import insert_user  

load_dotenv()

app = Flask(__name__)

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
merchant_id = os.getenv('MERCHANT_ID')

print(f"Client ID: {client_id}")
print(f"Client Secret: {client_secret}")

@app.route('/')
def home():
    return "Bem-vindo à API Financeira!"

access_token = None
token_expiration_time = 0
  
def get_access_token():
    global access_token, token_expiration_time
    
    if access_token is None or time.time() > token_expiration_time:
        url = 'https://merchant-api.ifood.com.br/authentication/v1.0/oauth/token'
        headers = {
            'accept': 'application/json',  
            'Content-Type': 'application/x-www-form-urlencoded'  
        }
        
        data = {
            'grantType': 'client_credentials',  
            'clientId': client_id,              
            'clientSecret': client_secret,      
            'authorizationCode': '',
            'authorizationCodeVerifier': '',
            'refreshToken': ''
        }
        
        print("Dados enviados:", data) 
        response = requests.post(url, data=data, headers=headers, timeout=10)

        print("Status da resposta:", response.status_code)  
        print("Corpo da resposta:", response.text)
        
        if response.status_code == 200:
            token_info = response.json()
            access_token = token_info['accessToken']
            token_expiration_time = time.time() + token_info['expiresIn']
            return access_token
        else:
            raise Exception(f"Failed to get access token: {response.text}")

    return access_token

@app.route('/financeiro/token', methods=['GET'])
def get_token():
    try:
        token = get_access_token()
        return jsonify({
            'accessToken': token,
            'type': 'bearer',
            'expiresIn': 21600
        }), 200
    except Exception as e:
        return jsonify({
            'error': {
                'code': 'Unauthorized' if 'credentials' in str(e) else 'InternalServerError',
                'message': str(e)
            }
        }), 401 if 'credentials' in str(e) else 500

# Função para gerar dados mockados de reconciliation
def mock_reconciliation_data(merchant_id):
    return {
        "totalSales": 1000.0,
        "netAmount": 950.0,
        "commission": 50.0,
        "period": "2024-10",
        "merchant_id": merchant_id,
        "items": [
            {
                "item": "Pedido 12345",
                "grossAmount": 150.0,
                "netAmount": 140.0,
                "commission": 10.0
            },
            {
                "item": "Pedido 67890",
                "grossAmount": 200.0,
                "netAmount": 180.0,
                "commission": 20.0
            }
        ]
    }

# Função para gerar dados mockados de settlements
def mock_settlements_data(merchant_id):
    return {
        "settlements": [
            {
                "settlementDate": "2024-10-15",
                "grossAmount": 500.0,
                "netAmount": 475.0,
                "commission": 25.0,
                "status": "settled"
            },
            {
                "settlementDate": "2024-10-16",
                "grossAmount": 600.0,
                "netAmount": 570.0,
                "commission": 30.0,
                "status": "pending"
            }
        ]
    }

@app.route('/financeiro/reconciliation/<string:merchant_id>', methods=['GET'])
def get_reconciliation(merchant_id):
    competence = request.args.get('competence')  
    print(f"Merchant ID: {merchant_id}")
    print(f"Competence: {competence}")

    if competence == 'mock':  # Checa se quer dados mockados
        return jsonify(mock_reconciliation_data(merchant_id)), 200

    try:
        token = get_access_token()  
        url = f'https://merchant-api.ifood.com.br/financial/v3.0/merchants/{merchant_id}/reconciliation?competence={competence}'
        headers = { 
            'accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        print("URL chamada:", url)

        response = requests.get(url, headers=headers, timeout=10) 
        if response.status_code == 200:
            return jsonify(response.json()), 200  
        elif response.status_code == 401:
            return jsonify({'error': {'code': 'Unauthorized', 'message': 'Bad credentials'}}), 401
        else:
            print("Resposta da API do iFood:", response.text) 
            return jsonify({'error': {'code': 'InternalServerError', 'message': 'Unexpected error'}}), 500
    except Exception as e:
        return jsonify({'error': {'code': 'InternalServerError', 'message': str(e)}}), 500
    
@app.route('/financeiro/settlements/<string:merchant_id>', methods=['GET'])
def get_settlements(merchant_id):
    begin_payment_date = request.args.get('beginPaymentDate')
    end_payment_date = request.args.get('endPaymentDate')
    begin_calculation_date = request.args.get('beginCalculationDate')
    end_calculation_date = request.args.get('endCalculationDate')

    # Checa se quer dados mockados
    if begin_payment_date == 'mock' and end_payment_date == 'mock':
        return jsonify(mock_settlements_data(merchant_id)), 200

    # Verifica se ao menos um conjunto de parâmetros de data foi fornecido
    if not (begin_payment_date and end_payment_date) and not (begin_calculation_date and end_calculation_date):
        return jsonify({'error': 'Missing required date parameters'}), 400

    try:
        token = get_access_token() 
        
        # Verifica qual conjunto de parâmetros foi fornecido
        if begin_payment_date and end_payment_date:
            url = f'https://merchant-api.ifood.com.br/financial/v3.0/merchants/{merchant_id}/settlements?beginPaymentDate={begin_payment_date}&endPaymentDate={end_payment_date}'
        elif begin_calculation_date and end_calculation_date:
            url = f'https://merchant-api.ifood.com.br/financial/v3.0/merchants/{merchant_id}/settlements?beginCalculationDate={begin_calculation_date}&endCalculationDate={end_calculation_date}'

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        print("URL chamada:", url)  
        print("Headers:", headers)   

        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return jsonify(response.json()) 
        else:
            print("Resposta da API do iFood:", response.text) 
            return jsonify({'error': 'Failed to fetch settlements'}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/dados-settlements')
def get_settlements_data():
    settlements_data = requisicao_settlements()
    return jsonify(settlements_data)

# Cadastro no banco
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    data = request.get_json() 
    nome = data['nome']
    email = data['email']
    tel = data['tel']
    usuario = data['user']
    senha = data['senha']
    insert_user(nome, email, tel, usuario, senha)
    
    return jsonify({"message": "Cadastro realizado com sucesso!"}), 201


@app.route('/financeiro/pedidos-unicos/<string:merchant_id>', methods=['GET'])
def get_unique_sales(merchant_id):
    competence = request.args.get('competence')  # Opcional: pegar o período
    token = get_access_token()

    # Montar a URL da API do iFood (substitua o endpoint conforme necessário)
    url = f'https://merchant-api.ifood.com.br/financial/v3.0/merchants/{merchant_id}/sales?competence={competence}'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        data = response.json()
        # Contar pedidos únicos
        unique_sales_count = len(set(item['order_id'] for item in data['orders']))
        return jsonify({"unique_sales_count": unique_sales_count}), 200
    else:
        return jsonify({'error': response.text}), response.status_code


if __name__ == '__main__':
    app.run(debug=True)
