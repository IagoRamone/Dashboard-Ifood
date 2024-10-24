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
    return "Bem-vindo à API Financeira!:"

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
        response = requests.post(url, data=data, headers=headers)

        print("Status da resposta:", response.status_code)  # Status da resposta
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
@app.route('/financeiro/reconciliation/<string:merchant_id>', methods=['GET'])
def get_reconciliation(merchant_id):
    competence = request.args.get('competence')  
    print(f"Merchant ID: {merchant_id}")
    print(f"Competence: {competence}")

    try:
        token = get_access_token()  
        url = f'https://merchant-api.ifood.com.br/financial/v3.0/merchants/{merchant_id}/reconciliation?competence={competence}'
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        print("URL chamada:", url)

        response = requests.get(url, headers=headers) 
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

    try:
        token = get_access_token() 
        
        # Verifica qual conjunto de parâmetros foi fornecido
        if begin_payment_date and end_payment_date:
            url = f'https://merchant-api.ifood.com.br/financial/v3.0/merchants/{merchant_id}/settlements?beginPaymentDate={begin_payment_date}&endPaymentDate={end_payment_date}'
        elif begin_calculation_date and end_calculation_date:
            url = f'https://merchant-api.ifood.com.br/financial/v3.0/merchants/{merchant_id}/settlements?beginCalculationDate={begin_calculation_date}&endCalculationDate={end_calculation_date}'
        else:
            return jsonify({'error': 'Missing required date parameters'}), 400

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        print("URL chamada:", url)  
        print("Headers:", headers)   

        response = requests.get(url, headers=headers)
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

#Cadastro no banco

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

if __name__ == '__main__':
    app.run(debug=True)