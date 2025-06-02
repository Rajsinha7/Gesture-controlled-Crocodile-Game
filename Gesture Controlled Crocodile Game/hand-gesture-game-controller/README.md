🎮 Project Title:
Gesture-Controlled Crocodile Game (with Falling Obstacles)

✅ Project Summary:
This is a fun arcade-style game where a cartoon crocodile moves left and right at the bottom of the screen, avoiding falling obstacles (red boxes) from the top. The game is controlled using real-time hand gestures captured via webcam using OpenCV and MediaPipe and the Game engine via pygame.

🧠 Key Features:
Feature	Description
Gesture Control	Uses your index finger’s position to control movement (left/right).
Real-Time Camera Feed	Webcam input is processed live using MediaPipe Hands.
Animated Crocodile	Croc moves with a simple 3-frame tail animation.
Falling Obstacles	Red boxes fall from random horizontal positions at a fixed speed.
Collision Detection	If the croc touches a box, the game ends.
Scoring System	Score increases over time as you survive.
Pause & Restart	Press 'P' to pause, 'R' to restart after Game Over.


🧱 Tech Stack:
Component	Library/Tool	Purpose
Language	Python	Main programming language
Graphics/Game	Pygame	For rendering graphics and game loop
Camera Input	OpenCV (cv2)	Access webcam feed
Hand Tracking	MediaPipe Hands	Detect finger position in real-time
Threading	Python threading	Run camera detection in parallel to game


🕹️ Game Logic Overview:
1. Gesture Detection
Library Used: OpenCV + MediaPipe
Approach:
Capture frame from webcam.
Detect hand landmarks using mediapipe.solutions.hands.
Track index finger tip (landmark 8).
If it’s in the left ⅓ of screen → move croc left.
If it’s in right ⅓ → move right.
Use threading to run this detection independently of game loop.

2. Game Engine
Library Used: pygame

Handles:
Game window rendering
Frame-based animation
Sprite drawing (crocodile, obstacles)
Collision detection
Score tracking
Keyboard pause/restart

🛠️ Requirements :
pip install pygame opencv-python mediapipe


🚀 How to Run the Game:
Step 1: Clone or Copy Code
git clone <your_repo_url>
cd gesture_croc_game

Step 2: Install dependencies
pip install -r requirements.txt

Step 3: Run the Game
python main.py

