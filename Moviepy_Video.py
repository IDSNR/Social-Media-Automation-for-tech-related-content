import moviepy.video.fx.all as vfx
import math
import srt
import pysrt
import json
from moviepy import editor
from moviepy.video.fx import resize
import moviepy
import os
from PIL import Image
import numpy as np
from moviepy.editor import ImageClip, concatenate_videoclips, vfx, VideoFileClip, AudioFileClip, ColorClip, CompositeVideoClip, TextClip, VideoClip
import random
from pprint import pprint
import csv

def do_random(doit):
    if doit:
        def lower_func(x):

            return x ** (x / 1.4)

        def get_random_json_data(path, type, id):
            rating = random.uniform(0.0, 10.0)
            duration = random.uniform(1.0, 2.5)
            transition = ["Crossfade", "Slide", "Wipe", "Zoom-In"][random.randint(0, 3)]
            zoom_effect = random.uniform(1.0, 1.4)
            zoom_focus = ["Center", "Upper left corner", "Upper right corner", "Lower left corner", "Lower right corner", "Left", "Right", "Top", "Bottom"][random.randint(0, 8)]
            return {
                "rating": rating,
                "duration": duration,
                "transition_out": transition,
                "zoom_effect": lower_func(zoom_effect),
                "zoom_focus": zoom_focus,
                "path": path,
                "type": type,
                "id": id
            }

        def item_is_folder(path):
            if os.path.isdir(path):
                return True
            return False

        directory = 'Videos/Images'

        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)

            if item == "Json":
                continue

            with open("Videos/Data.json", "r") as file:
                data_img = json.load(file)

            if item_is_folder(item_path):
                with open(os.path.join(item_path, 'Compilation_data.json'), 'w') as file:
                    json.dump(get_random_json_data(os.path.join(item_path, 'Video.mp4'), "Video", item), file, indent=2)
            else:
                try:
                    with open(directory + f'/Json/{item.replace(".jpg", ".json")}', 'w') as file:
                        json.dump(get_random_json_data(directory+f'/{item}', "Image", data_img[item.replace(".jpg", "")]["id"]), file, indent=2)
                except KeyError as e:
                    os.remove(os.path.join(directory, f'{item}'))
                    print(f"File: {item}, Error: {e}")

def zoom_in_effect(clip, zoom_ratio=0.04, focus_x=0.5, focus_y=0.5):
    def effect(get_frame, t):
        img = Image.fromarray(get_frame(t))
        base_size = img.size

        new_size = [
            math.ceil(img.size[0] * (1 + (zoom_ratio * t))),
            math.ceil(img.size[1] * (1 + (zoom_ratio * t)))
        ]

        new_size[0] = new_size[0] + (new_size[0] % 2)
        new_size[1] = new_size[1] + (new_size[1] % 2)

        img = img.resize(new_size, Image.LANCZOS)

        x = math.ceil(focus_x * (new_size[0] - base_size[0]))
        y = math.ceil(focus_y * (new_size[1] - base_size[1]) / 2)

        img = img.crop((
            x, y, x + base_size[0] , y + base_size[1]
        )).resize(base_size, Image.LANCZOS)

        result = np.array(img)
        img.close()

        return result
    return clip.fl(effect)

def apply_gradual_zoom_effect(clip, start_zoom, end_zoom, zoom_focus):
    """
    Apply a gradual zoom effect to the clip.

    :param clip: The video clip to apply the effect to.
    :param start_zoom: The starting zoom factor.
    :param end_zoom: The ending zoom factor.
    :param zoom_focus: The focus point for the zoom effect.
    :return: The video clip with the gradual zoom effect applied.
    """

    def zoom_effect(t):
        zoom_factor = start_zoom + (end_zoom - start_zoom) * (t / clip.duration)
        return zoom_factor

    width, height = clip.size
    center_x, center_y = width // 2, height // 2

    if zoom_focus == 'Upper right corner':
        center_x = width * 0.75
        center_y = height * 0.25
    elif zoom_focus == 'Upper left corner':
        center_x = width * 0.25
        center_y = height * 0.25
    elif zoom_focus == 'Lower right corner':
        center_x = width * 0.75
        center_y = height * 0.75
    elif zoom_focus == 'Lower left corner':
        center_x = width * 0.25
        center_y = height * 0.75
    elif zoom_focus == 'Left':
        center_x = width * 0.25
    elif zoom_focus == 'Right':
        center_x = width * 0.75
    elif zoom_focus == 'Top':
        center_y = height * 0.25
    elif zoom_focus == 'Bottom':
        center_y = height * 0.75

    def zoom_at_time(t):
        z = zoom_effect(t)
        new_clip = clip.resize(z).crop(x_center=center_x, y_center=center_y, width=width/z, height=height/z)
        return new_clip.duration

    # Apply the zoom effect
    return clip.fl_time(lambda t: zoom_at_time(t), apply_to=['mask', 'audio'])

