# EECS 605 Module 7

## Overview
Learn to create a pipeline that utilizes both an edge-device (DeepLens) and a cloud (AWS) - use Amazon DeepLens device with AWS to create an auto-selfie-capture-and-stylizer.

![alt text](./instructions-image-assets/selfie-capture-and-stylizer-demo.png)

## Objectives
1. Create an AWS pipeline that can automatically stylize (style-transfer) a .jpg image when it is uploaded to S3 bucket - very similar to Module 1.
2. Create a custom DeepLens project that automatically takes a video frame (.jpg) and uploads to S3 when a "smile" or "happiness" is detected in the video frame.
3. Deploy the DeepLens project to DeepLens.
4. Test the pipeline by running the s3-image-viewer-client script on your local computer - you could just go to the S3 bucket and download the stylized image and see it, but... that's no fun :P

![alt text](./instructions-image-assets/module-7-overview.jpg)

## 1. Create an AWS pipeline - automatically stylizes .jpg image when it is uploaded to S3
* Use the diagram to create the pipeline - it is very similar to Module 1.
* All of the necessary files and packages for Lambda are provided in the `/lambda-style-transfer`.
* Make sure to fill in the **TODOs** in the `lambda-style-transfer.py` before deploying it.
* Model we are using: https://github.com/onnx/models/tree/master/vision/style_transfer/fast_neural_style
* Use Python 3.6 for this.

## 2. Create a custom DeepLens project - uploads a video frame (.jpg) when a "smile"/"happiness" is detected in the video frame
* Steps for creating a custom DeepLens project is the same as the Module 6.
* All of the necessary files and packages for DeepLens project are provided in the `/emotion-detection`.
* Make sure to fill in the **TODOs** in the `emotion-detector.py` before deploying it.
* Model we are using: https://github.com/onnx/models/tree/master/vision/body_analysis/emotion_ferplus
* [NOTE]: You will notice that we are putting AWS credentials directly in the script - this is not the ideal way of doing it, but this is the easiest way to give the DeepLens the permission to access S3 without using IAM in AWS.

## 3. Install additional packages to DeepLens via SSH
* Additional packages: `PIL` and `Cropper`
  - Image: `sudo pip3.7 install pillow`
    - Used for processing video frames and saving new images as .jpg.
  - Cropper `sudo pip3.7 install autocrop`
    - Used to automatically detect faces and crop faces only. This is a necessary preprocessing step before predicting which emotion the face us expressing.

## 4. Use the s3-image-viewer-client script to automatically view the stylized.jpg in the S3 bucket
* There is nothing for you to do with this script - just fill in a **TODO** and you just have to run it on your local machine :)
* If you want to stop running the client script, press `q`.

## Notes
* To take a look at the logs of the DeepLens, use the Lambda logs, which can be found in the DeepLens console towards the bottom.
* In an ideal situation, we should be fully utilizing the hardware-acceleration capabilities of the DeepLens device to do machine-learning model inference. Unfortunately, DeepLens' hardware-acceleration library does not support ONNX models, so we are using normal CPU to do inference using `onnxruntime` package.
