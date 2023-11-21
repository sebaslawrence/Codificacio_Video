import subprocess

def download_subtitles(video_url, output_file):
    try:
        # Run youtube-dl command to download subtitles
        command = ['youtube-dl', '--write-sub', '--sub-lang', 'en', '-o', output_file, video_url]
        subprocess.run(command, check=True)

        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error during subtitle download:\n{e}")
        return None

''' 
# Only try of downloading subtitles that actually works,  
# but could not convert it into a format that works, the txt that i did
# does not work with my ffmpeg call

srt = YouTubeTranscriptApi.get_transcript("kLpH1nSLJSs")

# creating or overwriting a file "subtitles.txt" with
# the info inside the context manager
with open("subtitles.txt", "w") as f:

        # iterating through each element of list srt
    for i in srt:
        # writing each element of srt on a new line
        f.write("{}\n".format(i))
'''

def integrate_subtitles(video_file, subtitles_file, output_file):
    try:
        # Integrate subtitles into the video using ffmpeg
        command = [
            'ffmpeg',
            '-i', video_file,
            '-vf', f'subtitles={subtitles_file}',
            '-c:a', 'copy',
            output_file
        ]

        subprocess.run(command, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error during subtitle integration:\n{e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def ex5():
    print("Hello from exercise4.py!")


'''Ex4
#i've tried everything, but downloading a youtube subtitle is a chaos since 
#how to do it changes constantly and current method YouTubeTranscriptApi
#does not seem to have the correct format (dictionary lits instead of srt) so after much more spent time that i would
#like to a admit i gave up in this exercise, anyways i kept parts of my implementation
#in the script just in case, but it does not work.

video_url = "https://www.youtube.com/watch?v=kLpH1nSLJSs"  # URL of YT video
output_video_file = "amorfoda_subs.mp4"
subtitles_file = "subtitles.srt"

# Download subtitles as a string and save to file
downloaded_subtitles_file = download_subtitles(video_url, subtitles_file)

# Integrate subtitles into the video
if downloaded_subtitles_file:
    integrate_subtitles("amorfoda_nosubs.mp4", downloaded_subtitles_file, output_video_file)
'''