def item_is_folder(path):
    if os.path.isdir(path):
        return True
    return False

def slide_in(clip, duration, side='left'):
    """
    Slide a clip into the frame from the specified side.

    :param clip: The video clip to apply the effect to.
    :param duration: Duration of the slide effect.
    :param side: Side from which the clip slides in ('left', 'right', 'top', 'bottom').
    :return: The video clip with the slide-in effect applied.
    """
    w, h = clip.size

    def slide(t):
        if side == 'left':
            return (int(-w * (1 - t / duration)), 0)
        elif side == 'right':
            return (int(w * (1 - t / duration)), 0)
        elif side == 'top':
            return (0, int(-h * (1 - t / duration)))
        elif side == 'bottom':
            return (0, int(h * (1 - t / duration)))
        else:
            raise ValueError("Invalid side. Choose from 'left', 'right', 'top', 'bottom'.")

    return clip.set_position(slide)

def wipe_transition(clip, duration=1, direction='left'):
    width, height = clip.size
    assert direction in ['left', 'right', 'up', 'down']

    def invert_frame(frame):
        return 255 - frame

    # Create a mask clip that will animate the wipe effect
    def make_frame(t):
        progress = t / duration  # Progress of the transition
        mask = np.ones((height, width), dtype="uint8") * 255  # Start with a fully visible mask

        if direction == 'left':
            wipe_position = int(progress * width)
            mask[:, wipe_position:] = 0  # Hide part of the frame
        elif direction == 'right':
            wipe_position = int((1 - progress) * width)
            mask[:, :wipe_position] = 0
        elif direction == 'up':
            wipe_position = int((1 - progress) * height)
            mask[:wipe_position, :] = 0
        elif direction == 'down':
            wipe_position = int(progress * height)
            mask[wipe_position:, :] = 0

        return mask

    mask_clip = VideoClip(make_frame, duration=duration).set_duration(duration).set_ismask(True)

    # Apply the mask to the clip
    video_with_wipe = clip.set_mask(mask_clip)
    return video_with_wipe.set_duration(duration).fl_image(invert_frame)

def apply_transition_effect(clip, transition_type, duration):
    """
    Apply transition effects to the clip based on the transition type.

    :param clip: The video clip to apply the effect to.
    :param transition_type: The type of transition effect ('Crossfade', 'Slide', 'Wipe', 'Zoom-In').
    :param duration: Duration of the transition effect.
    :return: The video clip with the transition effect applied.
    """
    clip = clip.subclip(t_end=(0, 0, duration))
    if transition_type == 'Crossfade':
        # Apply crossfade effect
        return clip.crossfadein(duration)

    elif transition_type == 'Slide':
        # Apply slide effect (slide-in from the left)
        return slide_in(clip, duration, side=['left', 'right', 'top', 'bottom'][random.randint(0, 3)])

    elif transition_type == 'Wipe':
        # Apply a wipe effect using a fading color clip
        return wipe_transition(clip, duration=duration, direction=['left', 'up', 'right', 'down'][random.randint(0, 3)])

    elif transition_type == 'Zoom-In':

        subclip = clip.subclip(t_start=(0, 0, duration-0.2))
        clip = clip.subclip(t_end=(0, 0, 0.2))

        subclip = subclip.resize(lambda t: 1 + 0.30 * t)
        clip = concatenate_videoclips([clip, subclip])

        return clip

    else:
        raise ValueError(f"Unsupported transition type: {transition_type}")

index = 0

