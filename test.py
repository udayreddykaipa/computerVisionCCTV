import cv2
import numpy as np
# nom = 0
# l=0
# k=0
fr=cv2.imread(r'/home/pi/Desktop/Cam/0.jpg')
# print(fr[l,k,0])
# print(fr[l,k])
# print(fr[l,k,1])
# print(fr[l,k,2])
#f=open(r"ntresult.txt","a")
#for nom in range (0,37):
#    fr=cv2.imread(r'/home/pi/Desktop/Cam/'+str(nom)+'.jpg')
i=fr.shape[1]
j=fr.shape[0]
count=0
for k in range(0,i-1):
    for l in range(0,j-1):
        fr[l,k,0]=0
        fr[l,k,1]=0
        fr[l,k,2]=255
print(fr[l,k])
cv2.imshow('frame',fr)
cv2.waitKey()
#            if fr[l,k,0] > fr[l,k,1] and fr[l,k,1] > fr[l,k,2]:
#                count=count+1;   
#    f.write(str(count)+':'+str(nom)+"\n")
#    print(nom)
#f.close()