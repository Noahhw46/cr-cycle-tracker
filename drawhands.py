import cv2
from utils.drawingutils import concatenate_images_horizontally
from frame_processing.templatematching import find_best_match


def draw_rects_and_update_current_decks(current_deck, rects, frame, templates, cache, matched_cards):
    for i, rect in enumerate(rects):
        current_deck[i] = find_best_match(frame, rect, templates, cache, matched_cards)
        top_left = (rect[0], rect[1])
        bottom_right = (rect[2], rect[3])
        cv2.rectangle(frame, top_left, bottom_right, (0, 0, 255), 2)
    return current_deck

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