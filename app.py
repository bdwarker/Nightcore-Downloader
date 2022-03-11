# importing necessary modules
import os
import colorama
import time
import requests
from colorama import Fore, Style
from numpy import take
from pytube import Playlist
from pytube import YouTube
import eyed3
from moviepy.editor import *
import unicodedata
import re
os.system("cls")
# app version
app_Version = "1.1.0"
jsonFile = "https://unerasable.github.io/application.json"
def check_valid_status_code(request):
    if request.status_code == 200:
        return request.json()

    return False
def get_application_get_url():
    request = requests.get(jsonFile)
    data = check_valid_status_code(request)
    return data
app_URL=get_application_get_url()
checkAppVer = f"{app_URL['nightcoreDownloader']['verson']}"
def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def download(playlist, album_input, album_artist_input, save_Loc):
    for video in playlist.videos:
        try:
            print(f'{Fore.GREEN}[INFO]{Fore.RESET} Downloading {video.title}...')
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
            print(f'{Fore.GREEN}Downloaded {video.title}!{Style.RESET_ALL}')
        except:
            vid_NewName = slugify(video.title)
            video.streams.first().download(output_path=save_Loc, filename=str(vid_NewName)+ ".mp4")
            response = requests.get(str(video.thumbnail_url))
            with open(os.path.join(save_Loc, f"{str(vid_NewName)}.jpg"), "wb") as f:
                f.write(response.content)
            videoe = VideoFileClip("%s.mp4" % os.path.join(save_Loc, str(vid_NewName)))
            videoe.audio.write_audiofile("%s.mp3" % os.path.join(save_Loc, str(vid_NewName)))
            videoe.close()
            os.remove("%s.mp4" % os.path.join(save_Loc, str(vid_NewName)))
            song = eyed3.load(f"{os.path.join(save_Loc, str(vid_NewName))}.mp3")
            song.tag.images.set(3, open(f"{os.path.join(save_Loc, f'{str(vid_NewName)}.jpg')}", 'rb').read(), 'image/jpeg')
            song.tag.artist = f"{video.author}"
            song.tag.album = f"{album_input}"
            song.tag.album_artist = f"{album_artist_input}"
            song.tag.title = f"{video.title}"
            song.tag.save()
            os.remove("%s.jpg" % os.path.join(save_Loc, str(vid_NewName)))
            os.system(f'eyed3 "{os.path.join(save_Loc, str(vid_NewName))}.mp3"')
            print(f'{Fore.GREEN}Downloaded {video.title}!{Style.RESET_ALL}')
    print(f'{Fore.GREEN}[INFO]{Fore.RESET} All videos downloaded!')
    main()

def downloadOneFile(url, artist, album, save_Loc):
    try:
        video = YouTube(url)
        if album == "":
            album = "Unknown"
        if artist == "":
            artist = "Unknown"
        if save_Loc == "":
            save_Loc = "."
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
        song.tag.artist = f"{artist}"
        song.tag.album = f"{album}"
        song.tag.title = f"{video.title}"
        song.tag.save()
        os.remove("%s.jpg" % os.path.join(save_Loc, video.title))
        os.system(f'eyed3 "{os.path.join(save_Loc, video.title)}.mp3"')
        print(f'{Fore.GREEN}Downloaded {video.title}!{Style.RESET_ALL}')
        main()
    except Exception as e:
        vid_NewName = slugify(video.title)
        print(f'{Fore.RED}[ERROR]{Fore.RESET} {video.title} failed to download')
        print(f"{Fore.YELLOW}[WARNING]{Fore.RESET} Using the video ID to download...")
        video.streams.first().download(output_path=save_Loc, filename=str(vid_NewName)+ ".mp4")
        response = requests.get(str(video.thumbnail_url))
        with open(os.path.join(save_Loc, f"{str(vid_NewName)}.jpg"), "wb") as f:
            f.write(response.content)
        videoe = VideoFileClip("%s.mp4" % os.path.join(save_Loc, str(vid_NewName)))
        videoe.audio.write_audiofile("%s.mp3" % os.path.join(save_Loc, str(vid_NewName)))
        videoe.close()
        os.remove("%s.mp4" % os.path.join(save_Loc, str(vid_NewName)))
        song = eyed3.load(f"{os.path.join(save_Loc, str(vid_NewName))}.mp3")
        song.tag.images.set(3, open(f"{os.path.join(save_Loc, f'{str(vid_NewName)}.jpg')}", 'rb').read(), 'image/jpeg')
        song.tag.artist = f"{video.author}"
        song.tag.album = f"{album}"
        song.tag.album_artist = f"{artist}"
        song.tag.title = f"{video.title}"
        song.tag.save()
        os.remove("%s.jpg" % os.path.join(save_Loc, str(vid_NewName)))
        os.system(f'eyed3 "{os.path.join(save_Loc, str(vid_NewName))}.mp3"')
        print(f'{Fore.GREEN}Downloaded {video.title}!{Style.RESET_ALL}')

