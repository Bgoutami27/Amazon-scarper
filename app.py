from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import amazon_scraper  # Import your scraper script
from bson import ObjectId  # ✅ Import ObjectId for conversion

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["amazon_scraper"]
collection = db["tv_details"]

# ✅ Fix: Convert `_id` from ObjectId to String before returning JSON
def convert_objectid(data):
    """Convert MongoDB ObjectId to string"""
    data["_id"] = str(data["_id"])  # Convert ObjectId to string
    return data

@app.route('/data', methods=['GET'])
def get_data():
    """Fetch stored data from MongoDB"""
    data = list(collection.find({}))  # Fetch all documents
    data = [convert_objectid(doc) for doc in data]  # Convert `_id`
    return jsonify(data)

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
        collection.insert_one(product_data)  # ✅ Save data to MongoDB
        return jsonify(convert_objectid(product_data))  # Convert before returning
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Handle errors

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # ✅ Use Render's dynamic port
    app.run(host="0.0.0.0", port=port, debug=True)
