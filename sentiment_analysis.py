import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from transformers import pipeline
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
import csv

# This is a simple example to make sure we are integrating 
# Huggingface roberta into our program correctly

# example = 'I love this idea so much, but it does not work very well.'
MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

csv_file_path = 'comments.csv'
results = []

def perform_analysis():
    counter = 0
    #I am using encoding='utf-8-sig' to fix encoding and BOM issues.
    with open('comments.csv', 'r', encoding='utf-8-sig', errors='replace', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            counter = counter + 1
            results.append(polarity_scores_roberta(row))
            # print(f'row {counter}: ', row)
    
    print('perform_analysis finished')

def polarity_scores_roberta(example):

    encoded_text = tokenizer(example, return_tensors='pt')
    output = model(**encoded_text)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    scores_dict = {
        'roberta_neg' : scores[0],
        'roberta_nue' : scores[1],
        'roberta_pos' : scores[2]
    }
    print('polarity done')
    return scores_dict

# print(polarity_scores_roberta(example))
# results_df = pd.DataFrame(results)
def create_average():
    try:
        data = []
        #Extract the data and calculate averages for negative, neutral, positive
        negative = [item['roberta_neg'] for item in results]
        total_neg = sum(negative)
        average_neg = (total_neg/ len(negative)) * 100
        neg_dict = {'Category': 'Negative', 'Value': average_neg}
        data.append(neg_dict)


        neutral = [item['roberta_nue'] for item in results]
        total_neu = sum(neutral)
        average_neu = (total_neu/ len(neutral)) * 100
        neu_dict = {'Category': 'Neutral', 'Value': average_neu}
        data.append(neu_dict)

        positive = [item['roberta_pos'] for item in results]
        total_pos = sum(positive)
        average_pos = (total_pos/ len(positive)) * 100
        print(average_pos)
        pos_dict = {'Category': 'Positive', 'Value': average_pos}
        data.append(pos_dict)

        print(data)
        categories = [item['Category'] for item in data]
        values = [item['Value'] for item in data]

        total = average_neg + average_neu + average_pos
        print(total)
    except Exception as e:
        print(e)
    print('create_average finished')
    return categories, values


