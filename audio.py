
from mutagen.mp3 import MP3
import inflect


def get_audio_length():
    return ((MP3("voice.mp3").info.length))

def transcription():

    read_file = open('reddit_text.txt','r')
    write_file = open('transcription.txt','w')

    curr = ''
    space_count = 0
    char_count = 0
    for line in read_file:
        for char in line.strip():
            if (char == '.' or char == '?' or char == '!' or char==":" or char==")") and char_count>1 and space_count>=0:
                curr+=char
                write_file.write(curr+'\n')
                curr = ''
                space_count = 0
                char_count = 0
            elif char=='"' or char=="’" or char=="(":
                curr+=char
                continue
            elif char == ' ':
                if len(curr)==0:
                    continue
                space_count+=1

                if space_count >= 1 and char_count>=4:
                    write_file.write(curr+'\n')
                    curr = ''
                    space_count = 0
                    char_count = 0
                else:
                    curr += char
            elif char =="/":
                write_file.write(curr+'\n')
                curr = ''
                space_count = 0
                char_count = 0
            else:
                
                curr += char
                char_count+=1
    if curr != "":           
        write_file.write(curr+'\n')
            

    read_file.close()
    write_file.close()


def get_subs():
    p = inflect.engine()
    f = open("transcription.txt",'r')
    n = open('subscription.txt', 'w')

    subs = []
    start,end = 0,0
    #Hello how are you? Goodbye  2.3
    for line in f:
        char_count = 0
        for c in line.strip():

            if c=="." or c=="?" or c=="!" or c==",":
                end+=.2
            elif c==" ":
                end+=.03
            elif c.isnumeric():
                end+=(.015*(len(p.number_to_words(int(c)))))
            else:
                char_count+=.02

        if line == "...":
            end+=.15
        else:
            end+=.3+char_count
        subs.append([(start,end),str(line.strip())])
        n.write(f'[{(start,end)},{str(line.strip())}]\n')
        start,end = end,end

    
    f.close()
    n.close()
    
    return subs,int(end+1),

def get_title_length(title):

    p = inflect.engine()
    char_count,end = 0,0

    for c in title:

        if c=="." or c=="?" or c=="!" or c==",":
            end+=.25
        elif c==" ":
            end+=.35
        elif c.isnumeric():
            end+=(.0175*(len(p.number_to_words(int(c)))))
        else:
            char_count+=.015
        #print(f"C: {c}\tEnd: {end}\tCount: {char_count}\n")

    end+=char_count
    return end +.02


"""
Gets the time of when the last word of the post title is read

        Parameters
        ----------
        subs : list
            The 2D list of timestamps and strings displayed during timestamps
        last_word : string
            The last word in the title of the post
"""
def get_times(subs: list,last_word: str) -> float:
    
    for item in subs:
        if last_word in item[1].split():
            return item[0][1] + .001, 
            
