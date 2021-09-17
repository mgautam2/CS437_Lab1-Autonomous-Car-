from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import io
import re
import time

import numpy as np
import picamera
from collections import deque

from PIL import Image
from tflite_runtime.interpreter import Interpreter

import constants as co

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

class Eye:

    def __init__(self, m, map_lock):
        self.map = m
        self.map_lock = map_lock

    def load_labels(self, path):
        """Loads the labels file. Supports files with or without index numbers."""
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            labels = {}
            for row_number, content in enumerate(lines):
                pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
                if len(pair) == 2 and pair[0].strip().isdigit():
                    labels[int(pair[0])] = pair[1].strip()
                else:
                    labels[row_number] = pair[0].strip()
        return labels


    def set_input_tensor(self, interpreter, image):
        """Sets the input tensor."""
        tensor_index = interpreter.get_input_details()[0]['index']
        input_tensor = interpreter.tensor(tensor_index)()[0]
        input_tensor[:, :] = image


    def get_output_tensor(self, interpreter, index):
        """Returns the output tensor at the given index."""
        output_details = interpreter.get_output_details()[index]
        tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
        return tensor


    def detect_objects(self, interpreter, image, threshold):
        """Returns a list of detection results, each a dictionary of object info."""
        self.set_input_tensor(interpreter, image)
        interpreter.invoke()

        # Get all output details
        boxes = self.get_output_tensor(interpreter, 0)
        classes = self.get_output_tensor(interpreter, 1)
        scores = self.get_output_tensor(interpreter, 2)
        count = int(self.get_output_tensor(interpreter, 3))

        results = []
        for i in range(count):
            if scores[i] >= threshold:
                result = {
                    'bounding_box': boxes[i],
                    'class_id': classes[i],
                    'score': scores[i]
                }
                results.append(result)
        return results


    def classify_object_on_map(self, label, x, y):
        if self.map.getLabelAtPoint((x, y)) != co.UNCLASSIFIED_OBJECT:
            return False
        
        queue = deque()
        queue.append((x,y))
        
        while len(queue) > 0:
            a, b = queue.popleft()
            if not self.map.isPointInBounds((a, b)):
                continue
            if self.map.getLabelAtPoint((a, b)) == co.UNCLASSIFIED_OBJECT:
                self.map.setLableAtPoint((a, b), label)

                # Push all adjacent points in queue
                queue.append(a + 1, b)
                queue.append(a + 1, b + 1)
                queue.append(a, b + 1)
                queue.append(a - 1, b + 1)
                queue.append(a - 1, b)
                queue.append(a - 1, b - 1)
                queue.append(a, b - 1)
                queue.append(a + 1, b - 1)
        return True
                   

    def classify_on_map(self, label):
        x, y = self.map.current_position

        if self.map.orientation == co.UP:
            for j in range(max(y - 20, 0), min(y + 20, self.map.width), 1):
                for i in range(x, max(x - 20, 0), -1):
                    if self.classify_object_on_map(label, i, j):
                        break
        
        if self.map.orientation == co.RIGHT:
            for i in range(max(x - 20, 0), min(x + 20, self.map.height), 1):
                for j in range(y, min(y + 20, self.map.width), 1):
                    self.classify_object_on_map(label, i, j)
                    break

        if self.map.orientation == co.DOWN:
            for j in range(max(y - 20, 0), min(y + 20, self.map.width), 1):
                for i in range(x, min(x + 20, self.map.height), 1):
                    self.classify_object_on_map(label, i, j)
                    break
        
        if self.map.orientation == co.LEFT:
            for i in range(max(x- 20, 0), min(x + 20, self.map.height)):
                for j in range(y, max(y - 20, 0), -1):
                    self.classify_object_on_map(label, i, j)
                    break


    def main(self):
        threshhold = 0.6
        labels = self.load_labels("tmp/coco_labels.txt")
        interpreter = Interpreter("tmp/detect.tflite")
        interpreter.allocate_tensors()
        _, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']

        with picamera.PiCamera(resolution=(CAMERA_WIDTH, CAMERA_HEIGHT), framerate=30) as camera:
            camera.start_preview()
            try:
                stream = io.BytesIO()
                for _ in camera.capture_continuous(
                    stream, format='jpeg', use_video_port=True):
                    stream.seek(0)
                    image = Image.open(stream).convert('RGB').resize((input_width, input_height), Image.ANTIALIAS)
                    results = self.detect_objects(interpreter, image, threshhold)

                    for result in results:
                        label = co.LABEL_TO_MAP[int(result['class_id'])]
                        self.classify_on_map(label)

                    stream.seek(0)
                    stream.truncate()

            finally:
                camera.stop_preview()

