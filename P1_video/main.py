import subprocess
import numpy as np
from scipy.fftpack import dct, idct

def rgb_to_yuv(rgb):
    """
    Convert RGB to YUV.
    Input:
        rgb (tuple): RGB values as (R, G, B) where R, G, B are in the range [0, 255].
    Output:
        yuv (tuple): YUV values as (Y, U, V) where Y, U, V are in their respective ranges.
    """
    R, G, B = rgb
    Y = 0.299 * R + 0.587 * G + 0.114 * B
    U = -0.147 * R - 0.289 * G + 0.436 * B
    V = 0.615 * R - 0.515 * G - 0.100 * B
    return Y, U, V

def yuv_to_rgb(yuv):
    """
    Convert YUV to RGB.
    Input:
        yuv (tuple): YUV values as (Y, U, V) where Y, U, V are in their respective ranges.
    Output:
        rgb (tuple): RGB values as (R, G, B) where R, G, B are in the range [0, 255].
    """
    Y, U, V = yuv
    R = Y + 1.140 * V
    G = Y - 0.395 * U - 0.581 * V
    B = Y + 2.032 * U
    return int(R), int(G), int(B)

def resize_lower(input_path, output_path, width, height, quality):
    """
     Args:
        input_path (str): Path to the input image file.
        output_path (str): Path to the output image file.
        width (int): New width in pixels.
        height (int): New height in pixels.
        quality (int): Output image quality (0-51; lower values mean higher compression).

    Returns:
        None
    """
    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-vf', f'scale={width}:{height}',
        '-q:v', str(quality),
        output_path
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"Image resized and saved to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def read_image_serpentine(filename, width, height):
    """
        Read the bytes of an image file in a serpentine way.

        Args:
            filename (str): The path to the image file.
            width (int): Width of the image in pixels.
            height (int): Height of the image in pixels.

        Returns:
            bytes: The serpentine bytes of the JPEG file.
    """
    with open(filename, 'rb') as file:
        data = file.read()

    # Initialize variables for zigzag order
    serpentine_data = bytearray(width * height)
    x, y = -1, 0
    direction = 1  # 1 for right, -1 for left

    for i in range(width * height):
        index = y * width + x
        serpentine_data[i] = data[index]

        if y % 2 == 0:
            x += direction
        else:
            x -= direction

        if x < 0:
            y += 1
            x = 0
            direction = 1
        elif x >= width:
            y += 1
            x = width - 1
            direction = -1

    return bytes(serpentine_data)

def convert_to_bw_compression(input_image, output_image):
    """
    Convert an image to black and white (grayscale) with the highest compression using FFMPEG.

    Args:
        input_image (str): Input image file path.
        output_image (str): Output image file path (compressed in JPG format).
    """
    # Use FFMPEG to convert the image to grayscale and apply high compression
    ffmpeg_command = [
        "ffmpeg",
        "-i", input_image,
        "-vf", "format=gray",
        "-q:v", "100",  # high compression
        output_image
    ]

    try:
        subprocess.run(ffmpeg_command, check=True)
        print(f"Image converted and compressed to {output_image}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def run_length_encode(data):
    """
    Apply run-length encoding (RLE) to a series of bytes.

    Args:
        data (bytes): Input byte sequence to be encoded.

    Returns:
        bytes: RLE encoded byte sequence.
    """
    encoded_data = bytearray()
    i = 0

    while i < len(data):
        count = 1
        while i + 1 < len(data) and data[i] == data[i + 1]:
            count += 1
            i += 1
        encoded_data.append(count)
        encoded_data.append(data[i])
        i += 1

    return bytes(encoded_data)

class DCTConverter:
    def __init__(self, block_size=8):
        self.block_size = block_size

    def encode(self, data):
        """
        Encode input data using DCT.

        Args:
            data (np.array): Input data as a NumPy array.

        Returns:
            np.array: DCT encoded data.
        """
        # creates encoded array same size as data
        encoded_data = np.zeros_like(data)

        # 2 for loop to divide 8 blocks
        for i in range(0, data.shape[0], self.block_size):
            for j in range(0, data.shape[1], self.block_size):
                block = data[i:i + self.block_size, j:j + self.block_size] # go through the block
                encoded_block = dct(dct(block.T, norm='ortho').T, norm='ortho') # 2D dct (rows and columns)
                encoded_data[i:i + self.block_size, j:j + self.block_size] = encoded_block

        return encoded_data

    def decode(self, encoded_data):
        """
        Decode DCT encoded data.

        Args:
            encoded_data (np.array): DCT encoded data.

        Returns:
            np.array: Decoded data.
        """

        # All the same as encode but with idct
        decoded_data = np.zeros_like(encoded_data)

        for i in range(0, encoded_data.shape[0], self.block_size):
            for j in range(0, encoded_data.shape[1], self.block_size):
                block = encoded_data[i:i + self.block_size, j:j + self.block_size]
                decoded_block = idct(idct(block.T, norm='ortho').T, norm='ortho')
                decoded_data[i:i + self.block_size, j:j + self.block_size] = decoded_block

        return decoded_data

"""
# ex 1
rgb_color = (100, 200, 50)
yuv_color = rgb_to_yuv(rgb_color)
rgb_color_reconverted = yuv_to_rgb(yuv_color)

print("RGB Color:", rgb_color)
print("YUV Color:", yuv_color)
print("Reconverted to RGB Color:", rgb_color_reconverted)
"""

"""
# ex2
input_image = "duki.jpg"
output_image = "duki_lowerquality.jpg"
new_width = 368
new_height = 555
output_quality = 20

resize_lower(input_image, output_image, new_width, new_height, output_quality)
"""

"""
# ex 3
serpentine_bytes = read_jpeg_serpentine("kirby8x8.jpg", 8, 8)
"""

"""
# ex 4
convert_to_bw_compression("duki.jpg", "duki_bw_compressed.jpg")
"""

"""
# ex 5
input_bytes = b'\x01\x01\x01\x01\x01\x01\x02\x03\x03\x04\x05\x05\x05\x05\x05\x05\xFF'
encoded_bytes = run_length_encode(input_bytes)
print("Input bytes: ", input_bytes)
print("Encoded Bytes:", encoded_bytes)
"""

"""
# ex 6
if __name__ == '__main__':
    # Create a sample input data as a NumPy array
    # data must be 8-multiple
    input_data = np.random.rand(8,8)

    # Create an instance of the DCTConverter class
    dct_converter = DCTConverter()

    # Encode the input data using DCT
    encoded_data = dct_converter.encode(input_data)

    # Decode the encoded data
    decoded_data = dct_converter.decode(encoded_data)

    # Check if the decoded data is close to the original input data
    is_close = np.allclose(input_data, decoded_data, atol=1e-8) # if absolute difference < 0.00000001 algorithm works
    print("Encoded and then decoded data is close to the original input data:", is_close)
"""