import os
import yt_dlp
from music2emo import Music2emo

def download_audio_from_youtube(url, output_dir="inference/input"):
    os.makedirs(output_dir, exist_ok=True)
    # 出力ファイル名のテンプレートを指定
    output_template = os.path.join(output_dir, "temp.%(ext)s")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    # 変換後のファイル名（上記設定の場合、拡張子はmp3になります）
    output_file = os.path.join(output_dir, "temp.mp3")
    return output_file

# input_audioにYouTubeのURLまたはローカルファイルパスを指定
input_audio = "https://youtu.be/Ljr2wMSBHqU"

# URLが指定された場合、yt-dlpで動画をダウンロードしてmp3に変換する
if input_audio.startswith("http"):
    input_audio = download_audio_from_youtube(input_audio)

# Music2emoで音楽の感情認識を実行
music2emo = Music2emo()
output_dic = music2emo.predict(input_audio)

valence = output_dic["valence"]
arousal = output_dic["arousal"]
predicted_moods = output_dic["predicted_moods"]

print("\n🎵 **Music Emotion Recognition Results** 🎵")
print("-" * 50)
print(f"🎭 **Predicted Mood Tags:** {', '.join(predicted_moods) if predicted_moods else 'None'}")
print(f"💖 **Valence:** {valence:.2f} (Scale: 1-9)")
print(f"⚡ **Arousal:** {arousal:.2f} (Scale: 1-9)")
print("-" * 50)
