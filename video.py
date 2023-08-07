from moviepy.editor import VideoFileClip,AudioFileClip,  CompositeVideoClip,TextClip,ImageClip
import random
from audio import *
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.VideoFileClip import VideoFileClip

#The main video, which the subclip will come from
clip = VideoFileClip('Minecraft_Background.mov')

def create_subclip_params(length: int) -> int and int:

    """
    Creates the a random range for the duration of the subclip

    Parameters
    ----------
    length : int
        The duration of the audio file in seconds

    Return
    ------
    num : int
        starting point of the new subclip
    num+int(length) : int
        endning point of the new subclip
        
    """

    #finds a randomn point within the duration of 'Minecraft_Background.mov'
    #Makes sure the starting point isn't at the end of the video
    num = random.randrange(0,(int(clip.duration)-int(length)))
    return num, num+int(length)



def create_final_video(title: str):

    """
    Creates the final tiktok video and saves as f"{post.title}.mp4"

    Parameters
    ----------
    title : str
        The post title

    """
    
    #The generator that reads the str from subs and converts it into visual text for the video
    generator = lambda txt: TextClip(txt, font='Impact', fontsize=30, color='brown')

    #Gets the subtitles and length of video
    subs,length = get_subs(transcription())
    #Duration for the image to be displayed at the beginning of the video
    image_end_time = get_times(subs, title.split()[-1])
    #Creates the range for the subclip
    start,end = create_subclip_params(length)

    #Creates the background for the video
    background = clip.subclip(start,end)
    #Sets the audio for the background video
    audio = AudioFileClip('voice.mp3')
    background = background.set_audio(audio)
    #Creates the subtitles for the video
    subtitles = SubtitlesClip(subs, generator)
    #Creates the image of the Reddit post
    reddit_ss = ImageClip("reddit_post_ss.png").set_start(0).set_duration(image_end_time).set_pos(("center","center")).resize(height=120)
    #Compiles the background,subtitles, and image into the video
    result = CompositeVideoClip([background,subtitles.set_pos(('center','center')), reddit_ss])

    #Adds two seconds onto the video
    #result = result.subclip(0,get_audio_length()+2)

    #Renders the final video 
    result.write_videofile(f'{title}.mp4', 
                        codec='libx264', 
                        audio_codec='aac', 
                        temp_audiofile='temp-audio.m4a', 
                        remove_temp=True
                        )

