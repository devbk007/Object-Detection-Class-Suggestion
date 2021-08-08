# Object Prediction & Class Suggestions Quiz Application
A Rest API which provides the total number of objects, actual detected class names and a list of options as a JSON response.

# Detailed Working
User can give an image as input. Model will detect the objects in the image and gives a JSON response. Response includes count of objects in the image, actual detected object names, and 10 object names which includes the actual detected names also. This suggested class names are taken from the COCO dataset. Each time the suggestions will be shuffled.

# Setup
1. Create a virtual environment.
2. Install all the dependencies as described in requirements.txt.  
    pip install -r requirements.txt
4. Run app.py
5. Open Postman and send the request. Response will be obtained as shown below

![output_postman](https://user-images.githubusercontent.com/43404287/128636961-c361ba1c-ca63-47dc-862f-68706921adf9.JPG)


# Acknowledgements
https://github.com/theAIGuysCode/Object-Detection-API
