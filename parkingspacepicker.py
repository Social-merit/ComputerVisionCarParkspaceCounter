import cv2
import pickle

# Constants
WIDTH, HEIGHT = 108, 48

def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        params['posList'].append((x, y))
    elif events == cv2.EVENT_RBUTTONDOWN:
        posList = params['posList']
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + WIDTH and y1 < y < y1 + HEIGHT:
                posList.pop(i)

def main():
    try:
        with open('CarParkPos', 'rb') as f:
            posList = pickle.load(f)
    except FileNotFoundError:
        print("File not found. Initializing an empty list.")
        posList = []

    while True:
        img = cv2.imread('carParkImg.png')
        cv2.rectangle(img, (50, 192), (158, 240), (255, 0, 255), 2)

        for pos in posList:
            cv2.rectangle(img, pos, (pos[0] + WIDTH, pos[1] + HEIGHT), (255, 0, 255), 2)

        cv2.imshow('Image', img)
        cv2.setMouseCallback('Image', mouseClick, {'posList': posList})

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Dump the posList into the file 'CarParkPos'
    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
