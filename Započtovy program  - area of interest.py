_author_ = 'Patricia' 

import cv2 as cv2
import time
import numpy as np

# Loop until the end of the video
class Morse:
    def __init__(self, unitOfTime=0.3, camera_port = 0):
        """An iniciator of object Morse with the information about frequency of light broadcasting used for evaluation of light signal and
        camera port used for the light input with each frame.
        Inicializator objektu s nacitanou frekvenciou vysielania svetelneho signalu a premenna o kamerovom porte,ktory
        bude program pouzivat."""

        self.TIME_UNIT = unitOfTime         #dot 1 unit, dash 3 units
        self.ratio = 3
        self.cap = cv2.VideoCapture(camera_port)
        self.list_of_intervals = []
        self.active = False
        self.lights_on = False
        self.threshold = 15
        self.lasting=time.perf_counter()
        self.MORSE_DICTIONARY = {' ': "", '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F', '--.': 'G',
                                 '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N',
                                 '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T', '..-': 'U',
                                 '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y', '--..': 'Z', '.----': '1',
                                 '..---': '2', '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7',
                                 '---..': '8', '----.': '9', '-----': '0'}
        self.translated = "Neprebehlo svetelne prijimanie signalu "
    def load_video(self):
        """
        Function which loads video frame by frame and applies adjustmets by pressing specific keys on keyboard. Based on evaluation
        of brightness assigns value whether light source is on or off.
        :return:
        """
        while (self.cap.isOpened()):
            # Capture frame-by-frame
            ret, frame = self.cap.read()                    # Reads frame
            frame = self.compute_all(frame)

            if self.active == True:                         # Condition which detects switching lights ON and OFF
                frame[45:75, 10:120, 1] = 255
                cv2.putText(frame, "Aktivne", (20, 60), cv2.FONT_HERSHEY_COMPLEX, 0.55,
                            (0, 0, 0))                      # Adding text for user to know, whether light signaling has been activated

                if self.brightness > self.threshold and self.lights_on == False:
                    time_passed = self.time_watch()
                    if time_passed > self.TIME_UNIT*(5.5):                  # The space between words is 7 units of time
                        # used 5.5 because light focusing is delayed
                        self.list_of_intervals.append("OFFF")               # OFFF signals gap between words

                    elif time_passed > self.TIME_UNIT*(2.0):                # The space between letters is 3 units of time
                        # used 2.0 because light focusing is delayed
                        self.list_of_intervals.append("OFF")                # OFF signals gap between letters
                    else:
                        pass   # The space between perts of the same letter is one unit of time

                    self.lights_on = True

                elif self.brightness < self.threshold and self.lights_on == True:
                    time_passed = self.time_watch()
                    sign_from_time = self.into_morse(time_passed)
                    self.list_of_intervals.append(sign_from_time)
                    self.lights_on = False
                else:  # otherwise time-lasting continues
                    pass
            else:
                frame[45:75, 10:120, 2] = 255
                cv2.putText(frame, "Neaktivne", (20, 60), cv2.FONT_HERSHEY_COMPLEX, 0.55,
                            (0, 0, 0))                        # Adding text for user to know, whether light signaling has been activated
                pass

            frame = self.text_placing(frame)
            cv2.imshow('Webcam', frame)

            # Waitkeys for specfic responses
            if cv2.waitKey(25) & 0xFF == ord('q'):      # "q" as the exit button
                self.close_and_destroy()
            elif cv2.waitKey(30) & 0xFF == ord('w'):    # "w" as a button for raising treshold
                self.threshold = self.threshold + 2
            elif cv2.waitKey(27) & 0xFF == ord('s'):    # "s" as a button for lowering treshold
                self.threshold = self.threshold - 2
            elif cv2.waitKey(23) & 0xFF == ord('o'):    # "o" as a button for initialisation of signal recording
                self.active = True
                self.lasting = time.perf_counter()  # Time counting is set at the moment of activation
    def compute_all(self, frame):
        """ Frame computation - the function resizes frame from input and creates and edits now frame with shifted interest(used for brightness
        evaluation)"""
        frame = cv2.resize(frame, (460, 320), fx=0, fy=0)
        x = 120
        y = 130
        frame = cv2.rectangle(frame, (x, y), (x + 50, y + 50), (0, 100, 0), 3)  # Creating a shape (in original frame) which will be used for brightness evaluation
        roi_frame = frame[y:y + 50, x:x + 50]                                   # Frame with Region of Interest (roi)
        roi_frame = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)                 # Converting roi frame into black and white
        self.brightness = cv2.sumElems(roi_frame)[0] / roi_frame.size / 10      # Sum of pixels divided by number of pixels in roi frame + scaled down by 10

        return frame
    def text_placing(self, frame2):
        """ Text placement to give user an idea what is availible and neccesary for program running"""
        frame1 = np.zeros(shape=[320,460,3], dtype= np.uint8)
        # frame1 = frame2.copy()
        # frame1[0:320, 0:460] = (0, 0, 0)

        text= "Hold \"q\" to quit \n Hold \"o\" when ready to " \
               "start signalling \n \n \n \n \n Hold \"w\" to raise " \
               "threshold \n Hold \"s\" to lower threshold \n \n Adjust threshold to recognise light source \n Good " \
               "threshold should have value a little \n below the brightness when light source is ON \n and is placed in area of marked rectangle"
        for i, line in enumerate(text.split('\n')):                 #prints line by line from _text_ variable
            y = 40 + i * 20
            cv2.putText(frame1, line, (20, y), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                        (255, 255, 255))
        cv2.putText(frame1, "Svetlo " + str(round(self.brightness, 1)), (50, 100), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                    (0, 255, 255))
        cv2.putText(frame1, "with Threshold " + str(self.threshold), (50, 120), cv2.FONT_HERSHEY_COMPLEX, 0.50,
                    (255, 0, 255))

        frame = np.concatenate([frame1, frame2], axis=1)                # Joins 2 frames together along vertical axis
        return frame
    def into_morse(self, time):
        """ Sign assigning based on time unit. With ratio 1:3 the lasting of one ON state of light source
        is determined as dot or dash according to "boarder". Boarder is set on the average of dot and dash lasting
        (1 unit + 3 units) /2 = border """
        time_border = self.TIME_UNIT * self.ratio * (2/3)
        if time >= time_border:
            return "-"
        else:
            return "."
    def time_watch(self):
        """ Timing of events in program. Timing is calculated by subtraction of start time from an event for time assigning"""
        actual_time = time.perf_counter()
        time_passed = actual_time - self.lasting
        self.lasting = actual_time
        return time_passed
    def close_and_destroy(self):
        """ Closing and destroying opened windows"""
        self.cap.release()          # release the video capture object
        cv2.destroyAllWindows()     # Closes all the windows currently opened.
        self.translate()            # calling function for translation of dot and dash symbols
    def translate(self):
        """ Traslates dot/dash symbols into a letter which further translates into words."""
        if self.active == False:
            self.display_translated()
        else:
            signs=" "
            self.translated = ""
            for i in range (len(self.list_of_intervals)):
                if self.list_of_intervals[i] == "OFF":
                    # OFF indicated the separation between letters
                    letter = self.MORSE_DICTIONARY.get(signs)       # Composed string of symbols (-.) assigned letter from alphabet dictionary
                    try:                                            # If any error occured during loading of signal/translation and string of symbols not found, then "*" assigned
                        self.translated += letter
                    except TypeError:
                        self.translated += "*"                      # symbol of unrecognised letter in alphabet
                    signs=""

                elif self.list_of_intervals[i] == "OFFF":
                    # OFF indicated the separation between words
                    letter = self.MORSE_DICTIONARY.get(signs)
                    try:
                        self.translated += letter + " "             # Only adds additional space behind a letter
                    except TypeError:
                        self.translated += "*  "
                    signs = ""
                else:
                    signs += self.list_of_intervals[i]      #adds symbols (-.) into variable _signs_ while OFF/OFFF occurs

            letter = self.MORSE_DICTIONARY.get(signs)
            try:
                self.translated += letter
            except TypeError:
                self.translated += "*"

            self.display_translated()
    def display_translated(self):
        """ Final displaying of translated light signal into alphabet"""
        if len(self.translated)>150:
            line_max=60
            text_size=0.4
            spacing_between_lines=20
        else:
            line_max=45
            text_size=0.5
            spacing_between_lines=40
        if len(self.translated)>line_max:                     #Translating text into system of lines in case a long sentence is to be displayed
            n_of_lines = len(self.translated)%line_max
            start= 0
            line= ""
            for i in range(n_of_lines):
                line = line + self.translated[start: line_max + start] + "\n"
                start+=line_max
            self.translated = line
        frame = np.zeros(shape=[256,512,3], dtype= np.uint8)        #creating empty black window
        x=120
        y=130

        while True:
            for i, line in enumerate(self.translated.split('\n')):  #displaying translated system of words
                y = 50 + i * spacing_between_lines
                cv2.putText(frame, line, (40, y), cv2.FONT_HERSHEY_COMPLEX, text_size, (255, 255, 255))
            cv2.putText(frame, "press \"r\" to quit", (350, 250), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
            #cv2.putText(frame, self.translated, (50, y), cv2.FONT_HERSHEY_COMPLEX, 0.8,(255, 255, 255))
            cv2.imshow("preview", frame)
            if cv2.waitKey(26) & 0xFF == ord('r'):                  # "r" as the exit button
                break
print("  Inicializuj triedu Morse s udajmi \n o použitej casovej jednotke v \n sekundach na  vysielanie a kamerovym \n portom, ktory pouzijes \n")

frekvencia=float(input(" Zadaj casovu jednotku svetelneho signalu nie nizsiu ako 0.3 sekund: "))

print(" \n Pre vstavanu webkameru zadaj 0")

port = int(input(" Zadaj kamerovy port: "))
video = Morse(frekvencia,port)
video.load_video()