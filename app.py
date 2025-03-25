from flask import Flask, request, jsonify
from flask_cors import CORS  # ✅ Import CORS
import amazon_scraper  

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS for all domains

@app.route('/')
def home():
    return "Amazon Scraper API is Running!"

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({'error': 'URL is required'}), 400

        product_data = amazon_scraper.get_amazon_tv_details(url)  
        return jsonify(product_data)  
    except Exception as e:
        return jsonify({'error': str(e)}), 500  

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
