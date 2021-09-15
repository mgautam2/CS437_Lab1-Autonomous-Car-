from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import io
import re
import time

from annotation import Annotator

import numpy as np
import picamera

from PIL import Image
from tflite_runtime.interpreter import Interpreter

import map as mp
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


    def annotate_objects(self, annotator, results, labels):
        """Draws the bounding box and label for each object in the results."""
        for obj in results:
            # Convert the bounding box figures from relative coordinates
            # to absolute coordinates based on the original resolution
            ymin, xmin, ymax, xmax = obj['bounding_box']
            xmin = int(xmin * CAMERA_WIDTH)
            xmax = int(xmax * CAMERA_WIDTH)
            ymin = int(ymin * CAMERA_HEIGHT)
            ymax = int(ymax * CAMERA_HEIGHT)

            # Overlay the box, label, and score on the camera preview
            annotator.bounding_box([xmin, ymin, xmax, ymax])
            annotator.text([xmin, ymin], '%s\n%.2f' % (labels[obj['class_id']], obj['score']))

    def classify_on_map(self, label, start_index):
        current_position = self.map.current_position
        current_orientation = self.map.orientation

    def main(self):
        threshhold = 0.6
        labels = self.load_labels("tmp/coco_labels.txt")
        interpreter = Interpreter("tmp/detect.tflite")
        interpreter.allocate_tensors()
        _, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']

        with picamera.PiCamera(
            resolution=(CAMERA_WIDTH, CAMERA_HEIGHT), framerate=30) as camera:
            camera.start_preview()
            try:
                stream = io.BytesIO()
                annotator = Annotator(camera)
                for _ in camera.capture_continuous(
                    stream, format='jpeg', use_video_port=True):
                    stream.seek(0)
                    image = Image.open(stream).convert('RGB').resize((input_width, input_height), Image.ANTIALIAS)
                    start_time = time.monotonic()
                    results = self.detect_objects(interpreter, image, threshhold)
                    elapsed_ms = (time.monotonic() - start_time) * 1000

                    annotator.clear()
                    self.annotate_objects(annotator, results, labels)
                    annotator.text([5, 0], '%.1fms' % (elapsed_ms))
                    annotator.update()

                    start_index = 0
                    for result in results:
                        map_number = co.LABEL_TO_MAP[int(result['class_id'])]
                        self.classify_on_map(map_number, start)

                    stream.seek(0)
                    stream.truncate()

            finally:
                camera.stop_preview()
