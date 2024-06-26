from django.shortcuts import render
from .scraper import scrape_dark_web, parse_data
from .data_handler import predict
# Create your views here.
def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')


def check_suspicious(request):
    if request.method == 'POST':
        # Get the URL input from the form
        url = request.POST.get('url')

        # Call the function in scraper.py to scrape the website and save data to CSV
        scraped_file_path = scrape_dark_web(url)

        # Call the predict function from data_handler.py to check if the scraped data is suspicious
        input_strings = parse_data(scraped_file_path)  # Define input strings from the scraped data (you need to parse the CSV file)
        predicted_labels = predict(input_strings)

        # Check if any predicted label is suspicious
        is_suspicious = any(label in ['Drugs', 'Library Information', 'Counterfeit Products', 'Substances for Drugs', 'Services',
                   'Services/Money', 'Accounts', 'Drugs paraphernalia', 'Cryptocurrency', 'Violence',
                   'Counterfeit Personal-Identification', 'Leaked Data', 'Counterfeit Money', 'Counterfeit Other',
                   'Counterfeit Credit-Cards', 'Social Network', 'Porno', 'Counterfeit Personal Identification',
                   'Counterfeit Coupons', 'Fraud', 'Drugs Paraphernalia'] for label in predicted_labels)

        # Render the result template with the result
        return render(request, 'index.html', {'is_suspicious': is_suspicious, 'url': url})
    else:
        # If the request method is not POST, render the home page
        return render(request, 'index.html')