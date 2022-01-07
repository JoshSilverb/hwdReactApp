import os
import time
import cv2
import boto3

# Check S3 to see if the file has been created.
# If the file is detected, download, remove it from s3, and show it locally.

s3BucketName = None # TODO
stylizedImageFileName = "stylized.jpg"
accessKeyID = os.environ["AWS_ACCESS_KEY_ID"]
secretAccessKey = os.environ["AWS_SECRET_ACCESS_KEY"]

s3Client = boto3.client(
    's3',
    aws_access_key_id=accessKeyID,
    aws_secret_access_key=secretAccessKey
)

while(True):
    try:
        s3Client.download_file(s3BucketName, stylizedImageFileName, stylizedImageFileName)
        s3Client.delete_object(Bucket=s3BucketName, Key=stylizedImageFileName)
        stylizedImage = cv2.imread(stylizedImageFileName)
        cv2.imshow('s3 image', stylizedImage)
    except Exception as e:
	print(e)
	time.sleep(3)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
