import requests
import os
import re
import subprocess

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

res = requests.get(
    f"https://yt-api.p.rapidapi.com/dl?id={video_id}",
    headers=headers
).json()

all_formats = res.get("formats", []) + res.get("adaptiveFormats", [])
mp4_video = [f for f in all_formats if "video/mp4" in f.get("mimeType", "") and f.get("url")]

if not mp4_video:
    print("No MP4 found!")
    exit(1)

best = sorted(mp4_video, key=lambda x: int(x.get("qualityLabel", "0p").replace("p", "")), reverse=True)[0]
download_url = best["url"]

print(f"Quality: {best.get('qualityLabel')}")
subprocess.run(["wget", "-O", "video.mp4", download_url], check=True)

size = os.path.getsize("video.mp4")
print(f"File size: {size} bytes")
if size < 1000:
    print("Download failed!")
    exit(1)
print("Success!")
