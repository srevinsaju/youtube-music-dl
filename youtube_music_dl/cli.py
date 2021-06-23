#!/usr/bin/env python
import os
import click
from typing import List
from .main import YtMusicDownload


@click.command()
@click.argument("url", nargs=-1)
@click.option(
    "--output",
    help="Directory to store music",
    default=os.path.abspath("youtube_music_dl"),
    type=click.Path(),
)
@click.option(
    "--overwrite/--no-overwrite",
    help="Overwrite music even if it exists in the destination folder",
)
def cli(url: List[str], output: str, overwrite: bool = False):
    """Simple Youtube Music Downloader"""
    if len(url) == 0:
        print("You should provide at least one URL to download. See --help for more information.")
        return
    id_list_total = []
    ytdl = YtMusicDownload()
    for u in url:
        id_list = ytdl.fetch_info(u)
        id_list_total.extend(id_list)
    ytdl.download(id_list_total, overwrite=overwrite, destination=output)


if __name__ == "__main__":
    cli()
