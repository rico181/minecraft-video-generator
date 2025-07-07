from flask import Flask, render_template, request, jsonify
from gtts import gTTS
from moviepy.editor import *
import os, random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Get user input
        script = request.json.get('script', 'Default Minecraft parkour!')
        duration = int(request.json.get('duration', 30))
        
        # Generate voiceover
        tts = gTTS(text=script, lang='en')
        voice_path = "static/voice.mp3"
        tts.save(voice_path)
        
        # Process video (replace with your Google Drive link)
        video = VideoFileClip("static/source.mp4").subclip(0, duration)
        video = video.set_audio(AudioFileClip(voice_path))
        
        output_path = f"static/output_{random.randint(1000,9999)}.mp4"
        video.write_videofile(output_path, fps=60)
        
        return jsonify({"video": output_path})
    
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    os.makedirs("static", exist_ok=True)
    app.run(debug=True)