_author_ = 'Patricia'
import cv2 as cv2
import time
import numpy as np
#from datetime import datetime
#import keyboard

"""
img.dtype is very important while debugging because a large number of errors in OpenCV-Python code are caused by invalid datatype.
"""
# Loop until the end of the video
class Webcam:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.list_of_intervals_ON = []
        self.list_of_intervals_OFF = []
        self.min_brightness = 1000000
        self.max_brightness = 0
        self.activation = False
        self.lights_on = False
        self.counter = 3     # This should skip first 3 frames in funtions min/maxBrightness (will not assign values to self.minB and self.maxB )
        self.lasting=time.perf_counter()
    def loadVideo(self):
        while (self.cap.isOpened()):
            # Capture frame-by-frame
            ret, frame = self.cap.read()

            # self.img = np.zeros((512, 512, 3), np.uint8)
            # cv2.namedWindow('Webcam video')
            # cv2.setMouseCallback('Webcam video', self.draw_circle)

            computed_frame = self.computeAll(frame)
            cv2.imshow("For light evaluation", computed_frame)        # This is to be deleted at the end
            cv2.putText(frame, "Press \"q\" to quit", (20, 40), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255))
            cv2.putText(frame, "Press \"s\" when ready to start signalling", (20, 60), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                        (255, 255, 255))
            cv2.imshow('Webcam video', frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):      # q as the exit button
                self.closeAndDestroy()
            elif cv2.waitKey(27) & 0xFF == ord('s'):    # s as the start button
                self.activation = True      # Activation for the start of time tracking

    # def draw_circle(self,event, x, y, flags, param):
    #     if event == cv2.EVENT_LBUTTONDBLCLK:        # With doubleclick the coordinates will be saved
    #         cv2.circle(self.img, (x, y), 100, (255, 0, 0), -1)
    #         self.mouseX, self.mouseY = x, y
    #         print(self.mouseY)


    def computeAll(self,frame):
        frame = cv2.resize(frame, (460, 320), fx=0, fy=0)
        grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # to grey format

        brightness = cv2.sumElems(grey_frame)[0] / 1000000  # number from 0 position with scaling 1000000
        self.minBrightness(brightness)
        self.maxBrightness(brightness)
        self.pseudo_treshold = (self.min_brightness + self.max_brightness) / (1.9)  # threshold value which decides whether light on or off
        print("pseudo threshhold,          ", self.pseudo_treshold)
        print(brightness, "    Brightness \n ")

        if self.activation == True:
            cv2.putText(grey_frame, "Aktivne", (20, 60), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                        (0, 255, 0))
            if brightness > self.pseudo_treshold and self.lights_on == False:  #turning light on from off, write to list "time off"
                time_passed = self.timeWatch()
                self.list_of_intervals_OFF.append(round(time_passed,2))
                self.lights_on = True
            elif brightness < self.pseudo_treshold and self.lights_on == True:  # turning light off from on, write time to list "time on"
                time_passed = self.timeWatch()
                self.list_of_intervals_ON.append(round(time_passed,2))
                self.lights_on = False
            else:  # otherwise time-lasting continues
                pass
        else:
            cv2.putText(grey_frame, "Neaktivne", (20, 60), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                        (0, 0, 255))
            pass
        return grey_frame

    def timeWatch(self):
        actual_time = time.perf_counter()
        time_passed = actual_time - self.lasting
        self.lasting = actual_time
        print("    ",time_passed,"      time passed")
        return time_passed
    def closeAndDestroy(self):
        # release the video capture object
        self.cap.release()
        # Closes all the windows currently opened.
        cv2.destroyAllWindows()
        print("  \n")
        print(self.min_brightness)
        print(self.max_brightness)
        print("   ")
        print(self.list_of_intervals_ON)
        print(self.list_of_intervals_OFF)
        print("   ")
        print(self.lasting)
    def minBrightness(self, minB):
        self.counter-=1
        if minB < self.min_brightness and self.counter <= 0:
            self.min_brightness = minB
    def maxBrightness(self, maxB):
        self.counter -= 1
        if maxB > self.max_brightness and self.counter <= 0:
            self.max_brightness = maxB

"""morse_lookup = {
        '.-': 'A',
        '-...': 'B',
        '-.-.': 'C',
        '-..': 'D',
        '.': 'E',
        '..-.': 'F',
        '--.': 'G',
        '....': 'H',
        '..': 'I',
        '.---': 'J',
        '-.-': 'K',
        '.-..': 'L',
        '--': 'M',
        '-.': 'N',
        '---': 'O',
        '.--.': 'P',
        '--.-': 'Q',
        '.-.': 'R',
        '...': 'S',
        '-': 'T',
        '..-': 'U',
        '...-': 'V',
        '.--': 'W',
        '-..-': 'X',
        '-.--': 'Y',
        '--..': 'Z',
        '.----': '1',
        '..---': '2',
        '...--': '3',
        '....-': '4',
        '.....': '5',
        '-....': '6',
        '--...': '7',
        '---..': '8',
        '----.': '9',
        '-----': '0'
    }"""

video=Webcam()
video.loadVideo()

