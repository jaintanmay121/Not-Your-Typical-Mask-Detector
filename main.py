#Import essential libraries
import argparse
from sql_queries import Database
from CONFIG import *
from utils import get_faces, create
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

parser = argparse.ArgumentParser()
#Get as argument, the mode to run the program in
parser.add_argument('--mode', default='recognize', type=str, choices=['add', 'train', 'recognize'])

if __name__ == '__main__':
    
    args = parser.parse_args()

    if args.mode == 'add':

        #Get details of the user
        name=input("Enter Name of person: ")
        mail=input("Enter e-mail id: ")

        #Connect to the database
        db=Database()

        #Get the `id` of latest entry.
        i=db.show(columns="max(id)", get=True)
        i=str(int(i[0])+1) if i else 0
        #Insert values in database
        db.insert([i, name, mail])
        print("Added to the database")
        db.close()
        #Create the image dataset for that person
        print("Press 'k' to save image")
        create(name, frame_dir)



    elif args.mode == 'train':

        from model import build_model
        from tensorflow.keras.preprocessing.image import ImageDataGenerator

        #Extract faces from the dataset for training
        print("Extracting Faces")
        get_faces(frame_dir, face_dir)
        
        total_train=sum([len(os.listdir(os.sep.join((face_dir, i)))) for i in os.listdir(face_dir)])

        print("Preparing Data")
        image_gen = ImageDataGenerator(
        	rotation_range=30, zoom_range=0.1,
        	width_shift_range=0.2,
        	height_shift_range=0.2, shear_range=0.2, 
            horizontal_flip=True, fill_mode="nearest")

        data_gen = image_gen.flow_from_directory(batch_size=BATCH_SIZE,
                                                             directory=face_dir,
                                                             shuffle=True,
                                                             target_size=(IMG_SHAPE,IMG_SHAPE))

        print("Builing Model")
        model=build_model()

        model.fit(data_gen,
                steps_per_epoch=total_train // BATCH_SIZE,
                epochs=10)

        model.save("models/face_model.h5")
        print("Model saved as models/face_model.h5")
        print(data_gen.class_indices)
    


    elif args.mode == 'recognize':
        
        from recognise import recog
        from datetime import datetime
        #Check whether the person is wearing a mask
        temp=recog()

        date = datetime.now().strftime("%d/%m/%Y %H:%M")
        #If no mask is detected
        if temp:
            person=temp[1]
            db=Database()
            name, mailid = db.show(f'id={person}', "name, mail", get=True)
            db.close()
            print(f"\nIt was {name}\n")
            #Mail the fine to that recognized person
            mail(name, mailid, date)
            
