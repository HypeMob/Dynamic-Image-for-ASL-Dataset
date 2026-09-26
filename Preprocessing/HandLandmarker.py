# Full

import os
import cv2
import shutil
import mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions
from moviepy.editor import VideoFileClip

# --- 1. CONFIGURATION ---
BASE_PATH = "/content/drive/MyDrive/WLASL Trimmed/"
CROPPED_ROOT = "/content/drive/MyDrive/WLASL Cropped/"
ANNOTATED_ROOT = "/content/drive/MyDrive/WLASL Annotated/"
MODEL_PATH = '/content/hand_landmarker.task' # Local Colab path is faster
PADDING = 0.15

base_options = BaseOptions(model_asset_path=MODEL_PATH)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.IMAGE,
    num_hands=2
)
detector = vision.HandLandmarker.create_from_options(options)

# --- 2. HELPER FUNCTIONS ---

def get_static_boundaries(video_path):
    """Pass 1: Find the global max/min for this specific video."""
    try:
        clip = VideoFileClip(video_path)
        g_min_x, g_min_y, g_max_x, g_max_y = 1.0, 1.0, 0.0, 0.0
        found = False

        for frame in clip.iter_frames():
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            res = detector.detect(mp_image)
            if res.hand_landmarks:
                found = True
                for hand in res.hand_landmarks:
                    for lm in hand:
                        g_min_x, g_min_y = min(g_min_x, lm.x), min(g_min_y, lm.y)
                        g_max_x, g_max_y = max(g_max_x, lm.x), max(g_max_y, lm.y)

        if not found:
            clip.close()
            return None

        img_h, img_w = clip.size[1], clip.size[0]
        w_box, h_box = g_max_x - g_min_x, g_max_y - g_min_y

        x1 = max(0, int((g_min_x - w_box * PADDING) * img_w))
        y1 = max(0, int((g_min_y - h_box * PADDING) * img_h))
        x2 = min(img_w, int((g_max_x + w_box * PADDING) * img_w))
        y2 = min(img_h, int((g_max_y + h_box * PADDING) * img_h))

        clip.close()
        return (x1, y1, x2, y2)
    except Exception as e:
        return None

def process_video(video_path, rel_path, bbox):
    """Pass 2: Create both the Cropped and Annotated versions."""
    try:
        x1, y1, x2, y2 = bbox
        clip = VideoFileClip(video_path)

        # 1. Annotated Version
        ann_out = os.path.join(ANNOTATED_ROOT, rel_path)
        os.makedirs(os.path.dirname(ann_out), exist_ok=True)

        def draw_box(frame):
            img = frame.copy()
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 4)
            return img

        ann_clip = clip.fl_image(draw_box)
        ann_clip.write_videofile("/content/temp_ann.mp4", logger=None, audio=True, codec="libx264")
        shutil.move("/content/temp_ann.mp4", ann_out)

        # 2. Cropped Version
        crop_out = os.path.join(CROPPED_ROOT, rel_path)
        os.makedirs(os.path.dirname(crop_out), exist_ok=True)

        cropped_clip = clip.crop(x1=x1, y1=y1, x2=x2, y2=y2)
        # You can add .resize(height=224) here if your model needs consistent sizes
        cropped_clip.write_videofile("/content/temp_crop.mp4", logger=None, audio=True, codec="libx264")
        shutil.move("/content/temp_crop.mp4", crop_out)

        clip.close()
        return True
    except Exception as e:
        print(f"Pass 2 Error on {rel_path}: {e}")
        return False

# --- 3. MAIN LOOP ---

classes = sorted([f for f in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, f))])

for class_name in classes:
    class_dir = os.path.join(BASE_PATH, class_name)

    # for view_type in ["Front", "Side"]: # Or whatever your folder names are
    #     view_dir = os.path.join(class_dir, view_type)
    #     if not os.path.exists(view_dir): continue

    for video_file in sorted(os.listdir(class_dir)): #view_dir > class_dir
        if video_file.lower().endswith(('.mp4', '.mov', '.avi')):
            rel_path = os.path.join(class_name, video_file) #view_type > x
            final_destination = os.path.join(CROPPED_ROOT, rel_path)

            # --- RESUME CHECK ---
            if os.path.exists(final_destination):
                continue

            video_path = os.path.join(class_dir, video_file)

            bbox = get_static_boundaries(video_path)
            if bbox:
                process_video(video_path, rel_path, bbox)
            else:
                print(f" error")

detector.close()