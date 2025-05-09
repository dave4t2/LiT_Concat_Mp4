# -*- coding: utf-8 -*-
import os
import subprocess
import logging
from datetime import datetime

# Configure logging
log_filename = f"./logs/concat_Launch_v2_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}_Log.txt"
logging.basicConfig(
    filename=log_filename,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Script execution started.")

# Define Path names and file names
video1_name = 'Begin.mp4'
video3_name = 'End.mp4'
video1_path = os.path.join('./input/Video1', video1_name)
video2_path = './input/Video2/'
video3_path = os.path.join('./input/Video3', video3_name)
temp_folder = './temp'
ConcatVideo_path = './output'
os.makedirs(temp_folder, exist_ok=True)

try:
    # Check if the personalized videos directory exists
    if not os.path.exists(video2_path):
        raise FileNotFoundError(f"Directory not found: {video2_path}")

    logging.info(f"Personalized directory found: {video2_path}")

    # Check if the output directory exists
    if not os.path.exists(ConcatVideo_path):
        raise FileNotFoundError(f"Directory not found: {ConcatVideo_path}")

    logging.info(f"Output directory found: {ConcatVideo_path}")

    # Check if the first video exists
    if not os.path.exists(video1_path):
        raise FileNotFoundError(f"File not found: {video1_path}")

    logging.info(f"Clip 1 found: {video1_path}")

    # Check if the last video exists
    if not os.path.exists(video3_path):
        raise FileNotFoundError(f"File not found: {video3_path}")

    logging.info(f"Clip 3 found: {video3_path}")

    video_files = os.listdir(video2_path)
    mp4_files = [file for file in video_files if file.endswith(".mp4")]
    logging.info(f"Number of MP4 files in the directory: {len(mp4_files)}")

    # Function to run FFmpeg commands and handle logs
    def run_ffmpeg_command(command):
        logging.debug(f"Running FFmpeg command: {' '.join(command)}")
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            logging.error(f"FFmpeg command failed: {stderr}")
            raise RuntimeError(f"FFmpeg command failed: {stderr}")
        logging.debug(f"FFmpeg command succeeded: {stdout}")
        return stdout

    # Function to convert an MP4 file to TS
    def convert_to_ts(input_file, output_file):
        logging.info(f"Converting to TS: {input_file} -> {output_file}")
        run_ffmpeg_command([
            "ffmpeg", "-i", input_file, "-c", "copy", "-bsf:v", "h264_mp4toannexb", "-f", "mpegts", output_file, "-y"
        ])

    # Iterate over all MP4 files in the personalized directory
    for file in mp4_files:
        personalized_clip_path = os.path.join(video2_path, file)
        output_name = f"bodycam_{file}"
        output_path = os.path.join(ConcatVideo_path, output_name)

        # Skip if the output file already exists
        if os.path.exists(output_path):
            logging.info(f"File already exists, skipping: {output_path}")
            continue

        # Define paths for intermediate TS files
        ts1_path = os.path.join(temp_folder, "intermediate_1.ts")
        ts2_path = os.path.join(temp_folder, "intermediate_2.ts")
        ts3_path = os.path.join(temp_folder, "intermediate_3.ts")
        input_list_file = os.path.join(temp_folder, "input_list.txt")

        logging.debug(f"Intermediate TS paths: {ts1_path}, {ts2_path}, {ts3_path}")
        logging.debug(f"Input list file path: {input_list_file}")

        # Convert MP4 files to TS
        logging.info(f"Converting to TS: {video1_path}, {personalized_clip_path}, {video3_path}")
        convert_to_ts(video1_path, ts1_path)
        convert_to_ts(personalized_clip_path, ts2_path)
        convert_to_ts(video3_path, ts3_path)

        # Create the input list for FFmpeg concatenation
        with open(input_list_file, "w") as f:
            # Use absolute paths to avoid path resolution issues
            f.write(f"file '{os.path.abspath(ts1_path)}'\n")
            f.write(f"file '{os.path.abspath(ts2_path)}'\n")
            f.write(f"file '{os.path.abspath(ts3_path)}'\n")
        logging.debug("Input list file created successfully.")
        with open(input_list_file, "r") as f:
            logging.debug(f"Content of input_list.txt:\n{f.read()}")

        # Log the FFmpeg input file path
        logging.debug(f"FFmpeg input file: {input_list_file}")

        # Concatenate TS files into the final MP4
        logging.info(f"Concatenating videos into: {output_path}")
        run_ffmpeg_command([
            "ffmpeg", "-f", "concat", "-safe", "0", "-fflags", "+genpts",
            "-i", input_list_file, "-c", "copy", "-bsf:a", "aac_adtstoasc",
            "-y", output_path
        ])

        # Clean up intermediate files
        os.remove(ts1_path)
        os.remove(ts2_path)
        os.remove(ts3_path)
        os.remove(input_list_file)

        logging.info(f"Processing completed successfully: {output_path}")

    logging.info("All videos have been processed successfully.")

except Exception as e:
    logging.error(f"An error occurred: {e}")
    raise

logging.info("Script execution finished.")