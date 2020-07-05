import numpy as np
from PIL import Image
import math

w, l = 1024,1024 #paremeters of floor, cm
floor = np.zeros((l, w)) #0 for black, 1 for white

image_w, image_l = 512, 512  #pixels of image
out_image = np.zeros((image_l, image_w,3),dtype = np.uint8) #image output

for i in range(image_w):
    for j in range(image_l):
        out_image[i][j] = [255,255,255] #initialized as white

camera_phi = math.pi/2
camera_theta = 0
camera_height = 10

#direction of camera sight is expressed as polar cordinate

camera_cor = [0,0,camera_height]

#camera is in the middle

sight_phi = math.pi/3
sight_theta = math.pi/3

#viewing angle of camera


class Vector:
    def __init__(self, lst):
        self.v = lst
    def __repr__(self):
        return str(self.v)
    def __add__(self, rhs):
        return Vector([self.v[i]+rhs.v[i] for i in range(len(self.v))])
    def __sub__(self, rhs):
        return Vector([self.v[i]-rhs.v[i] for i in range(len(self.v))])
    def __rmul__(self, scalar):
        return Vector([self.v[i]*scalar for i in range(len(self.v))])
    def size(self):
        ret = 0
        for i in self.v:
            ret += i*i
        return ret**0.5
    def dot(self, rhs):
        ret = 0
        for i in range(len(self.v)):
            ret += self.v[i]*rhs.v[i]
        return ret
    def proj(self, v):
        l = self.dot(v)/v.size()**2
        return l*v
    def per(self, v):
        return self-self.proj(v)


def point_vector(cor, camera_cor): #vector from camera to point 
    return Vector([cor[0]-camera_cor[0], cor[1]-camera_cor[1], cor[2]-camera_cor[2]])


def sight_vector():
    return Vector([math.sin(camera_phi)*math.cos(camera_theta),math.sin(camera_phi)*math.sin(camera_theta), math.cos(camera_phi)])


def convert_to_image_cor(cor, camera_cor):
    v = point_vector(cor, camera_cor)
    v_per = v.per(sight_vector())
    x = v_per.dot(Vector([math.sin(camera_theta), -math.cos(camera_theta), 0]))
    y = v_per.dot(Vector([-math.cos(camera_phi)*math.cos(camera_theta),-math.cos(camera_phi)*math.sin(camera_theta), math.sin(camera_phi)]))
    l = v.dot(sight_vector())
    return (x/l, y/l)
    

def insight(cor, camera_cor):
    x, y = convert_to_image_cor(cor, camera_cor)
    if abs(x)>math.tan(sight_theta) or abs(y)>math.tan(sight_phi) or point_vector(cor, camera_cor).dot(sight_vector())<0:
        return False
    return True


def plot_to_image(cor, camera_cor, image):
    if(insight(cor, camera_cor)):
        x,y = convert_to_image_cor(cor, camera_cor)
        x*=((image_w-1)/math.tan(sight_theta)/2)
        y*=((image_l-1)/math.tan(sight_phi)/2)
        image[image_l//2-int(y)][image_w//2+int(x)] = [0,0,0]
    return image


for i in range(-l//2,l//2):
    for j in range(-w//2,w//2):
        
        plot_to_image([i,j,0], camera_cor, out_image)




img = Image.fromarray(out_image,'RGB')
img.save('my.png')
img.show()
