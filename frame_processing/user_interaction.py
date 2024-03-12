import cv2
def process_key_press(key, cap, frame_count):
    if key == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        exit()
    if key == ord('s'):
        for i in range(20):
            ret, frame = cap.read()
            frame_count += 1
            if not ret:
                break
    if key == ord('p'):
        print("Paused")
        while True:
            key = cv2.waitKey(0)
            if key == ord('p'):
                print("Unpaused")
                break
    if key == ord('r'):
        rewind_frames = 20 
        new_frame_count = max(frame_count - rewind_frames, 0) 
        cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame_count) 
        frame_count = new_frame_count 
        print(f"Rewound to frame {frame_count}")
    return frame_count