from audio import transcription
from reddit import getRandomHotPost,getTopComment,get_screenshot,create_url
from tiktok_tts import TikTokTTS
from video import  create_final_video


#sub = input("Enter a subreddit you'd like to search")
popular_subreddits = [

    'AskReddit',
    'AITA'

]
sub = 'AskReddit'

ans = 'n'
start = True

while start:

    while ans == 'n':
        
        post = getRandomHotPost(sub)
        ans = input(f"Is '{post[1]}' the post you'd like to search [y/n]")
        title = post[1]

    text = title +"\n"+ getTopComment(post[0])

    if text==title+"\n"+"":

        print(f"There wasn't a response long enough in {post[1]}, please try another")
        ans = 'n'

    else:

        start = False

file = open('reddit_text.txt','w')
file.write(text)
file.close()

TikTokTTS('reddit_text.txt')
transcription()
get_screenshot(create_url(sub,post[0],post[1]),post[0])
create_final_video(post[1])

