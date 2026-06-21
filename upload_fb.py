import os
import requests
import sys

PAGE_ID = os.environ["FB_PAGE_ID"]
TOKEN = os.environ["FB_ACCESS_TOKEN"]
YT_URL = os.environ.get("YOUTUBE_URL", "")
CAPTION = os.environ.get("CAPTION", "")

if not CAPTION:
    CAPTION = f"🎬 নতুন ভিডিও!\n\n▶️ YouTube: {YT_URL}\n\n#MuslimVoice #IslamicContent"
else:
    CAPTION = f"{CAPTION}\n\n▶️ YouTube: {YT_URL}"

VIDEO_FILE = "video_vintage.mp4"

if not os.path.exists(VIDEO_FILE):
    print("❌ video_vintage.mp4 পাওয়া যায়নি!")
    sys.exit(1)

file_size = os.path.getsize(VIDEO_FILE)
print(f"📁 ভিডিও সাইজ: {file_size / (1024*1024):.1f} MB")

print("🚀 Facebook আপলোড শুরু...")

start_res = requests.post(
    f"https://graph.facebook.com/v19.0/{PAGE_ID}/videos",
    data={
        "upload_phase": "start",
        "file_size": file_size,
        "access_token": TOKEN,
    }
).json()

if "upload_session_id" not in start_res:
    print(f"❌ Error: {start_res}")
    sys.exit(1)

session_id = start_res["upload_session_id"]
offset = 0
CHUNK_SIZE = 10 * 1024 * 1024

with open(VIDEO_FILE, "rb") as f:
    while True:
        chunk = f.read(CHUNK_SIZE)
        if not chunk:
            break
        transfer = requests.post(
            f"https://graph.facebook.com/v19.0/{PAGE_ID}/videos",
            data={
                "upload_phase": "transfer",
                "upload_session_id": session_id,
                "start_offset": offset,
                "access_token": TOKEN,
            },
            files={"video_file_chunk": chunk}
        ).json()
        offset = int(transfer.get("start_offset", offset))
        print(f"⬆️ আপলোড: {offset / (1024*1024):.1f} MB")

finish = requests.post(
    f"https://graph.facebook.com/v19.0/{PAGE_ID}/videos",
    data={
        "upload_phase": "finish",
        "upload_session_id": session_id,
        "description": CAPTION,
        "access_token": TOKEN,
    }
).json()

if finish.get("success"):
    print("✅ Facebook এ পোস্ট সফল!")
else:
    print(f"❌ Error: {finish}")
    sys.exit(1)
