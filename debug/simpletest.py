import cv2
import os

def match_and_draw(frame_path, template_path, rect, color, rect_id):
    template = cv2.imread(template_path)
    cv2.imshow("template", template)
    frame = cv2.imread(frame_path)

    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    template_height, template_width = template_gray.shape[:2]

    roi = frame_gray[rect[1]:rect[3], rect[0]:rect[2]]

    res = cv2.matchTemplate(roi, template_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    print(f"Match strength for {template_path[:-4]} in rectangle {rect_id}: {max_val:.4f}")

    center = (max_loc[0] + template_width // 2 + rect[0], max_loc[1] + template_height // 2 + rect[1])

    cv2.circle(frame, center, radius=20, color=color, thickness=-1)

    # Display the result
    cv2.imshow(f"{template_path[:-4]}", frame)
    
    #wait for key press 'q' to exit
    key = cv2.waitKey(0)
    if key == ord('q'):
        cv2.destroyAllWindows()




def main():
    """
    Helper script to test the basic functionality of the match_and_draw function for a single frame.
    """
    frame_path = input("Enter the frame path: ")

    battle_bar_red = (8,141,1171,471)
    battle_bar_blue = (8,2205,1171,2504)

    for template in os.listdir('templates/extracted_cards/combined'):
        if template.endswith('.png'):
            template_path = f"templates/extracted_cards/combined/{template}"
            print(template_path)
            match_and_draw(frame_path, template_path, battle_bar_red, (0, 0, 255), "red")
            match_and_draw(frame_path, template_path, battle_bar_blue, (255, 0, 0), "blue")
