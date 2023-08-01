import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import concurrent.futures
import csv
import os

csv_file_path = "data.csv"
df = pd.read_csv(csv_file_path)

def scrape_website(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        
        response = requests.get(url, headers=headers)
        time.sleep(0.1)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = []

            for link in soup.find_all('a', href=True):
                links.append(link['href'])
            return links

        return None
    except Exception as e:
        print("Error while scraping:", e)
        return None

def filter_product_solution_links(links):
    relevant_links = []
    try:
        keywords = ['product', 'products' , 'catalog', 'shop', 'buy', 'pricing', 'features','service', 'solution', 'consulting', 'support']

        for link in links:
            if any(keyword in link.lower() for keyword in keywords):
                relevant_links.append(link)
    except Exception as e:
        print("error in filtering")
    return relevant_links

def classify_website(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        
        response = requests.get(url, headers=headers)
        time.sleep(0.1)
        
        if response.status_code == 200:
                website_content = response.text.lower()

                product_keywords = ['products', 'catalog', 'shop', 'buy', 'pricing', 'features']
                service_keywords = ['services', 'solutions', 'consulting', 'support']



                product = sum(keyword in website_content for keyword in product_keywords)

                service = sum(keyword in website_content for keyword in service_keywords)

                if product>service:
                    return "Product Website"
                elif service>product:
                    return "Service Website"
                else:
                    return "Unclassified Website"
                return "Unclassified Website"

        return "Domain not Available"
    except Exception as e:
        return "Domain not Available"


def process_url(row):
    website_name = row[0]
    website_url = row[1]

    all_links = scrape_website(website_url)
    relevant_links = filter_product_solution_links(all_links)

    classification = classify_website(website_url)

    if classification == "Unclassified Website":
        for link in relevant_links:
            page_classification = classify_website(link)
            if page_classification == "Product Website":
                classification = "Product Website"
                break
            elif page_classification == "Service Website":
                classification = "Service Website"
                break

    return website_name, website_url, classification

def main():

    output_file_path = "output.csv"

    with open(output_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["company_name", "website", "isProductOrService"])

    for index, row in df.iterrows():
        company_name = row[0]
        website_url = row[1]
        
        website_data = process_url(row)

        with open(output_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([company_name, website_url, website_data[2]])

        print(company_name, website_url, website_data[2])

if __name__ == "__main__":
    main()