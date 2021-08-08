import time
import random

from numpy.lib.arraysetops import _unique_dispatcher
from absl import app, logging
import cv2
import numpy as np
import tensorflow as tf
from yolov3_tf2.models import (
    YoloV3, YoloV3Tiny
)
from yolov3_tf2.dataset import transform_images, load_tfrecord_dataset
from yolov3_tf2.utils import draw_outputs
from flask import Flask, request, Response, jsonify, send_from_directory, abort
import os

# customize your API through the following parameters
classes_path = './data/labels/coco.names'
weights_path = './weights/yolov3-tiny.tf'
tiny = True                    # set to True if using a Yolov3 Tiny model
size = 416                      # size images are resized to for model

num_classes = 80                # number of classes in model

# load in weights and classes
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

if tiny:
    yolo = YoloV3Tiny(classes=num_classes)
else:
    yolo = YoloV3(classes=num_classes)

yolo.load_weights(weights_path).expect_partial()
print('weights loaded')

class_names = [c.strip() for c in open(classes_path).readlines()]
print('classes loaded')

# Initialize Flask application
app = Flask(__name__)


# API that returns JSON with classes found in image
@app.route('/image', methods=['POST'])
def get_image():
    image = request.files["images"]
    image_name = image.filename
    image.save(os.path.join(os.getcwd(), image_name))
    img_raw = tf.image.decode_image(
        open(image_name, 'rb').read(), channels=3)
    img = tf.expand_dims(img_raw, 0)
    img = transform_images(img, size)

    boxes, scores, classes, nums = yolo(img)

    names = []
    response = []

    for i in range(nums[0]):
        names.append(class_names[int(classes[0][i])])

    # UNIQUE DETECTIONS
    unique_list = []
    for x in names:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)

    unique_list_len = len(unique_list)

    print("Detected names are :", unique_list)

    class_options = []

    # MAKING 10 SUGGESTED CLASS NAMES INCLUDING ORIGINAL DETECTED CLASSES
    for i in range(10-unique_list_len):
        # check if exists in unique_list or not
        x = random.choice(class_names)
        if x not in unique_list and (unique_list_len + len(class_options) < 10):
            class_options.append(x)
    for y in unique_list:
        class_options.append(y)

    # SHUFFLING SUGGESTIONS
    random.shuffle(class_options)

    # APPENDING LENGTH OF DETECTED CLASSES, ACTUAL DETECTIONS AND SUGGESTIONS
    response.append({
        "object count": unique_list_len,
        "detections": unique_list,
        "options": class_options
    })

    try:
        return jsonify({"response": response}), 200
    except FileNotFoundError:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True)
