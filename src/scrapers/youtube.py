from datetime import datetime, timedelta
from db import get_sync_mongo_conn
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from models.videos import Video, Thumbnail
import os
from pymongo import UpdateOne
from typing import List

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = os.getenv("API_KEY")
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_scrape(API_KEY_POOL: List[str] = []):
    if DEVELOPER_KEY:
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
        sync_db = get_sync_mongo_conn()
        # Call the search.list method to retrieve results matching the specified query term.
        published_after: datetime = datetime.now() - timedelta(seconds=60)

        continue_search: bool = True
        next_page_token: str | None = None

        videos: List[Video] = []
        bulk_write = []

        while continue_search:
            search_params = {
                "q": "football",
                "part": "id,snippet",
                "type": "video",
                "order": "date",
                "publishedAfter": published_after.isoformat() + "Z",
                "maxResults": 50,
            }

            if next_page_token:
                search_response["pageToken"] = next_page_token

            search_response = youtube.search().list(**search_params).execute()

            if not next_page_token:
                # First query to the API
                print("Total Results:")
                print(
                    search_response.get("pageInfo", {}).get(
                        "totalResults",
                    )
                )
            # Add each result to the appropriate list, and then display the lists of matching videos.
            for search_result in search_response.get("items", []):
                if search_result["id"]["kind"] == "youtube#video":
                    video = Video(
                        video_id=search_result["id"]["videoId"],
                        title=search_result["snippet"]["title"],
                        description=search_result["snippet"]["description"],
                        thumbnail=Thumbnail(**search_result["snippet"]["thumbnails"]["default"]),
                        published_at=search_result["snippet"]["publishedAt"],
                    )
                    videos.append(video)

                    video_dict = {k: v for k, v in video.dict().items() if v is not None}
                    bulk_write.append(UpdateOne({"video_id": video.video_id}, {"$set": video_dict}, upsert=True))

            next_page_token = search_response.get("nextPageToken")
            continue_search = bool(next_page_token)

            if len(bulk_write) > 1000:
                sync_db["videos"].bulk_write(bulk_write)
                bulk_write = []

        sync_db["videos"].bulk_write(bulk_write)
        bulk_write = []
