import math
import pyautogui
import time
import ast
import os
import sys


size = 30


points =[]


# Read the matrix from the file

with open("p.txt", "r") as file:
    file_content = file.read()
    points = ast.literal_eval(file_content)

l=[i[0] for i in points]
l=max(l)+abs(min(l))
l=abs(l)
oracle=l/4

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
    direction_fixery = -1 if py - ly > 0 else 1
    direction_fixer = -1 if px - lx > 0 else 1
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
    shades=[' ','00','@ ','( ','( ']
    o=25
    rotate_with_given_angle(degree, px, py, lx, ly)
    
    points_sorted = sorted(points, key=lambda x: x[2], reverse=True)
    
    points_dict = {(round(p[0]), round(p[1])): (shades[round((p[0]+50)/20)])  for p in points_sorted}

    buffer = []
    
    for yco in range(size, -size - 1, -1):
        line = ''.join([checker(xco, yco, points_dict) for xco in range(-size, size + 1)])
        buffer.append("\033[38;5;83m"+line)
    
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
        
        time.sleep(0.1)  


if __name__ == "__main__":
    main()
