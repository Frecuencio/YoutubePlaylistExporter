# YoutubePlaylistExporter
Youtube playlist exporter (HTML, CSV and TXT) written in python3.

Script requires pytube too work, you can install it via python pip:
```bash
python -m pip install pytube
```

## Usage

Only -pl argument is required, containging the YouTube plalyist id (String after https://www.youtube.com/playlist?list= ).
Note that HTML file is not a real backup or dump, use with urlfile or csv if you want a real backup.

```
YoutubePlaylistExporter.py -pl PLAYLIST [-n NAME] [-nd] [-nc] [-d DELIMITER] [-q QUOTECHAR] [-u] [-html] [-w WAIT] [-dl]

Backup Youtube playlist into CSV, html and/or txt file.

optional arguments:
  -h, --help            show this help message and exit
  -pl PLAYLIST, --playlist PLAYLIST
                        Playlist ID
  -n NAME, --name NAME  Generated filename (name+date if not -nd present). Playlist name used if not specified
  -nd, --nodate         Don't prepend date on filename
  -nc, --nocsv          Don't generate CSV file
  -d DELIMITER, --delimiter DELIMITER
                        Delimiter used in CSV file (Default= , )
  -q QUOTECHAR, --quotechar QUOTECHAR
                        Quote character used in CSV file (Default= | )
  -u, --urlfile         Generate TXT with only urls
  -html, --html         Generate HTML file
  -w WAIT, --wait WAIT  Wait specified seconds between videos, useful if you get HTTP Error 429: Too Many Requests
  -dl, --download       Automatic download all the videos
```


CSV contains: Name of the video, url, author, publish date, lenth, description and keywords.
Take in mind that script may take a long since it opens every video while is creating the CSV video to take all the data

Thanks to https://github.com/pytube/pytube for making the script way easier.
