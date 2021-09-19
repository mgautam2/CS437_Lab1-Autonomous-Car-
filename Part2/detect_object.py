from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import io
import re
import time
import math

import numpy as np
import picamera
from collections import deque

from PIL import Image
from tflite_runtime.interpreter import Interpreter

import picar_4wd as fc
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
        if not self.map.isPointInBounds((x,y)):
            return False
        if self.map.getLabelAtPoint((x, y)) > label:
            return False
        
        queue = deque()
        queue.append((x,y))
        
        while len(queue) > 0:
            a, b = queue.popleft()
            if not self.map.isPointInBounds((a, b)):
                continue
            if self.map.getLabelAtPoint((a, b)) == co.UNCLASSIFIED_OBJECT or (self.map.getLabelAtPoint((a, b)) >= co.WALL and self.map.getLabelAtPoint((a, b)) < label):
                self.map.setLabelAtPoint((a, b), label)

                # Push all adjacent points in queue
                queue.append((a + 1, b))
                queue.append((a + 1, b + 1))
                queue.append((a, b + 1))
                queue.append((a - 1, b + 1))
                queue.append((a - 1, b))
                queue.append((a - 1, b - 1))
                queue.append((a, b - 1))
                queue.append((a + 1, b - 1))
        return True
                   

    def classify_on_map(self, label, angle):
        h, w = self.map.current_position

        for i in range(co.RELTAIVE_MAP_HEIGHT):
            h_idx = round((math.cos(math.radians((angle)))*i))
            w_idx = round((math.sin(math.radians((angle)))*i))

            if self.map.orientation == co.UP:
                self.classify_object_on_map(label, h - h_idx, w + w_idx)
            if self.map.orientation == co.RIGHT:
                self.classify_object_on_map(label, h + w_idx, w + h_idx)
            if self.map.orientation == co.DOWN:
                self.classify_object_on_map(label, h + h_idx, w - w_idx)
            if self.map.orientation == co.LEFT:
                self.classify_object_on_map(label, h - w_idx, w - h_idx)
    
    def calssify_stop_sign_adjacent(self):
        for i in range(self.map.height):
            for j in range(self.map.width):
                if self.map.getLabelAtPoint((i, j)) == co.FREE_SPACE:
                    if self.map.getLabelAtPoint((i + 1, j)) == co.STOP_SIGN or self.map.getLabelAtPoint((i + 1, j - 1)) == co.STOP_SIGN or self.map.getLabelAtPoint((i, j - 1)) == co.STOP_SIGN or self.map.getLabelAtPoint((i - 1, j - 1)) == co.STOP_SIGN or self.map.getLabelAtPoint((i - 1, j)) == co.STOP_SIGN or self.map.getLabelAtPoint((i - 1, j + 1)) == co.STOP_SIGN or self.map.getLabelAtPoint((i, j + 1)) == co.STOP_SIGN or self.map.getLabelAtPoint((i + 1, j + 1)) == co.STOP_SIGN:
                        self.map.setLabelAtPoint((i, j), co.STOP_SIGN_ADJACENT)


    def main(self):
        threshhold = 0.4
        labels = self.load_labels("tmp/coco_labels.txt")
        interpreter = Interpreter("tmp/detect.tflite")
        interpreter.allocate_tensors()
        _, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']

        with picamera.PiCamera(resolution=(CAMERA_WIDTH, CAMERA_HEIGHT), framerate=30) as camera:
            camera.start_preview()
            camera.rotation = 180
            ANGLE_RANGE = 160
            STEP = 10
            us_step = STEP
            current_angle = -80
            max_angle = ANGLE_RANGE/2
            min_angle = -ANGLE_RANGE/2
            fc.get_distance_at(current_angle)

            try:
                stream = io.BytesIO()
                for _ in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
                    stream.seek(0)
                    image = Image.open(stream).convert('RGB').resize((input_width, input_height), Image.ANTIALIAS)
                    results = self.detect_objects(interpreter, image, threshhold)
                    max_label = None
                    for result in results:
                        if max_label == None:
                            max_label = co.LABEL_TO_MAP[int(result['class_id'])]
                        else:
                            max_label = max(max_label, co.LABEL_TO_MAP[int(result['class_id'])])

                    if max_label:
                        self.classify_on_map(max_label, current_angle)
                        self.calssify_stop_sign_adjacent()

                    # Set to new angle
                    current_angle += us_step
                    if current_angle >= max_angle:
                        current_angle = max_angle
                        us_step = -STEP
                    elif current_angle <= min_angle:
                        current_angle = min_angle
                        us_step = STEP
                    fc.get_distance_at(current_angle)

                    stream.seek(0)
                    stream.truncate()

                    if self.map.scanning_map:
                        time.sleep(4)

            finally:
                camera.stop_preview()
