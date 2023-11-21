import subprocess
import os
import sys
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
# create a 9s file
# subprocess.run('ffmpeg -i BadBunny.mp4 -t 9 -c:v copy -c:a copy badbunny9.mp4', shell=True)

class VideoEditor:
    def __init__(self, input_video, output_video):
        self.input_video = input_video
        self.output_video = output_video

    def analyze_frames(self):
        # Use FFmpeg with drawbox and minterpolate filters to show motion vectors
        subprocess.run(['ffmpeg', '-flags2', '+export_mvs', '-i', self.input_video, '-vf', 'codecview=mv=pf+bf+bb', self.output_video])

    def edit_video(self):
        # Cut BBB into 50 seconds only video
        subprocess.run(['ffmpeg', '-i', self.input_video, '-t', '50', '-c:v', 'copy', '-c:a', 'aac', 'temp.mp4'])

        # Export BBB(50s) audio as MP3 mono track
        subprocess.run(['ffmpeg', '-i', 'temp.mp4', '-vn', '-ac', '1', 'audio_mono.mp3'])

        # Export BBB(50s) audio in MP3 stereo w/ lower bitrate
        subprocess.run(['ffmpeg', '-i', 'temp.mp4', '-vn', '-b:a', '64k', 'audio_stereo.mp3'])

        # Export BBB(50s) audio in AAC codec
        subprocess.run(['ffmpeg', '-i', 'temp.mp4', '-vn', '-c:a', 'aac', 'audio_aac.aac'])

        # Package everything in a .mp4 with FFmpeg
        subprocess.run(['ffmpeg', '-i', 'temp.mp4', '-i', 'audio_mono.mp3', '-i', 'audio_stereo.mp3', '-i', 'audio_aac.aac','-c:v', 'copy', '-c:a', 'aac', self.output_video])

        # Clean up temporary files
        subprocess.run(['rm', 'temp.mp4', 'audio_mono.mp3', 'audio_stereo.mp3', 'audio_aac.aac'])

def count_tracks(input_video):
    try:
        # Run ffprobe command to get information about the tracks
        command = ['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type', '-of', 'default=noprint_wrappers=1:nokey=1', input_video]
        result = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)

        # Parse the output to count the different types of tracks
        track_types = result.strip().split('\n')

        # Count the occurrences of each track type
        track_counts = {track_type: track_types.count(track_type) for track_type in set(track_types)}

        return track_counts

    except subprocess.CalledProcessError as e:
        print(f"Error during ffprobe execution:\n{e.output}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


''' Ex1
if __name__ == "__main__":
    input_video_path = 'badbunny9.mp4'
    output_video_path = 'output_ex1.mp4'

    analyzer = VideoEditor(input_video_path, output_video_path)
    analyzer.analyze_frames()
'''

''' Ex2
if __name__ == "__main__":
    input_video_path = 'BadBunny.mp4'
    output_video_path = 'output_ex2.mp4'

    editor = VideoEditor(input_video_path, output_video_path)
    editor.edit_video()
'''

'''Ex3
input_video_path = "badbynny9.mp4" # downloaded another video with multiple tracks to check but deleted in the submission as it was too big to upload
track_counts = count_tracks(input_video_path)

if track_counts is not None:
    print(f"Track counts for '{input_video_path}': {track_counts}")
else:
    print(f"Failed to get track counts for '{input_video_path}'.")
'''

'''Ex5
# As i could not make that function really work, a created another, ex5()

# import the function
from exercise4 import ex5

# Call the function from exercise4.py
ex5()
'''

'''Ex6
# import the function
from exercise6 import extract_yuv_histogram

# Call the function from exercise6.py
input_video = 'badbunny9.mp4'
histogram_output_file = 'output_ex6.mp4'

extract_yuv_histogram(input_video, histogram_output_file)
'''