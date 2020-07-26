from CONFIG import *
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
from tensorflow.keras.layers import Dense, Input, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

input_shape=(IMG_SHAPE, IMG_SHAPE, 3)

def build_model():
    input_tensor = Input(shape=input_shape)
    base_model = MobileNetV2(
        include_top=False,
        weights='imagenet',
        input_tensor=input_tensor,
        input_shape=input_shape,
        pooling='avg')

    for layer in base_model.layers:
        layer.trainable = True  
        
    op = Dense(256, activation='relu')(base_model.output)
    op = Dropout(0.4)(op)
    
    output_tensor = Dense(2, activation='softmax')(op)

    model = Model(inputs=input_tensor, outputs=output_tensor)
    
    model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['categorical_accuracy'])

    return model