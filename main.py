from numpy import take
from pytube import Playlist
import eyed3
from moviepy.editor import *
import os
import time
import requests
import colorama
from colorama import Fore, Style


def download():
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
        except:
            print(f'{Fore.RED}[ERROR]{Fore.RESET} {video.title} failed to download')
            print(f"{Fore.YELLOW}[WARNING]{Fore.RESET} Using the video ID to download...")
            video = str(video.video_id)
            video.streams.first().download(output_path=save_Loc, filename=video+ ".mp4")
            response = requests.get(str(video.thumbnail_url))
            with open(os.path.join(save_Loc, f"{video}.jpg"), "wb") as f:
                f.write(response.content)
            videoe = VideoFileClip("%s.mp4" % os.path.join(save_Loc, video))
            videoe.audio.write_audiofile("%s.mp3" % os.path.join(save_Loc, video))
            videoe.close()
            os.remove("%s.mp4" % os.path.join(save_Loc, video))
            song = eyed3.load(f"{os.path.join(save_Loc, video)}.mp3")
            song.tag.images.set(3, open(f"{os.path.join(save_Loc, f'{video}.jpg')}", 'rb').read(), 'image/jpeg')
            song.tag.artist = f"{video.author}"
            song.tag.album = f"{album_input}"
            song.tag.album_artist = f"{album_artist_input}"
            song.tag.title = f"{video.title}"
            song.tag.save()
            os.remove("%s.jpg" % os.path.join(save_Loc, video))
            os.system(f'eyed3 "{os.path.join(save_Loc, video)}.mp3"')






def take_PL():
    global playlist
    global save_Loc
    global album_input
    global album_artist_input
    pl = input("Enter playlist link: ")
    if pl == "":
        print("No playlist link entered")
        take_PL()
    playlist = Playlist(f'{pl}')
    print(f'Name of the playlist: {playlist.title}, Number of videos in playlist: {len(playlist.video_urls)}')
    album_input = input("Album name: ")
    if album_input == "":
        album_input = "Unknown"
    album_artist_input = input("Album artist name: ")
    if album_artist_input == "":
        album_artist_input = "Unknown"
    save_Loc = input("Save location: ")
    if save_Loc == "":
        if os.path.exists("music"):
            save_Loc = "music"
        else:
            os.mkdir("music")
            save_Loc = "music"
    download()
take_PL()