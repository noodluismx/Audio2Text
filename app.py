from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from pydub import AudioSegment
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "audio_data" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    try:
        # Save uploaded WebM file
        webm_path = os.path.join(UPLOAD_FOLDER, "recorded.webm")
        wav_path = os.path.join(UPLOAD_FOLDER, "converted.wav")
        request.files["audio_data"].save(webm_path)

        # Convert WebM to WAV
        audio = AudioSegment.from_file(webm_path, format="webm")
        audio.export(wav_path, format="wav")

        # Transcribe WAV
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language="en-US")

        return jsonify({"transcription": text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
