import numpy as np
import cv2
import time
import smtplib

i=0
cap = cv2.VideoCapture(0)

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

if(cap.isOpened()==False):
    print("Cam disconnected!")
    alertfun()#to send mail

while(True):
    ret, frame = cap.read()
    #cv2.imshow('frame',frame)#showing video
    cv2.imwrite('./imgs/camimg'+str(i)+'.jpg',frame)
    i+=1
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    #time.sleep(10)


    
    
