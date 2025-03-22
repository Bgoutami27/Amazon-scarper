from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    with open('amazon_tv_details.json', 'r', encoding='utf-8') as f:
        product_data = json.load(f)
    return render_template('index.html', product=product_data)

@app.route('/api/data')
def get_data():
    with open('amazon_tv_details.json', 'r', encoding='utf-8') as f:
        product_data = json.load(f)
    return jsonify(product_data)

if __name__ == '__main__':
    app.run(debug=True)
