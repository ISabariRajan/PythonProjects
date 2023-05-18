from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

import json

config = {}
with open("config.json", "r") as f:
    config = json.loads("".join(f.readlines()))

# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
API_KEY = config["youtube-data-api"]
API_NAME = "youtube"
API_VERSION = "v3"

def scrape_youtube_comments(video_id):
    # Set up the YouTube API client
    youtube = build(API_NAME, API_VERSION, developerKey=API_KEY)
    print(video_id)

    # # Get the video ID from the user
    # video_id = input("Enter the video ID: ")

    # Call the YouTube API to retrieve the comments
    comments = []
    next_page_token = None
    quota_exceeded = False
    while True:
        try:
            response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                pageToken=next_page_token,
                
            ).execute()
            print(response.keys())
            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"].replace("\n", "<br>").replace("\r", "")
                author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
                likes = item["snippet"]["topLevelComment"]["snippet"]["likeCount"]
                reply_count = item["snippet"]["totalReplyCount"]
                comments.append((author, comment, likes, reply_count))
            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break
        except HttpError as error:
            if error.resp.status == 403:
                error_message = error._get_reason().strip()
                if error_message.startswith("The request cannot be completed because you have exceeded your "):
                    quota_exceeded = True
                    quota_limit = int(error_message.split()[-1])
                    break
                else:
                    raise error
            else:
                raise error

    if quota_exceeded:
        return {
            "success": False,
            "message": f"Quota Exceeded, Quota Limit: {quota_limit}"
        }
    else:
        return {
            "success": True,
            "data": comments
        }
        # # Print the comments with the user who commented, likes, and the number of replies
        # for author, comment, likes, reply_count in comments:
        #     print(f"{author}: {comment}")
        #     print(f"Likes: {likes}, Replies: {reply_count}")
        #     print()
