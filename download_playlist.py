from fastapi import APIRouter, HTTPException
from pydantic import HttpUrl
import youtube_dl

download_playlist_router = APIRouter()


@download_playlist_router.get("/playlist")
async def download_playlist(url: HttpUrl, resolution: str):
    if resolution not in ['audio', 'mp4']:
        raise HTTPException(
            status_code=400, detail="resolution should be audio or mp4")
    # getting the videos of the playlist
    try:
        ydl_opts = {}
        if resolution == 'audio':
            ydl_opts = {
                'format': 'bestaudio',
            }
        elif resolution == 'mp4':
            ydl_opts = {
                "format": "best",
            }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=False)
            playlist_videos = result['entries']
            video_data = []

            if resolution == 'audio':

                for video in playlist_videos:
                    audio_formats = [
                        f for f in video['formats'] if f['vcodec'] == 'none']
                    best_audio_format = max(
                        audio_formats, key=lambda f: f['filesize'])

                    video_info = {'title': video['title'], 'thumbnail': video['thumbnail'],
                                  'duration_sec': video['duration'], 'channel_name': video['uploader'],
                                  'quality': 'best', 'size_in_mb': best_audio_format['filesize'] / (1024 * 1024) if best_audio_format['filesize'] is not None else None,
                                  'media_type': best_audio_format['ext'], 'url': best_audio_format['url']}

                    video_data.append(video_info)
                return {'data': video_data}
            elif resolution == 'mp4':
                for video in playlist_videos:
                    video_info = {
                        'title': video['title'],
                        'thumbnail': video['thumbnail'],
                        'duration_sec': video['duration'],
                        'channel_name': video['uploader'],
                        'streams': []
                    }

                    for fmt in video['formats']:
                        if fmt['vcodec'] != 'none' and fmt['acodec'] != 'none':
                            if fmt['filesize'] is None:
                                for similar_fmt in video['formats']:
                                    if similar_fmt['format_note'] == fmt['format_note'] and similar_fmt['height'] <= fmt['height'] and similar_fmt['filesize'] is not None:
                                        fmt['filesize'] = similar_fmt['filesize']
                            if resolution in fmt['format_note'] and fmt['filesize'] is not None:
                                if resolution == '360p':
                                    for fmt_ in result['formats']:
                                        if resolution == '720p' and fmt_['filesize'] > fmt['filesize']:
                                            break
                            new_format = {

                                'quality': fmt['format_note'],
                                'size_in_mb': fmt['filesize'] / (1024 * 1024) if fmt['filesize'] is not None else None,
                                'media_type': fmt['ext'],
                                'url': fmt['url']
                            }
                            video_info['streams'].append(new_format)
                    video_data.append(video_info)
                return {'data': video_data}
            else:
                raise HTTPException(
                    status_code=404, detail="Format not available")
    except youtube_dl.utils.DownloadError as e:
        raise HTTPException(
            status_code=404, detail="Invalid video id or url or video is deleted from YouTube")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred, please try again later {e}")
