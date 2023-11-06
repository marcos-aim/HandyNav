import cv2
import mediapipe as mp
import os
import pyautogui
import time
import webbrowser  

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    min_detection_confidence=0.5, min_tracking_confidence=0.5)


# Function to count fingers based on landmarks.
def count_fingers(image, hand_landmarks, hand_no=0):
    # Assuming the hand is right, these landmarks correspond to fingertips.
    tip_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # 4 Fingers
    for id in range(1, 5):
        if hand_landmarks.landmark[tip_ids[id]].y < hand_landmarks.landmark[tip_ids[id] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)


cap = cv2.VideoCapture(0)
twoFingers = False
g1 = 0.5
oneFingerStartX = 0.5
oneFingerStartY = 0.5
while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Flip the image horizontally for a later selfie-view display.
    # Convert the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Process the image and detect hands.
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Count fingers and display the count.
            finger_count = count_fingers(image, hand_landmarks)
            cv2.putText(image, f'Fingers: {finger_count}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
            #Jedi gestures
            twoFingers = (finger_count == 2) 
            if not twoFingers:
                g1 = hand_landmarks.landmark[12].x
                
            if twoFingers and hand_landmarks.landmark[12].x - g1 > .1:
                webbrowser.open('https://www.chess.com/home')
                time.sleep(5)
            #if twoFingers and g1 - hand_landmarks.landmark[12].x > .1:
                #pyautogui.hotkey('command', 'n', interval=0.25)                   
            
    # Display the resulting image.
    #cv2.imshow('MediaPipe Hands', image)

    # Break the loop when 'q' is pressed.
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
        


# Release the webcam and destroy all OpenCV windows.
cap.release()
cv2.destroyAllWindows()
