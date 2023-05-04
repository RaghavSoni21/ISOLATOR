import cv2
import imutils
from scipy.spatial import distance as dist
import pygame as pg
from pygame import mixer

# Initializing the HOG person
# detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
cap = cv2.VideoCapture("vid4.mp4")#input of the program


#initilise / start mixer
mixer.init()

#load the file
mixer.music.load("Move Away.mp3")

#set volume
mixer.music.set_volume(21.0)

flag=0

while cap.isOpened():
	# Reading the video stream
	ret, image = cap.read()
	
	
	if ret:
		image = imutils.resize(image,width=min(400, image.shape[1]))

		# Detecting all the regions
		# in the Image that has a
		# pedestrians inside it


		(regions, _) = hog.detectMultiScale(image,winStride=(4, 4),padding=(4, 4),scale=1.05)
		#print(regions)
		# [[ 76   0 100 197]
 		# [169  13  95 190]]


		stack_x=[]
		stack_y=[]
		stack_x_print=[]
		stack_y_print=[]
		D_mid_x=[]	
		D_mid_y=[]
		global D
		# Drawing the regions in the
		# Image
		if(len(regions)==0): #len(regions)=no. of people detected
			pass
		else:
			for i in range (0,len(regions)):
				x1 = regions[i][0]
				y1 = regions[i][1]
				x2 = regions[i][0] + regions[i][2]
				y2 = regions[i][1] + regions[i][3]

				#centroid of the rectangle
				mid_x = int((x1+x2)/2)
				mid_y = int((y1+y2)/2)
				
				stack_x.append(mid_x)
				stack_y.append(mid_y)
				stack_x_print.append(mid_x)
				stack_y_print.append(mid_y)
				D_mid_x.append(mid_x)
				D_mid_y.append(mid_y)

				image = cv2.circle(image, (mid_x, mid_y), 3 , [255,0,0] , -1)
				image = cv2.rectangle(image , (x1, y1) , (x2,y2) , [0,255,0] , 2)
				
			if(len(regions)==2):

				#D is the distance between 2 people
				D = int(dist.euclidean((stack_x.pop(), stack_y.pop()), (stack_x.pop(), stack_y.pop())))

				d=str(D)
				
				image = cv2.line(image, (stack_x_print.pop(), stack_y_print.pop()), (stack_x_print.pop(), stack_y_print.pop()), [0,0,255], 2)
				d_mid_x=int(((D_mid_x.pop()+D_mid_x.pop())/2)-22)
				d_mid_y=int(((D_mid_y.pop()+D_mid_y.pop())/2)-10)
				image=cv2.putText(image,d,(d_mid_x,d_mid_y),cv2.FONT_HERSHEY_SIMPLEX,0.6,[255,0,0],2)
			else:
				D=0

			

			#checking the social-distancing condition
			if(D<75 and D!=0):
				image=cv2.putText(image,"!!MOVE AWAY!!",(100,50),cv2.FONT_HERSHEY_SIMPLEX,1,[0,0,255],4)
				if(flag==0):
					mixer.music.play()
					#start playing audio
					flag+=1

			else:
				flag=0

		# Showing the output Image
			cv2.imshow("Isolator", image)
			if cv2.waitKey(25) & 0xFF == ord('q'):
				break
	else:
		break
	

cap.release()
cv2.destroyAllWindows()
