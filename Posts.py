import datetime
import praw
import random
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from Data import apikey, clientId, clientSecret # newsapi apikey, reddit cliend id, client secret (hidden)

# from huggingface_hub improt login
# login("[YOUR_HUGGING_FACE_TOKEN_HERE]", add_to_git_credential=True)

global count
count = 0

def get_meme():

    reddit = praw.Reddit(
        client_id=clientId,
        client_secret=clientSecret,
        user_agent='IndertCT#1/0.1 by u/IndertCT'
    )

    # Choose a subreddit and post
    subreddit = reddit.subreddit('CryptoCurrencyMemes')

    def download_and_resize_image(url, output_path, size):
        """
        Downloads an image from the given URL, resizes it, and saves it to the output path.

        :param url: URL of the image to download.
        :param output_path: File path to save the resized image.
        :param size: Tuple (width, height) representing the new size of the image.
        """
        try:
            # Send a GET request to the URL
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP errors

            # Open the image from the response content
            img = Image.open(BytesIO(response.content))

            # Resize the image
            img = img.resize(size, Image.Resampling.LANCZOS)

            # Save the resized image
            img.save(output_path)

            print(f"Image downloaded and resized to {size} and saved as {output_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e

    # Extract media URL
    def get_meme_post():
        post = random.choice(list(subreddit.hot(limit=30)))
        try:
            if hasattr(post, 'url'):
                media_url = post.url
                print(f"Media URL: {media_url}")

                # Download the media file
                download_and_resize_image(media_url, "Posts/Memes/Upload.png", (1080, 1080))
            else:
                print("No media found in this post.")
        except Exception as e:
            print(f"An error occured: {e}")
            count += 1
            if count > 40:
                raise ValueError("Alright something is definitly not right")
            get_meme_post()

    get_meme_post()

def get_motivational_post():

    phrases = [
        "Believe in yourself!",
        "Stay positive and happy.",
        "Never give up on your dreams.",
        "Success is not final, failure is not fatal: It is the courage to continue that counts.",
        "Dream big, work hard.",
        "Push yourself, because no one else is going to do it for you.",
        "Great things never come from comfort zones.",
        "Success is what happens after you have survived all your mistakes.",
        "Don't watch the clock; do what it does. Keep going.",
        "Believe you can and you're halfway there.",
        "Don't stop until you're proud.",
        "You are capable of amazing things.",
        "Every accomplishment starts with the decision to try.",
        "Stay hungry, stay foolish.",
        "The only limit to our realization of tomorrow is our doubts of today.",
        "Work hard in silence, let your success be your noise.",
        "Your only limit is you.",
        "Believe in your infinite potential. Your only limitations are those you set upon yourself.",
        "The harder you work for something, the greater you'll feel when you achieve it.",
        "Do something today that your future self will thank you for.",
        "Little things make big days.",
        "It always seems impossible until it's done.",
        "Dream it. Wish it. Do it.",
        "Success doesn't just find you. You have to go out and get it.",
        "Wake up with determination. Go to bed with satisfaction.",
        "Do something today that your future self will thank you for.",
        "Believe in yourself and all that you are.",
        "The future belongs to those who believe in the beauty of their dreams.",
        "You are never too old to set another goal or to dream a new dream.",
        "Success is the sum of small efforts, repeated day in and day out.",
        "The key to success is to focus on goals, not obstacles.",
        "The way to get started is to quit talking and begin doing.",
        "You don't have to be great to start, but you have to start to be great.",
        "The only way to do great work is to love what you do.",
        "Success is not how high you have climbed, but how you make a positive difference to the world.",
        "Act as if what you do makes a difference. It does.",
        "Your limitation—it's only your imagination.",
        "If you want to achieve greatness stop asking for permission.",
        "Start where you are. Use what you have. Do what you can.",
        "The harder you work, the luckier you get.",
        "You are braver than you believe, stronger than you seem, and smarter than you think.",
        "What we achieve inwardly will change outer reality.",
        "Don't let what you cannot do interfere with what you can do.",
        "Success is the result of preparation, hard work, and learning from failure.",
        "Don't count the days, make the days count.",
        "Do not wait to strike till the iron is hot; but make it hot by striking.",
        "It is never too late to be what you might have been.",
        "The only limit to our realization of tomorrow is our doubts of today.",
        "You miss 100% of the shots you don't take.",
        "Every champion was once a contender that didn't give up.",
        "The difference between who you are and who you want to be is what you do.",
        "Don't let yesterday take up too much of today.",
        "If you want to fly, you have to give up the things that weigh you down.",
        "The secret of getting ahead is getting started.",
        "Winners never quit, and quitters never win.",
        "Success usually comes to those who are too busy to be looking for it.",
        "Fall seven times, stand up eight.",
        "Perseverance is failing 19 times and succeeding the 20th.",
        "If you are not willing to risk the usual, you will have to settle for the ordinary.",
        "The best way to predict your future is to create it.",
        "Opportunities don't happen. You create them.",
        "If you can dream it, you can do it.",
        "Don't wish it were easier, wish you were better.",
        "Don't be pushed around by the fears in your mind. Be led by the dreams in your heart.",
        "Hardships often prepare ordinary people for an extraordinary destiny.",
        "The best time to plant a tree was 20 years ago. The second best time is now.",
        "Believe in your dreams, and they may come true; believe in yourself, and they will come true.",
        "Success is not just about making money. It's about making a difference.",
        "Success is the sum of small efforts repeated day in and day out.",
        "Your mind is a powerful thing. When you fill it with positive thoughts, your life will start to change.",
        "Don't be afraid to give up the good to go for the great.",
        "Keep your eyes on the stars, and your feet on the ground.",
        "Nothing is impossible. The word itself says 'I'm possible!'",
        "The secret to getting ahead is getting started.",
        "The best revenge is massive success.",
        "If you want something you’ve never had, you must be willing to do something you’ve never done.",
        "Success is not about how much money you make, it’s about the difference you make in people’s lives.",
        "Never give up on a dream just because of the time it will take to accomplish it. The time will pass anyway.",
        "The only place where success comes before work is in the dictionary.",
        "Go confidently in the direction of your dreams. Live the life you have imagined.",
        "If you really look closely, most overnight successes took a long time.",
        "Success is how high you bounce when you hit bottom.",
        "Dream bigger. Do bigger.",
        "Success is walking from failure to failure with no loss of enthusiasm.",
        "Success means doing the best we can with what we have. Success is the doing, not the getting; in the trying, not the triumph.",
        "Success is to be measured not so much by the position that one has reached in life as by the obstacles which he has overcome.",
        "Believe in yourself, take on your challenges, dig deep within yourself to conquer fears. Never let anyone bring you down. You got this.",
        "Challenges are what make life interesting, and overcoming them is what makes life meaningful.",
        "The future belongs to those who believe in the beauty of their dreams.",
        "Start where you are. Use what you have. Do what you can.",
        "The harder the conflict, the more glorious the triumph.",
        "If you believe it will work out, you’ll see opportunities. If you believe it won’t, you will see obstacles.",
        "Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle.",
        "You are never too old to set another goal or to dream a new dream.",
        "The only way to achieve the impossible is to believe it is possible.",
        "There is no elevator to success, you have to take the stairs.",
        "You can’t cross the sea merely by standing and staring at the water.",
        "Life is 10% what happens to us and 90% how we react to it.",
        "Keep going. Everything you need will come to you at the perfect time.",
        "Success is getting what you want. Happiness is wanting what you get.",
        "Don't be afraid to give up the good to go for the great.",
        "I find that the harder I work, the more luck I seem to have.",
        "Do not wait for leaders; do it alone, person to person.",
        "Be miserable. Or motivate yourself. Whatever has to be done, it's always your choice.",
        "Go as far as you can see; when you get there, you’ll be able to see further.",
        "Do what you can, with what you have, where you are.",
        "The difference between ordinary and extraordinary is that little extra.",
        "A river cuts through rock, not because of its power, but because of its persistence.",
        "Your time is limited, don’t waste it living someone else’s life.",
        "You don't have to be great to start, but you have to start to be great.",
        "Don't let yesterday take up too much of today.",
        "In order to succeed, we must first believe that we can.",
        "The only way to do great work is to love what you do.",
        "Success is not how high you have climbed, but how you make a positive difference to the world.",
        "I can’t change the direction of the wind, but I can adjust my sails to always reach my destination.",
        "Perseverance is not a long race; it is many short races one after the other.",
        "Start where you are. Use what you have. Do what you can.",
        "You don’t have to see the whole staircase, just take the first step.",
        "It’s not whether you get knocked down, it’s whether you get up.",
        "Success isn’t just about what you accomplish in your life; it’s about what you inspire others to do.",
        "Success is a journey, not a destination.",
        "The road to success and the road to failure are almost exactly the same.",
        "There is only one way to avoid criticism: do nothing, say nothing, and be nothing."
    ]

    files = [
        {"Path": "Posts\\Media\\Ben_graham.png", "Align": "Center", "Place_words": "Center", "font-size": 50, "text-color": "white", "max_width_line": 600},
        {"Path": "Posts\\Media\\Indert_CT.png", "Align": "Left", "Place_words": (145, 305), "font-size": 50, "text-color": "black", "max_width_line": 400},
        {"Path": "Posts\\Media\\Joe_Simons.png", "Align": "Left", "Place_words": (300, 240), "font-size": 50, "text-color": "white", "max_width_line": 500},
        {"Path": "Posts\\Media\\No_One.png", "Align": "Center", "Place_words": "Center", "font-size": 50, "text-color": "white", "max_width_line": 400},
        {"Path": "Posts\\Media\\Quotes.png", "Align": "Center", "Place_words": "Center", "font-size": 30, "text-color": "white", "max_width_line": 400},
        {"Path": "Posts\\Media\\Satoshi_Nakamoto.png", "Align": "Center", "Place_words": "Center", "font-size": 50, "text-color": "white", "max_width_line": 400},
        {"Path": "Posts\\Media\\Warren_Buffet.png", "Align": "Left", "Place_words": (410, 95), "font-size": 50, "text-color": "white", "max_width_line": 400}
    ]

    phrase = '"' + random.choice(phrases) + '"'
    file = random.choice(files)

    image_path = file["Path"]
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    def wrap_text(text, font, max_width_line):
        """
        Wraps text into lines that fit within the specified maximum width.

        :param text: The text to wrap.
        :param font: The font to use for text measurement.
        :param max_width_line: The maximum width allowed for each line.
        :return: A list of wrapped lines.
        """
        lines = []
        words = text.split()
        line = ""

        for word in words:
            test_line = f"{line} {word}".strip()
            bbox = draw.textbbox((0, 0), test_line, font=font)
            width = bbox[2] - bbox[0]
            if width <= max_width_line:
                line = test_line
            else:
                if line:
                    lines.append(line)
                line = word

        if line:
            lines.append(line)

        return lines

    def draw_text_with_border(draw, text, position, font, text_color, border_color, border_width):
        """
        Draws text with a border around it.

        :param draw: The ImageDraw object.
        :param text: The text to draw.
        :param position: The position to draw the text.
        :param font: The font to use for text.
        :param text_color: The color of the text.
        :param border_color: The color of the border.
        :param border_width: The width of the border.
        """
        # Draw border
        x, y = position

        # Draw actual text on top
        draw.text(position, text, font=font, fill=text_color)

    font_size = file["font-size"]
    font_path = "Fonts/arial.ttf"  # Update this path as needed
    font = ImageFont.truetype(font_path, font_size)

    max_width_line = file["max_width_line"]
    lines = wrap_text(phrase, font, max_width_line)

    # Calculate text height
    line_height = draw.textbbox((0, 0), 'A', font=font)[3] - draw.textbbox((0, 0), 'A', font=font)[1]
    total_text_height = (line_height * len(lines)) + ((len(lines) - 1) * 20)

    max_text_width = max(
        draw.textbbox((0, 0), line, font=font)[2] - draw.textbbox((0, 0), line, font=font)[0] for line in lines)

    # Calculate starting positions based on alignment
    if file["Place_words"] == "Center":
        if file["Align"] == "Center":
            x_start = 0
            y_start = (image.height - total_text_height) // 2
        elif file["Align"] == "Left":
            x_start = file["Place_words"][0]
            y_start = file["Place_words"][1]
        else:
            y_start = 0
            x_start = 0
    else:
        if file["Align"] == "Left":
            x_start = file["Place_words"][0]
            y_start = file["Place_words"][1]
        else:
            x_start = 0
            y_start = 0

    # Draw text on the image
    y = y_start
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        if file["Align"] == "Center":
            x = x_start + (image.width - text_width) / 2
        elif file["Align"] == "Left":
            x = x_start
        else:
            x = 0
        draw_text_with_border(draw, line, (x, y), font, file["text-color"], "black", 3)
        y += line_height + 20

    # Save or display the image
    output_path = "Posts/Motivacional/output.png"
    image.save(output_path)
    image.show()

def get_n_post():

    tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
    model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")

    def get_response_sumamrized(message="How are you?"):

        # Tokenize the input message
        inputs = tokenizer.encode(message, return_tensors="pt")

        # Generate the output
        summary_ids = model.generate(inputs, max_length=50, min_length=5, length_penalty=2.0, num_beams=4,
                                     early_stopping=True)

        # Decode the output into text
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return summary

    def inverse(x):
        return x / 10

    def get_news_post():
        response = get_news()
        all_news = [f'Title: "{i['title']}", Description: "{i['description']}", Content: "{i['content']}"' for i in response['articles'][0:9]]
        news_choosen = get_response_sumamrized(all_news[int(inverse(random.uniform(1, 80)))])

        files = [
            {"Path": "Posts/Media/News1.png", "Align": "Right", "Place_words": (100, 340), "font-size": 33, "text-color": "white", "max_width_line": 500},
            {"Path": "Posts/Media/News2.png", "Align": "Left", "Place_words": (45, 450), "font-size": 37, "text-color": "white", "max_width_line": 610},
            {"Path": "Posts/Media/News3.png", "Align": "Left", "Place_words": (95, 470), "font-size": 45, "text-color": "white", "max_width_line": 530},
            {"Path": "Posts/Media/News4.png", "Align": "Right", "Place_words": (100, 330), "font-size": 33, "text-color": "black", "max_width_line": 480},
            {"Path": "Posts/Media/News5.png", "Align": "Right", "Place_words": (50, 300), "font-size": 50, "text-color": "black", "max_width_line": 500},
            {"Path": "Posts/Media/News6.png", "Align": "Left", "Place_words": (125, 800), "font-size": 30, "text-color": "white", "max_width_line": 900},
            {"Path": "Posts/Media/News7.png", "Align": "Right", "Place_words": (40, 265), "font-size": 40, "text-color": "white", "max_width_line": 600}
        ]

        phrase = news_choosen[:]
        file = random.choice(files)

        image_path = file["Path"]
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)

        def wrap_text(text, font, max_width_line):
            """
            Wraps text into lines that fit within the specified maximum width.

            :param text: The text to wrap.
            :param font: The font to use for text measurement.
            :param max_width_line: The maximum width allowed for each line.
            :return: A list of wrapped lines.
            """
            lines = []
            words = text.split()
            line = ""

            for word in words:
                test_line = f"{line} {word}".strip()
                bbox = draw.textbbox((0, 0), test_line, font=font)
                width = bbox[2] - bbox[0]
                if width <= max_width_line:
                    line = test_line
                else:
                    if line:
                        lines.append(line)
                    line = word

            if line:
                lines.append(line)

            return lines

        def draw_text_with_border(draw, text, position, font, text_color):
            """
            Draws text with a border around it.

            :param draw: The ImageDraw object.
            :param text: The text to draw.
            :param position: The position to draw the text.
            :param font: The font to use for text.
            :param text_color: The color of the text.
            :param border_color: The color of the border.
            :param border_width: The width of the border.
            """
            # Draw border
            x, y = position

            # Draw actual text on top
            draw.text(position, text, font=font, fill=text_color)

        font_size = file["font-size"]
        font_path = "Fonts/arial.ttf"  # Update this path as needed
        font = ImageFont.truetype(font_path, font_size)

        max_width_line = file["max_width_line"]
        lines = wrap_text(phrase, font, max_width_line)

        # Calculate text height
        line_height = draw.textbbox((0, 0), 'A', font=font)[3] - draw.textbbox((0, 0), 'A', font=font)[1]
        total_text_height = (line_height * len(lines)) + ((len(lines) - 1) * 20)

        max_text_width = max(
            draw.textbbox((0, 0), line, font=font)[2] - draw.textbbox((0, 0), line, font=font)[0] for line in lines)

        # Calculate starting positions based on alignment
        if file["Place_words"] == "Center":
            if file["Align"] == "Center":
                x_start = 0
                y_start = (image.height - total_text_height) // 2
            elif file["Align"] == "Left":
                x_start = file["Place_words"][0]
                y_start = file["Place_words"][1]
            elif file["Align"] == "Right":
                x_start = image.width - max_text_width
                y_start = file["Place_words"][1]
            else:
                y_start = 0
                x_start = 0
        else:
            if file["Align"] == "Left":
                x_start = file["Place_words"][0]
                y_start = file["Place_words"][1]
            elif file["Align"] == "Right":
                x_start = image.width - max_text_width
                y_start = file["Place_words"][1]
            elif file["Align"] == "Center":
                x_start = file["Place_words"][0] - max_text_width // 2
                y_start = file["Place_words"][1] - total_text_height // 2
            else:
                x_start = 0
                y_start = 0

        # Draw text on the image
        y = y_start
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            if file["Align"] == "Center":
                x = x_start + (image.width - text_width) / 2
            elif file["Align"] == "Left":
                x = x_start
            elif file["Align"] == "Right":
                x = image.width - text_width - file["Place_words"][0]
            else:
                x = 0
            draw_text_with_border(draw, line, (x, y), font, file["text-color"])
            y += line_height + 20

        # Save or display the image
        output_path = "Posts/Crypto News/output.png"
        image.save(output_path)
        image.show()

    def get_time(day=1):
        now = datetime.datetime.now()
        now -= datetime.timedelta(days=day)
        return now.strftime("%Y-%m-%d")

    def get_news(q='"cryptocurrency"', api_key=apikey):
        response = requests.get(f'https://newsapi.org/v2/everything?q={q}&apiKey={api_key}&language=en&from={get_time()}&searchIn=content&sortBy=relevancy').json()
        return response

    get_news_post()

if __name__ == '__main__':
    #get_n_post()
    #get_motivational_post()
    get_meme()
