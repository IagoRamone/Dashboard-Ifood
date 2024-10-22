import os
from dotenv import load_dotenv
import requests
from flask import Flask, jsonify, request
import time


load_dotenv()


app = Flask(__name__)   

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

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
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials' 
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
    
    try:
        token = get_access_token()
        url = f'https://merchant-api.ifood.com.br/merchants/{merchant_id}/reconciliation?competence={competence}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return jsonify(response.json()), 200
        elif response.status_code == 401:
            return jsonify({'error': {'code': 'Unauthorized', 'message': 'Bad credentials'}}), 401
        else:
            return jsonify({'error': {'code': 'InternalServerError', 'message': 'Unexpected error'}}), 500
    except Exception as e:
        return jsonify({'error': {'code': 'InternalServerError', 'message': str(e)}}), 500

@app.route('/financeiro/settlements/<string:merchant_id>', methods=['GET'])
def get_settlements(merchant_id):

    try:
        token = get_access_token() 
        url = f'https://merchant-api.ifood.com.br/merchants/{merchant_id}/settlements' 
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return jsonify(response.json()) 
        else:
            return jsonify({'error': 'Failed to fetch settlements'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        

if __name__ == '__main__':
    app.run(debug=True)