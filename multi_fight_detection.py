import cv2
import numpy as np
import winsound
import os

print("Current Working Folder:", os.getcwd())


cctv_videos = {
    "classroom_2.mp4.mp4": "Classroom 2nd",
    "classroom_5.mp4.mp4": "Classroom 5th",
    "ground.mp4.mp4": "College Ground"
}

caps = {}
prev_frames = {}
fight_count = {}
alert_on = {}


for video, location in cctv_videos.items():

    if not os.path.exists(video):
        print("❌ File Not Found:", video)
        continue

    cap = cv2.VideoCapture(video)

    if not cap.isOpened():
        print("❌ Cannot Open:", video)
        continue

    print("✅ Monitoring:", location)

    caps[video] = cap
    prev_frames[video] = None
    fight_count[video] = 0
    alert_on[video] = False

print("System Started... Press ESC to exit")


while True:

    for video, cap in caps.items():

        ret, frame = cap.read()

        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        location = cctv_videos[video]

        frame = cv2.resize(frame, (480, 360))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if prev_frames[video] is None:
            prev_frames[video] = gray
            continue

        diff = cv2.absdiff(prev_frames[video], gray)
        thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
        motion = np.sum(thresh)

       
        if motion > 120000:
            fight_count[video] += 1
        else:
            fight_count[video] = 0
            alert_on[video] = False

        if fight_count[video] > 5 and not alert_on[video]:
            alert_on[video] = True
            print("🚨 FIGHT DETECTED at", location)
            winsound.Beep(1500, 700)

        if alert_on[video]:
            cv2.putText(
                frame,
                f"ALERT: Fight at {location}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

        cv2.imshow(location, frame)

        prev_frames[video] = gray

    if cv2.waitKey(20) & 0xFF == 27:
        break


for cap in caps.values():
    cap.release()

cv2.destroyAllWindows()
print("System Closed")
