import os
import moviepy
import cv2
import imageio

# REMEMBER CHANGE PATH 
path = r'C:/Coding/Thesis/Dataset/Thesis Dataset Exp/HOUSE/'
full_path = os.path.abspath(path)


# change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.0-Q16-HDRI\magick.exe"}) 

# moviepy.config.check()

# print(os.listdir(path))
# os.mkdir(path + 'Trimmed')
# os.mkdir(path + 'Cropped')
# os.mkdir(path + 'Cropped/Front')
# os.mkdir(path + 'Cropped/Side')

names = os.listdir(path)
names.remove('Trimmed')
names.remove('Cropped')
names.remove('Frames')
print(names)

# test = ['sign_377806.mp4', 'sign_378003.mp4']
# print(test)

# VIDEO DURATION FOR TRIMMING
duration = 1

# Trim Video
def trimVideo(path, names):
    for idx, name in enumerate(names):
    #     # print(path + name)
        video = moviepy.VideoFileClip(os.path.join(path, name))
        if(video.duration < duration):
            video.write_videofile(os.path.join(path, 'Trimmed', name))
        else:
            action = video.subclipped(0, duration)
            action.write_videofile(os.path.join(path, 'Trimmed', name))

# Crop Video
def cropVideo(path, names):
    for idx, name in enumerate(names):
        # print(path + 'Trimmed/' + name)
        video = moviepy.VideoFileClip(os.path.join(path, 'Trimmed', name))
        front = video.cropped(x1=0, y1=0, x2=640, y2=720)
        side = video.cropped(x1=640, y1=0, x2=1280, y2=720)

        front.write_videofile(os.path.join(path, 'Cropped', 'Front', name))
        side.write_videofile(os.path.join(path, 'Cropped', 'Side', name))

# trimVideo(full_path, names)
cropVideo(full_path, names)
    

# Extract Frames
def extractFrames(path, names):
    if not os.path.exists(os.path.join(path, "Frames")):
        os.mkdir(os.path.join(path, "Frames"))
        print(f"Created Folder: {os.path.join(path, "Frames")} ")
        

    for idx, name in enumerate(names):
        video = moviepy.VideoFileClip(os.path.join(path, "Cropped", "Side", name))
        for idxx, frame in enumerate(video.iter_frames()):
            frame_name = os.path.join(path, "Frames", f"{name}_Side{idxx:04d}.jpg")

            imageio.imwrite(frame_name, frame)
    


extractFrames(full_path, names)
classes = os.listdir(r'C:/Coding/Thesis/Dataset/Thesis Dataset Exp')
classes = ['BUY']

for i in classes:
    filepath = os.path.join(path, i)
    if not os.path.exists(os.path.join(filepath, "Frames")):
        os.mkdir(os.path.join(filepath, "Frames"))
        print(f"Created Folder: {os.path.join(path, "Frames")} ")
    front = os.listdir(os.path.join(filepath, "Cropped", "Front"))
    side = os.listdir(os.path.join(filepath, "Cropped", "Side"))
    
    # print(front)
    
    for idx, name in enumerate(front):
        video = moviepy.VideoFileClip(os.path.join(filepath, "Cropped", "Front", name))
        for idxx, frame in enumerate(video.iter_frames()):
            frame_name = os.path.join(filepath, "Frames", f"{name}_Front{idxx:04d}.jpg")

            imageio.imwrite(frame_name, frame)

    for idx, name in enumerate(side):
        video = moviepy.VideoFileClip(os.path.join(filepath, "Cropped", "Side", name))
        for idxx, frame in enumerate(video.iter_frames()):
            frame_name = os.path.join(filepath, "Frames", f"{name}_Side{idxx:04d}.jpg")

            imageio.imwrite(frame_name, frame)

print(path + 'Trimmed/' + "sign.mp4")

video = moviepy.VideoFileClip('Dataset/Thesis Dataset Exp/Eat/sign_458664.mp4')
# print('Width: ', video.w, ' Height: ', video.h)
front = video.cropped(x1=0, y1=0, x2=640, y2=720)
side = video.cropped(x1=640, y1=0, x2=1280, y2=720)
front.write_videofile(path + 'Cropped/Front/Test.mp4')
side.write_videofile(path + 'Cropped/Side/Test.mp4')