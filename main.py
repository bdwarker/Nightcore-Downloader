from pytube import Playlist
import eyed3
from moviepy.editor import *
import os
import time
import requests
playlist = Playlist('https://www.youtube.com/playlist?list=PLHst1FdxJujSKn6lOj_NO-ymiaeFkGALu')
print('Number of videos in playlist: %s' % len(playlist.video_urls))
album_input = input("Album name: ")
album_artist_input = input("Album artist name: ")
save_Loc = input("Save location: ")
for video in playlist.videos:
    video.streams.first().download(output_path=save_Loc, filename=video.title+ ".mp4")
    response = requests.get(str(video.thumbnail_url))
    with open(os.path.join(save_Loc, f"{video.title}.jpg"), "wb") as f:
        f.write(response.content)
    videoe = VideoFileClip("%s.mp4" % video.title)
    videoe.audio.write_audiofile("%s.mp3" % video.title)
    videoe.close()
    os.remove("%s.mp4" % video.title)
    song = eyed3.load(f"{video.title}.mp3")
    song.tag.artwork.set(3, open("%s.jpg" % video.title, 'rb').read(), 'image/jpeg')
    song.tag.artist = f"{video.author}"
    song.tag.album = f"{album_input}"
    song.tag.album_artist = f"{album_artist_input}"
    song.tag.title = f"{video.title}"
    song.tag.save()
    os.system(f'eyed3 "{video.title}.mp3"')