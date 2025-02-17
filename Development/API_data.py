from googleapiclient.discovery import build
import pandas as pd
import os

API_KEY = os.getenv('YT_API_KEY')

if API_KEY is None:
    raise ValueError("API Key not found. Set the YT_API_KEY environment variable. \
        Refer to API_Key documentation by Youtube to create your own to run the file: \
            https://console.cloud.google.com/apis")

youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_video_comments(video_id, max_results=100):
    comments = []
    next_page_token = None
    
    while len(comments) < max_results:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            maxResults=min(100, max_results - len(comments)),
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "comment": comment["textDisplay"],
                "author": comment["authorDisplayName"],
                "published_at": comment["publishedAt"],
                "like_count": comment["likeCount"],
                "reply_count": item["snippet"]["totalReplyCount"]
            })
        
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
    
    return pd.DataFrame(comments)

    

video_id = "32t8AJx5FLE"
df = get_video_comments(video_id, max_results=200)

# Save data to CSV for further analysis
# df.to_csv("youtube_comments.csv", index=False)

print(df.head()[['comment']])