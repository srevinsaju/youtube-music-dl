# youtube-music-dl

Download Youtube Music playlists, songs with their Album Arts and some metadata, with
the help of [`ytmusicapi`](https://ytmusicapi.readthedocs.io/) and [`youtube-dl`](https://github.com/ytdl-org/youtube-dl/).

**Disclaimer**: Downloading copyright songs may be illegal in your country. 
This tool is for educational purposes only and was created only to show how Youtube Music's API 
can be used to download music from YouTube. Please support the artists by buying their music.


## Contributing
Pull requests are welcome. Feel free to...

* Revise documentation
* Add new features
* Fix bugs
* Suggest improvements

## Usage
`youtube_music_dl` is available as an AppImage.

```bash
rm -rf ~/.local/bin/youtube-music-dl
wget https://github.com/srevinsaju/youtube-music-dl/releases/download/continuous/youtube_music_dl-x86_64.AppImage -O ~/.local/bin/youtube-music-dl
chmod +x ~/.local/bin/youtube-music-dl

youtube-music-dl --help
```


## Development

All dependencies are managed by [`poetry`](https://github.com/python-poetry/poetry)

```bash
git clone https://github.com/srevinsaju/youtube-music-dl
cd youtube-music-dl
poetry install
poetry run cli --help
```


## Usage

To run, simply do
```bash
poetry run cli url_to_youtube_music_song_or_playlist
```


## License

MIT License. See [LICENSE](./LICENSE) for more information.
