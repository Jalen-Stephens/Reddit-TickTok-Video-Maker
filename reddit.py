from settings import reddit
from praw.models import MoreComments
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO


def getRandomHotPost(subreddit: str) -> tuple:
    """
        Gets the top ten reddit posts and stores the post id with its title into a dicitonary "posts"

        Dicitionary "Posts": key = post.id  | val = post.title

        Parameters
        ----------
        subreddit : str
            The name of the subreddit your searching through

        Return
        ------
        random.choice(list(posts.items())) : tuple
            A tuple of the randomnly selected post 
            Example:  (post.id, post.title)
    """
    sub = reddit.subreddit(f'{subreddit}').hot()
    posts = {}
    for count,post in enumerate(sub):
        posts[post.id] = post.title
        if count==20:
            break

    return random.choice(list(posts.items()))

def getTopComment(postId: str) -> str:
    """
    Gets the top comment from the reddit post

    Parameters
    ----------
    postId : str
        The id of the post from the subreddit

    Return
    ------
    topComment : str
        The text from the top comment of the reddit post
    """
    submission = reddit.submission(postId)
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


def get_screenshot(url: str,postId: str):
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

    #Sets up Chrome webdriver
    driver = webdriver.Chrome()
    #Opens Website
    driver.get(url)

    #We find the post in the html through the postId
    element = driver.find_element(By.ID, f"t3_{postId}")

    #Get the location and Size
    location = element.location
    size = element.size

    #Saves screenshot of entire page
    png = driver.get_screenshot_as_png()

    #Closes Webdriver
    driver.quit()

    #Uses PIL library to open image in memory
    im = Image.open(BytesIO(png)) 

    #Using the location and size of the post container, we can establish the dimensions of the post
    left = (location['x']*1.85)
    top = location['y'] *2
    right = left + (size['width']*2.15)
    bottom = top + (size['height']*2.14)

    #Crops and Saves image as 'reddit_post_ss.png'
    im = im.crop((left, top, right, bottom))
    im.save('reddit_post_ss.png')
    

def create_url(subreddit: str, postId: str, title: str) -> str:

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

    Return
    ------
    url : str
        A string form of the url to the reddit post
    """

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
