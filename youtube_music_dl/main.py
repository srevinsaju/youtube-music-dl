import os
from token import ISTERMINAL
import urllib

import mutagen
import youtube_dl
from youtube_dl.YoutubeDL import YoutubeDL
import ytmusicapi

from typing import List, Union
from mutagen.id3 import APIC, ID3
from mutagen.mp3 import MP3


class YoutubeSong:
    def __init__(
        self, video_id: str, album: str = None, artist: str = None, track: str = None
    ):
        self.video_id = video_id
        self.album = album
        self.artist = artist
        self.track = track


class YtMusicDownload:
    def __init__(self):
        self.yt_music = ytmusicapi.YTMusic()

    def fetch_info(self, url: str) -> List[YoutubeSong]:
        with youtube_dl.YoutubeDL({}) as ytdl:
            items = ytdl.extract_info(url, download=False)
        if "entries" not in items:
            # this is a single song
            ids = [
                YoutubeSong(
                    video_id=items["id"],
                    album=items.get("album"),
                    artist=items.get("artist"),
                )
            ]
        else:
            ids = [
                YoutubeSong(
                    video_id=items["entries"][x]["id"],
                    album=items["entries"][x].get("album"),
                    artist=items["entries"][x].get("artist"),
                )
                for x in range(len(items["entries"]))
            ]
        return ids

    def download(
        self,
        video_ids: Union[List[str], List[YoutubeSong]],
        overwrite: bool = False,
        destination: str = None,
    ):
        if destination is None:
            destination = os.path.abspath("youtube_music_downloads")

        destination = os.path.abspath(destination)
        os.makedirs(destination, exist_ok=True)

        for song in video_ids:
            if isinstance(song, str):
                data = self.yt_music.get_song(song)
                album = ""
            elif isinstance(song, YoutubeSong):
                data = self.yt_music.get_song(song.video_id)
                album = song.album
            else:
                raise ValueError("Invalid value provided")
            title = data["videoDetails"]["title"]
            artist = data["videoDetails"]["author"].rstrip(" - Topic")
            url = data["microformat"]["microformatDataRenderer"]["urlCanonical"]

            file_path = os.path.join(destination, f"{artist} - {title}")
            outtmpl = f"{file_path}.%(ext)s"
            if not overwrite and os.path.exists(f"{file_path}.mp3"):
                # already exists and the user has explicitly asked not to overwrite
                continue

            print(f"Downloading {title} by {artist} to {file_path} ({url})")
            ydl_opts = {
                "format": "bestaudio",
                "outtmpl": outtmpl,
                "noplaylist": True,
                "postprocessor_args": [
                    "-metadata",
                    "title=" + title,
                    "-metadata",
                    "artist=" + artist,
                ],
            }
            if album:
                ydl_opts["postprocessor_args"].extend(["-metadata", "album=" + album])
            mp3_postprocess_opts = {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "0",
            }

            ydl_opts["postprocessors"] = [mp3_postprocess_opts]

            with youtube_dl.YoutubeDL(ydl_opts) as ytdl:
                ytdl.download([url])
            thumbnails = data["videoDetails"]["thumbnail"]["thumbnails"]
            thumbnail = thumbnails[-1]
            thumbnail_url = thumbnail["url"]

            try:
                song_file = MP3(f"{file_path}.mp3", ID3=ID3)
            except mutagen.MutagenError as e:
                print(e)
                print(
                    "Failed to download: {}, please ensure YouTubeDL is up-to-date. ".format(
                        file_path
                    )
                )
                continue

            song_file.tags["APIC"] = APIC(
                encoding=3,
                mime="image/{}".format(thumbnail_url.split(".")[-1]),
                type=3,
                desc="Cover",
                data=urllib.request.urlopen(thumbnail_url).read(),
            )
            song_file.save()
