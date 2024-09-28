from moviepy.editor import VideoFileClip
import os

def convert_to_mp4(input_file, output_file):
    try:
        clip = VideoFileClip(input_file)
        clip.write_videofile(output_file, codec="libx264")
        clip.close()
        print(f"Converted {input_file} to MP4 successfully!")
    except Exception as e:
        print(f"Error converting {input_file} to MP4: {str(e)}")

def batch_convert_to_mp4(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(('.avi', '.mov', '.flv', '.wmv', '.mpeg', '.dav', '.h264')):
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, os.path.splitext(filename)[0] + '.mp4')
            convert_to_mp4(input_file, output_file)

# Specify input and output directories
input_folder = 'D:\Rohit\Input'
output_folder = 'D:\Rohit\output_videos'

# Convert all videos in the input folder to MP4 format
batch_convert_to_mp4(input_folder, output_folder)
