
import cv2


def click_event(event, x, y, flags, param):
    click_coords = []
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Clicked at: (x={x}, y={y})")
        click_coords.append((x, y))
        if len(click_coords) == 2:
            get_area(click_coords)
            count_pixels(click_coords)

def get_area(coords):
    x1, y1 = coords[0]
    x2, y2 = coords[1]
    area = abs((x2 - x1) * (y2 - y1))
    print(f"Area: {area} square pixels")

def count_pixels(coords, image):
    x1, y1 = coords[0]
    x2, y2 = coords[1]
    roi = image[y1:y2, x1:x2]
    white_pixels = cv2.countNonZero(cv2.inRange(roi, (255, 255, 255), (255, 255, 255)))
    print(f"Number of white pixels: {white_pixels}")

def display_image_and_detect_clicks(image_path):
    image = cv2.imread(image_path)

    if image is None:
        print("Error: Image not loaded. Check the file path.")
        return

    cv2.namedWindow('Image')

    cv2.setMouseCallback('Image', click_event)

    cv2.imshow('Image', image)

    cv2.waitKey(0)

    cv2.destroyAllWindows()


def main():
    """
    Helper script to test things like the number of white pixels in a roi, the bounds of some roi, etc.
    """
    image_path = input("Enter the image path: ")
    display_image_and_detect_clicks(image_path)
