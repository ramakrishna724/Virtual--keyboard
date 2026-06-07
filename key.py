import sys
import cv2
import math
import mediapipe as mp
from pynput.keyboard import Controller, Key

# ── Camera: try all backends ──────────────────────────────────────────────────
cap = None
for backend in [cv2.CAP_MSMF, cv2.CAP_DSHOW, 0]:
    try:
        c = cv2.VideoCapture(0, backend) if isinstance(backend, int) and backend != 0 else cv2.VideoCapture(0)
        if c.isOpened():
            ret, test = c.read()
            if ret and test is not None:
                cap = c
                break
            c.release()
    except:
        continue

if cap is None:
    print("Error: Camera not found or not readable.")
    sys.exit(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Warm up camera
for _ in range(5):
    cap.read()

# ── MediaPipe ─────────────────────────────────────────────────────────────────
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.7,
    max_num_hands=1
)
mp_draw = mp.solutions.drawing_utils

keyboard = Controller()

# ── Keyboard Layout ───────────────────────────────────────────────────────────
ROWS = [
    ["Q","W","E","R","T","Y","U","I","O","P"],
    ["A","S","D","F","G","H","J","K","L",";"],
    ["Z","X","C","V","B","N","M",",",".","/"],
]
SPECIAL = [("SPACE", 220), ("BKSP", 110), ("ENTER", 110)]

PINCH_THRESHOLD = 40
COOLDOWN_FRAMES = 18

# ── Button ────────────────────────────────────────────────────────────────────
class Button:
    def __init__(self, pos, text, size=(52, 52)):
        self.pos = pos
        self.text = text
        self.size = size

def build_buttons():
    btns = []
    ox, oy, gap = 20, 370, 6
    for r, row in enumerate(ROWS):
        for c, k in enumerate(row):
            btns.append(Button((ox + c*(52+gap), oy + r*(52+gap)), k))
    sx = ox
    for k, w in SPECIAL:
        btns.append(Button((sx, oy + 3*(52+gap)), k, (w, 52)))
        sx += w + gap
    return btns

buttons = build_buttons()

# ── Draw ──────────────────────────────────────────────────────────────────────
def draw_keys(img, hover):
    for btn in buttons:
        x, y = btn.pos
        w, h = btn.size
        active = btn.text == hover
        cv2.rectangle(img, (x,y), (x+w,y+h), (210,210,210) if active else (40,40,40), -1)
        cv2.rectangle(img, (x,y), (x+w,y+h), (150,150,150), 1)
        fs = 0.45 if len(btn.text) > 2 else 0.65
        tc = (0,0,0) if active else (255,255,255)
        tw, th = cv2.getTextSize(btn.text, cv2.FONT_HERSHEY_SIMPLEX, fs, 2)[0]
        cv2.putText(img, btn.text, (x+(w-tw)//2, y+(h+th)//2),
                    cv2.FONT_HERSHEY_SIMPLEX, fs, tc, 2)

def press_key(text):
    if   text == "SPACE": keyboard.press(Key.space);     keyboard.release(Key.space)
    elif text == "BKSP":  keyboard.press(Key.backspace); keyboard.release(Key.backspace)
    elif text == "ENTER": keyboard.press(Key.enter);     keyboard.release(Key.enter)
    else:                 keyboard.press(text.lower());  keyboard.release(text.lower())

# ── Main ──────────────────────────────────────────────────────────────────────
last_key = "-"
cooldown = 0

print("Virtual Keyboard running... Press Q or ESC to quit.")

try:
    while True:
        ok, img = cap.read()
        if not ok or img is None:
            print("Frame grab failed.")
            break

        img = cv2.flip(img, 1)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        res = hands.process(rgb)

        hover = None
        dist  = 999

        if res.multi_hand_landmarks:
            for hand in res.multi_hand_landmarks:
                mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)
                lm = hand.landmark
                h, w = img.shape[:2]
                ix, iy = int(lm[8].x*w), int(lm[8].y*h)
                tx, ty = int(lm[4].x*w), int(lm[4].y*h)
                dist = math.hypot(ix-tx, iy-ty)
                cv2.circle(img, (ix,iy), 10, (0,255,150), -1)

                for btn in buttons:
                    bx, by = btn.pos
                    bw, bh = btn.size
                    if bx < ix < bx+bw and by < iy < by+bh:
                        hover = btn.text
                        if dist < PINCH_THRESHOLD and cooldown == 0:
                            press_key(btn.text)
                            last_key = btn.text
                            cooldown = COOLDOWN_FRAMES
                            cv2.rectangle(img,(bx-3,by-3),(bx+bw+3,by+bh+3),(0,255,100),3)

        if cooldown > 0:
            cooldown -= 1

        draw_keys(img, hover)

        cv2.rectangle(img, (0,0), (520,32), (20,20,20), -1)
        cv2.putText(img, f"Last: {last_key}  Pinch: {dist:.0f}px  |  Q / ESC to quit",
                    (8,22), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180,180,180), 1)

        cv2.imshow("Virtual Keyboard", img)
        k = cv2.waitKey(10) & 0xFF
        if k == 27 or k == ord('q'):
            break
        if cv2.getWindowProperty("Virtual Keyboard", cv2.WND_PROP_VISIBLE) < 1:
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("Done.")