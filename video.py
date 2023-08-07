
from moviepy.editor import VideoFileClip,AudioFileClip,  CompositeVideoClip,TextClip,ImageClip
import random
from audio import *
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.VideoFileClip import VideoFileClip

#The main video, which the subclip will come from
clip = VideoFileClip('Minecraft_Background.mov')


"""
Creates the a random range for the duration of the subclip

        Parameters
        ----------
        length : int
            The duration of the audio file in seconds
"""
def create_subclip_params(length: int) -> int and int:
    num = random.randrange(0,(int(clip.duration)-int(length)))
    return num,num+int(length)



"""
Attaches the subtitles to 'background.mp4'
will return 'final.mp4' as the final tiktok video
"""
def create_final_video(title):

    generator = lambda txt: TextClip(txt, font='Impact', fontsize=30, color='white')
    subs,length = get_subs()

    image_end_time = get_times(subs,title.split()[-1])

    start,end = create_subclip_params(length)
    print(start,end,start-end)


    background = clip.subclip(start,end)
    audio = AudioFileClip('voice.mp3')
    background = background.set_audio(audio)
    subtitles = SubtitlesClip(subs, generator)
    reddit_ss = ImageClip("reddit_post_ss.png").set_start(0).set_duration(image_end_time).set_pos(("center","center")).resize(height=120)
    result = CompositeVideoClip([background,subtitles.set_pos(('center','center')), reddit_ss])
    result = result.subclip(0,get_audio_length()+2)
    result.write_videofile(f'{title}.mp4', 
                        codec='libx264', 
                        audio_codec='aac', 
                        temp_audiofile='temp-audio.m4a', 
                        remove_temp=True
                        )
