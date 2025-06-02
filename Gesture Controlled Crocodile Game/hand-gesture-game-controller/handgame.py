"""
import cv2
import mediapipe as mp
import pyautogui
import time

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

class IndexFingerSwipeTracker:
    def __init__(self):
        self.hands = mp_hands.Hands(min_detection_confidence=0.7, max_num_hands=1)
        self.last_pos = None  # (x, y)
        self.swipe_threshold_x = 0.05  # horizontal swipe sensitivity
        self.swipe_threshold_y = 0.05  # vertical swipe sensitivity
        self.cooldown = 0.5  # seconds between triggers
        self.last_trigger = time.time()

    def detect_gesture(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        gesture = None
        hand_landmarks = None

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            index_tip = hand_landmarks.landmark[8]
            current_pos = (index_tip.x, index_tip.y)

            if self.last_pos:
                dx = current_pos[0] - self.last_pos[0]
                dy = current_pos[1] - self.last_pos[1]

                # Invert horizontal swipe direction here
                if abs(dx) > self.swipe_threshold_x and abs(dx) > abs(dy):
                    gesture = "left" if dx > 0 else "right"  # inverted

                elif abs(dy) > self.swipe_threshold_y and abs(dy) > abs(dx):
                    gesture = "down" if dy > 0 else "up"

            self.last_pos = current_pos

        else:
            self.last_pos = None  # reset if no hand detected

        return gesture, hand_landmarks

def trigger_key(gesture, tracker):
    now = time.time()
    if gesture and (now - tracker.last_trigger > tracker.cooldown):
        if gesture == "left":
            pyautogui.press("left")
        elif gesture == "right":
            pyautogui.press("right")
        elif gesture == "up":
            pyautogui.press("up")
        elif gesture == "down":
            pyautogui.press("down")
        tracker.last_trigger = now

def main():
    cap = cv2.VideoCapture(0)
    tracker = IndexFingerSwipeTracker()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gesture, landmarks = tracker.detect_gesture(frame)

        if landmarks:
            mp_drawing.draw_landmarks(
                frame, landmarks, mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=4),
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2)
            )

        if gesture:
            cv2.putText(frame, gesture.upper(), (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            trigger_key(gesture, tracker)

        cv2.imshow("Index Finger Swipe Controls (Opposite Left/Right)", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
"""

import pygame
import sys
import cv2
import mediapipe as mp
import threading
import time
import random

# --- Gesture detection globals ---
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
latest_gesture = None
lock = threading.Lock()

