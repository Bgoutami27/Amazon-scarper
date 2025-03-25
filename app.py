from flask import Flask, render_template, request, jsonify
import os
import amazon_scraper  # Import your scraper script

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', product=None)  # No default product data

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        product_data = amazon_scraper.get_amazon_tv_details(url)  # Run scraper
        return jsonify(product_data)  # Send data to frontend
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Handle errors

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # ✅ Use Render's dynamic port
    app.run(host="0.0.0.0", port=port, debug=True)
