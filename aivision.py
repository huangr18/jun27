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
    frame_width = 300
    frame_height = 300
    size = (700, 500)
    result_filename = "result_" + filename
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    result = cv2.VideoWriter("static/result/%s" %result_filename, 
                         fourcc,
                         30, size)

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

                per = (upper + lowper) / 2 
                # print(lowAngle, lowper)
                #print(raper)

                upbar = np.interp(upAngle,(30, 300), (100, 400))
                lowbar = np.interp(lowAngle,(340, 350), (100, 400))

                bar = (upbar + lowbar) / 2
                #print(bar)

                # check jumping jacks
                color = (255, 0 ,255)
                if upper and lowper == 100:
                    color = (0, 255, 0)
                    if dir == 0:
                        count += 0.5
                        dir = 1
                if upper and lowper == 0:
                    color = (0, 255, 0)
                    if dir == 1:
                        count += 0.5
                        dir = 0
                if count >= 100 and count < 106:
                    cv2.putText(img, "stop", (500, 100), cv2.FONT_HERSHEY_COMPLEX, 4, (255, 0, 0), 4)

            #print(count)

            # Bar x+75
            cv2.rectangle(img, (600, 100), (650, 400), color, 3)
            cv2.rectangle(img, (600, int(bar)), (650, 400), color, cv2.FILLED)
            #print(bar)
            cv2.putText(img, f'{int(per)}%', (550, 50), cv2.FONT_HERSHEY_PLAIN, 2, color, 3)

            #cv2.rectangle(img, (0,450), (250, 720), (0, 255, 0), cv2.FILLED)
            #cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)

            cTime = time.time()
            fps = 1/(cTime - pTime)
            pTime = cTime
            cv2.putText(img, str(count), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

            

            #cv2.imshow("Image", img)
            #cv2.waitKey(1)
            result.write(img)
             
        else:
            cap.release()
            result.release()
            # os.system("ffmpeg -i %s - vcodec libx264 %s"%result_filename%result_filename)
            # ffmpeg.input('result/%s'%result_filename).output('result/%s'%result_filename).run()
            cv2.destroyAllWindows()
            total = [result_filename, count]

            return total

            
# runcv("v7.mp4")
