# downloader.py
import yt_dlp
import os
import uuid

DOWNLOAD_DIR = "downloads"

def download_video(url):
    """Downloads a YouTube video and returns the absolute path to the file."""
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
    output_template = os.path.join(DOWNLOAD_DIR, f"%(title).80s-{uuid.uuid4().hex[:8]}.%(ext)s")

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": output_template,
        "merge_output_format": "mp4",
        "cookiesfrombrowser": ("chrome",)  # Use Chrome browser cookies
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url)
        filename = ydl.prepare_filename(info)
        # Sometimes yt-dlp appends .mkv if mp4 merge fails
        if not os.path.exists(filename):
            filename = os.path.splitext(filename)[0] + ".mkv"
        return os.path.abspath(filename)
