#import function is used to include libraries,
#before interpreting starts
import numpy as np
import cv2
import time
import smtplib
import firebase_admin # sudo pip install firebase-admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import auth
#from threading import *
import threading
from datetime import datetime
global UID
cred = credentials.Certificate('cv-cam-firebase-adminsdk-o6qvt-d5c758eb05.json')
firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://cv-cam.firebaseio.com'
        })

def setup():
    fi = open("config.json", "w+")
    print("Entering configuration menu:")
    Email=str(input("Enter Email name :"))
    pwd=str(input("Enter Password :"))
    fi.writelines(Email)     
    fi.close()
    try:
        user=firebase_admin.auth.create_user(email=Email,password=pwd)
    except:
        print("Failed create an user, Enter valid details or user exist ")
        checkSetup()
        return 

    global UID
    UID=user.uid
    ref = db.reference('devices/'+UID)  #+'/value')#.value()
    ref.child("connecion").set('0')
    ref.child("fire").set("0")
    ref.child("lastTS").set(datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"))
    ref.child("deviceNumber").set('')
    ref.child("fire time").set('')
    return

def checkSetup():
    
    try:
        fi = open("config.json", "r")
        Email=fi.readline()
        print("User Exisits : "+Email)
        fi.close()
        print("would like enter setup (y/N)")
        
        x=str(input())
        if (x=='y' or x=='Y'):
            setup()
                
    except:
        print("erroe")
        setup()

    return 
      

def alertfun(msg):#alert on camera fail or disconnection
    li = ["m.phanisai007@gmail.com",
          "santhoshyadav09@gmail.com",
          "help.eceprojects@gmail.com"]
    #li is list of mail Id that gets alerts
    
    for i in range(len(li)): # iterate through all mail Ids
        s = smtplib.SMTP('smtp.gmail.com', 587) 
        s.starttls() 
        s.login("help.eceprojects@gmail.com", "vidyajyothi@03")
        #logins to a mailId (admin) to send mail
        
        sub="CCTV Alert !" #subject
        message = 'Subject: {}\n\n{}'.format(sub, msg)
        print(message)
        s.sendmail("help.eceprojects@gmail.com", li[i], message)
        s.quit()

def camConnCheck():
    flag=1
    # cap = cv2.VideoCapture(1)
    # if(cap.isOpened()==False):
    #     flag=0
    # else:
    #     flag=1
    #cap.release()
    global UID
    ref = db.reference('devices/'+UID)  #+'/value')#.value()
    ref.child("connecion").set(flag)
    time.sleep(10)
    camConnCheck()

def UploadImg():
    print("uploaded")
    time.sleep(120)
    UploadImg()

def fireCheck():
    global UID
    ref = db.reference('devices/'+UID)  #+'/value')#.value()
    ref.child("fire").set("0")
    
    ref = db.reference('devices/'+UID)  #+'/value')#.value()
    ref.child("fireTS").set("Not Applicable")
    #algo

    #on fire detect update fireTS and fire
    
    fireCheck()

def LatestTS():
    global UID
    ref = db.reference('devices/'+UID)  #+'/value')#.value()
    ref.child("lastTS").set(str(datetime.now()))
    time.sleep(10)
    time.sleep(10)
    LatestTS()

def algo():
    cap = cv2.VideoCapture(0)
    if(cap.isOpened()==False):
        return
    else:
        (grabbed, frame) = cap.read()
        if not grabbed:
            print("no image")
            return
        blur = cv2.GaussianBlur(frame, (21, 21), 0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
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
            
            msg = "FIRE DETECTED by CV Camera !\n\n\nNOTE: This auto system generated mail on disconnection of computer vision camera";
            alertfun(msg)# send mail
            return 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return 
 
    cv2.destroyAllWindows()
    cap.release()
if __name__=="__main__":
    checkSetup()
    fi = open("config.json", "r")
    Email=fi.readline()
    fi.close()
    
    global UID
    UID=firebase_admin.auth.get_user_by_email(Email).uid
    t1=threading.Thread(target=camConnCheck)
    ts=[t1]
    t2=threading.Thread(target=UploadImg)
    ts=[t2]
    t3=threading.Thread(target=fireCheck)
    ts=[t3]
    t4=threading.Thread(target=LatestTS)
    ts=[t4]
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    for i in ts:
        i.join()
    
    #use multi threading and create a thread to show active status in firebase and other to check fire and update in DB


#execution starts from here
# if __name__=="__main__":
#     checkSetup()
#     flag=0;
#     cap = cv2.VideoCapture(1)
#     while(flag==0):
#         if(cap.isOpened()==False):
#             print("Cam disconnected!")
#             flag=1
#             msg = "CV Camera disconnected!\n\n\nNOTE: This auto system generated mail on "+
#             "disconnection of computer vision camera";
#             alertfun(msg)#to send mail
#         else:
#             (grabbed, frame) = cap.read()
#             if not grabbed:
#                 print("no image")
#                 break
#             blur = cv2.GaussianBlur(frame, (21, 21), 0)
#             hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
#             cv2.imshow("output1", frame)
#             lower = [18, 50, 50]
#             upper = [35, 255, 255]
#             lower = np.array(lower, dtype="uint8")
#             upper = np.array(upper, dtype="uint8")
#             mask = cv2.inRange(hsv, lower, upper)
#             output = cv2.bitwise_and(frame, hsv, mask=mask)
#             no_red = cv2.countNonZero(mask)
#             cv2.imshow("output",output)
#             if int(no_red) > 1000:
#                 print ('Fire detected')
                
#                 flag=1
#                 msg = "FIRE DETECTED by CV Camera !\n\n\nNOTE: "
#                 "This auto system generated mail on disconnection of computer vision camera";
#                 alertfun(msg)# send mail
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
 
# cv2.destroyAllWindows()
# cap.release()
