import math


class Vec3:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

class Vec4:
    def __init__(self, x=0, y=0, z=0, w=1):
        self.x = x
        self.y = y
        self.z = z
        self.w = w



class Quaternion:

    def __init__(self, q):
        self.x = q[0]
        self.y = q[1]
        self.z = q[2]
        self.w = q[3]

    def to_axis_angle(self, targetAxis = [0,0,0,1]):
        self.normalize()  # if w > 1 acos and sqrt will produce errors, this cant happen if quaternion is normalised
        angle = 2 * math.acos(self.w)
        s = math.sqrt(1 - self.w * self.w)  # assuming quaternion normalised then w is less than 1, so term always positive.
        if (s < 0.001): # test to avoid divide by zero, s is always positive due to sqrt
            #if s close to zero then direction of axis not important
            targetAxis[0] = self.x  # if it is important that axis is normalised then replace with x=1; y=z=0;
            targetAxis[1] = self.y
            targetAxis[2] = self.z
        else:
            targetAxis[0] = self.x / s  # normalise axis
            targetAxis[1] = self.y / s
            targetAxis[2] = self.z / s

        return [targetAxis, angle];

    def normalize(self):
        l = math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z + self.w * self.w)
        if l == 0:
            self.x = 0
            self.y = 0
            self.z = 0
            self.w = 0
        else:
            l = 1 / l
            self.x *= l
            self.y *= l
            self.z *= l
            self.w *= l

