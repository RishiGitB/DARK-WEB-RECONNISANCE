print("hello")

index html page
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Dark-Web Reconnisance</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
  </head>
  <body>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container-fluid">
    <a class="navbar-brand" href="/index">Home</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="/about">About</a>
        </li>
      </ul>

    </div>
  </div>
</nav>
  </body>
</html>






<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dark Web Interface</title>
</head>
<body>
    <h1>Welcome to Dark Web Interface</h1>
    <p>Enter the URL of the suspicious website:</p>
    <form action="{% url 'check_suspicious' %}" method="post">
        {% csrf_token %}
        <input type="text" name="url">
        <input type="submit" value="Check">
    </form>
</body>
</html>



saksham code :

from transformers import BertForSequenceClassification, BertTokenizer
import torch
import numpy as np
CLASS_NAMES = {
     0: 'Drugs',
     1: 'Library Information',
     2: 'Counterfeit Products',
     3: 'Substances for Drugs',
     4: 'Services',
     5: 'Services/Money',
     6: 'Accounts',
     7: 'Drugs paraphernalia', 8: 'Cryptocurrency', 9: 'Violence', 10: 'Counterfeit Personal-Identification',
     11: 'Leaked Data', 12: 'Counterfeit Money', 13: 'Counterfeit Other', 14: 'Counterfeit Credit-Cards',
     15: 'Social Network', 16: 'Porno', 17: 'Counterfeit Personal Identification',
     18: 'Counterfeit Coupons', 19: 'Fraud', 20: 'Drugs Paraphernalia'
}

SAVED_MODEL = "D:\sb\mchtcModel"
tokenizer = BertTokenizer.from_pretrained(SAVED_MODEL, do_lower_case=True)

N_labels = 21
model = BertForSequenceClassification.from_pretrained(SAVED_MODEL,
                                                      num_labels=N_labels,
                                                      output_attentions=False,
                                                      output_hidden_states=False)
model.eval()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

def predict(input_strings, device="cuda" if torch.cuda.is_available() else "cpu", batch_size=32):
    test_pred = []
    test_loss = 0

    # Tokenize input strings
    tokenizer_out = tokenizer.batch_encode_plus(input_strings, padding=True, truncation=True, return_tensors="pt")
    input_ids = tokenizer_out['input_ids']
    att_mask = tokenizer_out['attention_mask']

    # Load input data onto the specified device
    input_ids = input_ids.to(device)
    att_mask = att_mask.to(device)

    # Generate predictions
    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=att_mask)

        # Extract logits from the output
        logits = outputs.logits

        # Get predicted labels by selecting the index with the maximum probability
        predictions = np.argmax(logits.cpu().numpy(), axis=-1)

    return predictions

input_strings = ["guns armoury glock", "marijuana cocaine"]
predicted_labels = predict(input_strings)
print([CLASS_NAMES[labels] for labels in predicted_labels])


my dat ahndler older code:
import csv

def load_data_from_csv(file_path):
    """
    Load data from a CSV file.
    """
    data = "" #variable to store the loaded data
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile) #: This creates a CSV reader object named reader that reads the contents of the opened CSV file csvfile.
            for row in reader:
                data += " ".join(row) + " "  # Concatenate rows into a single string
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    return data

def check_for_suspicious_content(data, suspicious_words): #explaination in notes
    """
    Check if the loaded data contains any suspicious words or phrases.
    """
    suspicious_found = False
    for word in suspicious_words:
        if word in data:
            print(f"Suspicious content found: '{word}'")
            suspicious_found = True
    if not suspicious_found:
        print("No suspicious content found.")

def main():
    # Define the file path to the CSV file containing the scraped data
    csv_file_path = r'D:\cyber-security\projects\DARK WEB RECONNISANCE\scraped_data.csv'

    # Load data from the CSV file
    data = load_data_from_csv(csv_file_path) #to call the first defined function

    # Define a list of suspicious words or phrases
    suspicious_words = ['hacking', 'malware', 'phishing', 'cybersecurity threat', 'hacking services','human trafficking','drugs','weapon for sale']

    # Check for suspicious content in the loaded data
    check_for_suspicious_content(data, suspicious_words)

main()