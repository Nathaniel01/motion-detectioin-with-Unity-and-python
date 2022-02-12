import cv2
import numpy as np
import socket  # to convert data to binary

# Connection between host and port
host, port = "127.0.0.1", 25001
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

# Variable to send data over the Socket
socketIntVar = 0  # Integer variable
socketStrVar = ''  # String variable


# Motion detection function
def motion_detection():

    # using the webcam
    video_capture = cv2.VideoCapture(0)

    # for History threshold and background subtraction Algorithm (MOG2). history, Threshold, Detect shadows
    background_subtractor = cv2.createBackgroundSubtractorMOG2(40, 50, True)

    # count the frame we are on
    frame_count = 0

    while True:
        # return the value and the current frame
        ret, frame = video_capture.read()

        # check if the current frame exists
        if not ret:
            break

        frame_count += 1

        # give size of the frame
        resized_frame = cv2.resize(frame, (0, 0), fx=0.60, fy=0.60)

        # generate  the foreground mask
        fgmask = background_subtractor.apply(resized_frame)

        # Count all non zero pixels
        count = np.count_nonzero(fgmask)

        print('Frame: %d, Pixel Count: %d' % (frame_count, count)) #Print the number of frames and the Pxel count

        if frame_count > 1 and count >= 1000:

            socketIntVar = count  # Count when motion is detected

            socketStrVar = str(socketIntVar)  # Convert integer var above to string
            sock.sendall(socketStrVar.encode("UTF-8"))  # Convert String to bytes and send over socket
            print("Data sent!")

            #Display  Display 'motion detected' on window
            cv2.putText(resized_frame, 'Motion detected', (10, 50),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255,), 2,
                        cv2.LINE_AA)


        cv2.imshow('frame', resized_frame, )

        key = cv2.waitKey(5) & 0xff
        if key == 27 or key == 13:  # Destroy when the escape/enter key is pressed
            video_capture.release()
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    motion_detection()