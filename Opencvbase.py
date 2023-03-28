import cv2
import dlib
import math
import time

# initialize face detector and landmark predictor

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# initialize video capture
cap = cv2.VideoCapture(0)

# initialize camera parameters
fov = 60 # in degrees
focal_length = 500 # in pixels

# initialize variables
start_time = None
last_seen_screen = None
last_seen_far = None
last_seen_near = None

while True:
    # read frame from video capture
    ret, frame = cap.read()
    # detect faces in the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    # for each face, detect facial landmarks and estimate distance
    for face in faces:
        landmarks = predictor(gray, face)
        size = math.sqrt((face.right() - face.left())**2 + (face.bottom() - face.top())**2)
        distance = (focal_length * math.tan(math.radians(fov/2))) / (size/2)

        # determine if the user is looking at the screen or not
        if distance <= 50:

            # user is looking at the screen now
            if last_seen_screen is None:
                start_time = time.time()
                last_seen_screen = time.time()
            else:
                last_seen_screen = time.time()
        else:
            # user is not looking at the screen
            if last_seen_screen is not None:

                print("Time spent on screen: {:.2f}s".format(last_seen_screen - start_time))
                start_time = None
                last_seen_screen = None

            # determine if the user is seeing far or near objects

            if distance > 50 and last_seen_far is None:

                last_seen_far = time.time()

                print("Time spent seeing far objects: {:.2f}s".format(last_seen_far - last_seen_near if last_seen_near is not None else 0))

            elif distance <= 50 and last_seen_near is None:

                last_seen_near = time.time()

                print("Time spent seeing near objects: {:.2f}s".format(last_seen_near - last_seen_far if last_seen_far is not None else 0))

        # draw circles on the facial landmarks for visualization

        for i in range(68):

            cv2.circle(frame, (landmarks.part(i).x, landmarks.part(i).y), 2, (0, 255, 0), -1)

    # display the frame

    cv2.imshow("Frame", frame)

    # exit on key press

    if cv2.waitKey(1) & 0xFF == ord('q'):

        break

# release resources

cap.release()

cv2.destroyAllWindows()
