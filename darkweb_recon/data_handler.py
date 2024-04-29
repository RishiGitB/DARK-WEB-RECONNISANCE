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

SAVED_MODEL = "D:\cyber-security\projects\DARK WEB RECONNISANCE\HackingWebsiteMultiClassTextClassification\mchtcModel"
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