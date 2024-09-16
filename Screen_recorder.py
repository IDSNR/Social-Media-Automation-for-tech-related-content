import cv2
from PIL import ImageGrab
import numpy as np
from screeninfo import get_monitors
import os
import time
import pyaudio
import threading
import wave
from moviepy.editor import VideoFileClip, AudioFileClip

def record_audio():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    frames = []
    now = time.time()
    try:
        while time.time() > now + 50:
            data = stream.read(1024)
            frames.append(data)
    except KeyboardInterrupt as KI:
        pass

    stream.stop_stream()
    stream.close()
    audio.terminate()

    sound_file = wave.open("Videos/Audio/Audio.wav", 'wb')
    sound_file.setnchannels(1)
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(44100)
    sound_file.writeframes(b''.join(frames))
    sound_file.close()

def main(running):
    '''    def record_audio(wave_output_filename):
        CHUNK = 1024  # Audio chunk size
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = 60  # Set duration

        p = pyaudio.PyAudio()

        # Open stream for recording audio
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        frames = []

        while nonlocal_running:
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        # Save the recorded audio as a WAV file
        wf = wave.open(wave_output_filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    wf.close()'''

    def real_main():
        # Ensure output directory exists
        if not os.path.exists("Videos/Done"):
            os.makedirs("Videos/Done")

        # Video encoding setup
        fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
        captured_video = cv2.VideoWriter("Videos/Done/Video_nosubs.mp4", fourcc, 30.0, (608, 1080))

        '''audio_output = "Videos/Done/audio.wav"
        audio_thread = threading.Thread(target=record_audio, args=(audio_output,))
        audio_thread.start()'''

        # Find primary monitor
        monitor = None
        for m in get_monitors():
            if m.is_primary:
                monitor = m
                break

        if monitor is None:
            print("Primary monitor not found!")
            return

        now = time.time()

        while time.time() < now + 50:
            screen_width = 1920
            screen_height = 1080

            capture_width = 608
            capture_height = 1080

            # Calculate top-left coordinates to center the capture
            left = (screen_width - capture_width) // 2
            top = (screen_height - capture_height) // 2

            bbox = (left, top, left + capture_width, top + capture_height)

            # Capture screen center
            img = ImageGrab.grab(bbox=bbox)
            np_image = np.array(img)
            cvt_img = cv2.cvtColor(np_image, cv2.COLOR_BGR2RGB)

            captured_video.write(cvt_img)

        captured_video.release()

    real_main()

def compile():
    video = VideoFileClip("Videos/Done/Video_nosubs.mp4")
    

if __name__ == '__main__':
    compile()
