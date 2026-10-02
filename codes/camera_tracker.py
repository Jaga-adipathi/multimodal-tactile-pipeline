import cv2
import mediapipe as mp
import socket

UDP_IP = "1xx.x.x.x"
UDP_PORT = 5xxx
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=1)
cap = cv2.VideoCapture(0)

print(f"[SYSTEM] Transmitting Spatial Camera Data to Port {UDP_PORT}...")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: continue

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)
    
    h, w, c = frame.shape

    if result.multi_hand_landmarks:
        wrist = result.multi_hand_landmarks[0].landmark[0]
        # Send X, Y, Z to Unity
        msg = f"{wrist.x:.4f},{wrist.y:.4f},{wrist.z:.4f}"
        sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))
        
        cv2.circle(frame, (int(wrist.x * w), int(wrist.y * h)), 10, (0, 255, 255), -1)

    cv2.imshow("Spatial Tracker", frame)
    if cv2.waitKey(1) == 27: break

cap.release()
cv2.destroyAllWindows()
