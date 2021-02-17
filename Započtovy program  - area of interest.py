_author_ = 'Patricia' 
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
class Morse:
    def __init__(self, unitOfTime=0.3, ratio=3):
        self.TIME_UNIT = unitOfTime   #dot 1 unit, dash 2q units
        self.ratio = ratio
        self.cap = cv2.VideoCapture(0)
        self.list_of_intervals = []
        self.active = False
        self.lights_on = False
        self.threshold = 15
        self.lasting=time.perf_counter()
        self.morse_dictionary = {' ':"",'.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F', '--.': 'G',
                                 '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N',
                                 '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T', '..-': 'U',
                                 '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y', '--..': 'Z', '.----': '1',
                                 '..---': '2', '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7',
                                 '---..': '8', '----.': '9', '-----': '0'}
        self.translated = ""
    def loadVideo(self):
        while (self.cap.isOpened()):
            # Capture frame-by-frame
            ret, frame = self.cap.read()
            frame = cv2.resize(frame, (460, 320), fx=0, fy=0)
            x=120
            y= 130
            frame = cv2.rectangle(frame, (x, y), (x+50, y+50), (0, 100, 0), 3)
            roi_frame = frame[y:y+50, x:x+50]
            roi_frame = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)
            brightness = cv2.sumElems(roi_frame)[0] / roi_frame.size /10

            frame_for_text=frame.copy()
            frame_for_text[0:320, 0:460]=(0,0,0)


            if self.active == True:
                frame[45:75, 10:120, 1] = 255
                cv2.putText(frame, "Aktivne", (20, 60), cv2.FONT_HERSHEY_COMPLEX, 0.55,
                            (0, 0, 0))
                if brightness > self.threshold and self.lights_on == False:  # turning light on from off, write to list "time off"
                    time_passed = self.timeWatch()
                    if time_passed > self.TIME_UNIT*(3):
                        self.list_of_intervals.append("OFFF")
                    elif time_passed > self.TIME_UNIT*(9/6):
                        self.list_of_intervals.append("OFF")
                    else:
                        pass
                    self.lights_on = True
                elif brightness < self.threshold and self.lights_on == True:  # turning light off from on, write time to list "time on"
                    time_passed = self.timeWatch()
                    sign_from_time = self.intoMorse(time_passed)
                    self.list_of_intervals.append(sign_from_time)
                    self.lights_on = False
                else:  # otherwise time-lasting continues
                    pass
            else:
                frame[45:75, 10:120, 2] = 255
                cv2.putText(frame, "Neaktivne", (20, 60), cv2.FONT_HERSHEY_COMPLEX, 0.55,(0, 0, 0))
                pass

            text = "Hold \"q\" to quit \n Hold \"o\" when ready to " \
                   "start signalling \n \n \n \n \n Hold \"w\" to raise " \
                   "threshold \n Hold \"s\" to lower threshold \n \n Adjust threshold to recognise light source \n Good " \
                   "threshold should have value \n a little below the brightness when light source \n is placed in the marked rectangle"
            for i, line in enumerate(text.split('\n')):
                y = 40 + i * 20
                cv2.putText(frame_for_text, line, (20, y), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                            (255, 255, 255))
            cv2.putText(frame_for_text, "Svetlo " + str(round(brightness, 1)), (50, 100), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                        (0, 255, 255))
            cv2.putText(frame_for_text, "with Threshold " + str(self.threshold), (50, 120), cv2.FONT_HERSHEY_COMPLEX, 0.50,
                        (255, 0, 255))


            frame = np.concatenate([frame_for_text, frame], axis=1)

            #Finally prints the frames with text
            cv2.imshow('Webcam', frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):      # q as the exit button
                self.closeAndDestroy()
            elif cv2.waitKey(30) & 0xFF == ord('w'):
                self.threshold = self.threshold + 2
            elif cv2.waitKey(27) & 0xFF == ord('s'):
                self.threshold = self.threshold - 2
            elif cv2.waitKey(23) & 0xFF == ord('o'):
                self.active = True
                self.lasting = time.perf_counter()
    def intoMorse(self, time):
        time_border = self.TIME_UNIT * self.ratio * (2/3)
        if time >= time_border:
            return "-"
        else:
            return "."
    def timeWatch(self):
        actual_time = time.perf_counter()
        time_passed = actual_time - self.lasting
        self.lasting = actual_time
        return time_passed
    def closeAndDestroy(self):
        # release the video capture object
        self.cap.release()
        # Closes all the windows currently opened.
        cv2.destroyAllWindows()
        self.translate()

    def translate(self):
        signs=" "
        for i in range (len(self.list_of_intervals)):
            if self.list_of_intervals[i] == "OFF":
                letter = self.morse_dictionary.get(signs)
                try:
                    self.translated += letter
                except TypeError:
                    self.translated += "*X*"
                signs=""
            elif self.list_of_intervals[i] == "OFFF":
                letter = self.morse_dictionary.get(signs)
                try:
                    self.translated += letter + " "
                except TypeError:
                    self.translated += "*X*  "
                signs = ""
            else:
                signs += self.list_of_intervals[i]
        letter = self.morse_dictionary.get(signs)
        try:
            self.translated += letter
        except TypeError:
            self.translated += "*X*"
        print(self.translated)



video=Morse(0.3)
video.loadVideo()
