import subprocess

def extract_yuv_histogram(input_video, histogram_file):
    try:
        # Run FFmpeg command to extract YUV histogram
        command = [
            'ffmpeg',
            '-i', input_video,
            '-vf', 'split=2[a][b],[b]histogram,format=yuva444p[hh],[a][hh]overlay',
            '-vcodec', 'libx264',
            '-preset', 'ultrafast',
            '-y',
            histogram_file
        ]

        subprocess.run(command, check=True)

        print(f"YUV histogram extracted successfully. Output file: {histogram_file}")

    except subprocess.CalledProcessError as e:
        print(f"Error during YUV histogram extraction:\n{e}")
    except Exception as e:
        print(f"Unexpected error: {e}")