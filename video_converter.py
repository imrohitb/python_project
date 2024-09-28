from moviepy.editor import VideoFileClip
from tqdm import tqdm
import os
import time

def convert_to_mp4(input_file, output_file):
    try:
        video = VideoFileClip(input_file)
        video.write_videofile(output_file, codec="libx264", audio_codec="aac")
        video.close()
    except Exception as e:
        print(f"Error converting {input_file}: {e}")

def batch_convert_to_mp4(input_folder, output_folder):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of all video files in the input folder
    video_files = [f for f in os.listdir(input_folder) if f.endswith(('.avi', '.mov', '.mkv', '.mpg', '.wmv', '.ts', '.dav'))]

    for video_file in tqdm(video_files, desc="Converting videos", unit="file"):
        input_path = os.path.join(input_folder, video_file)
        output_file = os.path.join(output_folder, os.path.splitext(video_file)[0] + '.mp4')

        print(f"Converting {video_file} to {output_file}")

        start_time = time.time()
        convert_to_mp4(input_path, output_file)
        elapsed_time = time.time() - start_time

        print(f"Conversion time: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    input_folder = r"D:\Rohit\Input"  # Use 'r' before the path to treat it as a raw string
    output_folder = r"D:\Rohit\Output"

    batch_convert_to_mp4(input_folder, output_folder)
