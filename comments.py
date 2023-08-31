from googleapiclient.discovery import build
import credentials

#global variables
comment_list = []
video_id_list = []
query = 'Something to search'

# Connect to the YouTube API
youtube = build('youtube', 'v3', developerKey=credentials.capstone_API_Key)

#Function to perform a search and retrieve top 5 - 10 video Ids returned.
def get_video_results(youtube):
    print('getting video search results')

    #Use YouTube .search() to search for top 5 videos returned, given a specific query (q)
    search_response = youtube.search().list(
        q=query,
        type='video',
        part='id',
        maxResults=5
    )
    response = search_response.execute()

    # Extract the videoId from the return object.
    for item in response['items']:
        video_id = item['id']['videoId']
        # print(video_id)
        video_id_list.append(video_id)

    return video_id_list

#Function to retrieve the comments given a video Id
def get_video_comments(youtube, vidId, token=''):
    print('Getting comments for videoId', vidId)

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
        # What information from the comment do I need in the list. Possibly just the text.
        #Maybe it makes sense to store the comment in a dictionary so we can search for comment per video id.
        comment_list.append([Ttext])

#Function to retrieve comments for each video id provided.
def get_comments_per_vid_id(vidIdsList):
    for vid_id in vidIdsList:
        get_video_comments(youtube, vid_id)


# To test that the comments were retrieved per Id.
get_comments_per_vid_id(get_video_results(youtube))
for item in comment_list:
    print(item)

# To test that the video id were retrieved. 
# get_video_results(youtube)
# for item in top_video_id_list:
#     print(item)

# To test that comments were retrieved
# get_video_comments(youtube, vid_id)
# for item in comment_list:
#     print(item)

#Function for cleaning the text for analyzing
#Function for exporting

    
