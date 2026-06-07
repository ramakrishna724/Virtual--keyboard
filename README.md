# Virtual Keyboard — Gesture Controlled Typing

Type on any application using hand gestures detected through your webcam. No physical keyboard required.

---

## How It Works

Your webcam captures live frames. MediaPipe tracks 21 points on your hand in real time. The index fingertip acts as a cursor over the on-screen keyboard. Pinching your index finger and thumb together triggers a keypress. pynput sends the actual keystroke to your operating system — works in Notepad, browser, Word, or any app.

```
Webcam → MediaPipe Hand Tracking → Index Finger Position
→ Hover over Key → Pinch to Press → pynput types on your PC
```

---

## Gesture Guide

| Gesture | Action |
|---|---|
| Move index finger | Navigate keys |
| Pinch index + thumb | Press the key |
| `Q` or `ESC` | Quit |

---

## Requirements

- Python 3.11
- Windows 10 or 11
- Webcam

---

## Installation

```bash
git clone https://github.com/your-username/virtual-keyboard.git
cd virtual-keyboard
pip install opencv-python mediapipe==0.10.14 pynput
```

---

## Usage

```bash
python key.py
```

Point your index finger at a key to hover. Pinch your thumb and index finger together to type. The status bar at the top shows the last key pressed and current pinch distance.

---

## Project Structure

```
virtual-keyboard/
├── key.py            # Main application
├── requirements.txt  # Dependencies
├── .gitignore        # Git ignored files
└── README.md         # Documentation
```

---

## Troubleshooting

| Error | Fix |
|---|---|
| `No module named 'cv2'` | `pip install opencv-python` |
| `no attribute 'solutions'` | `pip install mediapipe==0.10.14` |
| Camera not opening | Change index in line 9: `VideoCapture(1)` |
| Window closes instantly | Run from terminal, check camera permissions |

---

## Stack

`Python 3.11` · `OpenCV 4.9` · `MediaPipe 0.10.14` · `pynput 1.8` · `Windows`

---

## License

MIT © 2025 Ramkrishna
