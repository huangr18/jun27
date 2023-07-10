import cv2
import numpy as np
import time
import PoseModule as pm
from flask import render_template
import os
import ffmpeg

# run on camera
#cap = cv2.VideoCapture(0)
#vedio demo
def runcv(filename):
    cap = cv2.VideoCapture(("static/files/%s"%filename))
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
    fps = cap.get(cv2.CAP_PROP_FPS)
    result_filename = "result_" + filename
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    result = cv2.VideoWriter("static/result/%s" %result_filename, 
                         fourcc,
                         fps, size)

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
                upAngle = detector.findAngle(img, 16, 0, 15, False)
                lowAngle = detector.findAngle(img, 28, 24, 27, False)

                upper = np.interp(upAngle,(30, 300), (100, 0))
                lowper = np.interp(lowAngle,(340, 350), (100, 0)) 
                per = lowper
                per = (upper + lowper) / 2 
                # print(lowAngle, lowper)
                print(per)

                upbar = np.interp(upAngle,(30, 300), (int(height / 8), int(height / 1.5)))
                lowbar = np.interp(lowAngle,(340, 350), (int(height / 8), int(height / 1.5)))
                # bar = lowbar
                bar = (upbar + lowbar) / 2
                #print(bar)

                # check jumping jacks
                color = (255, 0 ,255)
                if per == 100:
                    color = (0, 255, 0)
                    if dir == 0:
                        count += 0.5
                        dir = 1
                if per == 0:
                    color = (0, 255, 0)
                    if dir == 1:
                        count += 0.5
                        dir = 0
                if count >= 100 and count < 106:
                    cv2.putText(img, "stop", (500, 100), cv2.FONT_HERSHEY_COMPLEX, 4, (255, 0, 0), 4)

            #print(count)

            # Bar x+75
            cv2.rectangle(img, (int(width / 1.1), int(height / 8)), (int(width / 1.05), int(height / 1.5)), color, 3)
            cv2.rectangle(img, (int(width / 1.1), int(bar)), (int(width / 1.05), int(height / 1.5)), color, cv2.FILLED)
            #print(bar)
            cv2.putText(img, f'{int(per)}%', (int(width / 1.1), int(height / 10)), cv2.FONT_HERSHEY_PLAIN, 2, color, 3)


            #cv2.rectangle(img, (0,450), (250, 720), (0, 255, 0), cv2.FILLED)
            #cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)

            cTime = time.time()
            fps = 1/(cTime - pTime)
            pTime = cTime
            cv2.putText(img, str(count), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

            

            cv2.imshow("Image", img)
            cv2.waitKey(1)
            result.write(img)
             
        else:
            cap.release()
            result.release()
            # os.system("ffmpeg -i %s - vcodec libx264 %s"%result_filename%result_filename)
            # ffmpeg.input('result/%s'%result_filename).output('result/%s'%result_filename).run()
            cv2.destroyAllWindows()
            total = [result_filename, count]

            return total

            
runcv("v7.mp4")
