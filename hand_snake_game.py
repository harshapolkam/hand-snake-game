import math
import random
import cvzone
import cv2
import numpy as np
import os
from cvzone.HandTrackingModule import HandDetector

# --- Setup ---
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

if not cap.isOpened():
    print("❌ Could not open webcam.")
    exit()

detector = HandDetector(detectionCon=0.7, maxHands=1)


class SnakeGame:
    def __init__(self, pathFood):
        self.points = []  # all points of the snake
        self.lengths = []  # distance between points
        self.currentLength = 0
        self.allowedLength = 150
        self.previousHead = 0, 0
        self.score = 0
        self.gameOver = False

        # --- Load donut safely ---
        self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        if self.imgFood is None:
            print(f"⚠️ '{pathFood}' not found — using default circle.")
            self.imgFood = np.zeros((80, 80, 4), np.uint8)
            cv2.circle(self.imgFood, (40, 40), 35, (0, 255, 0, 255), -1)
        else:
            # ✅ Add alpha channel if missing
            if self.imgFood.shape[2] == 3:
                self.imgFood = cv2.cvtColor(self.imgFood, cv2.COLOR_BGR2BGRA)
                print("✅ Added alpha channel to Donut.png automatically!")

        # ✅ Resize donut to fit game (150×150)
        self.imgFood = cv2.resize(self.imgFood, (150, 150), interpolation=cv2.INTER_AREA)
        self.hFood, self.wFood, _ = self.imgFood.shape

        # ✅ Generate first random food location
        self.randomFoodLocation()


    def randomFoodLocation(self):
        self.foodPoint = random.randint(100, 1100), random.randint(100, 600)

    def update(self, imgMain, currentHead):
        if self.gameOver:
            cvzone.putTextRect(imgMain, "GAME OVER", [380, 350],
                               scale=6, thickness=6, colorR=(0, 0, 255), offset=20)
            cvzone.putTextRect(imgMain, f"Score: {self.score}", [500, 500],
                               scale=3, thickness=3, colorR=(255, 255, 0), offset=10)
            return imgMain

        px, py = self.previousHead
        cx, cy = currentHead
        distance = math.hypot(cx - px, cy - py)

        # prevent sudden jumps when hand moves too fast
        if distance > 5:
            self.points.append([cx, cy])
            self.lengths.append(distance)
            self.currentLength += distance
            self.previousHead = cx, cy

        # limit snake length
        while self.currentLength > self.allowedLength and len(self.lengths) > 0:
            self.currentLength -= self.lengths[0]
            self.lengths.pop(0)
            self.points.pop(0)

        # check food eating
        rx, ry = self.foodPoint
        if rx - self.wFood//2 < cx < rx + self.wFood//2 and ry - self.hFood//2 < cy < ry + self.hFood//2:
            self.randomFoodLocation()
            self.allowedLength += 50
            self.score += 1
            print(f"🍩 Score: {self.score}")

        # draw snake
        for i in range(1, len(self.points)):
            cv2.line(imgMain, self.points[i - 1], self.points[i], (0, 0, 255), 20)
        if self.points:
            cv2.circle(imgMain, self.points[-1], 20, (0, 255, 0), cv2.FILLED)

        # draw food safely
        try:
            imgMain = cvzone.overlayPNG(imgMain, self.imgFood, (rx - self.wFood // 2, ry - self.hFood // 2))
        except Exception as e:
            print("⚠️ Overlay failed:", e)

        # draw score
        cvzone.putTextRect(imgMain, f'Score: {self.score}', [50, 80], scale=3, thickness=3, offset=10)

        # collision check (only when snake long enough)
        if len(self.points) > 10:
            pts = np.array(self.points[:-2], np.int32)
            pts = pts.reshape((-1, 1, 2))
            minDist = cv2.pointPolygonTest(pts, (cx, cy), True)
            if minDist is not None and -1 <= minDist <= 1:
                print("💥 Collision Detected — Game Over!")
                self.gameOver = True

        return imgMain


# --- Game Setup ---
game = SnakeGame("Donut.png")
print("🎮 Hand Snake Game Started — Press 'r' to restart, ESC to quit")

# --- Main Loop ---
while True:
    success, img = cap.read()
    if not success:
        print("⚠️ Frame not captured — retrying...")
        continue

    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']
        pointIndex = lmList[8][0:2]
        img = game.update(img, pointIndex)
    else:
        cvzone.putTextRect(img, "Show your hand to start!", [450, 360], scale=2, thickness=2, offset=10)

    cv2.imshow("🖐️ Hand Snake Game", img)
    key = cv2.waitKey(1)
    if key == ord('r'):
        game = SnakeGame("Donut.png")
        print("🔄 Restarted Game!")
    elif key == 27:  # ESC
        print("👋 Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
