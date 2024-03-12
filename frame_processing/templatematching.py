import cv2
from utils.white_pixel_filter import has_problematic_colors


def find_best_match(frame, rect, templates, cache, matched_cards, threshold=0.7):
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