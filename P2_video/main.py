import subprocess
import sys
import os

path_to_P1_video = os.path.abspath('/home/sebas/PycharmProjects')
sys.path.append(path_to_P1_video)

# Import the 2 functions from 'main.py' in the 'P1_video' project
from P1_video.main import rgb_to_yuv
from P1_video.main import yuv_to_rgb

# create a 10s file to faster working
# subprocess.run('ffmpeg -i BadBunny.mp4 -t 10 -c:v copy -c:a copy badbunny10.mp4', shell=True)

def change_resolution(input_video, output_video, width, height):
    """
    Change the resolution of a video using ffmpeg.

    Args:
        input_video (str): Path to the input video file.
        output_video (str): Path to the output video file.
        width (int): New width of the video.
        height (int): New height of the video.

    Returns:
        None
    """
    resize_command = f'ffmpeg -i "{input_video}" -vf "scale={width}:{height}" -c:a copy "{output_video}"'

    try:
        subprocess.run(resize_command, shell=True, check=True)
        print(f"Video resolution changed to {width}x{height}.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def change_chroma_subsampling(input_video, output_video):
    """
    Change the chroma subsampling of a video using ffmpeg.

    Args:
        input_video (str): Path to the input video file.
        output_video (str): Path to the output video file.

    Returns:
        None
    """
    subsampling_command = f'ffmpeg -i "{input_video}" -vf "format=yuv422p" -c:v libx264 -c:a copy "{output_video}"'

    try:
        subprocess.run(subsampling_command, shell=True, check=True)
        print(f"Chroma subsampling changed to 4:2:0.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def get_video_info(video_file):
    try:
        # Run FFprobe to get video information
        info_command = f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height,duration,r_frame_rate,codec_name -of default=noprint_wrappers=1:nokey=1 "{video_file}"'
        info_output = subprocess.check_output(info_command, shell=True, text=True)

        # Parse the output to get relevant data
        data = info_output.strip().split('\n')
        codec_name, width, height, frame_rate, duration = data

        # Print the relevant data
        print(f"Video File: {video_file}")
        print(f"Resolution: {width}x{height}")
        print(f"Duration: {duration} s")
        print(f"Frame Rate: {frame_rate} fps")
        print(f"Codec Name: {codec_name}")

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Error code: {e.returncode}")


'''
# Ex1
# Run the conversion command
subprocess.run('ffmpeg -i BadBunny.mp4 -q:a 0 -map a BBB.mp2', shell=True)

# Parse
subprocess.run('ffmpeg -i BBB.mp2', shell=True)
'''
'''
# Ex2
input_video = "badbunny10.mp4"
output_video = "BadBunny_newres.mp4"
new_width = 640
new_height = 360

change_resolution(input_video, output_video, new_width, new_height)
'''
'''
# Ex3
input_video = "badbunny10.mp4"
output_video = "BBBsubsampling.mp4"

change_chroma_subsampling(input_video, output_video)
'''
'''
# Ex4
video_file = "badbunny10.mp4"
get_video_info(video_file)
'''
'''
# Ex5
rgb_color = (100, 200, 50)
yuv_color = rgb_to_yuv(rgb_color)
rgb_color_reconverted = yuv_to_rgb(yuv_color)

print("RGB Color:", rgb_color)
print("YUV Color:", yuv_color)
print("Reconverted to RGB Color:", rgb_color_reconverted)
'''