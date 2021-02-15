_author_ = 'Patricia' 
import cv2 as cv2
import time
import keyboard
from tkinter import *



"""
img.dtype is very important while debugging because a large number of errors in OpenCV-Python code are caused by invalid datatype.
"""
# Loop until the end of the video
class Webcam:
    def __init__(self):
        #cv2.namedWindow("preview")
        master = Tk()
        master.bind_all("<Button-1>", self.activate)
        self.cap = cv2.VideoCapture(0)
        self.activation = False
        self.list_of_intervals_ON = []
        self.list_of_intervals_OFF = []
        self.min_brightness = 1000000
        self.max_brightness = 0

        self.lights_on = False
        self.counter= 5     # This should skip first 5 frames in funtions min/maxBrightness (will not assign values to self.minB and self.maxB )
   # def activate(self):
   #     self.activation = True
    def activate(self):
        self.activation = True
    def loadVideo(self):
        while (self.cap.isOpened()):
            # Capture frame-by-frame
            ret, frame = self.cap.read()
            frame = cv2.resize(frame, (460, 320), fx=0, fy=0)
            cv2.imshow('Webcam video', frame)

            if self.activation == True:
                pass
            else:
                continue

            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)       # to HSV format
            cv2.imshow('HSV Frame', hsv_frame)                      # Display the resulting frame

            v_value_frame = cv2.inRange(hsv_frame,(0,0,0), (0,0,255))   # Extracting V value from HSV - brightness
            cv2.imshow("V value", v_value_frame)                        # Display the resulting frame

            brightness = cv2.sumElems(v_value_frame)[0]/1000000         # number from 0 position with scaling 1000000
            self.minBrightness(brightness)
            self.maxBrightness(brightness)
            self.pseudo_treshold = (self.min_brightness + self.max_brightness) / 2        #threshold value which decides whether light on or off
            print(brightness)

            if brightness > self.pseudo_treshold and self.lights_on == False:       #lights on from off, write to list "time on"
                self.list_of_intervals_ON.append(self.lasting)
                self.lasting=0
                self.lights_on = True
            elif brightness < self.pseudo_treshold and self.lights_on == True:  #light off from on, write time to list "time off"
                self.list_of_intervals_OFF.append(self.lasting)
                self.lasting = 0
                self.lights_on = False
            else:       #otherwise time-lasting continues
                pass

            # define q as the exit button
            if cv2.waitKey(25) & 0xFF == ord('q'):
                self.closeAndDestroy()
    def timeWatch(self):
        self.lasting = time.time()
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

mainloop()
