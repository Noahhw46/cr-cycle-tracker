import cv2


def getframes():
    video_path = input("Enter the video path: ")
    video = cv2.VideoCapture(video_path)

    video_name = video_path.split('/')[-1].split('.')[0]

    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break

        cv2.imwrite(f"frames/{video_name}/frame{int(video.get(cv2.CAP_PROP_POS_FRAMES))}.jpg", frame)
