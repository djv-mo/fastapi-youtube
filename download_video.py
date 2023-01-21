from fastapi import APIRouter
import youtube_dl
download_video_router = APIRouter()


@download_video_router.get("/video")
async def download_video(video_id: str, resolution: str):
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        ydl_opts = {}
        if resolution == 'audio':
            ydl_opts = {
                'format': 'bestaudio',
                # 'no-m3u8-prefer-native': True,
            }
        elif resolution == 'mp4':
            ydl_opts = {
                "format": "best",
            }
        else:
            return {'error': 'resolution should be audio or mp4'}

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:

            result = ydl.extract_info(url, download=False)

            if resolution == 'audio':
                audio_formats = [f for f in result['formats']
                                 if f['vcodec'] == 'none']
                best_audio_format = max(
                    audio_formats, key=lambda f: f['filesize'])
                return {'title': result['title'],
                        'thumbnail': result['thumbnail'],
                        'duration_sec': result['duration'],
                        'channel_name': result['uploader'],
                        'quality': 'best',
                        'size_in_mb': best_audio_format['filesize'] / (1024 * 1024),
                        'media_type': best_audio_format['ext'],
                        'url': best_audio_format['url']}

            elif resolution == 'mp4':
                best_formats = []
                for fmt in result['formats']:

                    if fmt['vcodec'] != 'none' and fmt['acodec'] != 'none':
                        if fmt['filesize'] is None:
                            for similar_fmt in result['formats']:
                                if similar_fmt['format_note'] == fmt['format_note']\
                                        and similar_fmt['height'] <= fmt['height']\
                                        and similar_fmt['filesize'] is not None:
                                    fmt['filesize'] = similar_fmt['filesize']
                        if resolution in fmt['format_note'] and fmt['filesize'] is not None:
                            if resolution == '360p':
                                for fmt_ in result['formats']:
                                    if resolution == '720p' and fmt_['filesize'] > fmt['filesize']:
                                        break
                        new_format = {
                            'quality': fmt['format_note'],
                            'size_in_mb': fmt['filesize'] / (1024 * 1024),
                            'media_type': fmt['ext'],
                            'url': fmt['url']
                        }
                        best_formats.append(new_format)
                if best_formats:
                    return {'title': result['title'],
                            'thumbnail': result['thumbnail'],
                            'duration_sec': result['duration'],
                            'channel_name': result['uploader'],
                            'formats': best_formats}

                else:
                    return {"error": "Format not available"}
    except:
        return {"error": "check the url make sure you use  video id"}
 
