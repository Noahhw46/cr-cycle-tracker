import cv2
import numpy as np

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