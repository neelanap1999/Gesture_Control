import cv2
import time
import mediapipe as mp


class handDetector():
    def __init__(self,mode=False,maxHands=2,model_complexity=1,detectcon=0.5,trackcon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectcon=detectcon
        self.trackcon=trackcon
        self.model_complexity=model_complexity
        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(self.mode,self.maxHands,self.model_complexity,self.detectcon,self.trackcon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for x in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, x, self.mphands.HAND_CONNECTIONS)
        return img

    def findPosition(self,img,hand_no=0,draw=True):

        lmList=[]
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(myhand.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                #print(id,cx,cy)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),10,(255,0,0),cv2.FILLED)
        return lmList
def main():
    cTime = 0
    pTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success,img = cap.read()
        img = detector.findHands(img)
        lmList=detector.findPosition(img)
        if len(lmList)!=0:
            print(lmList[4])
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.imshow('Image',img)
        cv2.waitKey(1)
        cv2.putText(img, str(int(fps)), (20, 40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)



if __name__ == '__main__':
    main()