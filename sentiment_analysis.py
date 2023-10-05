import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from transformers import pipeline
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
import csv

#HuggingFace Roberta
MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

#global variables
csv_file_path = 'comments.csv'
results = []
negative_scores = []
neg_scores_total = 0.0
pos_scores_total = 0.0
total_neg = 0
total_pos = 0
sentiment_distribution = 0.0

#Function to start the analysis
def perform_analysis(comment_list):
    global sentiment_distribution
    global pos_scores_total
    global neg_scores_total
    counter = 0
    #Clear numbers to prevent packing
    if pos_scores_total > 0:
        pos_scores_total = 0.0
        neg_scores_total = 0.0

    for comment in comment_list:
        results.append(polarity_scores_roberta(comment))

    try:
        sentiment_distribution = pos_scores_total/neg_scores_total

    except ZeroDivisionError as e:
        print(e)

#Function performs analysis against Roberta model
def polarity_scores_roberta(comment):
    global neg_scores_total
    global pos_scores_total

    #Limit length to prevent tensor overflow
    max_text_length = 505

    #Initiate scores_dict with averages incase no scoring was performed.
    scores_dict = {
        'negative_score' : 0.33,
        'neutral_score' : 0.33,
        'positive_score' : 0.33
    }

    try:
        #Check and clip the length of the comment so that it does not exceed the max tensor size
        if len(comment) > max_text_length:
            comment = comment[:max_text_length]  
        
        #Perform the analysis
        encoded_text = tokenizer(comment, return_tensors='pt')
        output = model(**encoded_text)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

        #add the negative scores to the list for the scatter plot
        negative_scores.append(scores[0])
        #Total the scores for sentiment distribution
        neg_scores_total += scores[0]
        pos_scores_total += scores[2]

        #store the scores in a dictionary for analysis
        scores_dict = {
            'negative_score' : scores[0],
            'neutral_score' : scores[1],
            'positive_score' : scores[2]
        }
        
    except RuntimeError as e:
            #Handle an over tensor limit problem
            print('tensor problem')

    #Return the scores for further analysis
    return scores_dict
    
def create_average():
    try:
        data = []
        #Extract the data and calculate averages for negative, neutral, positive
        negative = [item['negative_score'] for item in results]
        total_neg = sum(negative)
        average_neg = (total_neg/ len(negative)) * 100
        neg_dict = {'Category': 'Negative', 'Value': average_neg}
        data.append(neg_dict)


        neutral = [item['neutral_score'] for item in results]
        total_neu = sum(neutral)
        average_neu = (total_neu/ len(neutral)) * 100
        neu_dict = {'Category': 'Neutral', 'Value': average_neu}
        data.append(neu_dict)

        positive = [item['positive_score'] for item in results]
        total_pos = sum(positive)
        average_pos = (total_pos/ len(positive)) * 100
        pos_dict = {'Category': 'Positive', 'Value': average_pos}
        data.append(pos_dict)

        categories = [item['Category'] for item in data]
        values = [item['Value'] for item in data]

        total = average_neg + average_neu + average_pos
        
        return categories, values
    
    except Exception as e:
        print(e)

