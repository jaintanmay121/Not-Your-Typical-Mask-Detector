print("Loading Libraries...")
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow.keras.models import load_model
import time
import cv2
import numpy as np
from utils import face
from CONFIG import IMG_SHAPE

#Loading trained MobileNet models
print("Loading Models")
mask_model = load_model("models/mask_model.h5")
face_img_recog_model = load_model("models/face_model.h5")

print("Starting Camera...")
vs = cv2.VideoCapture(0)
time.sleep(1.0)

mask_labels = {'0': 'Not Masked', '1': 'Masked'}

masked = []
unmasked_faces = []


def recog():
    while True:
        _,	frame = vs.read()
        frame = cv2.flip(frame, 1)
        box=face(frame)
        try:
            (startX, startY, endX, endY) = box.astype("int")
            #Preparing the frame for prediction
            face_img = frame[startY:startY+endY, startX:startX+endX]
            face_img = cv2.resize(face_img, (IMG_SHAPE, IMG_SHAPE))
            face_img = np.expand_dims(face_img, axis=0)
            #Check for mask
            prediction = mask_model.predict(face_img, batch_size=32)
            mask, withoutMask = prediction[0]
            
            if mask > withoutMask:
                label = '1'
            else:
                label = '0'
                unmasked_faces.append(face_img)

            masked.append(label)
            color = (0, 255, 0) if label == "1" else (0, 0, 255)
            cv2.putText(frame, mask_labels[label], (startX, startY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

        except:
            pass

        cv2.imshow("Image", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vs.release()
    cv2.destroyAllWindows()

    #Find whether the person was wearing a mask
    mask = max(set(masked), key=masked.count)
    print(f"\nThe person was {mask_labels[mask]}")

    #If Unmasked
    if mask == "0":
        names = []
        #Identify the person in all the frames
        for face_img in unmasked_faces:
            name = np.argmax(face_img_recog_model.predict(face_img))
            names.append(name)

        person = max(set(names), key=names.count)

        return mask, person