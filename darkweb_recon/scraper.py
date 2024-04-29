import requests
from bs4 import BeautifulSoup
import csv

def scrape_dark_web(url):
    # Tor proxy settings
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }

    # Send request using Tor proxy
    response = requests.get(url, proxies=proxies)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extracting all text from the website
        all_text = soup.get_text()

        # Write the scraped text to a CSV file
        with open('scraped_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Scraped Text'])
            writer.writerow([all_text])

        print("Scraped data saved to scraped_data.csv")
    else:
        print("Failed to scrape data from the URL:", url)

if __name__ == "__main__": #checks if the script is being run directly as the main program
    # url = "http://muaw5mpgden7ubj55ettmdh6vmk3kpob5lyd2t47ius2lom3bltgs5qd.onion/"
    url = input("enter the website link to be scraped > ")
    scrape_dark_web(url)