# --- Gesture detection thread ---
def gesture_control_loop():
    global latest_gesture
    cap = cv2.VideoCapture(0)
    hands = mp_hands.Hands(min_detection_confidence=0.7, max_num_hands=1)

    cv2.namedWindow("Gesture Control", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Gesture Control", 640, 480)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        height, width, _ = frame.shape
        gesture = None

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            index_tip = hand_landmarks.landmark[8]
            index_x = int(index_tip.x * width)
            index_y = int(index_tip.y * height)

            # Draw landmarks
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=4),
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2)
            )

            # Determine gesture based on position
            if index_x < width // 3:
                gesture = "left"
            elif index_x > 2 * width // 3:
                gesture = "right"
            # Up/down gestures can be ignored or used if you want
            # elif index_y < height // 3:
            #     gesture = "up"
            # elif index_y > 2 * height // 3:
            #     gesture = "down"

            # Draw guidance lines
            cv2.line(frame, (width // 3, 0), (width // 3, height), (255, 255, 0), 2)
            cv2.line(frame, (2 * width // 3, 0), (2 * width // 3, height), (255, 255, 0), 2)

            cv2.putText(frame, f"Finger Pos: ({index_x},{index_y})", (10, height - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        if gesture:
            with lock:
                latest_gesture = gesture
            cv2.putText(frame, f"Gesture: {gesture.upper()}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Gesture Control", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
            break

    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()
    sys.exit()

# --- Game constants ---
WIDTH, HEIGHT = 800, 600
GROUND_Y = 540  # croc on bottom with height 60

# --- Crocodile sprite placeholders ---
def create_croc_frame(color, tail_offset):
    surf = pygame.Surface((60, 40), pygame.SRCALPHA)
    # Body
    pygame.draw.ellipse(surf, color, (10, 10, 40, 20))
    # Head
    pygame.draw.circle(surf, color, (55, 20), 12)
    # Tail (triangle)
    pygame.draw.polygon(surf, color, [(0, 20), (tail_offset, 10), (tail_offset, 30)])
    # Eye
    pygame.draw.circle(surf, (0, 0, 0), (50, 15), 3)
    return surf

# Create running animation frames (tail moves a bit)
RUN_FRAMES = [
    create_croc_frame((0, 150, 0), 5),
    create_croc_frame((0, 180, 0), 0),
    create_croc_frame((0, 150, 0), 5),
]

# Crash frame (red croc)
CRASH_FRAME = create_croc_frame((150, 0, 0), 0)

# --- Obstacle class for vertical falling boxes ---
class Obstacle:
    def __init__(self):
        self.width = 30
        self.height = 30
        self.x = random.randint(0, WIDTH - self.width)
        self.y = 0  # start at top
        self.color = (255, 0, 0)
        self.speed = 7

    def move(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# --- Game loop ---
def game_loop():
    global latest_gesture
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Gesture Controlled Crocodile Eats Boxes")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    big_font = pygame.font.SysFont(None, 72)

    char_x = WIDTH // 2
    char_y = GROUND_Y
    animation_index = 0
    animation_timer = 0

    obstacles = []
    obstacle_spawn_timer = 0
    obstacle_spawn_interval = 1500  # milliseconds

    score = 0
    game_over = False
    paused = False

    def reset_game():
        nonlocal char_x, char_y, animation_index, animation_timer
        nonlocal obstacles, obstacle_spawn_timer, score, game_over, paused
        char_x = WIDTH // 2
        char_y = GROUND_Y
        animation_index = 0
        animation_timer = 0
        obstacles = []
        obstacle_spawn_timer = 0
        score = 0
        game_over = False
        paused = False

    while True:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_r and game_over:
                    reset_game()

        if paused:
            screen.fill((50, 50, 50))
            pause_text = big_font.render("PAUSED", True, (255, 255, 255))
            screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2 - pause_text.get_height()//2))
            pygame.display.flip()
            continue

        if game_over:
            screen.fill((0, 0, 0))
            over_text = big_font.render("GAME OVER", True, (255, 0, 0))
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            restart_text = font.render("Press R to Restart", True, (255, 255, 255))
            screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 100))
            screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
            screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))
            pygame.display.flip()
            continue

        screen.fill((135, 206, 235))  # sky blue background

        # Get latest gesture input
        with lock:
            gesture = latest_gesture
            latest_gesture = None

        # Move croc left/right with gesture
        if gesture == "left":
            char_x = max(0, char_x - 15)
        elif gesture == "right":
            char_x = min(WIDTH - 60, char_x + 15)

        # Animate croc tail
        animation_timer += dt
        if animation_timer > 100:
            animation_index = (animation_index + 1) % len(RUN_FRAMES)
            animation_timer = 0

        char_img = RUN_FRAMES[animation_index]
        screen.blit(char_img, (char_x, char_y))

        # Spawn obstacles falling down
        obstacle_spawn_timer += dt
        if obstacle_spawn_timer > obstacle_spawn_interval:
            obstacles.append(Obstacle())
            obstacle_spawn_timer = 0

        char_rect = pygame.Rect(char_x, char_y, 60, 40)

        # Move, draw obstacles and check collision
        for obstacle in obstacles[:]:
            obstacle.move()
            obstacle.draw(screen)
            if obstacle.get_rect().colliderect(char_rect):
                game_over = True
            if obstacle.y > HEIGHT:
                obstacles.remove(obstacle)

        # Update and draw score
        if not game_over:
            score += 1  # simple increment per frame; can adjust
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

if __name__ == "__main__":
    gesture_thread = threading.Thread(target=gesture_control_loop, daemon=True)
    gesture_thread.start()

    game_loop()

     