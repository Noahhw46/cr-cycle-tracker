import cv2
from utils.white_pixel_filter import has_problematic_colors
from handlogic import update_hand
from utils.printing import color_print

def find_best_match(frame, rect, templates, cache, matched_cards, threshold=0.7):
    """
    Finds the best match for a given region of interest (ROI) in a frame using template matching.

    Parameters:
    frame (np.array): The frame in which to find the match.
    rect (tuple): A tuple (x1, y1, x2, y2) defining the ROI.
    templates (dict): A dictionary of templates to match against. The keys are template names and the values are the templates themselves.
    cache (dict): A cache of previous matches. The keys are rectangles and the values are the names of the templates that matched.
    matched_cards (list): A list of cards that have already been matched for a given player.
    threshold (float, optional): The threshold for a match. Defaults to 0.7.

    Returns:
    str: The name of the best matching template if a match is found, "uncertain" otherwise.
    """
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
        if template_name in matched_cards:  #We don't need to check templates that have already been matched for a given player
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



def post_process_decks(match_frequency, current_deck, true_deck, prev_deck, prev_cards, frame_count, color, hand):
    """
    This is the main logic for processing the cards played by the players. It is called every match_frequency frames and recieves all the information that
    the main matching function gives.
    The basic problem that it solves is that when a card is played, there are a few frames where there is high variation in how the card is detected.
    Ie frame 1 it might not find a match then frame 2 it will, etc. But all we are interested in is the first frame where we don't find a match.

    The basic logic is as follows:
    1. If the new card is a question mark (ie the match finding function was uncertain) and the previous card wasn't then we know that that card was played
    2. If the new card is not a questionmark and the previous card was then we know that that was a new card that was played.

    It returns the updated previous deck, previous cards and hand.
    """

    for rect, card in current_deck.items():
        if true_deck[rect] != "questionmark":
            if prev_deck[rect] not in prev_cards.keys():
                if card == "uncertain" and prev_deck[rect] != "uncertain":
                    color_print(color, f"{color} Player played: {prev_deck[rect]} at frame {frame_count}")
                    prev_cards[prev_deck[rect]] = frame_count
                    hand = update_hand(hand, prev_deck[rect])

            elif frame_count - prev_cards[prev_deck[rect]] > match_frequency*5:
                if card == "uncertain" and prev_deck[rect] != "uncertain":
                    color_print(color, f"{color} Player played: {prev_deck[rect]} at frame {frame_count}")
                    prev_cards[prev_deck[rect]] = frame_count
                    hand = update_hand(hand, prev_deck[rect])

        elif card != "uncertain" and card != "questionmark" and true_deck[rect] == "questionmark":
                color_print(color, f"{color} Player played: {card} at frame {frame_count}")
                prev_cards[card] = frame_count
                true_deck[rect] = card
                hand = update_hand(hand, card)


    return prev_deck, prev_cards, hand