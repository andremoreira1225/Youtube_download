from flask import Flask, request, render_template, redirect, url_for, session
from pytube import YouTube
from moviepy.editor import *
import os

app = Flask(__name__)


@app.route("/", methods = ["GET", "POST"])
def inicial_page():
    if request.method == "POST":
        if 'submit_button' in request.form:
            pLink = request.form['link']
            global yt 
            yt = YouTube(pLink)
            type_file = request.form['type']
            type(yt)
            if(pLink != None):
                if(type_file == "mp4"):
                    return redirect(url_for("download_video"))
                elif(type_file == "mp3"):
                    return redirect(url_for("download_audio"))
                else:
                    return redirect(url_for("inicial_page"))
            else:
                return redirect(url_for("inicial_page"))
    return render_template("inicial_page.html")


@app.route("/downloadVideo", methods = ["GET", "POST"])
def download_video():
    print(yt)
    descricao = yt.title 
    itagV = videoPreferences(yt)
    if request.method == "POST":
        if 'submit_button' in request.form:
            path = request.form['path']
            quality_anwser = request.form['quality']
            file_name = request.form['file_name']
            videoDownload(quality_anwser, yt, path)
            merge(file_name, path)
            return convertion()
    return render_template("download_video.html", descricao=descricao, tag=itagV)

@app.route("/downloadAudio", methods = ["GET", "POST"])
def download_audio():
    print(yt)
    descricao = yt.title + str(yt.views) + str(yt.length) + yt.description + str(yt.rating)
    if request.method == "POST":
        if 'submit_button' in request.form:
            path = request.form['path']
            quality_anwser = request.form['quality']
            file_name = request.form['file_name']
            audioDownload(quality_anwser, yt, file_name, path)
            return convertion()
    return render_template("download_audio.html", descricao=descricao)

@app.route("/convertion", methods = ["GET", "POST"])
def convertion():
    if request.method == "POST":
        return redirect(url_for("inicial_page"))
    return render_template("convertion.html")
    
def videoPreferences(yt):
    #youtube streams filtering
    itagV = None
    streams = yt.streams.filter(file_extension="mp4", progressive=None)
    resStream = []

    for stream in streams:
        resStream.append(str(stream.resolution))

    if("2160p" in resStream):
        itagV = 401
        return itagV
    elif("1440p" in resStream):
        itagV = 400
        return itagV
    elif("1080p" in resStream):
        itagV = 137
        return itagV
    elif("720p" in resStream):
        itagV = 39
        return itagV


def videoDownload(itagV, yt, path):
    print("\n **************************************************")

    itagA = 140

    print(itagV, path)
    dV = yt.streams.get_by_itag(itagV)
    dV.download(filename= "video.mp4", output_path=path)

    ys = yt.streams.get_by_itag(itagA)
    ys.download(filename="audio.mp4", output_path=path)

def audioDownload(itagA, yt, file_name, path):
    ys = yt.streams.get_by_itag(itagA)
    ys.download(filename=file_name+".mp4", output_path=path)

def merge(file_name, path):
    input_video = VideoFileClip(path + 'video.mp4')

    input_audio = AudioFileClip(path + 'audio.mp4')

    new_audioclip = CompositeAudioClip([input_audio])
    input_video.audio = new_audioclip
    input_video.write_videofile(path + file_name + '.mp4')

    if(os.path.isfile(path+ 'video.mp4')):
        os.remove(path + 'video.mp4')

    if(os.path.isfile(path+ 'audio.mp4')):
        os.remove(path + 'audio.mp4')


if __name__ == "__main__":
    app.run(debug=True)