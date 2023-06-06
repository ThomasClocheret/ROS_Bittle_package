import cv2
import mediapipe as mp
import pandas as pd  
import os
import numpy as np 
import rospy
from std_msgs.msg import String
import pickle

def image_processed(hand_img):

    # Image processing
    # 1. Convert BGR to RGB
    img_rgb = cv2.cvtColor(hand_img, cv2.COLOR_BGR2RGB)

    # 2. Flip the img in Y-axis
    img_flip = cv2.flip(img_rgb, 1)

    # accessing MediaPipe solutions
    mp_hands = mp.solutions.hands

    # Initialize Hands
    hands = mp_hands.Hands(static_image_mode=True,
    max_num_hands=1, min_detection_confidence=0.7)

    # Results
    output = hands.process(img_flip)

    hands.close()

    try:
        data = output.multi_hand_landmarks[0]
        #print(data)
        data = str(data)

        data = data.strip().split('\n')

        garbage = ['landmark {', '  visibility: 0.0', '  presence: 0.0', '}']

        without_garbage = []

        for i in data:
            if i not in garbage:
                without_garbage.append(i)
                        
        clean = []

        for i in without_garbage:
            i = i.strip()
            clean.append(i[2:])

        for i in range(0, len(clean)):
            clean[i] = float(clean[i])
        return(clean)
    except:
        return(np.zeros([1,63], dtype=int)[0])

# load model
with open('model.pkl', 'rb') as f:
    svm = pickle.load(f)

# Initialize the message list
message_list = []

def check_and_send(y_pred):
    # Initialize the ROS node and publisher
    rospy.init_node('sender')
    pub = rospy.Publisher('bittle', String, queue_size=10)  # Replace with the desired topic name

    # Append the first prediction to the list
    message_list.append(y_pred[0])

    # Check if the last 5 predictions are the same
    if len(message_list) >= 5 and all(x == message_list[-1] for x in message_list[-5:]):
        # Send the message to the ROS topic
        message = 'kbalance'

        # If y_pred is ... send the message
        if y_pred == 'stop':
            message = 'kbalance'
        elif y_pred == 'sit':
            message = 'ksit'
        elif y_pred == 'pootje':
            message = 'khi'
        elif y_pred == 'pump':
            message = 'kpu'

        rospy.loginfo('Sending message: %s', message)
        pub.publish(message)

        # Wait for 5 seconds
        time.sleep(5)

import cv2 as cv
#cap = cv.VideoCapture(0)
cap = cv2.VideoCapture("http://10.3.25.19:8080/?action=stream")
if not cap.isOpened():
    print("Cannot open camera")
    exit()
i = 0    
while True:
    
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # frame = cv.flip(frame,1)
    data = image_processed(frame)
    
    # print(data.shape)
    data = np.array(data)
    y_pred = svm.predict(data.reshape(-1,63))
    print(y_pred)
    
    # Check and send the message
    check_and_send(y_pred)

    # font
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # org
    org = (50, 100)
    
    # fontScale
    fontScale = 3
    
    # Blue color in BGR
    color = (255, 0, 0)
    
    # Line thickness of 2 px
    thickness = 5
    
    # Using cv2.putText() method
    frame = cv2.putText(frame, str(y_pred[0]), org, font, 
                    fontScale, color, thickness, cv2.LINE_AA)
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()