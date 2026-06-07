import cv2

print("Scanning camera indexes 0 to 5...")
for i in range(6):
    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
    if cap.isOpened():
        print(f"  ✅ Camera found at index: {i}")
        cap.release()
    else:
        print(f"  ❌ No camera at index: {i}")
print("Done.")