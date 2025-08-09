# downloader.py
import yt_dlp
import os
import uuid

DOWNLOAD_DIR = "downloads"

def download_video(url):
    """Downloads a YouTube video and returns the absolute path to the file."""
    import re
    YT_REGEX = r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$"
    if not re.match(YT_REGEX, url):
        raise ValueError("Invalid YouTube URL.")

    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    # Use only title for filename, avoid uuid for easier debugging
    output_template = os.path.join(DOWNLOAD_DIR, "%(title).80s.%(ext)s")

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": output_template,
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            # Sometimes yt-dlp appends .mkv if mp4 merge fails
            if not os.path.exists(filename):
                alt_filename = os.path.splitext(filename)[0] + ".mkv"
                if os.path.exists(alt_filename):
                    filename = alt_filename
                else:
                    raise FileNotFoundError("Downloaded file not found.")
            return os.path.abspath(filename)
    except Exception as e:
        # Log error for debugging
        print(f"Error downloading video: {e}")
        raise
