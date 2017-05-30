from apiclient.discovery import build  # need to build the service object

DEVELOPER_KEY = "AIzaSyDVOMg9cWYeYa93dBf7SXMH5OlaDYShSjQ"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

yt = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

video_ids = []
video_titles = []

res = yt.search().list(q="modeselektor", type="video", part="id,snippet", maxResults=1, order="rating").execute()

for r in res["items"]:
	video_titles.append(r["snippet"]["title"])
	video_ids.append(r["id"]["videoId"])

for i in video_ids:
	res1 = yt.videos().list(part='statistics', id=i).execute()
	for k in res1["items"]:
		print(k['statistics'])

