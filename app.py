from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # ✅ Import CORS
import amazon_scraper  
import os

app = Flask(__name__, template_folder="templates")  # ✅ Ensure Flask can find templates folder
CORS(app, resources={r"/scrape": {"origins": "*"}})   # ✅ Enable CORS for all domains

@app.route('/')
def home():
    return render_template("index.html")  # ✅ Serve the HTML page instead of text

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
    port = int(os.environ.get("PORT", 5000))  # ✅ Use Render's dynamic port
    app.run(host="0.0.0.0", port=port, debug=True)
    