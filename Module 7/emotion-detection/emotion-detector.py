import os
import json
import time
import numpy as np
import awscam
import cv2
import mo
import greengrasssdk
from utils import LocalDisplay

import sys
import onnxruntime as rt

from PIL import Image, ImageEnhance
from autocrop import Cropper
import boto3

np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)

def softmax(x):
    # your softmax function
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

def preprocess(image):
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    input_shape = (1, 1, 64, 64)
    img = Image.fromarray(grayImage)
    img = img.resize((64, 64), Image.ANTIALIAS)
    img_data = np.array(img, dtype=np.float32)
    img_data = np.resize(img_data, input_shape)
    return img_data

def postprocess(scores):
    prob = softmax(scores)
    prob = np.squeeze(prob)
    classes = np.argsort(prob)[::-1]
    return classes

def isSmiling(sess, image):
    x = np.array(image)
    input_name = sess.get_inputs()[0].name
    pred_onx = sess.run([], {input_name: x})[0]
    results = postprocess(pred_onx)
    print(results)
    # 1 == happiness.
    if results[0] == 1:
        return True
    return False

def lambda_handler(event, context):
    """Empty entry point to the Lambda function invoked from the edge."""
    return

# Create an IoT client for sending to messages to the cloud.
client = greengrasssdk.client('iot-data')
iot_topic = '$aws/things/{}/infer'.format(os.environ["AWS_IOT_THING_NAME"])

def infinite_infer_run():
    """ Run the DeepLens inference loop frame by frame"""
    try:
        model_directory = "/opt/awscam/artifacts/"
        model_name = "emotionDetection.onnx"

        s3BucketName = None # TODO
        frameImageFileName = "original.jpg"
        deepLensTempDirectory = "/tmp"
        frameImageDeepLensLocation = os.path.join(deepLensTempDirectory, frameImageFileName)

        s3Client = boto3.client(
            's3',
            aws_access_key_id=None, # TODO
            aws_secret_access_key=None # TODO
        )

        local_display = LocalDisplay('480p')
        local_display.start()

        model_file_path = os.path.join(model_directory, model_name)
        sess = rt.InferenceSession(model_file_path)
        
        cropper = Cropper(face_percent=65)
        
        while True:
            ret, frame = awscam.getLastFrame()
            if not ret:
                raise Exception('Failed to get frame from the stream')
                
            try:
                # Lowering the brightness of the input image from DeepLens.
                # When it's too bright, emotion-detection ONNX and face-cropper don't perform very well.
                # Documentation: https://pythonexamples.org/python-pillow-adjust-image-brightness/
                frame = Image.fromarray(frame)
                enhancer = ImageEnhance.Brightness(frame)
                frame = enhancer.enhance(None) # TODO
                frame = np.array(frame)
                
                # Face cropping.
                croppedImage = cropper.crop(frame)
                preprocessedImage = preprocess(croppedImage)
                
                # Checking to see if the person in the video frame is "smiling"/"happy".
                # If "smiling"/"happy" emotion is detected, upload the current video frame to S3 and
                # show the cropped face to the project stream in the DeepLens console.
                if isSmiling(sess, preprocessedImage):
                    frameImage = Image.fromarray(frame)
                    frameImage.save(frameImageDeepLensLocation)
                    s3Client.upload_file(Filename=frameImageDeepLensLocation, Bucket=s3BucketName, Key=frameImageFileName)
                    os.remove(frameImageDeepLensLocation)
                    local_display.set_frame_data(croppedImage)
                    time.sleep(5)
            except Exception as e:
                print(e)

    except Exception as ex:
        print('Error in lambda {}'.format(ex))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("error details:" + str(exc_type) + str(fname) + str(exc_tb.tb_lineno))

infinite_infer_run()
