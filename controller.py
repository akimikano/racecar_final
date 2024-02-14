import time
import cv2
import numpy as np
from car_api import turn, get_frame, change_speed
from voice import listen_for_command

# region of full image which is processed to get the line slope
offset1, offset2 = 240, 360
offset11, offset22 = 360, 480


def get_right_point(arr):
    array_of_arrays = arr
    sorted_indices = np.argsort(array_of_arrays[:, 0])[::-1]
    sorted_array_of_arrays = array_of_arrays[sorted_indices]
    result_list = sorted_array_of_arrays.tolist()
    return result_list[0]


def detect_lines_coordinates(frame, offset1, offset2):
    cropped_img = frame[offset1:offset2, :]
    hsv = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2HSV)
    low_yellow = np.array([18, 94, 140])
    up_yellow = np.array([48, 255, 255])
    mask = cv2.inRange(hsv, low_yellow, up_yellow)
    edges = cv2.Canny(mask, 75, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, maxLineGap=100)
    lines = lines.reshape((len(lines), 4))
    right_line = get_right_point(lines)
    x1, y1, x2, y2 = right_line
    if x1 > x2:
        return x1, offset1+y1
    else:
        return x2, offset1+y2


def calculate_angle(a, b):
    if a != 0:
        alpha = np.degrees(np.arctan(b / a))
        return alpha
    return 90


def regulate_car(angle):
    coef = 0.01
    if abs(angle) < 85:
        time_to_wait = (90 - abs(angle)) * coef
        if angle > 0:
            turn(135)
        else:
            turn(45)
        time.sleep(time_to_wait)
        turn(100)


def main():
    change_speed(0.15)  # start moving forward

    try:
        while True:
            frame = get_frame()
            alpha = 1.5  # Contrast control
            beta = 30  # Brightness control

            frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
            try:
                x1, y1 = detect_lines_coordinates(frame, 600, 800)
                x2, y2 = detect_lines_coordinates(frame, 800, 1000)
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
                angle = calculate_angle(x2 - x1, y2 - y1)
                if abs(angle) < 60:  # in this case it is definitely an error line
                    continue
                regulate_car(angle)
                print('line found')
            except AttributeError:
                print('Lines not found')
                pass

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(1)
    except KeyboardInterrupt:
        change_speed(0)  # stop moving
        pass


if __name__ == '__main__':
    main()


def check_orthogonal_line(frame):
    """
    looks for orthogonal line to make 90 degrees turn
    """
    return True


def follow_line(frame):
    try:
        x1, y1 = detect_lines_coordinates(frame, 600, 800)
        x2, y2 = detect_lines_coordinates(frame, 800, 1000)
        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
        angle = calculate_angle(x2 - x1, y2 - y1)
        if abs(angle) < 60:  # in this case it is definitely an error line
            return
        regulate_car(angle)
        print('line found')
    except AttributeError:
        print('Lines not found')
        pass


def make_90_degrees_turn():
    pass


def position_tracker(curr_position):
    """
    generator for moving within 4 points: [1, 2, 3, 4]
    """
    while True:
        yield curr_position
        if curr_position == 4:
            curr_position = 1
            continue
        curr_position += 1


def start():
    current_position = 1
    position = position_tracker(current_position)
    while True:
        target_position = listen_for_command()
        while current_position != target_position:
            frame = get_frame()
            alpha = 1.5  # Contrast control
            beta = 30  # Brightness control

            frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

            orthogonal_line_is_present = check_orthogonal_line(frame)

            if orthogonal_line_is_present:
                make_90_degrees_turn()
            else:
                follow_line(frame)

            current_position = next(position)

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(1)
        change_speed(0)  # stop moving
