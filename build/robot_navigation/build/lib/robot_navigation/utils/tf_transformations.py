import numpy as np
import math
from transforms3d import euler, quaternions

def quaternion_from_euler(roll, pitch, yaw):
    """
    Convert Euler angles to quaternion.
    
    Parameters:
    - roll (float): Roll angle in radians
    - pitch (float): Pitch angle in radians
    - yaw (float): Yaw angle in radians
    
    Returns:
    - list: Quaternion [x, y, z, w]
    """
    q = euler.euler2quat(roll, pitch, yaw, 'sxyz')
    return [q[1], q[2], q[3], q[0]]  # Transforms3d returns w, x, y, z, we want x, y, z, w

def euler_from_quaternion(quaternion):
    """
    Convert quaternion to Euler angles.
    
    Parameters:
    - quaternion (list): Quaternion [x, y, z, w]
    
    Returns:
    - tuple: Euler angles (roll, pitch, yaw) in radians
    """
    x, y, z, w = quaternion
    q = [w, x, y, z]  # Transforms3d expects w, x, y, z
    return euler.quat2euler(q, 'sxyz')