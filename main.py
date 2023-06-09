import cvzone
import cv2
import os
import math
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# TA1. Create list to hold menu images and pathList
menuImages = []
path = "filters"
pathList = os.listdir(path)

# TA1. Sorting is done for MAC
pathList.sort()
print(type(pathList))
# TA1. Load all the images in the list
for pathImg in pathList:
    img = (cv2.imread(path+"/"+pathImg, cv2.IMREAD_UNCHANGED))
    menuImages.append(img)

# TA2. Count the number of images in the menuList
menuCount = len(menuImages)


detector = HandDetector(detectionCon=0.8)

# TA3.1 Flag variable for item selected from the filters menu
menuChoice = -1

# TA3.2 Flag variable to show if we are dragging an image or mot
isImageSelected = False

while True:
    success, cameraFeedImg = cap.read()
    cameraFeedImg = cv2.flip(cameraFeedImg, 1)

    # TA2. Get width and height of final output screen
    wHeight, wWidth, wChannel = cameraFeedImg.shape

    # TA2. Set initial position to 0 (menu will start displaying at 0)
    x = 0
    # TA2. Calculate imcrements to display next menuImage
    xIncrement = math.floor(wWidth / menuCount)

    hands, cameraFeedImg = detector.findHands(cameraFeedImg, flipType=False)

    indexFingerTop = 0
    try:
        if hands:
            hand1 = hands[0]
            lmList1 = hand1["lmList"]  
            indexFingerTop = lmList1[8]
            indexFingerBottom = lmList1[6]

            # TA3.1 Find which image is selected by the pointer finger
            if (indexFingerTop[1] < xIncrement):
                i = 0
                while (xIncrement*i <= wWidth):
                    if (indexFingerTop[0] < xIncrement*i):
                        menuChoice = i-1
                        isImageSelected = True #TA3.2 Set isImageSelected flag variable to true to show that image can be dragged now
                        break
                    i = i+1

            # TA3.2 Stop dragging
            if (indexFingerTop[1] > indexFingerBottom[1]):
                isImageSelected = False

        # TA3.2 Drag the selected image
        if (isImageSelected):
            image = cv2.resize(menuImages[menuChoice], (100, 100))
            cameraFeedImg = cvzone.overlayPNG(cameraFeedImg, image, [int(indexFingerTop[0]), int(indexFingerTop[1])])

    except Exception as e:
        print(e)


    try:
        # TA2. Overlay menu images to camera feed
        for image in menuImages:
            margin = 20
            image = cv2.resize(image, (xIncrement - margin, xIncrement - margin))
            cameraFeedImg = cvzone.overlayPNG(cameraFeedImg, image, [x, 0])
            x = x + xIncrement
    except:
        print("out of bounds")
    #TA1: Only in TA1 to show loaded image
    #cv2.imshow("Face Filter App", menuImages[2])

    cv2.imshow("Face Filter App", cameraFeedImg)
    cv2.waitKey(1)