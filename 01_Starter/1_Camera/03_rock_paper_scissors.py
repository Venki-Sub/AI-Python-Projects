"""
03 - Rock, paper, scissors against the computer
-----------------------------------------------
Uses the finger counter from project 02:
    0 fingers = ROCK      2 fingers = SCISSORS      5 fingers = PAPER

Show your hand and press SPACE: the computer picks at random and the winner is shown.

Run:  python 03_rock_paper_scissors.py      (SPACE = play, 'q' = quit)
"""

import random
import cv2
import mediapipe as mp

hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
draw = mp.solutions.drawing_utils

CHOICES = {0: "ROCK", 2: "SCISSORS", 5: "PAPER"}  # number of fingers -> move
# Who beats who: (winner, loser)
WINS = {("ROCK", "SCISSORS"), ("SCISSORS", "PAPER"), ("PAPER", "ROCK")}


def count_fingers(points):
    """Same function as in 02_finger_counter.py."""
    count = sum(1 for tip in [8, 12, 16, 20] if points[tip].y < points[tip - 2].y)
    if abs(points[4].x - points[17].x) > abs(points[3].x - points[17].x):
        count += 1
    return count


score_player, score_computer = 0, 0
message = "Show your hand and press SPACE"

cap = cv2.VideoCapture(0)
while True:
    ok, frame = cap.read()
    if not ok:
        break
    frame = cv2.flip(frame, 1)
    result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    player = None  # the move the player is showing right now (None = not a valid move)
    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        draw.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
        player = CHOICES.get(count_fingers(hand.landmark))  # .get() gives None if not 0, 2 or 5

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    if key == ord(" "):                              # SPACE pressed -> play one round
        if player is None:
            message = "Move not recognised: show 0, 2 or 5 fingers"
        else:
            computer = random.choice(list(CHOICES.values()))  # the computer picks at random
            if player == computer:
                result_text = "DRAW"
            elif (player, computer) in WINS:
                result_text = "YOU WIN!"
                score_player += 1
            else:
                result_text = "YOU LOSE"
                score_computer += 1
            message = f"You: {player}  Computer: {computer}  -> {result_text}"

    # Display (OpenCV text cannot show accents, so we keep it in plain English)
    cv2.putText(frame, f"Your move: {player or '?'}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.putText(frame, message, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(frame, f"Score  you {score_player} - {score_computer} computer", (10, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.imshow("Rock Paper Scissors", frame)

cap.release()
cv2.destroyAllWindows()
