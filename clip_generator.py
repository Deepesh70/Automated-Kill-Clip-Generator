import cv2 
import numpy as np
from moviepy.editor import VideoFileClip

# ========Detecting kill timestamps========

def find_kill_timestamps(video_path, template_path):

    print("Starting kill detection")

    video = cv2.VideoCapture(video_path)

    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    w,h = template.shape[::-1]

    threshold = 0.8

    kill_timestamps = []

    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)

    frame_number = 0
    while(video.isOpened()):

        ret, frame = video.read()

        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)

        loc = np.where(result >= threshold)

        if len(loc[0]) > 0:
            timestamp = frame_number/fps
            print(f"Kill detected at {round(timestamp, 2)} seconds.")

            if not kill_timestamps or timestamps > kill_timestamps[-1] + 2: #2 second colldown
                kill_timestamps.append(timestamp)
                print(f"Confirmed kill at {round(timestamp, 2)} seconds.")  
            frame_number += 1

    video.realease()
    print(f"Detection complete. FOund{len(kill_timestamps)} kills.")
    return kill_timestamps


# Creating clips

def create_clips(video_path, timestamps, output_folder= 'clips'):
    if not timestamps:
        print("No timestamps found, no clips to create")
        return
    print("starting clip creation")

    original_video = VideoFileClip(video_path)

    for i , ts in enumerate(timestamps):
        start_time = max(0, ts-5)
        end_time= min(original_video.duration, ts+5)

        print(f"Creating clip{i+1}: from {round(start_time, 2)}s to {round(end_time ,2)}s")

        new_clip= original_video.subclip(start_time, end_time)

        output_filename= f"{output_folder}/kill_clip_{i+1}.mp4"
        new_clip.write_videofile(output_filename, codec="libx264")

    print("All clips have been created")


if __name__ == "__main__":


    input_video_path = " "
    template_image_path = " "

    foudn_timestamps = find_kill_timestamps(input_video_path, template_image_path)

    import os
    if not os.path.exists("clips"):
        os.makedirs("clips")

    create_clips(input_video_path, foudn_timestamps)
