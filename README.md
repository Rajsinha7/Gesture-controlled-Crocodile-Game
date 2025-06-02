# Gesture-controlled-Crocodile-Game
--> Feature	Description :::
Gesture Control	Uses your index finger’s position to control movement (left/right).
Real-Time Camera Feed	Webcam input is processed live using MediaPipe Hands.
Animated Crocodile	Croc moves with a simple 3-frame tail animation.
Falling Obstacles	Red boxes fall from random horizontal positions at a fixed speed.
Collision Detection	If the croc touches a box, the game ends.
Scoring System	Score increases over time as you survive.
Pause & Restart	Press 'P' to pause, 'R' to restart after Game Over.


🧱 Tech Stack:::
Component:	Library/Tool	Purpose
Language:	Python	Main programming language
Graphics/Game:	Pygame	For rendering graphics and game loop
Camera Input:	OpenCV (cv2)	Access webcam feed
Hand Tracking:	MediaPipe Hands	Detect finger position in real-time
Threading	Python threading	Run camera detection in parallel to game