def main():
    vidorpl = input(f'{Fore.GREEN}[INFO]{Fore.RESET} Would you like to download a playlist or a video(pl/vid): ')
    if vidorpl.lower() == "pl":
        pl = input(f"{Fore.BLUE}[INPUT]{Fore.RESET} Enter the playlist URL: ")
        album_input = input(f"{Fore.BLUE}[INPUT]{Fore.RESET} Enter the album name: ")
        album_artist_input = input(f"{Fore.BLUE}[INPUT]{Fore.RESET} Enter the album artist: ")
        save_Loc = input(f"{Fore.BLUE}[INPUT]{Fore.RESET} Enter the save location: ")
        try:
            playlist = Playlist(pl)
            if album_input == "":
                album_input = "Unknown"
            if album_artist_input == "":
                album_artist_input = "Unknown"
            if save_Loc == "":
                save_Loc = "."
            download(playlist, album_input, album_artist_input, save_Loc)
        except:
            print(f"{Fore.RED}[ERROR]{Fore.RESET} Invalid playlist URL")
            main()
    elif vidorpl.lower() == "vid":
        try:
            url = input(f"{Fore.BLUE}[INPUT]{Fore.RESET} Enter the video URL: ")
            artist = input(f"{Fore.BLUE}[INPUT]{Fore.RESET} Enter the album artist: ")
            album = input(f"{Fore.BLUE}[INPUT]{Fore.RESET} Enter the album: ")
            save_Loc = input(f"{Fore.BLUE}[INPUT]{Fore.RESET} Enter the save location: ")
            downloadOneFile(url, artist, album, save_Loc)
        except:
            print(f"{Fore.RED}[ERROR]{Fore.RESET} An error occured please try again")
            main()
    else:
        print(f"{Fore.RED}[ERROR]{Fore.RESET} Invalid input")
        main()





if app_Version == checkAppVer:
    print(f"{Fore.GREEN}[INFO]{Fore.RESET} You are using the latest version of the application")
    print(f"{Fore.GREEN}[INFO]{Fore.RESET} Version: {app_Version}")
    main()
elif app_Version > checkAppVer:
    print(f"{Fore.RED}[ERROR]{Fore.RESET} You are using an outdated version of the application")
    print(f"{Fore.YELLOW}[WARNING]{Fore.RESET} You are using {app_Version} and the latest version is {checkAppVer}")
    print(f"{Fore.YELLOW}[WARNING]{Fore.RESET} Please update the application")
    print(f"{Fore.YELLOW}[WARNING]{Fore.RESET} You can download the latest version from {app_URL['nightcoreDownloader']['download']}")
    exit()
elif app_Version < checkAppVer:
    print(f"{Fore.RED}[ERROR]{Fore.RESET} You are using a version that has not even been released? HOWWW?")
    print(f"{Fore.YELLOW}[WARNING]{Fore.RESET} You can download the latest version from {app_URL['nightcoreDownloader']['download']}")
    exit()

if __name__ == "__main__":
    main()