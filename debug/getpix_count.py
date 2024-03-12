import cv2
import numpy as np
import json
from utils.init_functions import init_rects

def count_color_pixels_within_rects(image_path, target_color, image, rects):


    count_white = []

    for rect in rects:
        x1, y1, x2, y2 = rect 
        roi = image[y1:y2, x1:x2]
        match = np.all(roi == target_color, axis=-1)
        count = np.sum(match)

        count_white.append(count)

    return count_white

def main():
    target_color = [255, 255, 255] 

    frame_path = input("Enter the frames path: ")

    for image_path in frame_path:
        image = cv2.imread(image_path)
        frame_height, frame_width = image.shape[:2]
        red_rects, blue_rects = init_rects(frame_height, frame_width)
        rects = red_rects + blue_rects
        pixel_count = count_color_pixels_within_rects(image_path, target_color, image, rects)
        print(f"Number of pixels matching the target color in {image_path}: {pixel_count}")
