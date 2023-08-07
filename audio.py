
from mutagen.mp3 import MP3
import inflect


def get_audio_length() -> float:
    """
    Returns the length of the audio file in seconds
    """
    return ((MP3("voice.mp3").info.length))

def transcription() -> int:
    """
    Reads through 'reddit_text.txt' and chops the text into shorter lines to be displayed on screen
    Writes the text to 'transcription.txt'

        Returns
        -------
        line_count : int
            The number of lines in the txt file
    """

    read_file = open('reddit_text.txt','r')
    write_file = open('transcription.txt','w')

    curr = ''
    space_count = 0
    char_count = 0
    line_count = 0
    #Goes through each line and then every char in that line
    for line in read_file:
        for char in line.strip():

            #If there is an end puncuation we end the line on punctuation and move on
            if (char == '.' or char == '?' or char == '!' or char==":") and char_count>1 and space_count>=0:
                curr+=char
                write_file.write(curr+'\n')
                line_count+=1
                curr = ''
                space_count = 0
                char_count = 0
            #if its a start of a quote or text in parantheses we just add to the current string
            elif char=='"' or char=="’":
                curr+=char
                continue
            elif char=="(" or char ==")":
                continue
            #if its a space we add to count and see if there is characters stored in curr
            elif char == ' ':
                if len(curr)==0:
                    continue
                space_count+=1
                #if char in curr then we end the line and write curr to the file
                if space_count >= 1 and char_count>=4:
                    write_file.write(curr+'\n')
                    line_count+=1
                    curr = ''
                    space_count = 0
                    char_count = 0
                #if the curr isn't bigger 3 letters we add the space to curr and add another word
                else:
                    curr += char
            #if two words are joined by a / 
            #Example: "harmless/Safe" we would want to seperate those words for the display on screen 
            elif char =="/":
                write_file.write(curr+'\n')
                line_count+=1
                curr = ''
                space_count = 0
                char_count = 0
            #If the char is just a basic letter we add to curr to make the word and increase the count 
            else:
                
                curr += char
                char_count+=1
    #Makes sure the last word in 'reddit_text.txt' is added
    if curr != "":           
        write_file.write(curr+'\n')
        line_count+=1
            
    #Close the files
    read_file.close()
    write_file.close()

    return line_count


def get_subs(line: int) -> list and int:

    """
        Reads through 'transcription.txt' and creates timestamps for each line displayed
        Writes the timestamp and text to 'subscription.txt' 
        Ex:     [(0.00, 2.3), Hello World!]

        Parameters
        ----------
        line : int
            The number of lines in "transcription.txt" file

        Returns
        -------
        subs : list
            The 2D list that has the timestamps and text
        length : int
            The last timestamp which is the length of the video 
    """

    #Open Fles
    f = open("transcription.txt",'r')
    n = open('subscription.txt', 'w')

    #Array for timestamps/text
    subs = []
    start,end = 0,0


    #The amount of time a line will be displayed
    const = get_audio_length()/line

    #Goes through each line in file
    for line in f:
        #Adds the time of the line to end
        end+=const

        #append the timestamp (star,end) and the line to list subs 
        subs.append([(start,end),str(line.strip())])
        #write the data to 'subscription.txt' to visualize the data
        n.write(f'[{(start,end)},{str(line.strip())}]\n')
        #Set new start and end times
        start,end = end,end

    #Close files
    f.close()
    n.close()
    length = int(end+1)
    return subs,length


def get_times(subs: list,last_word: str) -> float:
    """
        Gets the time of when the last word of the post title is read

        Parameters
        ----------
        subs : list
            The 2D list of timestamps and strings displayed during timestamps
        last_word : string
            The last word in the title of the post

        Returns
        -------
        item[0][1] + .001 : float
            The ending timestamp for when the last word of the post title is read
    """
    print(last_word)
    for item in subs:
        if last_word in item[1].split():
            print(item[0][1] + .001)
            return item[0][1] + .001, 
            