def compile_video(dicts, doit, ratio_video_all=1.5):
    audio = AudioFileClip('Videos/Audio/Audio.wav')
    duration_audio = audio.duration

    ids = []

    global index
    if not doit:
        return None
    dicts_a = sorted(dicts, key=lambda x: x['rating'], reverse=True)
    clips = []
    duration_now = 0
    dicts = []
    for i in dicts_a:
        duration_now += i["duration"]
        if duration_audio * ratio_video_all < duration_now:
            break
        dicts.append(i)

    for item in dicts:
        # Load the media
        if item['type'] == 'Image':
            clip = ImageClip(item['path'])
        elif item['type'] == 'Video':
            clip = VideoFileClip(item['path'])
        else:
            raise ValueError(f"Unsupported media type: {item['type']}")

        clip = clip.set_duration(item['duration'])

        end_zoom = item['zoom_effect']
        zoom_focus = item['zoom_focus']
        x, y = 0.5, 0.5
        if zoom_focus == 'Upper left corner':
            x, y = 0.25, 0.25
        elif zoom_focus == 'Upper right corner':
            x, y = 0.75, 0.25
        elif zoom_focus == 'Right':
            x, y = 0.75, 0.5
        elif zoom_focus == 'Bottom':
            x, y = 0.5, 0.75
        elif zoom_focus == 'Left':
            x, y = 0.25, 0.5
        elif zoom_focus == 'Top':
            x, y = 0.5, 0.25
        elif zoom_focus == 'Lower left corner':
            x, y = 0.25, 0.75
        elif zoom_focus == 'Lower right corner':
            x, y = 0.75, 0.75

        clip = zoom_in_effect(clip, zoom_ratio=end_zoom-1, focus_x=x, focus_y=y)

        assert clip.duration == item["duration"]

        transition_out = item['transition_out']
        clip = apply_transition_effect(clip, transition_out, item['duration'])

        ids.append(item["id"])

        '''
        os.makedirs(f"Tests/{index}", exist_ok=True)
        clip.write_videofile(f'Tests/{index}/{index}.mp4', fps=24)
        with open(f"Tests/{index}/{index}.json", "w") as file:
            json.dump(item, file, indent=2)
        index += 1
        '''

        clips.append(clip)

    with open("Videos/delete.csv", "a", newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(ids)

    final_clip = concatenate_videoclips(clips, method="compose")

    final_clip = final_clip.volumex(0.0)
    assert final_clip.duration >= duration_audio
    final_clip = final_clip.subclip(0, audio.duration)
    final_clip = final_clip.set_audio(audio)

    # Write the final video to a file
    final_clip.write_videofile("Videos/Done/Video_nosubs.mp4")

def load(doit=True):
    if not doit:
        return None
    directory = 'Videos/Images'
    all_data = []
    for i in os.listdir(directory):
        if i == "Json":
            continue
        if i[-4:] == ".jpg":
            with open(os.path.join(directory, f'Json/{i.replace(".jpg", ".json")}'), 'r') as file:
                data = json.load(file)
                all_data.append(data)
        if item_is_folder(os.path.join(directory, i)):
            with open(os.path.join(directory, i, 'Compilation_data.json'), 'r') as file:
                data = json.load(file)
                all_data.append(data)
    return all_data

def split_into_threes_and_fours(number):
    result = []

    while number > 0:
        if number % 4 == 0 or number == 4:
            result.append(4)
            number -= 4
        else:
            result.append(3)
            number -= 3

    return result

def time_to_seconds(time_obj):
    return time_obj.hours * 3600 + time_obj.minutes * 60 + time_obj.seconds + time_obj.milliseconds / 1000

def add_srt(doit):
    if not doit:
        return None

    def create_subtitle_clip(subtitle, start, end, videosize=(1080, 1920), fontsize=24, font='Arial', color='yellow'):

        duration = end - start

        video_width, video_height = videosize

        text_clip = TextClip(subtitle, fontsize=fontsize, font=font, color=color, bg_color='black',
                            size=(video_width * 3 / 4, None), method='caption').set_start(start).set_duration(
            duration)
        subtitle_x_position = (video_width - text_clip.w) // 2
        subtitle_y_position = video_height * 4 / 5

        text_position = (subtitle_x_position, subtitle_y_position)

        return text_clip.set_position(text_position)

    to_compile = []
    video = VideoFileClip('Videos/Done/Video_nosubs.mp4')
    subtitles = pysrt.open('Videos/Audio/SRT.srt')
    for index_nnn, i in enumerate(subtitles):
        start = time_to_seconds(i.start)
        end = time_to_seconds(i.end)
        duration = end - start
        content = i.text.upper()
        words = content.split(" ")
        n_words = len(words)
        interval = duration / n_words
        numbers = split_into_threes_and_fours(n_words)
        index_now = 0
        for index_nn, k in enumerate(numbers):
            mini_phrase = " ".join(words[index_now:index_now + k])
            mini_phrase_words = words[index_now:index_now + k]
            for j in range(k):
                to_compile.append({
                    "start": start,
                    "end": start + interval,
                    "whole_phrase": content,
                    "mini_phrase": mini_phrase,
                    "highlight": words[index_now + j],
                    "letter_n": j,
                    "numbers_n": index_nn,
                    "phrase_n": index_nnn,
                    "before": " ".join(mini_phrase_words[0:j]),
                    "after": " ".join(mini_phrase_words[j+1:])
                })
                start += interval
            index_now += k

    subtitles = []
    for i in to_compile:
        subtitles.append(CompositeVideoClip([create_subtitle_clip(i["before"], i["start"], i["end"], color='white'), create_subtitle_clip(i["highlight"], i["start"], i["end"], color='yellow'), create_subtitle_clip(i["after"], i["start"], i["end"], color='white')]))
    subtitles_compiled = CompositeVideoClip(subtitles)
    final_video = CompositeVideoClip([video] + [subtitles_compiled])

    final_video.write_videofile('Videos/Done/Video.mp4')

if __name__ == '__main__':
    do_random(False)
    compile_video(load(True), True)
    add_srt(False)

