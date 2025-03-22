import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def get_amazon_tv_details(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
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

# Run the scraper and save data
url = "https://www.amazon.in/Samsung-inches-Ready-UA32T4380AKXXL-Glossy/dp/B0B8YTGC23/ref=sr_1_3?adgrpid=1313918002217057&dib=eyJ2IjoiMSJ9.sIU0B8VBuS719wDNklkGjAvgQ_-S7UziqsRbDGlGyznycuGypqzPOrJjtiDFPZmqdGInJw7wn4BS2ZQ3QcXRyppf6K2Zp4hrcrL4O1X7cisDBiTpGoi4_VrSobiQX_YQX8UF7wOIwjDFQl1hh5qsPMP2BaXOYCxpBulY4WINtN38Nr3rheSnJ89PrOuQRklEDqfNTU2BXnDb1AJMpQzitu7IVTPnGT1rOhbwgPZAIGU.uENyCxzy1JqGLwxS-Gnw4RSuA066gjUXkmUcR72Dxh0&dib_tag=se&hvadid=82120134631363&hvbmt=be&hvdev=c&hvlocphy=149309&hvnetw=o&hvqmt=e&hvtargid=kwd-82120754607171%3Aloc-90&hydadcr=21659_1988875&keywords=tv&msclkid=6e01e209bdee1e4edc6685d70153a54d&qid=1742650559&sr=8-3&th=1"
get_amazon_tv_details(url)
