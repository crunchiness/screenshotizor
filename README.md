Downloads a list of youtube videos and "converts them into screenshots".
Use for videos that are for the most part static.

This has 3 major dependencies:

* numpy
* youtube-dl
* avconv

As output produces PNG images that comprehensively represent the video,
and a CSV file with schema ```video_id,url,start,end``` where each row
represents a screenshot.


```
usage: screenshotizor.py [-h] [-v VIDEOS_DST] [-s SCREENSHOTS_DST]
                         [-o OUTPUT_FILE]
                         input_file screenshots_url

Create screenshots from YouTube videos.

positional arguments:
  input_file            Input file - list of YouTube links.
  screenshots_url       URL to prefix file names with.

optional arguments:
  -h, --help            show this help message and exit
  -v VIDEOS_DST, --videos_dst VIDEOS_DST
                        Destination folder for downloaded videos.
  -s SCREENSHOTS_DST, --screenshots_dst SCREENSHOTS_DST
                        Destination folder for created screenshots.
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Output CSV file.
```
