import json
import cv2
from handlogic import init_hand

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

def init_hands_and_decks(current_red_deck, current_blue_deck, frame_count):
                #On the first frame, we need to initialize the previous decks and hands
    prev_red_deck = current_red_deck.copy()
    prev_blue_deck = current_blue_deck.copy()
    
    true_red_deck = current_red_deck.copy()
    true_blue_deck = current_blue_deck.copy()

    print(f"True red deck: {true_red_deck} as of frame {frame_count}")
    print(f"True blue deck: {true_blue_deck} as of frame {frame_count}")
    print("\n\n")
    
    red_hand = init_hand()
    blue_hand = init_hand()

    return prev_red_deck, prev_blue_deck, true_red_deck, true_blue_deck, red_hand, blue_hand