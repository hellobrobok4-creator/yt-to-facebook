import requests
import os
import re

url = os.environ["YOUTUBE_URL"]
api_key = os.environ["RAPIDAPI_KEY"]

video_id = re.search(r"(?:v=|shorts/)([a-zA-Z0-9_-]{11})", url)
if not video_id:
    print("Invalid URL")
    exit(1)
video_id = video_id.group(1)

headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "yt-api.p.rapidapi.com"
}

print(f"Getting video info for: {video_id}")
res = requests.get(
    f"https://yt-api.p.rapidapi.com/dl?id={video_id}",
    headers=headers
).json()

print(f"Response keys: {list(res.keys())}")

formats = res.get("formats", [])
mp4_formats = [f for f in formats if "video/mp4" in f.get("mimeType", "") and f.get("url")]

if not mp4_formats:
    print(f"No MP4 found. Available formats: {[f.get('mimeType') for f in formats]}")
    exit(1)

best = sorted(mp4_formats, key=lambda x: int(x.get("qualityLabel", "0p").replace("p", "")), reverse=True)[0]
download_url = best["url"]

print(f"Downloading quality: {best.get('qualityLabel')}")
r = requests.get(download_url, stream=True, headers={"User-Agent": "Mozilla/5.0"})

with open("video.mp4", "wb") as f:
    for chunk in r.iter_content(chunk_size=8192):
        if chunk:
            f.write(chunk)

size = os.path.getsize("video.mp4")
print(f"Downloaded! File size: {size} bytes")

if size < 1000:
    print("File too small, download failed!")
    exit(1)
