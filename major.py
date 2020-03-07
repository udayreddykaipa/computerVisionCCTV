import numpy as np
import cv2
import time
import smtplib

def alertfun():#alert on camera fail or disconnection
    li = ["m.phanisai007@gmail.com", "santhoshyadav09@gmail.com","help.eceprojects@gmail.com"]
    for i in range(len(li)): 
        s = smtplib.SMTP('smtp.gmail.com', 587) 
        s.starttls() 
        s.login("help.eceprojects@gmail.com", "vidyajyothi@03")
        sub="CCTV Alert !"
        msg = "CV Camera disconnected!\n\n\nNOTE: This auto system generated mail on disconnection of computer vision camera"
        message = 'Subject: {}\n\n{}'.format(sub, msg)
        s.sendmail("help.eceprojects@gmail.com", li[i], message)
        s.quit()
        
if __name__=="__main__":
    cap = cv2.VideoCapture(0)
    while(True):
        if(cap.isOpened()==False):
            print("Cam disconnected!")
            #alertfun()#to send mail
        else:
            (grabbed, frame) = cap.read()
            if not grabbed:
                print("no image")
                break
            blur = cv2.GaussianBlur(frame, (21, 21), 0)
            hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
            cv2.imshow("output1", frame)
            lower = [18, 50, 50]
            upper = [35, 255, 255]
            lower = np.array(lower, dtype="uint8")
            upper = np.array(upper, dtype="uint8")
            mask = cv2.inRange(hsv, lower, upper)
            output = cv2.bitwise_and(frame, hsv, mask=mask)
            no_red = cv2.countNonZero(mask)
            cv2.imshow("output",output)
            if int(no_red) > 1000:
                print ('Fire detected')
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
 
cv2.destroyAllWindows()
cap.release()