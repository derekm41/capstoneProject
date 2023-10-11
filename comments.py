from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import credentials
import csv
import os
from urlextract import URLExtract
import html
from bs4 import BeautifulSoup
import demoji
import sentiment_analysis
import random

#global variables
 #Random number for accuracy testing.
random_number1 = random.randint(1, 25)
random_number2 = random. randint(26, 50)
video_counter = 0
comment_list = []
video_comments_list = []
video_id_list = []
likes = []
comments = []
sentiment_score = []
# query = 'golfing'

# Connect to the YouTube API
youtube = build('youtube', 'v3', developerKey=credentials.capstone_API_Key)

#Function to remove urls and emojis
def data_cleaning(text):
    #using BeautifulSoup to remove html elements ie <a href>
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text()
    #using URLExtract() to remove urls
    extractor = URLExtract()
    urls = list(set(extractor.find_urls(text)))
    for url in urls:
        text = text.replace(url, '')
    #using demoji to remove emojis.
    text = demoji.replace(text, '')
    return text

#Function to perform a search and retrieve top 100 video Ids returned.
def get_video_ids(youtube, query, max_results=100):
    print('getting video search results')
    
    next_page_token = None

    while True:
        #Use YouTube .search() to search for top 100 videos returned, given a specific query (q)
        search_response = youtube.search().list(
            q=query,
            type='video',
            part='id',
            maxResults=min(50, max_results - len(video_id_list)),
            pageToken=next_page_token
        )
        response = search_response.execute()

        # Extract the videoId from the returned object.
        for item in response['items']:
            video_id = item['id']['videoId']
            video_id_list.append(video_id)
            
        if 'nextPageToken' in response:
            next_page_token = response['nextPageToken']
        else:
            break

        if len(video_id_list) >= max_results:
            break

    return video_id_list

#Function to retrieve the comments given a video Id
def get_video_comments(youtube, vidId, token=''):
    global video_counter

    print('Getting comments for videoId', vidId)
    video_counter += 1
    global video_comments_list

    #check if video_comments_list has anything in it so we can clear it before 
    #doing analysis on the other comments.
    if video_comments_list:
        video_comments_list = []

    #Call get_video_performance() for like and comment count retrieval
    get_video_performance(vidId)

    #Retrieve the comments
    try:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=vidId,
            maxResults=5,
            pageToken=token
        )
        response = request.execute()

        for item in response['items']:
            # Tauthor = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            Ttext = item['snippet']['topLevelComment']['snippet']['textDisplay']
            #html encoding
            Ttext = html.unescape(Ttext)
            #data cleaning
            Ttext = data_cleaning(Ttext)
            #Add comment text to combined comment list.
            comment_list.append([Ttext])
            #Add comment to comment sublist per video
            video_comments_list.append([Ttext])
        #Export to csv for manual accuracy testing.
        if video_counter == random_number1 or video_counter == random_number2 :
            sentiment_analysis.perform_analysis(video_comments_list, True)
        else: sentiment_analysis.perform_analysis(video_comments_list, False)     

    except HttpError as e:
        error_response = e.content.decode('utf-8')
        error_message = e._get_reason()
        if "commentsDisabled" in error_response:
            print('Comments are disabled for this video.')
            video_comments_list.append('Comments Disabled')


    #Update the sentiment scores.
    sentiment_score.append(sentiment_analysis.sentiment_distribution)
    #Clear sentiment_distribution to prevent stacking
    sentiment_analysis.sentiment_distribution = 0.0
    
#Function to retrieve the amount of likes on each video by id.
def get_video_performance(vid_Id):

    #Make api call for video data
    request = youtube.videos().list(part='statistics', id=vid_Id)
    response = request.execute()

    #Get like count
    try:
        like_count = response['items'][0]['statistics']['likeCount']
        likes.append(int(like_count))
    except KeyError as e:
        like_count = 1
        likes.append(like_count)

    #Get comment count
    try:
        #Get comment count
        comment_count = response['items'][0]['statistics']['commentCount']
        comments.append(int(comment_count))
    except KeyError as e:
        comment_count = 1
        comments.append(comment_count)

#Function to initiate the retrieval of comments for all the video ids in list
def get_comments_per_vid_id(vidIdsList):
    for vid_id in vidIdsList:
        get_video_comments(youtube, vid_id)

#Function to create a csv file with the retrieved text data.
def generate_csv(videos_comments):
    print('Generating new csv file')
    file_path = 'D:\capstoneProject\comments.csv'
    if os.path.isfile(file_path):
        os.remove(file_path)

    with open('comments.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['Comment', 'Sentiment']
        thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        thewriter.writeheader()

        for data in videos_comments:
            sentiment_dict = eval(data['Sentiment'])
            data['Sentiment'] = sentiment_dict
            thewriter.writerow(data)

# Call the functions
# get_video_ids(youtube, query)
# get_comments_per_vid_id(get_video_ids(youtube, query))
# check_comment_csv()
# generate_csv()


    
