import csv
import numpy as np
import os
import shutil
import subprocess
from PIL import Image


def mse(image1, image2):
    """
    the 'Mean Squared Error' between the two images is the
    sum of the squared difference between the two images;
    NOTE: the two images must have the same dimension
    """
    err = np.sum((image1 - image2) ** 2)
    err /= float(image1.shape[0] * image1.shape[1])
    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


def remove_trailing_slash(path):
    if len(path) == 0:
        return ''
    return path[:-1] if path[-1] == '/' else path


def download_videos(input_file, dst):
    dst = remove_trailing_slash(dst)

    with open(input_file, 'r') as f:
        for line in f:
            subprocess.call(['youtube-dl', '--no-playlist', line, '-o{}/%(id)s.%(ext)s'.format(dst)])


def get_video_ids(dst):
    return map(lambda x: x[:-4], os.listdir(dst))


def make_screenshots(videos_dst, video_id, screenshots_dst, fmt='mkv'):
    videos_dst = remove_trailing_slash(videos_dst)
    screenshots_dst = remove_trailing_slash(screenshots_dst)

    subprocess.call(['mkdir', '{}/{}'.format(screenshots_dst, video_id)])
    subprocess.call(['avconv', '-i', '{}/{}.{}'.format(videos_dst, video_id, fmt), '-vsync', '1', '-r', '1', '-an', '-y', '{}/{}/%d.png'.format(screenshots_dst, video_id)])


def compress_screenshots(video_id, screenshots_dst, threshold=3.):
    screenshots_dst = remove_trailing_slash(screenshots_dst)

    frame_files = sorted(os.listdir('{}/{}'.format(screenshots_dst, video_id)), key=lambda x: int(x[:-4]))

    screenshots = []
    frame_to_save = None
    start_time = 0
    for frame1, frame2 in zip(frame_files[:-1], frame_files[1:]):
        frame_to_save = frame1 if frame_to_save is None else frame_to_save
        image1 = np.array(Image.open('{}/{}/{}'.format(screenshots_dst, video_id, frame1)).convert('L'))
        image2 = np.array(Image.open('{}/{}/{}'.format(screenshots_dst, video_id, frame2)).convert('L'))
        frame1_num = int(frame1[:-4])
        frame2_num = int(frame2[:-4])
        err = mse(image1, image2)
        if err > threshold:
            screenshots.append(('{}/{}/{}'.format(screenshots_dst, video_id, frame_to_save), start_time, frame1_num))
            start_time = frame2_num
            frame_to_save = frame2
    if len(frame_files) > 1:
        screenshots.append(('{}/{}/{}'.format(screenshots_dst, video_id, frame_to_save), start_time, frame2_num))

    for (orig_name, start, end) in screenshots:
        shutil.copyfile(orig_name, '{}/{}/{}-{}.png'.format(screenshots_dst, video_id, start, end))

    frame_paths = map(lambda frame_file: '{}/{}/{}'.format(screenshots_dst, video_id, frame_file), frame_files)
    subprocess.call(['rm'] + frame_paths)


def write_compressed_info(video_id, screenshots_dst, writer, screenshots_url):
    screenshots_dst = remove_trailing_slash(screenshots_dst)
    screenshots_url = remove_trailing_slash(screenshots_url)

    for frame_file in os.listdir('{}/{}'.format(screenshots_dst, video_id)):
        start, end = map(int, frame_file[:-4].split('-'))
        writer.writerow({
            'video_id': video_id,
            'url': '{}/{}/{}'.format(screenshots_url, video_id, frame_file),
            'start': start,
            'end': end
        })


if __name__ == '__main__':
    input_file = 'youtube.txt'
    videos_dst = 'videos'
    screenshots_dst = 'screenshots'
    screenshots_url = 'https://storage.googleapis.com/studysmart-984.appspot.com/screenshots/'
    # download_videos(input_file, videos_dst)
    video_ids = get_video_ids(videos_dst)

    subprocess.call(['rm', '-fr', screenshots_dst])
    subprocess.call(['mkdir', screenshots_dst])

    output_file = 'output.csv'
    with open(output_file, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['video_id', 'url', 'start', 'end'])
        writer.writeheader()
        for video_id in video_ids:
            make_screenshots(videos_dst, video_id, screenshots_dst)
            compress_screenshots(video_id, screenshots_dst)
            write_compressed_info(video_id, screenshots_dst, writer, screenshots_url)