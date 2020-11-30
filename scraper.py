import requests, os, csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def main():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(options=options)
    wait = WebDriverWait(browser, 100)
    urls = {}

    for page in range(5, 53):
        urls[page] = 'https://www.vind-een-psycholoog.be/zoeken/300.html?p={}&per-page=25'.format(page)
        os.makedirs('scraped_urls', exist_ok=True)

    for link in urls.keys():
        output = scrape(browser, wait, urls[link])
        save_info(output)

def scrape(browser, wait, url):
    browser.get(url)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.detail-summary')))
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    # lijst met psychologen
    output = soup.select('a.detail-summary')
    return output

def save_info(output): 
    for row in output:
        page = requests.get(row['href'])
        page_soup = BeautifulSoup(page.text, 'html.parser')

        name_output = page_soup.select('div.col-12 h1.page__heading')
        name = name_output[0].text

        zipcode_output = page_soup.select('div.col-12 p.detail-page__address-line')[1]
        zipcode = zipcode_output.text[:4]

        try:
            phone_output = page_soup.select('div.js-profile-detail-phone p')[1]
            phone = phone_output.text
        except:
            phone = 'Geen telefoonnummer'
        
        try:
            website_output = page_soup.select('a.--with-arrow')[1]
            website = website_output['href']
        except:
            website = 'Geen website'

        psych = [name, zipcode, phone, website]
        with open('psychologen.csv', 'a') as urls:
            writer = csv.writer(urls)
            writer.writerow(psych)
        print("Appending info for {} to csv.".format(name))

if __name__ == '__main__':
    main()