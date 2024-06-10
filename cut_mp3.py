from pydub import AudioSegment
song = AudioSegment.from_mp3("audio.mp3")
song[0:30*1000].export('audio_30s.mp3') 