import requests
from bs4 import BeautifulSoup
import csv
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove punctuation
    tokens = [word for word in tokens if word.isalnum()]

    # Convert to lowercase
    tokens = [word.lower() for word in tokens]

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    return tokens


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
        return 'scraped_data.csv'
    else:
        print("Failed to scrape data from the URL:", url)
        return None


def parse_data(scraped_file_path):
    input_strings = []

    # Read the contents of the CSV file
    with open(scraped_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            # Assume the scraped text is in the second column
            scraped_text = row[0]  # Assuming the text is in the first column
            # Preprocess the text
            preprocessed_text = preprocess_text(scraped_text)
            # Select 2-3 key phrases or words
            if len(preprocessed_text) >= 3:
                input_strings.append(' '.join(preprocessed_text[:3]))
            else:
                input_strings.append(' '.join(preprocessed_text))

    return input_strings


if __name__ == "__main__":
    url = "https://www.countryliving.com/shopping/gifts/g1478/gifts-for-dog-lovers/"
    # url = "http://muaw5mpgden7ubj55ettmdh6vmk3kpob5lyd2t47ius2lom3bltgs5qd.onion/"
    # url = input("enter the website link to be scraped > ")
    scraped_file_path = scrape_dark_web(url)
    if scraped_file_path:
        input_strings = parse_data(scraped_file_path)
        print("Input strings:", input_strings)
