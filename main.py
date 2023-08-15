import cv2

face = cv2.CascadeClassifier('Model/haarcascade_frontalface_default.xml')
# glass=cv2.imread('DATASET/specs_no_bg/glasses.png')
glass=cv2.imread('DATASET/specs_no_bg/specs_38.png')

def put_glass(glass, fc, x, y, w, h):
    face_width = w
    face_height = h

    hat_width = face_width + 1
    hat_height = int(0.50 * face_height) + 1

    glass = cv2.resize(glass, (hat_width, hat_height))

    # print(glass[0][0] > [0,0,0])
    for i in range(hat_height):
        for j in range(hat_width):
            # print(glass[i][j])
            if glass[i][j][0] != 0 and glass[i][j][0] != 255:
                fc[y + i - int(-0.20 * face_height)][x + j] = glass[i][j]

    # for i in range(hat_height):
    #     for j in range(hat_width):
    #         for k in range(3):
    #             if glass[i][j][k] < 235:
    #                 fc[y + i - int(-0.20 * face_height)][x + j][k] = glass[i][j][k]
    return fc

choice = 0
webcam = cv2.VideoCapture(0)
while True:
    size=4
    (rval, im) = webcam.read()
    im = cv2.flip(im, 1, 0)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    fl = face.detectMultiScale(gray,1.19,7)

    for (x, y, w, h) in fl:
        im = put_glass(glass, im, x, y, w, h)

    cv2.imshow('Hat & glasses',im)
    key = cv2.waitKey(30) & 0xff
    if key == 27:  # The Esc key
       break

