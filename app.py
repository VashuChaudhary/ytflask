from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from downloader import download_video
import os

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        # Validate YouTube url as before...
        try:
            filepath = download_video(url)  # Downloads to server temp dir
            filename = os.path.basename(filepath)
            # Send the video as an HTTP attachment to the browser
            return send_file(filepath, as_attachment=True, download_name=filename)
        except Exception as e:
            flash(f"Download failed: {str(e)}", "error")
            return redirect(url_for("index"))
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
