from IPython import get_ipython
import os
from pydub import AudioSegment
from whisperspeech.pipeline import Pipeline
import numpy as np
from gtts import gTTS
import soundfile as sf

def text_to_speech(text, output_path):
    tts = gTTS(text=text, lang='en')
    tts.save(output_path)

voices = ["Audios/Martin Luther King.mp3", "Audios/Nietszche pod.mp3","Audios/Steve Jobs.mp3", "https://upload.wikimedia.org/wikipedia/commons/7/75/Winston_Churchill_-_Be_Ye_Men_of_Valour.ogg"]

pipe = Pipeline(s2a_ref='collabora/whisperspeech:s2a-q4-base-en+pl.model', device="cuda")

with open('Videos/Audio/Script.txt', "r") as file:
    text = file.read()


text_split = text.split(" ")
len_text = len(text_split)

text_split_1 = text_split[:len_text//2]
text_split_2 = text_split[len_text//2:]

text1 = " ".join(text_split_1)
text2 = " ".join(text_split_2)

def get_audio():
    audio1 = pipe.generate(text1, lang="en")
    audio2 = pipe.generate(text2, lang="en")
    return audio1, audio2

def get_audio_text(texto1, texto2):
    audio1 = pipe.generate(texto1, lang="en")
    audio2 = pipe.generate(texto2, lang="en")
    return audio1, audio2


def get_audio_speaker(speaker: int):
    audio1 = pipe.generate(text1, lang="en", speaker=voices[speaker])
    audio2 = pipe.generate(text2, lang="en", speaker=voices[speaker])
    return audio1, audio2

def load_it_in(audio, output_path, format="wav"):
    audio_np = (audio.cpu().numpy() * 32767).astype(np.int16)

    if len(audio_np.shape) == 1:
        audio_np = np.expand_dims(audio_np, axis=0)
    else:
        audio_np = audio_np.T

    try:
        audio_segment = AudioSegment(
            audio_np.tobytes(),
            frame_rate=24000,
            sample_width=2,
            channels=1
        )
        audio_segment.export(output_path, format=format)
        print(f"Audio file generated: Audio.{format}")
    except Exception as e:
        print(f"Error writing audio file: {e}")

def concatenate_audios(audio1_path, audio2_path, output_path):
    # Load the audio files
    audio1, samplerate1 = sf.read(audio1_path)
    audio2, samplerate2 = sf.read(audio2_path)

    # Ensure both audios have the same sample rate
    if samplerate1 != samplerate2:
        raise ValueError("Sample rates of the audio files do not match!")

    # Concatenate the audio data
    combined_audio = np.concatenate((audio1, audio2))

    # Export the result to the specified output path
    sf.write(output_path, combined_audio, samplerate1)

    print(f"Concatenated audio saved to: {output_path}")

def main():
    with open('Videos/Audio/Script.txt', "r") as file:
        text = file.read()

    if not text:
        raise ValueError("Must get the script from chat gpt")

    text_split = text.split(" ")
    len_text = len(text_split)

    text_split_1 = text_split[:len_text // 2]
    text_split_2 = text_split[len_text // 2:]

    text1 = " ".join(text_split_1)
    text2 = " ".join(text_split_2)

    print("Started getting the audio")

    audio1, audio2 = get_audio_text(text1, text2)
    load_it_in(audio1, "Videos/Audio/Audio1.wav")
    load_it_in(audio2, "Videos/Audio/Audio2.wav")
    concatenate_audios("Videos/Audio/Audio1.wav", "Videos/Audio/Audio2.wav", "D:/ICTsocials/Videos/Audio/Audio.wav")

    open('Videos/Audio/Script.txt', "w").write('')

if __name__ == '__main__':
    audio1, audio2 = get_audio()
    load_it_in(audio1, "Videos/Audio/Audio1.wav")
    load_it_in(audio2, "Videos/Audio/Audio2.wav")
    concatenate_audios("Videos/Audio/Audio1.wav", "Videos/Audio/Audio2.wav", "Videos/Audio/Audio.wav")