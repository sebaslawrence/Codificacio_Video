import subprocess


# create a 30s file to faster working
# subprocess.run('ffmpeg -i BadBunny.mp4 -t 30 -c:v copy -c:a copy Bunny.mp4', shell=True)

class VideoConverter:
    def __init__(self, input_video):
        self.input_video = input_video

    def convert_to_vp8(self, output_video):
        self._convert_video('libvpx', 'vp8', output_video)

    def convert_to_vp9(self, output_video):
        self._convert_video('libvpx-vp9', 'vp9', output_video)

    def convert_to_h265(self, output_video):
        self._convert_video('libx265', 'h265', output_video)

    def convert_to_av1(self, output_video):
        self._convert_video('libaom-av1', 'av1', output_video)

    def _convert_video(self, codec, extension, output_video):
        command = [
            'ffmpeg',
            '-i', self.input_video,
            '-c:v', codec,
            output_video
        ]
        subprocess.run(command)


class VideoComparison:
    def __init__(self, input_vp8, input_vp9, output_video):
        self.input_vp8 = input_vp8
        self.input_vp9 = input_vp9
        self.output_video = output_video

    def compare_vp8_vp9(self):
        # Combine VP8 and VP9 videos side by side
        subprocess.run(['ffmpeg', '-i', self.input_vp8, '-i', self.input_vp9, '-filter_complex', 'hstack=inputs=2', self.output_video])


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


''' Convert bunny 30s video to all the resolutions needed
input_video = "Bunny.mp4"
output_video = "Bunny_120p.mp4"
new_width = 160
new_height = 120
change_resolution(input_video, output_video, new_width, new_height)
'''

''' Ex1
input_video_path = 'Bunny_480p.mp4'
converter = VideoConverter(input_video_path)

# Convert to VP8
converter.convert_to_vp8('output_vp8.webm')

# Convert to VP9
converter.convert_to_vp9('output_vp9.webm')

# Convert to H.265 (HEVC)
converter.convert_to_h265('output_h265.mp4')

# Convert to AV1
converter.convert_to_av1('output_av1.webm')
'''

''' Ex2
input_vp8_path = 'output_vp8.webm'
input_vp9_path = 'output_vp9.webm'
output_video_path = 'comparison_output.mp4'

video_comparison = VideoComparison(input_vp8_path, input_vp9_path, output_video_path)
video_comparison.compare_vp8_vp9()

# Viendo los videos uno al lado del otr, creo que no veo ninguna diferencia.
# Lo cierto es que la resolucion es demasiado baja como para notar nada.
# Pero si que me da la sensacion de que el vp9 sea mejor, ya que no se
# si me lo estoy imaginando pero parece muy ligeramente que los colores
# tengan mas profundidad y los de vp8 sean mas planos, aunque no se si
# soy yo ya.
'''

