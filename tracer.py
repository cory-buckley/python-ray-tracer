#!/usr/bin/python

import sys, os
from structures import *
from writepng import *

aspect_height = 1
aspect_width = 1
viewing_plane_multiplier = 1
pixel_height = 500
pixel_width = 500

background_color = Color(0,0,0,1.0)

objects = dict()
lights = []

specular_intensity = 30
specular_adjust = 1.0

view_plane_center = Point(0,0,1)
view_plane_up = Vector(0,1,0)

eye = Point(0,0,0)

pixels = []
img_buffer = []

def setup_pixels():
   
   delta_height = (1.0*aspect_height*viewing_plane_multiplier)/pixel_height
   delta_width = (1.0*aspect_width*viewing_plane_multiplier)/pixel_width
   
   down = (-1.0*view_plane_up).get_normalized()
   over = (-1.0*(view_plane_up%(eye-view_plane_center))).get_normalized()
   
   half_height = (aspect_height*viewing_plane_multiplier)/2.0
   half_width = (aspect_width*viewing_plane_multiplier)/2.0
   
   start = view_plane_center + ((half_height-(delta_height/2))*view_plane_up) + ((half_width-(delta_width/2))*(-1*over))
   next_start = start + (delta_height*down)
  
   current_x = 0
   current_y = 0
   
   for y in range(pixel_height):
      for x in range(pixel_width):
         pixels.append(Pixel((start+((x*delta_width)*over)), x, y))
      start = next_start
      next_start = next_start + (delta_height*down)


def get_color(ray):
   
   obj_amb_color = (objects[ray.collision_object]).ambient
   obj_dif_color = (objects[ray.collision_object]).diffuse
   obj_spec_color = (objects[ray.collision_object]).specular
   
   hit_normal = ray.hit.normal
   
   # add ambient color
   
   amb_r = obj_amb_color.r
   amb_g = obj_amb_color.g
   amb_b = obj_amb_color.b

   # add diffuse color

   dif_r = 0.0
   dif_g = 0.0
   dif_b = 0.0
   
   for light in lights:
      hit_to_light = ( light.location - ray.hit.location ).get_normalized()
      diffused = (hit_normal*hit_to_light)
      if diffused < 0:
         continue
      dif_r += light.color.r * obj_dif_color.r * diffused
      dif_g += light.color.g * obj_dif_color.g * diffused
      dif_b += light.color.b * obj_dif_color.b * diffused
   
   # add specular color
   
   spec_r = 0.0
   spec_g = 0.0
   spec_b = 0.0
   
   for light in lights:
      hit_to_light = ( light.location - ray.hit.location ).get_normalized()
      if (hit_normal*hit_to_light) < 0:
         continue
      R = hit_to_light - (2*(hit_normal*hit_to_light)*hit_normal)
      V = (ray.hit.location-eye).get_normalized()
      specularity = ((R*V)**specular_intensity)*specular_adjust
      spec_r += light.color.r * obj_spec_color.r * specularity
      spec_g += light.color.g * obj_spec_color.r * specularity
      spec_b += light.color.b * obj_spec_color.r * specularity
   
   return Color(amb_r+dif_r+spec_r, amb_g+dif_g+spec_g, amb_b+dif_b+spec_b, 1.0)


def shoot_ray(ray):

   keys = objects.keys()

   closest_hit = None
   closest_object_key = None
   
   smallest_distance = None

   for key in keys:
      collided = (objects[key]).collide(ray)
      if collided != False:
         if closest_hit == None:
            closest_hit = collided
            closest_object_key = key
            smallest_distance = (closest_hit.location-eye).get_magnitude()
         elif smallest_distance > (collided.location-eye).get_magnitude():
            closest_hit = collided
            closest_object_key = key
            smallest_distance = (closest_hit.location-eye).get_magnitude()
       
   ray.hit = closest_hit
   ray.collision_object = closest_object_key
   
   if closest_hit != None:
      color = get_color(ray)
      return color
   else:
      return None


def trace_scene():
   count = 1.0
   reportingInterval = len(pixels)/10;
   reportingIntervals = [];
   for i in range (10):
      reportingIntervals.append(reportingInterval*(i+1))

   for pixel in pixels:
      color = shoot_ray(Ray(eye,pixel.three_d_space_location-eye))
      
      if count in reportingIntervals:
         print("%02d" % ((count/len(pixels))*100) + "% complete")
      
      if color != None:
         img_buffer.append((color.r*color.a)+((1.0-color.a)*(background_color.a*background_color.r)))
         img_buffer.append((color.g*color.a)+((1.0-color.a)*(background_color.a*background_color.g)))
         img_buffer.append((color.b*color.a)+((1.0-color.a)*(background_color.a*background_color.b)))
         img_buffer.append(color.a+((1.0-color.a)*background_color.a))
      else:
         img_buffer.append(background_color.r)
         img_buffer.append(background_color.g)
         img_buffer.append(background_color.b)
         img_buffer.append(background_color.a)
         
      count = count + 1.0

def main():
   
   sph_pt = Point(0,0,10)
   sph_amb = Color(0.2,0,0,0)
   sph_dif = Color(1.0,0,0,0)
   sph_spec = Color(1,1,1,0)
   
   test_sphere = Sphere(sph_pt,3.0,sph_amb,sph_dif,sph_spec,0.0)
   
   lit_pt = Point(-10,10,-5)
   lit_col = Color(1,1,1,0)
   
   test_light = PointLight(lit_pt,lit_col)
   
   objects[1] = test_sphere
   lights.append( test_light )
   
   setup_pixels()
   
   trace_scene()
   
   writePNG('output.png', pixel_width, pixel_height, True, 16, img_buffer)
      

if __name__ == "__main__":
  main()