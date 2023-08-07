from settings import reddit
from praw.models import MoreComments
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO

"""
Gets the top ten reddit posts and stores the post id with its title into a dicitonary "posts"

Dicitionary "Posts": key = post.id  | val = post.title

        Parameters
        ----------
        subreddit : str
            The name of the subreddit your searching through

returns a list of a randomnly selected post with its id at index 0 and title at index 1
"""
def getRandomHotPost(subreddit: str) -> tuple:

    sub = reddit.subreddit(f'{subreddit}').hot()
    posts = {}
    for count,post in enumerate(sub):
        posts[post.id] = post.title
        if count==20:
            break

    return random.choice(list(posts.items()))

"""
Gets the top comment from the reddit post

        Parameters
        ----------
        postId : str
            The id of the post from the subreddit

returns a str of the comment
"""
def getTopComment(postId: str) -> str:
  submission = reddit.submission(f"{postId}")
  maxScore = 0
  topComment = ""
  topID = ""

  #searches through every comment in the post
  for top_level_comment in submission.comments:

    if isinstance(top_level_comment, MoreComments):
        continue
    #Makes sure the post has more than 800 characters, so the audio is longer then a minute
    if len(top_level_comment.body) > 800:

        #Gets the comment with the most amount of upvotes
        if top_level_comment.score > maxScore:
            maxScore = top_level_comment.score
            topComment = top_level_comment.body
            topID = top_level_comment.id

  return topComment

"""
Gets the screenshot of the reddit post

        Parameters
        ----------
        url : str
            The url to the the reddit post 
        postId : str
            The id of the post from the subreddit

creates a png file called "reddit_post_ss.png"
"""
def get_screenshot(url: str,postId: str):

    driver = webdriver.Chrome()
    driver.get(url)
    element = driver.find_element(By.ID, f"t3_{postId}")
    location = element.location
    size = element.size
    png = driver.get_screenshot_as_png() # saves screenshot of entire page
    driver.quit()

    im = Image.open(BytesIO(png)) # uses PIL library to open image in memory

    left = (location['x']*1.85)
    top = location['y'] *2
    right = left + (size['width']*2.15)
    bottom = top + (size['height']*2.14)

    #1215 x 420
    im = im.crop((left, top, right, bottom)) # defines crop points
    im.save('reddit_post_ss.png') # saves new cropped image
    

"""
Creates the url for the reddit posts

        Parameters
        ----------
        subreddit : str
            The name of the subreddit
        postId : str
            The id of the post from the subreddit
        title : str
            The title of the post from the subreddit

returns a string form of the url to the reddit post
"""
def create_url(subreddit: str, postId: str, title: str) -> str:

    punc = '''!()-[]}{;:'"\,<>./?@#$%^&*_~''“”'''
    title = title.lower()
    for c in title:
        #Replaces any punctuation with blank
        if c in punc:
            title = title.replace(c,'')
        #Replaces any space with underscore
        if c == " ":
            title = title.replace(c,'_')
            

    return f'https://www.reddit.com/r/{subreddit}/comments/{postId}/{title}/'




