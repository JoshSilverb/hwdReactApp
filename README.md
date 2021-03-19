# EECS 605 Modules

# Overview
1. Setup a simple AWS Pipeline: Familiarizing Lambda and S3 (Module 1.0)
2. Create role-specific credentials for AWS (Module 1.1)

3. Create client-side UI using Jupyter and AWS to do handwriting recognition (Module 2.0)
4. Modularize previous dashboard to only show the UI elements to the user (Module 2.1)

5. Setup Docker and Heroku (Machine dependent) and create a Docker image of the modularized Jupyter dashboard and deploy it to Heroku (Module 3)

6. Create a pipeline consisted of master, preprocessor, frame_classifier, and post-processor (Module 4)

7. Stress-test and observe how it behaves as the size (number of video frames) of input-data increases. Based on what is observed, improve the performance of the pipeline by offloading parts of the pipeline to ECS (Module 5)

8. Use Amazon DeepLens device to do on-device handwriting recognition (Module 6)

9. Use Amazon DeepLens device with AWS to create an auto-selfie-capture-and-stylizer (Module 7)

# Installations and Requirements
* Linux bash shell (if on windows): https://eecs280staff.github.io/p1-stats/setup.html#windows
* Use Python 3.7
* Take a look at the module spec to see which additional libraries to install.
