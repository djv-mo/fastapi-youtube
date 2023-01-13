from fastapi import APIRouter, Query
from pydantic import HttpUrl
from pytube import Playlist, YouTube

download_playlist_router = APIRouter()


@download_playlist_router.get("/playlist/{url:path}")
async def download_playlist(url: HttpUrl, format: str = Query(..., title='playlist Format', description='Choose the format of the playlist',
                                                              choices=["144p", "360p", "720p", "1080p", 'audio'])):
    # getting the videos of the playlist
    yt = Playlist(url)
    playlist_videos = []
    for i in yt.videos:
        playlist_videos.append(i.watch_url)

    video_data = []
    # stock for resolutions

    def video_stock(res):
        for video in playlist_videos:
            ytv = YouTube(video)
            title = ytv.title
            thumbnail = ytv.thumbnail_url
            duration = ytv.length
            mp4_streams = ytv.streams.filter(
                progressive=True, resolution=res + 'p')
            mp4 = {}
            for stream in mp4_streams:
                mp4[stream.itag] = {'resolution': stream.resolution,
                                    'size_in_mb': stream.filesize_mb,
                                    'download_url': stream.url}
            video_data.append(
                {"title": title, 'thumbnail': thumbnail, 'duration': duration, 'streams': mp4})
    if format == '144p':
        video_stock(str(144))
    elif format == '360p':
        video_stock(str(360))
    elif format == '720p':
        video_stock(str(720))
    elif format == '1080p':
        video_stock(str(1080))
    elif format == 'audio':
        for video in playlist_videos:
            ytv = YouTube(video)
            title = ytv.title
            thumbnail = ytv.thumbnail_url
            duration = ytv.length
            mp3_streams = ytv.streams.get_audio_only()
            mp3 = {'abr': mp3_streams.abr,
                   'size_in_mb': mp3_streams.filesize_mb,
                   'audio_codec': mp3_streams.audio_codec.split(".")[0],
                   'download_url': mp3_streams.url}
            video_data.append(
                {"title": title, 'thumbnail': thumbnail, 'duration': duration, 'streams': mp3})
    return video_data
