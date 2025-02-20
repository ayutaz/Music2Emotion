import os
import sys
import yt_dlp
from music2emo import Music2emo

def download_audio_from_youtube(url, output_dir="inference/input"):
    # 出力ディレクトリがなければ作成
    os.makedirs(output_dir, exist_ok=True)
    
    # yt_dlpのオプション設定（出力ファイル名は固定: tmp.mp3）
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, 'tmp.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
        'quiet': True,
    }
    
    # yt_dlpで情報抽出とダウンロードを実施
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get('title', 'Unknown Title')
    
    # 固定ファイル名tmp.mp3を指定
    output_file = os.path.join(output_dir, "tmp.mp3")
    return output_file, title

def main():
    # コマンドライン引数からURLを取得
    if len(sys.argv) < 2:
        print("使い方: python sample_youtube.py <YouTube URL>")
        sys.exit(1)
    
    input_audio = sys.argv[1]
    
    # URLの場合はダウンロードしてmp3に変換
    if input_audio.startswith("http"):
        input_audio, video_title = download_audio_from_youtube(input_audio)
    else:
        # URLでなければローカルファイルとみなす
        video_title = os.path.basename(input_audio)
    
    # Music2emoで音楽感情認識を実行
    music2emo = Music2emo()
    output_dic = music2emo.predict(input_audio)
    
    valence = output_dic["valence"]
    arousal = output_dic["arousal"]
    predicted_moods = output_dic["predicted_moods"]
    
    # 結果表示（動画タイトルを含む）
    print(f"\n🎵 **Music Emotion Recognition Results [{video_title}]** 🎵")
    print("-" * 50)
    print(f"🎭 **Predicted Mood Tags:** {', '.join(predicted_moods) if predicted_moods else 'None'}")
    print(f"💖 **Valence:** {valence:.2f} (Scale: 1-9)")
    print(f"⚡ **Arousal:** {arousal:.2f} (Scale: 1-9)")
    print("-" * 50)

if __name__ == "__main__":
    main()
