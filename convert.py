#!/usr/bin/env python3
import os

import subprocess

src = '../Desktop/ySi0DomdkJs'
dst = '../Desktop/ySi0DomdkJs_new'
video_ids = os.listdir(src)

for video_id in video_ids:
    print 'converting screenshots of', video_id
    src_path = src + '/' + video_id
    dst_path = dst + '/' + video_id

    if not os.path.exists(dst_path):
        os.makedirs(dst_path)

    files = os.listdir(src_path)
    for f in files:
        src_file = src_path + '/' + f
        dst_file = dst_path + '/' + f[:-3] + 'jpg'
        subprocess.call(['convert', '-define', 'jpeg:extent=150kb', src_file, dst_file])
        print dst_file

# convert -define jpeg:extent=150kb 20-22.png 20-22.jpg
