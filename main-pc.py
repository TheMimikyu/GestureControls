import cv2
import mediapipe as mp
from pynput.keyboard import Controller, Key

class HandController:
    def __init__(self):
        self.mp_hands = mp.solutions.hands.Hands()
        self.keyboard = Controller()
        self.cap = cv2.VideoCapture(0)
        self.x1, self.x2, self.y1, self.y2 = 0, 0, 0, 0

    def process_frame(self):
        _, image = self.cap.read()

        imageHeight, imageWidth, _ = image.shape
        image = cv2.flip(image, 1)
        rgbImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        outputHands = self.mp_hands.process(rgbImage)
        allHands = outputHands.multi_hand_landmarks

        if allHands:
            hand = allHands[0]
            oneHandLandmarks = hand.landmark

            for id, landmark in enumerate(oneHandLandmarks):
                x = int(landmark.x * imageWidth)
                y = int(landmark.y * imageHeight)

                if id == 12:
                    self.x1 = x
                    self.y1 = y

                if id == 0:
                    self.x2 = x
                    self.y2 = y

            distX = self.x1 - self.x2
            distY = self.y1 - self.y2

            if distY > -140 and distY != 0:
                # press Shift + S
                self.release_keys()
                self.keyboard.press(Key.shift)
                self.keyboard.press('S')
                print("Shift + S")

            if distY < -200 and distY != 0:
                # press Shift + W
                self.release_keys()
                self.keyboard.press(Key.shift)
                self.keyboard.press('W')
                print("Shift + W")

            if distX < -100 and distX != 0:
                # press Shift + A
                self.release_keys()
                self.keyboard.press(Key.shift)
                self.keyboard.press('A')
                print('Shift + A')

            if distX > 55 and distX != 0:
                # press Shift + D
                self.release_keys()
                self.keyboard.press(Key.shift)
                self.keyboard.press('D')
                print('Shift + D')

        else:
            print('none')
            self.release_keys()

    def release_keys(self):
        self.keyboard.release('A')
        self.keyboard.release('S')
        self.keyboard.release('D')
        self.keyboard.release('W')
        self.keyboard.release(Key.shift)

    def run(self):
        while True:
            self.process_frame()
            q = cv2.waitKey(1)
            if q == ord("q"):
                break

        cv2.destroyAllWindows()

# Create an instance of the HandController class and run the hand controller
hand_controller = HandController()
hand_controller.run()
