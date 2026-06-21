import requests
import os
import re
import subprocess

url = os.environ["YOUTUBE_URL"]

video_id = re.search(r"(?:v=|shorts/)([a-zA-Z0-9_-]{11})", url)
if not video_id:
    print("Invalid URL")
    exit(1)
video_id = video_id.group(1)

servers = [
    "https://invidious.snopyta.org",
    "https://yewtu.be",
    "https://invidious.kavin.rocks"
]

download_url = None
for server in servers:
    try:
        res = requests.get(f"{server}/api/v1/videos/{video_id}", timeout=10).json()
        formats = res.get("formatStreams", [])
        mp4 = [f for f in formats if f.get("container") == "mp4"]
        if mp4:
            download_url = mp4[0]["url"]
            print(f"Found on: {server}")
            break
    except:
        continue

if not download_url:
    print("All servers failed!")
    exit(1)

subprocess.run(["wget", "-O", "video.mp4", download_url], check=True)

size = os.path.getsize("video.mp4")
print(f"File size: {size} bytes")
if size < 1000:
    print("Download failed!")
    exit(1)
print("Success!")
