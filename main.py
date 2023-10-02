import cv2
import numpy as np
import cvzone
import pickle

# Initialize constants
WIDTH, HEIGHT = 108, 48  # Dimensions of each parking space in pixels
FREE_SPACE_THRESHOLD = 500  # Number of white pixels to consider a parking space free
GAUSSIAN_BLOCK_SIZE = 25
GAUSSIAN_C = 16

# Load pre-saved positions of parking spaces from a pickle file
with open('CarPark2Pos', 'rb') as f:
    posList = pickle.load(f)

# Initialize video capture from file
cap = cv2.VideoCapture('carPark.mp4')

# Function to preprocess each video frame
def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    blurred = cv2.GaussianBlur(gray, (3, 3), 1)  # Apply Gaussian blur
    # Apply adaptive thresholding
    thresholded = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV, GAUSSIAN_BLOCK_SIZE, GAUSSIAN_C)
    median = cv2.medianBlur(thresholded, 5)  # Apply median blur
    kernel = np.zeros((3, 3), np.uint8)  # Initialize kernel for dilation
    dilated = cv2.dilate(median, kernel, iterations=1)  # Dilate the image
    return dilated

# Function to check and mark each parking space as occupied or free
def check_parking_space(processed_img, original_img):
    free_space_count = 0  # Counter for free spaces

    # Loop through each parking position
    for x, y in posList:
        crop_img = processed_img[y:y + HEIGHT, x:x + WIDTH]  # Crop image around parking space
        count = cv2.countNonZero(crop_img)  # Count the number of white pixels
        # Display the white pixel count on the original image
        cvzone.putTextRect(original_img, str(count), (x, y + HEIGHT - 1), scale=1, thickness=1, offset=0, colorR=(0, 0, 255))

        # Check if parking space is free based on white pixel count
        if count < FREE_SPACE_THRESHOLD:
            color = (0, 255, 0)  # Green for free
            thickness = 4  # Thicker rectangle for free space
            free_space_count += 1  # Increment free space counter
        else:
            color = (0, 0, 255)  # Red for occupied
            thickness = 2  # Thinner rectangle for occupied space

        # Draw rectangle around parking space on original image
        cv2.rectangle(original_img, (x, y), (x + WIDTH, y + HEIGHT), color, thickness)

    # Display the number of free spaces on the original image
    free_space_text = f"FREE: {free_space_count}/{len(posList)}"
    cvzone.putTextRect(original_img, free_space_text, (450, 50), scale=2, thickness=3, offset=20, colorR=(0, 200, 0))

# Main loop to process video frames
while True:
    # Loop the video when it reaches the end
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Read the next video frame
    success, frame = cap.read()
    if not success:
        print("Failed to read frame")
        break

    # Process the frame and check parking spaces
    processed_frame = process_frame(frame)
    check_parking_space(processed_frame, frame)

    # Display the processed frame
    cv2.imshow('Parking Monitoring', frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and destroy all OpenCV windows
cap.release()
cv2.destroyAllWindows()
