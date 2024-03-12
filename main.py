import cv2
import numpy as np
from utils.loadtemplates import load_templates
from utils.init_functions import init_video, init_rects

def process_key_press(key, cap, frame_count):
    if key == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        exit()
    if key == ord('s'):
        for i in range(20):
            ret, frame = cap.read()
            frame_count += 1
            if not ret:
                break
    if key == ord('p'):
        print("Paused")
        while True:
            key = cv2.waitKey(0)
            if key == ord('p'):
                print("Unpaused")
                break
    if key == ord('r'):
        rewind_frames = 20 
        new_frame_count = max(frame_count - rewind_frames, 0) 
        cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame_count) 
        frame_count = new_frame_count 
        print(f"Rewound to frame {frame_count}")
    return frame_count

def has_problematic_colors(roi, pixel_threshold=250):
    problematic_colors = [
        [255, 255, 255],  
    ]
    count = 0
    for color in problematic_colors:
        count += np.sum(np.all(roi == color, axis=-1))

        # If the count exceeds the threshold, assume an emote is present
        if count > pixel_threshold:
            return True

    return False

def color_print(color, text):
    if color == "red":
        print(f"\033[91m{text}\033[00m")
    elif color == "blue":
        print(f"\033[94m{text}\033[00m")

def print_template_sizes(templates):
    for template_name, template in templates.items():
        print(f"Template {template_name} has size {template.shape[0]}, {template.shape[1]}.")

def find_best_match(frame, framenum, rect, templates, cache, matched_cards, threshold=0.7):
    # Check the cache first
    roi = frame[rect[1]:rect[3], rect[0]:rect[2]]
    
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if rect in cache:
        cached_template_name = cache[rect]
        cached_template = templates[cached_template_name] if len(templates[cached_template_name].shape) == 2 else cv2.cvtColor(templates[cached_template_name], cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(gray_frame[rect[1]:rect[3], rect[0]:rect[2]], cached_template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)
        if max_val > threshold:
            return cached_template_name # Cached match is still good
        elif has_problematic_colors(roi) and cached_template_name != "questionmark":
            return cached_template_name # if the rect is in the cache and we are now not finding a match, we can assume that the card is covered by an emote
        elif cached_template_name != "questionmark":
            return "uncertain" # If it was in the cache but didnt match (given that it wasn't a questionmark), that means it was played, and we can return. 
    
    roi = gray_frame[rect[1]:rect[3], rect[0]:rect[2]]

    
    best_match_score = -1
    best_match_name = None
    
    for template_name, template in templates.items():
        if template_name in matched_cards:  
            continue
        gray_template = template if len(template.shape) == 2 else cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        res = cv2.matchTemplate(roi, gray_template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)

        if max_val > best_match_score:
            best_match_score = max_val
            best_match_name = template_name

    # Update the cache with the new best match
    if best_match_score > threshold:
        cache[rect] = best_match_name

    return best_match_name if best_match_score > threshold else "uncertain"


def update_hand(prev_hand, card_played):
    #Move the played card to the end of the hand
    try:
        prev_hand.remove(card_played)
    except ValueError:
        prev_hand.remove("questionmark")
    prev_hand.append(card_played)
    return prev_hand

def init_hand():
    #Since we don't know the positions of any of the cards in the deck, we initialize the hand with question marks in all positions.
    hand = ["questionmark" for _ in range(8)]
    return hand

def print_hand(color, hand):
    color_print(color, f"{color} players hand: {hand}")
    print()


def show_hand(hand_name, hand, templates):
    # Collect images of the cards in the hand
    card_images = [templates[card_name] for card_name in hand if card_name in templates]

    if card_images:
        # Concatenate card images horizontally
        hand_image = concatenate_images_horizontally(card_images)

        if hand_image is not None:
            # Display the hand in a separate window for each hand
            cv2.imshow(f"{hand_name} Hand", hand_image)
        else:
            print(f"No images found for {hand_name} hand.")
    else:
        print(f"No card images to display for {hand_name} hand.")

def concatenate_images_horizontally(image_list, separator_width=10, separator_color=(0, 0, 0), standard_height=150):
    if not image_list:
        return None

    resized_images = []
    for image in image_list:
        # Calculate the new width of the image to maintain the aspect ratio
        scale_ratio = standard_height / image.shape[0]
        new_width = int(image.shape[1] * scale_ratio)

        # Resize the image to the standard height while maintaining the aspect ratio
        resized_image = cv2.resize(image, (new_width, standard_height))
        resized_images.append(resized_image)

    # Add a black separator between images
    separator = np.zeros((standard_height, separator_width, 3), dtype=np.uint8)
    separator[:] = separator_color  # Set separator color

    # Initialize the final concatenated image as the first resized image
    concatenated_image = resized_images[0]

    for image in resized_images[1:]:
        concatenated_image = np.concatenate((concatenated_image, separator, image), axis=1)

    return concatenated_image



def draw_rects_and_update_current_decks(current_deck, rects, frame, frame_count, templates, cache, matched_cards):
    for i, rect in enumerate(rects):
        current_deck[i] = find_best_match(frame, frame_count, rect, templates, cache, matched_cards)
        top_left = (rect[0], rect[1])
        bottom_right = (rect[2], rect[3])
        cv2.rectangle(frame, top_left, bottom_right, (0, 0, 255), 2)
    return current_deck


def post_process_decks(match_frequency, current_deck, true_deck, prev_deck, prev_cards, frame_count, color, hand):
    #If the new card is a question mark and the previous card wasn't then we know that that card was played 
    #However, we need to check if it was played before, as sometimes there is an issue where the matching function
    #will on one frame detect a question mark (ie the card was played) and then on the next frame detect that same card and then on the *next*
    #frame detect a different card. This is a problem because it will look like the card was played twice.
    for rect, card in current_deck.items():
        if true_deck[rect] != "questionmark":
            if prev_deck[rect] not in prev_cards.keys():
                if card == "uncertain" and prev_deck[rect] != "uncertain":
                    color_print(color, f"Player played: {prev_deck[rect]} at frame {frame_count}")
                    prev_cards[prev_deck[rect]] = frame_count
                    hand = update_hand(hand, prev_deck[rect])

            elif frame_count - prev_cards[prev_deck[rect]] > match_frequency*5:
                if card == "uncertain" and prev_deck[rect] != "uncertain":
                    color_print(color, f"Player played: {prev_deck[rect]} at frame {frame_count}")
                    prev_cards[prev_deck[rect]] = frame_count
                    hand = update_hand(hand, prev_deck[rect])

        elif card != "uncertain" and card != "questionmark" and true_deck[rect] == "questionmark":
                color_print(color, f"Player played: {card} at frame {frame_count}")
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

        current_red_deck = draw_rects_and_update_current_decks(current_red_deck, red_rects, frame, frame_count, templates, red_cache, matched_red_cards)
        current_blue_deck = draw_rects_and_update_current_decks(current_blue_deck, blue_rects, frame, frame_count, templates, blue_cache, matched_blue_cards)

        if frame_count == match_frequency:
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

        # Wait for key press for a short time (e.g., 1 millisecond)
        key = cv2.waitKey(1)

        # Process the key press
        frame_count = process_key_press(key, cap, frame_count)
        
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()