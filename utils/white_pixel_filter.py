import numpy as np
def has_problematic_colors(roi, pixel_threshold=250):
    """
    This is my extremely hacky way of detecting if an emote is present in a card. Obviously
    this doesn't work all the time, but surprisingly it works well enough to be useful except in a few tricky cases.
    """
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