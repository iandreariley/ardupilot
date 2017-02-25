import math
import numpy as np
from math import pi
from math import tan
from math import cos
from math import sin

px = 960 / 2
py = 720 / 2
alpha = -pitch
R = 6378100
hcar = 1
Bx = 44.44 * (pi / 180)
By = (pi / 180) * 44.44 * 75

# lat, long, h, pitch roll, yaw are all from 
def relative_target_position(lat, long, h, pitch, roll, yaw, target):
    target_rel = np.array([ 1.0 / px, 1.0 / py]) * target
    theta = target_rel * np.array([Bx, By])
    x = tan(alpha - theta[1] * By)
    y = x * tan(theta[0])
    return np.array([x, y, -h])

def ne_down(roll, pitch, yaw, position):
    rbn_roll = np.array([[1, 0, 0], [0, cos(roll), sin(roll)], [0, -sin(roll), cos(roll)]])
    rbn_yaw = np.array([[cos(yaw), sin(yaw), 0], [-sin(yaw), cos(yaw), 0], [0, 0, 1]])
    return rbn_roll.dot(rbn_yaw).dot(position)

def ned_to_ecef(lat, lon, ned):
    rne = np.array([[-cos(lon) * sin(lat), -sin(lon), -cos(lon) * cos(lat)], [-sin(lon) * sin(lat), cons(lon), -cos(lat) * sin(lon)], [cos(lat), 0, -sin(lat)]])
    return rne.dot(ned)

def coords(lat, lon, h, pitch, roll, yaw, target):
    target_pos = relative_target_position(lat, lon, h, pitch, roll, yaw, target)
    transformed_pos = ne_down(roll, pitch, yaw, target_pos)
    ecef = ned_to_ecef(lat, lon, transformed_pos)

    xd = R * cos(lon) * cos(lat)
    yd = R * cos(lat) * sin(lon)
    zd = R * sin(lat)
    pde = np.array([xd, yd, zd])

    pte = ecef + pde
    longt = acos(pte[0] / sqrt(pte[0]**2 + pte[1]**2))
    latt = acos(pte[2] / sqrt(pte[0]**2 + pte[1]**2 + R**2))
    return longt, latt, hcar
    
