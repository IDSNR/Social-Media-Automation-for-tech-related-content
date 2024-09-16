## A project for making automatic videos for Social Media (about cryptocurrency)

## Considerations
    - The script has to be manually fetched from chat-gpt, as I don´t have the means to pay for an open-ai api subscription, but if you do it can be easily implemented
    - All api´s and services used are free (hugging-face, reddit api, newsapi)
    - Make sure hugging face already hasd your authentication data
    - Required dependencies:
        - moviepy
        - numpy
        - pandas
        - requests
        - praw
        - imagemagik (for moviepy)git 
        - ffmpeg (for moviepy)
        - torch
        - tensorflow
        - transformers
        - hugging-face-hub
    - The code relies on external google colab for getting the subtitles of the video, as it is faster than running it locally (at least in my PC)
        
