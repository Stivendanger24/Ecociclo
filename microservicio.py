from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/api/get-current-datetime', methods=['GET'])
def get_current_datetime():
    now = datetime.now()
    current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({'datetime': current_datetime}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
