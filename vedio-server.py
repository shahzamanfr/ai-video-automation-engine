
import os
import base64
import uuid
import subprocess
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
TEMP_DIR = os.path.join(BASE_DIR, "temp")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/create-video", methods=["POST"])
def create_video():
    try:
        payload = request.json or {}

        name = payload.get("name", "video")
        images = payload.get("images", [])
        audio_base64 = payload.get("audio")
        captions_base64 = payload.get("captions")

        if not images:
            raise ValueError("No images received")
        if not audio_base64:
            raise ValueError("No audio received")

        job_id = uuid.uuid4().hex
        job_dir = os.path.join(TEMP_DIR, job_id)
        os.makedirs(job_dir, exist_ok=True)

        # ---------------- SAVE IMAGES ----------------
        image_files = []
        for i, img in enumerate(images):
            fname = f"img_{i}.png"
            with open(os.path.join(job_dir, fname), "wb") as f:
                f.write(base64.b64decode(img))
            image_files.append(fname)

        # ---------------- SAVE AUDIO ----------------
        audio_path = os.path.join(job_dir, "audio.mp3")
        with open(audio_path, "wb") as f:
            f.write(base64.b64decode(audio_base64))

        # ---------------- AUDIO DURATION ----------------
        duration = float(subprocess.check_output([
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            audio_path
        ]).decode().strip())

        # ---------------- SAVE SRT ----------------
        has_captions = False
        if captions_base64:
            srt_path = os.path.join(job_dir, "captions.srt")
            with open(srt_path, "w", encoding="utf-8") as f:
                f.write(base64.b64decode(captions_base64).decode("utf-8"))
            has_captions = os.path.getsize(srt_path) > 10

        # ---------------- IMAGES.TXT ----------------
        img_duration = duration / len(image_files)
        with open(os.path.join(job_dir, "images.txt"), "w", encoding="utf-8") as f:
            for img in image_files:
                f.write(f"file '{img}'\n")
                f.write(f"duration {img_duration}\n")
            f.write(f"file '{image_files[-1]}'\n")

        # ---------------- CONVERT SRT → ASS ----------------
        if has_captions:
            subprocess.run(
                ["ffmpeg", "-y", "-i", "captions.srt", "captions.ass"],
                cwd=job_dir,
                check=True
            )

        # ---------------- OUTPUT ----------------
        output_name = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        output_path = os.path.join(OUTPUT_DIR, output_name)

        # ---------------- FFMPEG (FINAL) ----------------
        cmd = [
            "ffmpeg",
            "-y",
            "-fflags", "+genpts",
            "-f", "concat",
            "-safe", "0",
            "-i", "images.txt",
            "-i", "audio.mp3",
        ]

        if has_captions:
            cmd += ["-vf", "ass=captions.ass"]

        cmd += [
            "-pix_fmt", "yuv420p",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-shortest",
            output_path
        ]

        subprocess.run(cmd, cwd=job_dir, check=True)

        with open(output_path, "rb") as f:
            video_b64 = base64.b64encode(f.read()).decode("utf-8")

        return jsonify({
            "success": True,
            "filename": output_name,
            "duration": round(duration, 2),
            "video_data": video_b64
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    print("🚀 Video server running at http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)                                                                                                                                                                                                                                                                                                                                                                                                                                             
