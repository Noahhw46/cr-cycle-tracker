import cv2
import os
import numpy as np
import json
from utils.init_functions import init_rects

def is_point_inside_rect(x, y, rect):
    # Unpack the rectangle's top-left and bottom-right points
    x1, y1, x2, y2 = rect
    return x1 <= x <= x2 and y1 <= y <= y2

def check_white_pixels_in_row_within_rects(image, rects, min_white_pixels):
    white_pixel_sequences = []  # List to hold the start and end points of sequences within rectangles

    for rect in rects:
        x1, y1, x2, y2 = rect  

        for y in range(y1, y2):  
            white_count = 0  
            start_x = None  

            for x in range(x1, x2):  
                color = image[y, x]
                if np.all(color == 255):  
                    white_count += 1  
                    if start_x is None:
                        start_x = x  

                    if white_count > min_white_pixels and x == x2 - 1:  
                        white_pixel_sequences.append(((start_x, y), (x, y)))
                        white_count = 0 
                        start_x = None
                else:
                    if white_count > min_white_pixels:
                        white_pixel_sequences.append(((start_x, y), (x - 1, y))) 
                    white_count = 0 
                    start_x = None 

    return white_pixel_sequences

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        color = param[y, x]  # Use the passed image (param) instead of the global one
        print(f"BGR Color at position ({x}, {y}): {color}")

def process_frame(image_path):
    image = cv2.imread(image_path)
    frame_height, frame_width = image.shape[:2]
    red_rects, blue_rects = init_rects(frame_height, frame_width)

    #Draw the rectangles
    for rect in red_rects:
        cv2.rectangle(image, (rect[0], rect[1]), (rect[2], rect[3]), (0, 0, 255), 2)
    for rect in blue_rects:
        cv2.rectangle(image, (rect[0], rect[1]), (rect[2], rect[3]), (255, 0, 0), 2)
    if image is None:
        print(f"Error: Image at {image_path} not loaded. Check the file path.")
        return

    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', click_event, image)  # Pass the image as a parameter to the callback

    min_white_pixels = 50
    
    white_pixel_sequences_in_red = check_white_pixels_in_row_within_rects(image, red_rects, min_white_pixels)
    white_pixel_sequences_in_blue = check_white_pixels_in_row_within_rects(image, blue_rects, min_white_pixels)

    for seq in white_pixel_sequences_in_red + white_pixel_sequences_in_blue:
        print(f"Sequence of white pixels in a row found within a rectangle from {seq[0]} to {seq[1]}")
        x1, y1 = seq[0]
        x2, y2 = seq[1]
        zoomed_in = image[max(y1-64, 0):min(y2+64, frame_height), max(x1-64, 0):min(x2+64, frame_width)]
        cv2.imshow('Zoomed in view', zoomed_in)
        cv2.waitKey(0)
        cv2.destroyAllWindows()



    cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

frames_dir = 'frames/logbait'
start_frame = 670
end_frame = 700

# Loop through the frames and process each one
for i in range(start_frame, end_frame + 1):
    frame_path = os.path.join(frames_dir, f"frame{i}.jpg")
    print(f"Processing frame {frame_path}")
    process_frame(frame_path)
