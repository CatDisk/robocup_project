import numpy as np

def vec2tuple(vec: np.ndarray):
    return (vec[0], vec[1])

def deg2rad(deg):
    return deg * (np.pi/180)

def rad2deg(rad):
    return rad * (180/np.pi)

def normalize(vec):
    norm = np.linalg.norm(vec)
    if norm == 0:
        return vec
    else:
        return vec / norm