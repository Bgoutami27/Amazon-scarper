import time
import json
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Install Chrome if missing
def install_chrome():
    subprocess.run("wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb", shell=True)
    subprocess.run("apt-get install -y ./google-chrome-stable_current_amd64.deb", shell=True)

# Configure Chrome options
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Use ChromeDriverManager to install ChromeDriver
    service = Service(ChromeDriverManager().install())  
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def get_amazon_tv_details(url):
    install_chrome()  # Ensure Chrome is installed
    driver = get_driver()  # Use updated driver settings

    try:
        driver.get(url)
        time.sleep(5)  

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
        
        product_info = {}
        info_table = soup.find('table', {'id': 'productDetails_techSpec_section_1'})
        if info_table:
            rows = info_table.find_all('tr')
            for row in rows:
                key = row.find('th').text.strip()
                value = row.find('td').text.strip()
                product_info[key] = value

        image_urls = []
        image_section = soup.find('div', {'id': 'altImages'})
        if image_section:
            images = image_section.find_all('img')
            for img in images:
                image_urls.append(img['src'])

        manufacturer_images = []
        manufacturer_section = soup.find('div', {'id': 'aplus'})
        if manufacturer_section:
            images = manufacturer_section.find_all('img')
            for img in images:
                manufacturer_images.append(img['src'])

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
            'Product Information': product_info,
            'Amazon Product Images': image_urls,
            'From the Manufacturer Images': manufacturer_images,
            'AI Generated Review Summary': ai_review_summary
        }

        with open('amazon_tv_details.json', 'w', encoding='utf-8') as f:
            json.dump(product_data, f, ensure_ascii=False, indent=4)

        return product_data
    
    finally:
        driver.quit()

# Example: Run the scraper with a sample URL
if __name__ == "__main__":
    url = "https://www.amazon.in/dp/B0B8YTGC23"
    print(get_amazon_tv_details(url))
