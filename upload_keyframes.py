#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import argparse
import csv
import os
import re
import subprocess


def remove_trailing_slash(path):
    if len(path) == 0:
        return ''
    return path[:-1] if path[-1] == '/' else path


def get_keyframe_names(dst):
    return map(lambda x: (x[:-4], x[-3:]), os.listdir(dst))


def upload_keyframes(keyframes_folder, keyframes_url):
    gcloud_url = 'gs://' + keyframes_url.split('googleapis.com/')[1]
    print keyframes_folder
    subprocess.call(['gsutil', '-m', 'rsync', '-d', '-r', '{}'.format(keyframes_folder), gcloud_url])

    gcloud_urls = [gcloud_url + '/' + keyframe_name for keyframe_name in os.listdir(keyframes_folder)]

    # for url in sorted(gcloud_urls):
    #     subprocess.call(['gsutil', '-m', 'acl', '-r', 'ch', '-u', 'AllUsers:R', url])
    return gcloud_url


def main(input_folder, keyframes_url, output_file):
    keyframe_folders = get_keyframe_folders(input_folder)
    keyframe_names = reduce(lambda x, y: x + y, [map(lambda x: (input_folder + '/' + keyframe_folder + '/' + x[0], x[1]), get_keyframe_names(input_folder + '/' + keyframe_folder)) for keyframe_folder in keyframe_folders], [])
    keyframe_names = map(lambda x: x[0] + '.' + x[1], keyframe_names)
    gcloud_url = upload_keyframes(input_folder, keyframes_url)
    # gcloud_url = 'gs://studysmart-984.appspot.com/keyframes'
    with open(output_file, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['topic_name', 'order', 'url'])
        writer.writeheader()
        for keyframe_name in keyframe_names:
            match = re.match('(.*?) ?([0-9]+)\.jpg', keyframe_name.split('/')[-1])
            if match is None:
                print 'did\'t match', keyframe_name
            writer.writerow({
                'topic_name': match.group(1).strip(),
                'order': match.group(2),
                'url': '{}/{}'.format(gcloud_url, keyframe_name.split('/')[-2] +'/'+keyframe_name.split('/')[-1])
            })


def get_keyframe_folders(input_folder):
    return os.listdir(input_folder)

input_folder = '/home/crunch/Desktop/keyframes'
keyframes_url = 'https://storage.googleapis.com/studysmart-984.appspot.com/keyframes'
main(input_folder, keyframes_url, 'out.csv')
#
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Create screenshots from YouTube videos.')
#     parser.add_argument('input_folder', help='Input file - list of YouTube links.')
#     parser.add_argument('screenshots_url', help='URL to prefix file names with.')
#     parser.add_argument('-v', '--videos_dst', help='Destination folder for downloaded videos.', default='videos')
#     parser.add_argument('-s', '--screenshots_dst', help='Destination folder for created screenshots.', default='screenshots')
#     parser.add_argument('-o', '--output_file', help='Output CSV file.', default='screenshots.csv')
#
#     args = parser.parse_args()
#     main(args.input_file, args.videos_dst, args.screenshots_dst, args.screenshots_url, args.output_file)
