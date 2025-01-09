import instaloader
import yt_dlp

from pytube import YouTube

video_url= "https://youtu.be/u7dRMiyM-wI?si=Fhr_ZYD1rhjfCJck"

ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    print(ydl.download([video_url]))