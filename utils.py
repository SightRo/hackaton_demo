from io import BytesIO
from pydub import AudioSegment

def wav_to_mp3(wavBinary):
    wav = AudioSegment.from_wav(wavBinary)
    silence = AudioSegment.silent(duration=3000)
    audio = silence + wav + silence
    buffer = BytesIO()
    audio.export(buffer, format="mp3")
    return buffer