#!/usr/bin/env python

import math

class Vector:

   def __init__(self, x, y, z):
      self.x = x
      self.y = y
      self.z = z
      
   def __add__(self, v2):
      if v2.identify() == "Vector":
         return Vector(self.x+v2.x,self.y+v2.y,self.z+v2.z)
      else:
         raise TypeError("Types do not make sense for this operation")
      
   def __sub__(self, v2):
      if v2.identify() == "Vector":
         return Vector(self.x-v2.x,self.y-v2.y,self.z-v2.z)
      
      else:
         raise TypeError("Types do not make sense for this operation")
      
   def __mul__(self, v2):
      if type(v2) == type(int()) or type(v2) == type(float()):
         return Vector(self.x*v2,self.y*v2,self.z*v2)
      elif v2.identify() == "Vector":
         return ((self.x*v2.x)+(self.y*v2.y)+(self.z*v2.z))
      else:
         raise TypeError("Types do not make sense for this operation")
         
   # To handle Scalar * Vector cases as opposed to Vector * Scalar cases
   __rmul__ = __mul__
      
   def __mod__(self, v2):
      if v2.identify() == "Vector":
         return Vector(((self.y*v2.z)-(self.z*v2.y)),((self.z*v2.x)-(self.x*v2.z)),((self.x*v2.y)-(self.y*v2.x)))
      else:
         raise TypeError("Types do not make sense for this operation")
      
   def __repr__(self):
      return "[" + str(self.x) + " " + str(self.y) + " " + str(self.z) + "]"
      
   def get_magnitude(self):
      return math.sqrt((self.x*self.x)+(self.y*self.y)+(self.z*self.z))
     
   def get_normalized(self):
      mag = self.get_magnitude()
      return Vector((self.x/mag),(self.y/mag),(self.z/mag))
      
   def identify(self):
      return "Vector"
      
class Point:

   def __init__(self, x, y, z):
      self.x = x
      self.y = y
      self.z = z
      
   def __sub__(self, p2):
      return Vector(self.x-p2.x,self.y-p2.y,self.z-p2.z)
      
   def __add__(self, p2):
      return Point(self.x+p2.x,self.y+p2.y,self.z+p2.z)
      
   def __repr__(self):
      return "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"
      
   def identify(self):
      return "Point"
      
class Ray:

   def __init__(self, source, direction):
      self.source = source
      self.direction = direction.get_normalized()
      self.hit = None
      self.collision_object = None
      self.bounced_rays = []
      
   def __repr__(self):
      return "{" + str(self.source) + "," + str(self.direction) + "}"
      
   def identify(self):
      return "Ray"

class Color:

   def __init__(self, r, g, b, a):

      self.r = r
      self.g = g
      self.b = b
      self.a = a
      
      if self.r > 1.0:
         self.r = 1.0
      if self.r < 0.0:
         self.r = 0.0
         
      if self.g > 1.0:
         self.g = 1.0
      if self.g < 0.0:
         self.g = 0.0
         
      if self.b > 1.0:
         self.b = 1.0
      if self.b < 0.0:
         self.b = 0.0
         
      if self.a > 1.0:
         self.a = 1.0
      if self.a < 0.0:
         self.a = 0.0
      
   def __repr__(self):
      return "(" + str(self.r) + "," + str(self.g) + "," + str(self.b) + str(self.a) + ")"
      
   def identify(self):
      return "Color"

class PointLight:

   def __init__(self, location, color):
      self.location = location
      self.color = color
      
   def __repr__(self):
      return "{" + str(self.location) + "," + str(self.color) + "}"
      
   def identify(self):
      return "PointLight"

class Pixel:

   def __init__(self, three_d_space_location, two_d_space_x, two_d_space_y):
      self.three_d_space_location = three_d_space_location
      self.two_d_space_x = two_d_space_x
      self.two_d_space_y = two_d_space_y

   def __repr__(self):
      return "{" + str(self.three_d_space_location) + ",(" + str(self.two_d_space_x) + "," + str(self.two_d_space_y) + ")}"
      
   def identify(self):
      return "Pixel"

class Hit:

   def __init__(self, location, normal):
      self.location = location
      self.normal = normal.get_normalized()
      
   def __repr__(self):
      return "{" + str(self.location) + "," + str(self.normal) + "}"
      
   def identity(self):
      return "Hit"

class Sphere:

   def __init__(self, location, radius, ambient, diffuse, specular, reflectivity):
      self.location = location
      self.radius = radius
      self.radius_squared = radius*radius
      self.ambient = ambient
      self.diffuse = diffuse
      self.specular = specular
      self.reflectivity = reflectivity
 
   def collide(self, ray):
      d = ray.source - self.location
      d2 = d*d
      g = d*ray.direction
      
      disc = (g*g) - d2 + self.radius_squared
      
      if disc < 0:
         return False
         
      t = -g - math.sqrt(disc)
      
      if t > 0:
         hit_point = ray.source + (ray.direction*t)
         hit_normal = (hit_point - self.location).get_normalized()
         return Hit(hit_point, hit_normal)
         
      return False
      
   def __repr__(self):
      return "{" + str(self.location) + ", " + str(self.radius) + "}"
      
   def identify(self):
      return "Sphere"