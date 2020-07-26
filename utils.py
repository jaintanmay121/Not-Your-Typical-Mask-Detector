import cv2
import numpy as np
import os
from CONFIG import *


#Function to extract a face from a given frame using FaceNet model
def face(frame):

    prot="models/deploy.prototxt.txt"
    face_model_path="models/res10_300x300_ssd_iter_140000.caffemodel"
    net = cv2.dnn.readNet(prot, face_model_path)

    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0)) 
    #pass the blob through network and obtain detections and predictions
    net.setInput(blob)
    detections = net.forward()
    for i in range(0, detections.shape[2]):
    	confidence = detections[0, 0, i, 2] 
    	if confidence > 0.8:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])

            return box



#Function to get extract faces from images in a directory and save them
def get_faces(input_dir, output_dir):
    
    from imutils import paths

    if output_dir not in os.listdir():
        os.makedirs(output_dir)

    imagePaths = list(paths.list_images(input_dir))
    
    count=0

    for (i, imagePath) in enumerate(imagePaths):

        name = imagePath.split('/')[-2]
        if len(os.listdir(input_dir+'/'+name)) != len(os.listdir(output_dir+'/'+name)):
            name_dir=os.sep.join((output_dir, name))
            try:
                os.makedirs(name_dir)
            except:
                pass

            image = cv2.imread(imagePath)

            try:
                box=face(image)
                (startX, startY, endX, endY) = box.astype("int")
                face_im = image[startY:startY+endY, startX:startX+endX]
                
                cv2.imwrite(f"{name_dir}/{i}.jpeg", face_im)
            except:
                count+=1
                print(f"No face {imagePath}")

    if count:
        print(f"Couldn't find face for {count} images")



#Create a dataset for a new entry in face recognition
def create(person, out_dir=frame_dir):

    from imutils.video import VideoStream
    import imutils
    import time

    cascPath = "models/haarcascade_frontalface_default.xml"

    detector = cv2.CascadeClassifier(cascPath)


    if out_dir not in os.listdir():
    	os.makedirs(out_dir)

    if person not in os.listdir(f'{out_dir}'):
    	os.makedirs(f"{out_dir}/{person}")  

    print("Starting video stream")
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    total = 0

    while True:
    
    	frame = vs.read()
    	orig = frame.copy()
    	frame = imutils.resize(frame, width=400)    
    	rects = detector.detectMultiScale(
    		cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor=1.1, 
    		minNeighbors=5, minSize=(30, 30))   

    	for (x, y, w, h) in rects:
    		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    		cv2.imshow("Frame", frame)
    	key = cv2.waitKey(1) & 0xFF

    	if key == ord("k"):
    		p = os.path.sep.join([out_dir, person, "{}.png".format(
    			str(total).zfill(3))])
    		cv2.imwrite(p, orig)
    		total += 1  
    	elif key == ord("q"):
    		break

    print("{} face images stored".format(total))
    cv2.destroyAllWindows()
    vs.stop()



#Send a fine to the recognized person's mail
def mail(name, mailid, time):

    import smtplib 
    from CONFIG import MY_ADDRESS, PASSWORD

    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls() 
    s.login(MY_ADDRESS, PASSWORD) 
    message = f"""Dear citizen,
You({name}) were recently(at {time}) noticed not wearing a face mask at a public place.
Due to this, you are asked to pay a fine of ₹500. 
This amount can be paid using bank transfer at A/C number 'XXXXXXXXXXX' or by visiting the challan office.
You are to pay this amount within 10 days of receiving this mail.

Thank You.
    """

    message=message.encode("utf-8")
    s.sendmail(MY_ADDRESS, f"{mailid}", message) 
    s.quit()
    print(f"Fine sent to {mailid}")