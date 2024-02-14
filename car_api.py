import shutil
import cv2
import requests


BASE = 'https://14ce-194-95-60-241.ngrok-free.app'  # car IP


def turn(angle):
    requests.post(
        BASE + '/command',
        json={
            'angle': angle
        }
    )


def change_speed(speed):
    requests.post(
        BASE + '/command',
        json={
            'speed': speed
        }
    )


def get_frame():
    r = requests.get(BASE + '/camera', stream=True)
    with open('test.jpg', 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    return cv2.imread('test.jpg')


