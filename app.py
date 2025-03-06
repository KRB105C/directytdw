from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route("/download", methods=["GET"])
def download_video():
    url = request.args.get("url")  # Ambil URL dari parameter
    if not url:
        return jsonify({"error": "URL video YouTube diperlukan"}), 400

    ydl_opts = {
        "format": "bv",  # Ambil kualitas terbaik
        "outtmpl": "%(title)s.%(ext)s",  # Simpan sesuai judul video
        "merge_output_format": "mp4",  # Format output
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)  # Download video
            video_title = info.get("title", "video")
            video_filename = f"{video_title}.mp4"

        return jsonify({
            "success": True,
            "title": info["title"],
            "duration": info["duration"],
            "uploader": info["uploader"],
            "upload_date": info["upload_date"],
            "webpage_url": info["webpage_url"],
            "filename": video_filename,
            "path": os.path.abspath(video_filename)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
