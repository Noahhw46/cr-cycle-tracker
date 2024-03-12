import cv2
from utils.loadtemplates import load_templates
from utils.init_functions import init_video, init_rects, init_hands_and_decks
from frame_processing.user_interaction import process_key_press
from frame_processing.templatematching import post_process_decks
from drawhands import show_hand, draw_rects_and_update_current_decks

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
            prev_red_deck, prev_blue_deck, true_red_deck, true_blue_deck, red_hand, blue_hand = init_hands_and_decks(current_red_deck, current_blue_deck, frame_count)


        prev_red_deck, red_prev_cards, red_hand = post_process_decks(match_frequency, current_red_deck, true_red_deck, prev_red_deck, red_prev_cards, frame_count, "red", red_hand)
        prev_blue_deck, blue_prev_cards, blue_hand = post_process_decks(match_frequency, current_blue_deck, true_blue_deck, prev_blue_deck, blue_prev_cards, frame_count, "blue", blue_hand)


        show_hand("red", red_hand, templates)
        show_hand("blue", blue_hand, templates)

        prev_red_deck = current_red_deck.copy()
        prev_blue_deck = current_blue_deck.copy()

        cv2.imshow('Game', frame)

        key = cv2.waitKey(1)

        frame_count = process_key_press(key, cap, frame_count)
        
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()