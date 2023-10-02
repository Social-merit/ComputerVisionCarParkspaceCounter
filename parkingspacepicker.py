import cv2
import pickle

# Constants
# WIDTH, HEIGHT = 108, 48
# width, height = (158 - 50), (240 - 192) # Width and height of the car parking space
# WIDTH, HEIGHT = (79 - 25), (120 - 96)  # Width and height of the car parking space
# cv2.rectangle(img,   (25, 96), (79, 120), (255, 0, 255), 2)  # (50, 192) is the top left corner of the parking space


width,height = (158-50), (240-192)  # for carParkImg1.png
# width, height = (70 - 48), (50 - 40)  # for busy parking lot app


try:
    with open('CarParkPos','rb') as f:
        posList = pickle.load(f)
except:
    posList = []

def mouseClick(events,x,y,flags,params):
    if events ==cv2.EVENT_LBUTTONDOWN:
        posList.append((x,y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1,y1 = pos
            if x1<x<x1+width and y1<y<y1+height:
                posList.pop(i)
    with open('CarParkPos','wb') as f:
        pickle.dump(posList,f)

while True:
    img = cv2.imread('carParkImg2.png')

    cv2.rectangle(img, (50, 192), (158, 240), (255, 0, 255), 2)  ## for carParkImg1.png
    # cv2.rectangle(img,   (48, 40), (70, 50), (255, 0, 255), 1)  # for busy parking lot img

    for pos in posList:
        cv2.rectangle(img,pos,(pos[0]+width,pos[1]+height),(255,0,255),1)
    cv2.imshow('Image', img)

    cv2.setMouseCallback('Image',mouseClick)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break






# Release video capture and destroy all OpenCV windows
# cap.release()
cv2.destroyAllWindows()
