import math


def determine_shift(frame_width, object_left, object_right):
    frame_center = frame_width / 2
    object_center = object_right - ((object_right - object_left)/2)
    center_window = frame_width / 8
    difference = frame_center - object_center
    direction = math.copysign(1, difference)
    abs_difference = abs(difference)

    print("DIFF: ", difference)
    if abs_difference > center_window:
        return abs_difference, direction
    return 0, 0


def bound(low, high, value):
    return max(low, min(high, value))


def determine_update_movement(current_value, direction, magnitude=None):
    # TODO: use magnitude to make relative shift
    # direction: +1/-1 python truthies
    nudge_value = 0.2
    new_pwm = current_value + nudge_value*direction
    bounded_pwm = bound(2.5, 12.5, new_pwm)
    return bounded_pwm
