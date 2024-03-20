# vms
Vehicle Management System (React, AWS, IoT)

This repository holds all the work done towards Cloud Communcations for Autonomous Vehicles Project. 

The UI System is built with React using aws-amplify, aws-sdk. 
Setup Instructions:
1. Create an aws-exports.js file in src directory with credentials and configurations from Location Services, Identitiy Pool and App Sync.
2. npm install
3. npm start (run locally on port 8080)

The IoT side of the system is mainly  writted in python and each file typically represent a consumer application for ROS publisher topics. 
Setup Instructions:
1. Install AWS IoT SDK for python from here: https://github.com/aws/aws-iot-device-sdk-python-v2
2. Run required python files. 
