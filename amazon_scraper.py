import os
import platform
import time
import json
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # ✅ Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # ✅ Use pre-installed Chrome and ChromeDriver on Render
    chrome_path = "/usr/bin/google-chrome"
    driver_path = "/usr/bin/chromedriver"

    if os.path.exists(chrome_path) and os.path.exists(driver_path):
        service = Service(driver_path)  # ✅ Use Render's built-in ChromeDriver
    else:
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())  # ✅ Use only if not available

    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def get_amazon_tv_details(url):
    """ ✅ Scrape Amazon TV details """
    driver = get_driver()

    try:
        driver.get(url)
        time.sleep(5)  # Allow page to load

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        product_name = soup.find(id='productTitle').text.strip() if soup.find(id='productTitle') else 'N/A'
        rating = soup.find('span', {'class': 'a-icon-alt'})
        rating = rating.text.strip() if rating else 'N/A'
        num_ratings = soup.find('span', {'id': 'acrCustomerReviewText'})
        num_ratings = num_ratings.text.strip() if num_ratings else 'N/A'
        
        price = soup.find('span', {'class': 'a-price-whole'})
        price = price.text.strip() if price else 'N/A'
        
        discount = soup.find('span', {'class': 'savingsPercentage'})
        discount = discount.text.strip() if discount else 'N/A'
        
        bank_offers = []
        offers_section = soup.find('div', {'id': 'mir-layout-DELIVERY_BLOCK'})
        if offers_section:
            offers = offers_section.find_all('span')
            for offer in offers:
                bank_offers.append(offer.text.strip())

        about_section = soup.find('div', {'id': 'feature-bullets'})
        about_this_item = [li.text.strip() for li in about_section.find_all('li')] if about_section else []
        
        image_urls = []
        image_section = soup.find('div', {'id': 'altImages'})
        if image_section:
            images = image_section.find_all('img')
            for img in images:
                image_urls.append(img['src'])

        ai_review_section = soup.find('span', {'id': 'cr-summarization-content'})
        ai_review_summary = ai_review_section.text.strip() if ai_review_section else 'N/A'

        product_data = {
            'Product Name': product_name,
            'Rating': rating,
            'Number of Ratings': num_ratings,
            'Selling Price': price,
            'Total Discount': discount,
            'Bank Offers': bank_offers,
            'About This Item': about_this_item,
            'Amazon Product Images': image_urls,
            'AI Generated Review Summary': ai_review_summary
        }

        return product_data
    
    finally:
        driver.quit()

@app.route('/scrape', methods=['POST'])
def scrape():
    """ ✅ API to handle scraping requests """
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        result = get_amazon_tv_details(url)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), debug=True)
