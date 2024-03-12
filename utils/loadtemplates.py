import cv2
import os

def load_templates():
    templates = {}
    for file in os.listdir('templates/extracted_cards/combined'):
        if file.endswith('.png'):
            # Load the template image
            template = cv2.imread(f"templates/extracted_cards/combined/{file}")

            # Assuming template is not None and has enough width to be cropped
            if template is not None and template.shape[1] > 20:  # Ensure image width is greater than 20 pixels
                # Crop 10 pixels from each side in the x direction
                cropped_template = template[:, 14:-14]
                # Crop 10 pixels from the top and bottom in the y direction
                cropped_template = cropped_template[12:-12, :]
                #display the cropped template
                #cv2.imshow("cropped template", cropped_template)
                #cv2.waitKey(0)
                # Store the cropped template in the dictionary using the file name before .png as the key
                templates[file[:-4]] = cropped_template
            else:
                print(f"Skipping {file} due to size constraints or loading issues.")

    return templates

#templates = load_templates()