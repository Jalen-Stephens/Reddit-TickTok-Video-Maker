import praw

username = 'Your Reddit Username'
userAgent = "Minecraft Stories Bot/0.1 by " + username
clientId = 'Your client Id'
clientSecret = "Your Secret reddit key"
password = "Your Reddit Password"
reddit = praw.Reddit(user_agent=userAgent, client_id=clientId, client_secret=clientSecret)