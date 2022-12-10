from pytube import YouTube
from moviepy.editor import *
import os

#input user

linkVideo = input("Insert link of video: ")
yt = YouTube(linkVideo)


def download(option, file_name):
    print("\n *********************Info**************************")
    #Title of video
    print("Title: ", yt.title)

    #Number of views
    print("Number of views: ", yt.views)

    #Video length
    print("Length: ", yt.length, "sec")

    #Description of video
    print("Description: ", yt.description)

    #Rating
    print("Rating ", yt.rating)

    print("\n ******************EndInfo****************************")

    if(option=="1"):
        videoPreferences()
        merge(file_name)
    elif(option=="2"):
        audioPreferences(file_name)
    


def videoPreferences():
    #youtube streams filtering
    itagV = null
    streams = yt.streams.filter(file_extension="mp4", progressive=None)
    resStream = []

    for stream in streams:
        resStream.append(str(stream.resolution))

    if("2160p" in resStream):
        fourK = True
        option = int(input("""\n Which stream quality you want: 
                            
                            1.2160p (4k)
                            2.1440p (2k)
                            3.1080p (FullHD)
                            4.720p (HD)
        """))

        if(option==1):
            itagV = 401
        elif(option==2):
            itagV = 400
        elif(option==3):
            itagV = 137
        elif(option==4):
            itagV = 39

        videoDownload(itagV)
    elif("1440p" in resStream):
        option = int(input("""\n Which stream quality you want: 
                            
                            1.1440p (2k)
                            2.1080p (FullHD)
                            3.720p (HD)
        """))


        if(option==1):
            itagV = 400
        elif(option==2):
            itagV = 137
        elif(option==3):
            itagV = 39

        videoDownload(itagV)
    elif("1080p" in resStream):
        option = int(input("""\n Which stream quality you want: 
                            
                            1.1080p (FullHD)
                            2.720p (HD)
        """))

        if(option==1):
            itagV = 137
        elif(option==2):
            itagV = 39

        videoDownload(itagV)
    

def videoDownload(itagV):
    print("\n **************************************************")

    itagA = 140

    dV = yt.streams.get_by_itag(itagV)
    dV.download(filename= "video.mp4", output_path=path)

    ys = yt.streams.get_by_itag(itagA)
    ys.download(filename="audio.mp4", output_path=path)

def audioPreferences(file_name):
    itagA = null

    print("\n **************************************************")

    print(yt.streams.filter(only_audio=True),"\n")
    option = int(input("""\n Which stream audio (itag) you want: 
                            
                            1.Mp4 high quality
                            2.Mp4 medium quality 
    """))

    if(option==1):
        itagA = 137
    elif(option==2):
        itagA = 140
    
    ys = yt.streams.get_by_itag(itagA)
    ys.download(filename=file_name+".mp4", output_path=path)

def merge(file_name):
    input_video = VideoFileClip(path + 'video.mp4')

    input_audio = AudioFileClip(path + 'audio.mp4')

    new_audioclip = CompositeAudioClip([input_audio])
    input_video.audio = new_audioclip
    input_video.write_videofile(path + file_name + '.mp4')

    if(os.path.isfile(path+ 'video.mp4')):
        os.remove(path + 'video.mp4')

    if(os.path.isfile(path+ 'audio.mp4')):
        os.remove(path + 'audio.mp4')



menu = input("""
            1.Download Video + Audio
            2.Download Audio
            3.Exit

            """)

if(menu=="1"):
    path = input("What path you want to save file: ")
    file_name = input("Enter the name for file: ")
    download(menu,file_name)
    
elif(menu=="2"):
    path = input("What path you want to save file: ")
    file_name = input("Enter the name for file: ")
    download(menu, file_name)
elif(menu=="3"):
    pass

print("\n End convertion!")