# EECS 605 Module 7

## Overview
We will be creating and deploying a React app to Heroku that can do handwritten-digit recognition via the handwritten-digit API that we created in Module 6.

## Objectives
1. Refactor a React app template to utilize the handwritten-digit API.
2. Deploy the React app to Heroku.

## Step 1: React app preparation.
0. Create a public GitHub repository dedicated storing the React app components. (If you do not have a GitHub account, create one https://docs.github.com/en/get-started/signing-up-for-github/signing-up-for-a-new-github-account)
1. Move 

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
