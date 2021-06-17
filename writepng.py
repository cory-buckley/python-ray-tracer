#!/usr/bin/python

import png

def writePNG(output_filename, width, height, al, bd, img_buf):
   f = open(output_filename, 'wb')
   w = png.Writer(width=width, height=height, greyscale=False, alpha=al, bitdepth=bd)
   row = []
   img = []
   
   maxval = (2**bd)-1
   componentsPerPixel = 4 if al else 3
   
   for component in img_buf:
      row.append(int(component*maxval))
      if len(row) >= (width*componentsPerPixel):
         img.append(row)
         row = []
   
   w.write(f, img)
   f.close()