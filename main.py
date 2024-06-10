import os
import whisper
from pydub import AudioSegment
from pydub.silence import split_on_silence

model = whisper.load_model("large")
# model = whisper.load_model("base")

# 使用Whisper本地进行音频转录
def transcribe_audio_whisper(path):
    result = model.transcribe(path, fp16=False)
    text = result['text']
    return text

# 将音频文件按固定时间间隔分割成块，并使用Whisper API进行语音识别的函数
def get_large_audio_transcription_fixed_interval_whisper(path, minutes=10):
    sound = AudioSegment.from_file(path)
    chunk_length_ms = int(1000 * 60 * minutes)
    chunks = [sound[i:i + chunk_length_ms] for i in range(0, len(sound), chunk_length_ms)]

    folder_name = "audio-fixed-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    whole_text = ""
    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.mp3")
        audio_chunk.export(chunk_filename, format="mp3")

        try:
            text = transcribe_audio_whisper(chunk_filename)
        except Exception as e:
            print("Error:", str(e))
        else:
            text = f"{text.capitalize()}. "
            print(chunk_filename, ":", text)
            whole_text += text

    return whole_text

path="audio.mp3"

print("\nFull text:", get_large_audio_transcription_fixed_interval_whisper(path, minutes=1/6))