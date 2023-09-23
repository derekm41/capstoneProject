from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import credentials
import csv
import os
from urlextract import URLExtract
import html
from bs4 import BeautifulSoup
import demoji

#global variables
comment_list = []
video_id_list = []
#query = 'crypto'
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

#Function to perform a search and retrieve top 5 - 10 video Ids returned.

#   I NEED TO MAKE SURE I'M CAPTURING ALL COMMENTS FOR ACCURATE DATA
def get_video_ids(youtube, query):
    print('getting video search results')
    print(query)

    #Use YouTube .search() to search for top 5 videos returned, given a specific query (q)
    search_response = youtube.search().list(
        q=query,
        type='video',
        part='id',
        maxResults=3
    )
    response = search_response.execute()

    # Extract the videoId from the returned object.
    for item in response['items']:
        video_id = item['id']['videoId']
        # print(video_id)
        video_id_list.append(video_id)
    print(video_id_list)

    return video_id_list

#Function to retrieve the comments given a video Id
def get_video_comments(youtube, vidId, token=''):
    print('Getting comments for videoId', vidId)

    try:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=vidId,
            maxResults=3,
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
            # What information from the comment do I need in the list. Possibly just the text.
            #Maybe it makes sense to store the comment in a dictionary so we can search for comment per video id.
            comment_list.append([Ttext])


    except HttpError as e:
        error_response = e.content.decode('utf-8')
        error_message = e._get_reason()
        if "commentsDisabled" in error_response:
            print('Comments are disabled for this video.')
    
#Function to retrieve comments for each video id provided.
def get_comments_per_vid_id(vidIdsList):
    for vid_id in vidIdsList:
        get_video_comments(youtube, vid_id)


#Function to create a csv file with the retrieved text data.
def generate_csv():
    print('Generating new csv file')
    file_path = 'D:\capstoneProject\comments.csv'
    if os.path.isfile(file_path):
        os.remove(file_path)

    with open('comments.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        thewriter = csv.writer(csvfile)

        for comment in comment_list:
            text = comment
            thewriter.writerow(text)


# Call the functions
# get_comments_per_vid_id(get_video_ids(youtube))
# check_comment_csv()
# generate_csv()


    
