import cv2
import numpy as np
import cvzone
import pickle

# Constants
width, height = (70 - 48), (50 - 40)  # Width and height of the car parking space
FREE_SPACE_THRESHOLD = 110 # Threshold for free space

# Load video file using OpenCV's VideoCapture
# cap = cv2.VideoCapture('carPark.mp4')
cap = cv2.VideoCapture('BusyParkingLot.mp4')

if not cap.isOpened():
    print("Error: Couldn't open the video file.")
    exit()

# Load a list of car parking positions
try:
    with open('CarPark1Pos', 'rb') as f: # rb = read binary mode
        posList = pickle.load(f)
except FileNotFoundError:
    print("Error: CarPark1Pos file not found.")
    exit()





def checkParkingSpace(imgPro, img, posList, width, height):
    # imgPro = image processed, img = original image, posList = list of positions, width = width of car parking space, height = height of car parking space
    # Loop through the list of positions and check if the car parking space is free or not. If it is free, draw a green rectangle on the image. If it is not free, draw a red rectangle on the image.
    # If the car parking space is free, increment the spaceCounter variable.
    # Print the number of free spaces and the total number of spaces in the car park.
    # Display the image.
    # Save the image.

    # Draw a rectangle on the image for each position in the posList.
    # Check if the car parking space is free or not. If it is free, draw a green rectangle on the image. If it is not free, draw a red rectangle on the image.
    # If the car parking space is free, increment the spaceCounter variable.
    # Print the number of free spaces and the total number of spaces in the car park.
    # Display the image.
    # Save the image.
    spaceCounter = 0
    for pos in posList: #
        x, y = pos
        imgCrop = imgPro[y:y + height, x:x + width]
        count = cv2.countNonZero(imgCrop)
        # cvzone.putTextRect(img, str(count), (x, y + height - 1), scale=1, thickness=1, offset=0, colorR=(0, 0, 255))

        if count < FREE_SPACE_THRESHOLD:
            color = (0, 255, 0)
            thickness =1
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 1

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)

    cvzone.putTextRect(img, f'FREE {str(spaceCounter)}/{len(posList)}', (450, 50), scale=2, thickness=3, offset=20,
                       colorR=(0, 200, 0))


while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):   # Check if the video file is at the end. If it is, set the video file to the beginning.
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()  # Read the video file.
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert the video file to grayscale.
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1 ) # Blur the grayscale image.
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 9) # Threshold the blurred image.
    imgMedian = cv2.medianBlur(imgThreshold, 3) # Median blur the thresholded image.
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1) # Dilate the median blurred image.

    checkParkingSpace(imgDilate, img, posList, width, height) # Call the checkParkingSpace function.

    cv2.imshow('Image', img) # Display the image.
    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break





# Release video capture and destroy all OpenCV windows
cap.release()
cv2.destroyAllWindows()