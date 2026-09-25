import cv2

img = cv2.imread("Donut.png", cv2.IMREAD_UNCHANGED)
print(img.shape if img is not None else "❌ Not loaded")
cv2.imshow("Donut", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
