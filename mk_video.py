import getVids as gV
import Download_drive as Dd
import Scripts
import Posts
import Upload_drive as Ud
import Moviepy_Video as MV
import json
import random
import webbrowser


def load():
    with open("data.json", "r") as file:
        return json.load(file)
data = load()

motivation_keywords = ["motivation", "hard work", "work", "discipline", "persistence", "success", "growth", "achievement", "inspirational", "trading"]
cryptocurrency_news_keyswords = ["cryptocurrency", "trading", "blockchain", "bitcoin", "ethereum", "AI", "future", "science"]
cryptocurrency_education_keywords = cryptocurrency_news_keyswords[:]

day = data["day"] % 3
if day == 0:
    Scripts.main()
    gV.getImages(random.choice(motivation_keywords))
    Posts.get_motivational_post()
    MV.do_random(True)
    MV.compile_video(MV.load(True), True)
elif day == 1:
    Scripts.main()
    Posts.get_meme()
    gV.getImages(random.choice(cryptocurrency_news_keyswords))
    MV.do_random(True)
    MV.compile_video(MV.load(True), True)
elif day == 2:
    Scripts.main()
    gV.getImages(random.choice(cryptocurrency_education_keywords))
    Posts.get_n_post()
    MV.do_random(True)
    MV.compile_video(MV.load(True), True)

Ud.upload()

webbrowser.open('https://colab.research.google.com/drive/12AqmTEwTyp6cvj5HyCMR_5voQAhcapan#scrollTo=ocKGVeqEQGbh')

data["day"] += 1
def post(data):
    with open("data.json", "w") as file:
        json.dump(data, file, indent=2)
post(data)

input("Press enter when the video is ready:")

Dd.main()
