import cv2
import numpy as np
import time
import PoseModule as pm
import os
import math
import ffmpeg



def squatscv(filename):
    cap = cv2.VideoCapture("static/files/%s"%filename)
    detector = pm.poseDetector()
    count = 0
    dir = 0
    pTime = 0
    color = (225, 0 ,225)
    bar = 0
    per = 0
    width  = int(cap.get(3)) # float `width`
    height = int(cap.get(4))
    size = (width, height)
    result_filename = "result_" + filename
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)

    result = cv2.VideoWriter("static/result/%s" %result_filename, fourcc, fps, size)

    while True:
        success, img = cap.read()
        #success, src = cap.read()
        #img = cv2.flip(src, 180)
        # img = cv2.resize(img, size)
        #img = cv2.resize(img, (1179, 2556))
        # img = cv2.imread("PoseImage/jumping_Jacks.jpg")
        if (success):
            img = cv2.resize(img, size)
            img = detector.findPose(img, False)
            lmList = detector.findPosition(img, False)
            # print(lmList)
            if len(lmList) != 0:
                # Right Arm
                lLegAngle = detector.findAngle(img, 23, 25, 27, False)
                rLegAngle = detector.findAngle(img, 24, 26, 28)
                lHipAngle = detector.findAngle(img, 12, 24, 26, False)
                rHipAngle = detector.findAngle(img, 11, 23, 27, False)

                lLegper = np.interp(lLegAngle,(190, 280), (100, 0))
                rLegper = np.interp(rLegAngle,(69, 170), (0, 100)) 
                lHipper = np.interp(lHipAngle,(69, 180), (0, 100)) 
                rHipper = np.interp(rHipAngle,(110, 180), (0, 100))
                
                per = rLegper
                # per = (lLegper + rLegper + lHipper + rHipper) / 4
                # # print(lowAngle, lowper)
                print(per)
                # print(img.shape)

                lLegbar = np.interp(lLegAngle,(190, 280), (int(height / 8), int(height / 1.5)))
                rLegbar = np.interp(rLegAngle, (69, 170), (int(height / 8), int(height / 1.5)))

                bar = rLegbar
                # bar = (lLegbar + rLegbar) / 2
                # print(bar)

                # check jumping jacks
                color = (255, 0 ,255)
                if per == 100:
                    color = (0, 255, 0)
                    if dir == 1:
                        count += 0.5
                        dir = 0
                if per == 0:
                    color = (0, 255, 0)
                    if dir == 0:
                        count += 0.5
                        dir = 1
                # if count >= 100 and count < 106:
                #     cv2.putText(img, "stop", (500, 100), cv2.FONT_HERSHEY_COMPLEX, 4, (255, 0, 0), 4)

            #print(count)

            # Bar x+75
            cv2.rectangle(img, (int(width / 1.1), int(height / 8)), (int(width / 1.05), int(height / 1.5)), color, 3)
            cv2.rectangle(img, (int(width / 1.1), int(bar)), (int(width / 1.05), int(height / 1.5)), color, cv2.FILLED)
            # #print(bar)
            cv2.putText(img, f'{int(per)}%', (int(width / 1.1), int(height / 10)), cv2.FONT_HERSHEY_PLAIN, 2, color, 3)

            #cv2.rectangle(img, (0,450), (250, 720), (0, 255, 0), cv2.FILLED)
            #cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)

            cTime = time.time()
            fps = 1/(cTime - pTime)
            pTime = cTime
            cv2.putText(img, str(count), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

            

            # cv2.imshow("Video", img)
            # cv2.waitKey(1)
            result.write(img)

                
        else:
            cap.release()
            result.release()
            # os.system("ffmpeg -i %s - vcodec libx264 %s"%result_filename%result_filename)
            # ffmpeg.input('result/%s'%result_filename).output('result/%s'%result_filename).run()
            cv2.destroyAllWindows()
            total = [result_filename, math.floor(count)]
            return total
            
        