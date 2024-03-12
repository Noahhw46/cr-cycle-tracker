import cv2
import numpy as np
from utils.loadtemplates import load_templates
from utils.init_functions import init_video, init_rects
from handlogic import update_hand, init_hand
from utils.printing import color_print
from frame_processing.user_interaction import process_key_press
from drawhands import show_hand, draw_rects_and_update_current_decks

def post_process_decks(match_frequency, current_deck, true_deck, prev_deck, prev_cards, frame_count, color, hand):
    #If the new card is a question mark and the previous card wasn't then we know that that card was played 
    #However, we need to check if it was played before, as sometimes there is an issue where the matching function
    #will on one frame detect a question mark (ie the card was played) and then on the next frame detect that same card and then on the *next*
    #frame detect a different card. This is a problem because it will look like the card was played twice.
    for rect, card in current_deck.items():
        if true_deck[rect] != "questionmark":
            if prev_deck[rect] not in prev_cards.keys():
                if card == "uncertain" and prev_deck[rect] != "uncertain":
                    color_print(color, f"{color} Player played: {card} at frame {frame_count}")
                    prev_cards[prev_deck[rect]] = frame_count
                    hand = update_hand(hand, prev_deck[rect])

            elif frame_count - prev_cards[prev_deck[rect]] > match_frequency*5:
                if card == "uncertain" and prev_deck[rect] != "uncertain":
                    color_print(color, f"{color} Player played: {card} at frame {frame_count}")
                    prev_cards[prev_deck[rect]] = frame_count
                    hand = update_hand(hand, prev_deck[rect])

        elif card != "uncertain" and card != "questionmark" and true_deck[rect] == "questionmark":
                color_print(color, f"{color} Player played: {card} at frame {frame_count}")
                prev_cards[card] = frame_count
                true_deck[rect] = card
                hand = update_hand(hand, card)


    return prev_deck, prev_cards, hand

def main():
    true_red_deck = {}
    true_blue_deck = {}
    prev_red_deck = {}
    prev_blue_deck = {}
    current_red_deck = {}
    current_blue_deck = {}

    red_prev_cards = {}
    blue_prev_cards = {}

    frame_count = 0
    match_frequency = 3

    matched_red_cards = set()
    matched_blue_cards = set()

    templates = load_templates()
    game_file = input("Enter the path to the game file: ")
    cap = init_video(game_file)
    # Initialize rectangles with frame dimensions
    red_rects, blue_rects = init_rects()
    red_cache = {}
    blue_cache = {}


    while cap.isOpened():
        ret, frame = cap.read()
        frame_count += 1

        if frame_count % match_frequency != 0:
            continue
        if not ret:
            break

        current_red_deck = draw_rects_and_update_current_decks(current_red_deck, red_rects, frame, templates, red_cache, matched_red_cards)
        current_blue_deck = draw_rects_and_update_current_decks(current_blue_deck, blue_rects, frame, templates, blue_cache, matched_blue_cards)

        if frame_count == match_frequency:
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


        prev_red_deck, red_prev_cards, red_hand = post_process_decks(match_frequency, current_red_deck, true_red_deck, prev_red_deck, red_prev_cards, frame_count, "red", red_hand)
        prev_blue_deck, blue_prev_cards, blue_hand = post_process_decks(match_frequency, current_blue_deck, true_blue_deck, prev_blue_deck, blue_prev_cards, frame_count, "blue", blue_hand)


        show_hand("red", red_hand, templates)
        show_hand("blue", blue_hand, templates)

        prev_red_deck = current_red_deck.copy()
        prev_blue_deck = current_blue_deck.copy()

        cv2.imshow('Matched Frame', frame)

        key = cv2.waitKey(1)

        frame_count = process_key_press(key, cap, frame_count)
        
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()