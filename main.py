from numpy import take
from pytube import Playlist
import eyed3
from moviepy.editor import *
import os
import time
import requests
import colorama
from colorama import Fore, Style
import tkinter as tk
from plyer import notification
import webbrowser

app_Version = "1.1.0"
application_get_url = "https://unerasable.github.io/application.json"
def check_valid_status_code(request):
    if request.status_code == 200:
        return request.json()

    return False


def get_application_get_url():
    request = requests.get(application_get_url)
    data = check_valid_status_code(request)
    return data
app_URL=get_application_get_url()
checkAppVer = f"{app_URL['nightcoreDownloader']['verson']}"
def download(playlist, album_input, album_artist_input, save_Loc):
    for video in playlist.videos:
        try:
            print(f'Downloading {video.title}...')
            video.streams.first().download(output_path=save_Loc, filename=video.title+ ".mp4")
            response = requests.get(str(video.thumbnail_url))
            with open(os.path.join(save_Loc, f"{video.title}.jpg"), "wb") as f:
                f.write(response.content)
            videoe = VideoFileClip("%s.mp4" % os.path.join(save_Loc, video.title))
            videoe.audio.write_audiofile("%s.mp3" % os.path.join(save_Loc, video.title))
            videoe.close()
            os.remove("%s.mp4" % os.path.join(save_Loc, video.title))
            song = eyed3.load(f"{os.path.join(save_Loc, video.title)}.mp3")
            song.tag.images.set(3, open(f"{os.path.join(save_Loc, f'{video.title}.jpg')}", 'rb').read(), 'image/jpeg')
            song.tag.artist = f"{video.author}"
            song.tag.album = f"{album_input}"
            song.tag.album_artist = f"{album_artist_input}"
            song.tag.title = f"{video.title}"
            song.tag.save()
            os.remove("%s.jpg" % os.path.join(save_Loc, video.title))
            os.system(f'eyed3 "{os.path.join(save_Loc, video.title)}.mp3"')
            notification.notify(title= 'Downloaded',
                    message= f'{video.title} has been downloaded',
                    app_icon = 'app.ico',
                    timeout= 0.1,
                    toast=False)
        except:
            print(f'{Fore.RED}[ERROR]{Fore.RESET} {video.title} failed to download')
            print(f"{Fore.YELLOW}[WARNING]{Fore.RESET} Using the video ID to download...")
            video.streams.first().download(output_path=save_Loc, filename=str(video.video_id)+ ".mp4")
            response = requests.get(str(video.thumbnail_url))
            with open(os.path.join(save_Loc, f"{str(video.video_id)}.jpg"), "wb") as f:
                f.write(response.content)
            videoe = VideoFileClip("%s.mp4" % os.path.join(save_Loc, str(video.video_id)))
            videoe.audio.write_audiofile("%s.mp3" % os.path.join(save_Loc, str(video.video_id)))
            videoe.close()
            os.remove("%s.mp4" % os.path.join(save_Loc, str(video.video_id)))
            song = eyed3.load(f"{os.path.join(save_Loc, str(video.video_id))}.mp3")
            song.tag.images.set(3, open(f"{os.path.join(save_Loc, f'{str(video.video_id)}.jpg')}", 'rb').read(), 'image/jpeg')
            song.tag.artist = f"{video.author}"
            song.tag.album = f"{album_input}"
            song.tag.album_artist = f"{album_artist_input}"
            song.tag.title = f"{video.title}"
            song.tag.save()
            os.remove("%s.jpg" % os.path.join(save_Loc, str(video.video_id)))
            os.system(f'eyed3 "{os.path.join(save_Loc, str(video.video_id))}.mp3"')
            notification.notify(title= 'Downloaded',
                    message= f'{video.title} has been downloaded',
                    app_icon = 'app.ico',
                    timeout= 0.1,
                    toast=False)
def take_PL(pl, album_input, album_artist_input, save_Loc):
    if pl.get() == "":
        print("No playlist link entered")
        take_PL()
    playlist = Playlist(f'{pl.get()}')
    print(f'Name of the playlist: {playlist.title}, Number of videos in playlist: {len(playlist.video_urls)}')
    if album_input.get() == "":
        album_input = "Unknown"
    if album_artist_input.get() == "":
        album_artist_input = "Unknown"
    if save_Loc.get() == "":
        if os.path.exists("music"):
            save_Loc = "music"
        else:
            os.mkdir("music")
            save_Loc = "music"
    download(playlist, album_input.get(), album_artist_input.get(), save_Loc.get())

def makeWindow():
    global root
    root = tk.Tk()
    root.title("Nightcore Downloader")
    root.geometry("300x200")
    root.resizable(False, False)
    root.configure(background='#24283b')
    tk.Label(root, text="Nightcore Downloader", font=("Helvetica", 16), fg="white", bg="#24283b").pack()
    if checkAppVer != app_Version:
        tk.Label(root, text="New Update Available", font=("Helvetica", 12), fg="white", bg="#24283b").pack()
        tk.Button(root, text="Update", command=lambda: webbrowser.open("https://www.github.com/unerasable/nightcore-downloader/releases")).pack()
    else:
        pl = tk.Entry(root)
        pl.pack()
        album_input = tk.Entry(root)
        album_input.pack()
        album_artist_input = tk.Entry()
        album_artist_input.pack()
        save_Loc = tk.Entry(root)
        save_Loc.pack()
        tk.Button(root, text="Download", command=lambda: take_PL(pl,album_input,album_artist_input,save_Loc)).pack()
    root.mainloop()
makeWindow()