# 🐍 Hand Tracking Snake Game

An interactive computer vision application that reimagines the classic Snake game using real-time hand gesture tracking via your webcam. Control the snake head using your index fingertip!

Built with **Python**, **OpenCV**, **cvzone**, and **MediaPipe**.

---

## 🌟 Key Features

* **Gesture Control:** Track your index fingertip (landmark 8) to steer the snake across the camera frame in real time.
* **Dynamic Length Scaling:** Every target item eaten increases your score and extends the snake's body length.
* **Self-Collision Detection:** Uses OpenCV's `pointPolygonTest` to detect when the snake collides with its own body.
* **Asset Alpha Handling:** Automatically injects transparency (alpha channels) and resizes food overlays dynamically.
* **Fallback Asset Generator:** Automatically generates a default target graphic if external images are missing, keeping the game functional.

---

## 🛠️ Installation & Setup

### 1. Prerequisites
Make sure you have Python 3.8 or higher installed on your system.

### 2. Install Required Dependencies
Open your terminal or Command Prompt and run:

```bash
pip install opencv-python cvzone numpy mediapipe
