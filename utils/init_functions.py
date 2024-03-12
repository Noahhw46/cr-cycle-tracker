import json
import cv2

def init_rects():
    rect_locs = json.loads(open('locations/boxes.json').read())
    red_rects = []
    blue_rects = [] 

    for location in rect_locs["rect1"]:
        # Apply padding while ensuring the coordinates remain within frame boundaries
        new_location = (
            (location[0]),
            (location[1]),
            (location[2]),
            (location[3])
        )
        red_rects.append(new_location)

    for location in rect_locs["rect2"]:
        new_location = (
            (location[0]),
            (location[1]),
            (location[2]),
            (location[3])
        )
        blue_rects.append(new_location)

    return red_rects, blue_rects


def init_video(capture_file):
    cap = cv2.VideoCapture(capture_file)
    return cap if cap.isOpened() else None