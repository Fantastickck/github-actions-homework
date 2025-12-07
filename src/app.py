from datetime import datetime
import json
from flask import Flask
from flask import request, jsonify
from pydantic import BaseModel, ValidationError

app = Flask(__name__)

def validate_post_data(data: dict) -> bool:
    if not isinstance(data, dict):
        return False
    if not data.get('name') or not isinstance(data['name'], str):
        return False
    if data.get('age') and not isinstance(data['age'], int):
        return False
    return True

@app.route('/', methods=['GET'])
def hello():
    return 'Hello World!'

@app.route('/add', methods=['GET'])
def add():
    try:
        a = float(request.args.get('a'))
        b = float(request.args.get('b'))
    except (TypeError, ValueError):
        return 'a и b - НЕ числа'
    return str(a + b)


@app.route('/api', methods=['GET', 'POST'])
def api():
    """
    /api entpoint
    GET - returns json= {'status': 'test'}
    POST -  {
            name - str not null
            age - int optional
            }
    :return:
    """
    if request.method == 'GET':
        return jsonify({'status': 'test'})
    elif request.method == 'POST':
        if validate_post_data(request.json):
            return jsonify({'status': 'OK'})
        else:
            return jsonify({'status': 'bad input'}), 400


class CreateTransactionRequest(BaseModel):
    amount: float
    payer: str
    recipient: str


TRANSACTIONS_PATH = 'src/data.json'
    

@app.route('/transactions/', methods=['GET', 'POST'])
def transactions():
    with open(TRANSACTIONS_PATH) as f:
        transactions: list = json.load(f)

    if request.method == 'GET':
        return jsonify(transactions)
    elif request.method == 'POST':
        try:
            request_data = CreateTransactionRequest.model_validate(request.json)
        except ValidationError as e:
            return jsonify({'message': f'Ошибка валидации: {e}'}), 400

        create_data = {
            **request_data.model_dump(),
            'created_at': datetime.now().isoformat()
        }
        transactions.append(create_data)
        with open(TRANSACTIONS_PATH, 'w') as f:
            json.dump(transactions, f)
        return jsonify({'message': 'Транзакция успешно добавлена'})


def main():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    main()