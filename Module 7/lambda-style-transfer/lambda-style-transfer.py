import sys
sys.path.append("./packages")
import os
import numpy as np
from PIL import Image
import onnxruntime as rt
import boto3


# Download original.jpg from S3, stylize it, and upload stylized.jpg to S3.
def lambda_handler(event, context):    
    s3BucketName = None # TODO
    modelFileName = "stylizeModel.onnx"
    originalImageFileName = "original.jpg"
    stylizedImageFileName = "stylized.jpg"
    lambdaDirectory = "/tmp"

    modelLambdaLocation = os.path.join(lambdaDirectory, modelFileName)
    originalImageLambdaLocation = os.path.join(lambdaDirectory, originalImageFileName)
    stylizedImageLambdaLocation = os.path.join(lambdaDirectory, stylizedImageFileName)

    # Downloading the onnx model and original.jpg.
    s3Client = boto3.client('s3')
    s3Client.download_file(s3BucketName, modelFileName, modelLambdaLocation)
    s3Client.download_file(s3BucketName, originalImageFileName, originalImageLambdaLocation)

    # Load and preprocess the image.
    image = Image.open(originalImageLambdaLocation)
    image = image.resize((int(224), int(224)), Image.ANTIALIAS)
    x = np.array(image).astype('float32')
    x = np.transpose(x, [2, 0, 1])
    x = np.expand_dims(x, axis=0)

    # Stylize image.
    sess = rt.InferenceSession(modelLambdaLocation)
    input_name = sess.get_inputs()[0].name
    pred_onx = sess.run(None, {input_name: x})[0]

    # Postprocess image.
    stylizedResult = np.clip(pred_onx[0], 0, 255)
    stylizedResult = stylizedResult.transpose(1,2,0).astype("uint8")

    # Save and upload stylized image.
    stylizedImage = Image.fromarray(stylizedResult)
    stylizedImage.save(stylizedImageLambdaLocation)
    s3Client.upload_file(Filename=stylizedImageLambdaLocation, Bucket=s3BucketName, Key=stylizedImageFileName)

    # Remove files from tmp and S3.
    os.remove(modelLambdaLocation)
    os.remove(originalImageLambdaLocation)
    os.remove(stylizedImageLambdaLocation)
    s3Client.delete_object(Bucket=s3BucketName, Key=originalImageFileName)

# Remove comment for running locally.
# lambda_handler(None, None)