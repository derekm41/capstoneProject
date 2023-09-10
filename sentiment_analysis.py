import numpy as np
import pandas as pd
from transformers import pipeline
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
import csv

# This is a simple example to make sure we are integrating 
# Huggingface roberta into our program correctly

# example = 'I love this idea so much, but it does not work very well.'
# MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
# tokenizer = AutoTokenizer.from_pretrained(MODEL)
# model = AutoModelForSequenceClassification.from_pretrained(MODEL)

csv_file_path = 'comments.csv'

def perform_analysis():
    counter = 0
    with open('comments.csv', 'r', errors='replace', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            counter = counter + 1
            # print(f'row {counter}: ', row)

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
    return scores_dict

# print(polarity_scores_roberta(example))
perform_analysis()

# iterate over data set
# I need to read in the data correctly first.
# for i, row in tqdm(df.iterrows(), total=len(df)):
#     text = row['Text']

#     roberta_result = polarity_scores_roberta(text)
#     break



