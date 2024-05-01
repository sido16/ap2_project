from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from rest_framework import status

from PIL import Image
import io

import tensorflow as tf
from tensorflow.keras import layers
import cv2
import numpy as np

import warnings
warnings.filterwarnings("ignore")


class RootView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, *args, **kwargs):
        return Response({
            'message': 'Root',
        })

class ImageUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        if 'image' not in request.FILES:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        image = request.FILES['image']

        # Save the uploaded image to a temporary location (or any other location you prefer)
        filename = default_storage.save('images/' + image.name, ContentFile(image.read()))

        # You can process the image here if needed, then respond with JSON
        return Response({
            'message': 'Image uploaded successfully',
            'filename': filename,
            'size': image.size,
            'content_type': image.content_type,
        })
    





# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------


class Model_Loader:
    
    def init(self):
        self.model = self.build_model()
    
    def build_model(self):

        model = tf.keras.Sequential()
        model.add(layers.Resizing(150, 150))
        model.add(layers.Rescaling(1/255.0))

        model.add(layers.Flatten())
        model.add(layers.Dense(units=256, activation='relu'))
        model.add(layers.Dropout(0.2))
        model.add(layers.BatchNormalization())

        model.add(layers.Dense(units=11, activation='softmax'))
        
        return model


class ImageClassification(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        if 'image' not in request.FILES:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the uploaded image file
        image_file = request.FILES['image']


        # Read the image data into a format suitable for processing
        image_data = image_file.read()  # Read the image data
        image = Image.open(io.BytesIO(image_data))  # Open it with PIL

        # Convert to RGB (if needed)
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Resize the image
        image = image.resize((150, 150))

        # Convert the image to a NumPy array
        image_array = np.array(image)

        # Normalize the image (assuming model expects this)
        image_normalized = image_array / 255.0

        # Expand dimensions to fit the model input shape
        image_expanded = np.expand_dims(image_normalized, axis=0)





        # Prediction logic
        model = Model_Loader().build_model()
            
        model.load_weights('myapp/models/xception_weights.h5', by_name=True)

        model.compile(
            optimizer='adam', 
            loss='categorical_crossentropy', 
            metrics=['accuracy']
        )

        # Get predictions
        prediction = model.predict(image_expanded)[0]
        max_index = np.argmax(prediction)  # Get the index of the maximum probability
        max_probability = prediction[max_index]
        return Response({
            'message': 'Image uploaded successfully',
            # 'filename': image_file.name,
            # 'filename20':filename,
            # 'size': image_file.size,
            # 'content_type': image_file.content_type,
            'prediction de xception': str(max_probability),
        })