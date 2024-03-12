import cv2
import os
import json

mydict = json.loads(open('card_locs.json').read())


def extract_card_locs(frame_path):
    image = cv2.imread(frame_path)

    #save folder = templates/extracted_cards and then /<the text in frame_path after frames/ and before the next />
    save_folder = f"templates/extracted_cards/{frame_path.split('frames/')[1].split('/')[0]}"
    os.makedirs(save_folder, exist_ok=True) 

    red_bar = (8,141,1171,471)
    blue_bar = (8,2205,1171,2504)

    #show the red bar
    red_bar_image = image[red_bar[1]:red_bar[3], red_bar[0]:red_bar[2]]
    blue_bar_image = image[blue_bar[1]:blue_bar[3], blue_bar[0]:blue_bar[2]]


    count = 0

    #Now "screenshot" each innerrectangle and save it to a file in /screenshots"
    for location in mydict["rect1"]:
        count += 1
        x = location[0][0]
        y = location[0][1]
        w = location[1][0] - location[0][0]
        h = location[1][1] - location[0][1]
        cv2.imwrite(f"{save_folder}/rect1_{count}.png", red_bar_image[y:y+h, x:x+w])

    count = 0
    for location in mydict["rect2"]:
        count += 1
        x = location[0][0]
        y = location[0][1]
        w = location[1][0] - location[0][0]
        h = location[1][1] - location[0][1]
        cv2.imwrite(f"{save_folder}/rect2_{count}.png", blue_bar_image[y:y+h, x:x+w])




    
extract_card_locs("frames/piggy2/frame2724.jpg")