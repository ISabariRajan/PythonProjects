import shutil
import cv2
import json
import time
from os.path import join as joinpath, splitext, exists
from os import listdir, makedirs

config = {}
with open('config.json', "r") as f:
    config = json.loads("".join(f.readlines()))

def check_and_create_folder(foldername):
    if not exists(foldername):
        makedirs(foldername)

def convert_video_to_image(
            video_file,
            convert_to,
            output_folder,
            move_video_file=False,
            output_file=None
        ):
    if move_video_file:
        if output_file == None:
            print("output_file keyword is required when move_video_file is True")
    check_and_create_folder(output_folder)
    vid = cv2.VideoCapture(video_file)
    if not vid.isOpened():
        print("NOT OPEN")
        vid.release()
        return
    frameId = 1
    while True:
        # Read frame and ret
        ret, frame = vid.read()
        if ret:
            img_path = joinpath(output_folder, str(frameId).rjust(3, "0") + convert_to)
            cv2.imwrite(img_path, frame)
            frameId += 1
        else:
            break
    time.sleep(3)
    if move_video_file:
        shutil.move(filename, output_file)

input_folder = config["input_folder"]
output_folder = config["output_folder"]
output_format = config["output_format"]
try:
    print("VideoConverter --- Started")
    while True:
        filelist = listdir(input_folder)
        for c_file in filelist:
            filename = joinpath(input_folder, c_file)
            name, ext = splitext(c_file)
            if ext in config["accepted_formats"]:
                print("Converting " + filename + " to " + output_format)
                convert_video_to_image(
                    filename,
                    output_format,
                    joinpath(output_folder, name),
                    move_video_file=True,
                    output_file=joinpath(output_folder, c_file)
                )
                print("Convertion Complete..")

except KeyboardInterrupt:
    print("Exiting..")
    print("VideoSoftware --- Ended")

except Exception as e:
    print("Other " + str(e))
