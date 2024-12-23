import math
import pyautogui
import time
import os
import sys
from colorama import Fore,Style

size = 21




#-----------------------------------------------------------------------------
coordinates = []

for y in range(-10, 11):
    for x in range(-10, 11):
        coordinates.append([x, y, 0,"\033[38;5;28m" +'()'+ '\033[0m'])
    for z in range(0, 20):
        coordinates.append([x, y, z,"\033[38;5;34m" +'$$'+ '\033[0m'])
for x in range(-10,11):
     for z in range(0,20):
          coordinates.append([x,10,z,"\033[38;5;83m"+'&&'+'\033[0m'])
          coordinates.append([x,-10,z,"\033[38;5;83m"+'&&'+'\033[0m'])



for y in range(-10, 11):
    for x in range(-10, 11):
        coordinates.append([x, y, 20,"\033[38;5;28m"+'()'+'\033[0m'])
    for z in range(0, 20):
        coordinates.append([x - 20, y, z, "\033[38;5;34m"+'##'])

points = coordinates

center_translation = [
    -sum([p[0] for p in points]) / len(points),
    -sum([p[1] for p in points]) / len(points),
    -sum([p[2] for p in points]) / len(points)
]


def translate(points, dx, dy, dz):
    for i in range(len(points)):
        points[i][0] += dx
        points[i][1] += dy
        points[i][2] += dz


def rotator(x, y, z, angle, px, py, lx, ly):
    direction_fixery = 1 if py - ly > 0 else -1
    direction_fixer = 1 if px - lx > 0 else -1
    anglex = math.radians(angle * direction_fixer)
    angley = math.radians(angle * direction_fixery)

    x1 = x * math.cos(anglex) + z * math.sin(anglex)
    y1 = y
    z1 = -x * math.sin(anglex) + z * math.cos(anglex)

    x_ud = x1
    y_ud = y1 * math.cos(angley) - z1 * math.sin(angley)
    z_ud = y1 * math.sin(angley) + z1 * math.cos(angley)

    return x_ud, y_ud, z_ud


def rotate_with_given_angle(angle, px, py, lx, ly):
    for i in range(len(points)):
        points[i][0], points[i][1], points[i][2] = rotator(points[i][0], points[i][1], points[i][2], angle, px, py, lx, ly)


def checker(x, y, points_dict):
    return points_dict.get((round(x), round(y)), '  ')


def plot(points, degree, px, py, lx, ly):
    rotate_with_given_angle(degree, px, py, lx, ly)
    
    points_sorted = sorted(points, key=lambda x: x[2], reverse=False)
    
    points_dict = {(round(p[0]), round(p[1])): p[3] for p in points_sorted}

    buffer = []
    
    for yco in range(size, -size - 1, -1):
        line = ''.join([checker(xco, yco, points_dict) for xco in range(-size, size + 1)])
        buffer.append(line)
    
    sys.stdout.write('\033[H')
    sys.stdout.write('\n'.join(buffer) + '\n')
    sys.stdout.flush()


def main():
    translate(points, *center_translation)

    last_position = pyautogui.position()
    while True:
        pointer = pyautogui.position()

        if last_position != pointer:
            plot(points, 15, pointer.x, pointer.y, last_position.x, last_position.y)
            last_position = pointer
        
        time.sleep(0.07)  


if __name__ == "__main__":
    main()