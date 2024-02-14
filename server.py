from flask import Flask, request, send_file
import json
from adafruit_servokit import ServoKit
import os
import cv2


kit = ServoKit(channels=16)

drive_channel = 13
turn_channel = 15

cap = cv2.VideoCapture(0)


app = Flask(__name__)


@app.route('/')
def index():
    return 'ok'


@app.route('/command', methods=['POST'])
def command():
    """
    endpoint for controlling a car
    """
    data = json.loads(request.data)
    kit.continuous_servo[drive_channel].throttle = float(data['speed'])
    kit.servo[turn_channel].angle = float(data['angle'])
    return 'ok'


@app.route('/camera')
def get_image():
    """
    endpoint for getting image from camera
    """
    ret, frame = cap.read()
    cv2.imwrite('test.jpg', frame)
    filename = os.path.abspath('test.jpg')
    return send_file(filename, mimetype='image/jpg')


def main():
    app.run('localhost')
    kit.continuous_servo[drive_channel].throttle = 0


if __name__ == '__main__':
    main()
