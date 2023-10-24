import numpy as np
from PIL import Image
from scipy.ndimage import zoom

INTERP=["Constante", "Bilineal", "Bicubico"]

def downsample_img(img, interp, n_levels=None):
    downsampled = np.array(img)[::2,::2]
    if interp=="Constante":
      interpolated = zoom(downsampled, 2, order=0)
    elif interp == "Bilineal":
      interpolated = zoom(downsampled, 2, order=1)
    elif interp=="Bicubico":
      interpolated = zoom(downsampled, 2, order=3)
    return Image.fromarray(interpolated.astype(np.uint8), "L")

def upsample_img(img, interp, n_levels=None):
    if interp=="Constante":
      interpolated = zoom(np.array(img), 2, order=0)
    elif interp == "Bilineal":
      interpolated = zoom(np.array(img), 2, order=0)
    elif interp=="Bicubico":
      interpolated = zoom(np.array(img), 2, order=3)
    return Image.fromarray(interpolated.astype(np.uint8), "L")

def cuantize_uniform(img, interp, n_levels):
   img_arr = np.array(img)
   step = 256/n_levels
   output = np.floor(img_arr/step)*(255/(n_levels-1))
   return  Image.fromarray(output.astype(np.uint8), "L")

def cuantize_dither_rand(img, interp, n_levels):
   img_arr = np.array(img)
   step = 256/n_levels
   img_arr = img_arr + (np.random.rand(*img_arr.shape)-0.5)*step
   img_arr = img_arr.clip(0,255)
   output = np.floor(img_arr/step)*(255/(n_levels-1))
   return  Image.fromarray(output.astype(np.uint8), "L")

def inRange(x, low, high):
  return x>=low and x<high  #check if x is between low and high

def cuantize_dither_diffusion(img, interp, n_levels):
   img_arr = np.array(img).astype(np.float64)
   step = 256/n_levels
   output = img_arr.copy()

   #wtDict is a dictionary with keys as relative index of neighbour and values as weights
   wtDict = {(0,1):7, (1,-1):3, (1,0):5, (1,1):1}
   wtDictNormalized = {k:wtDict[k]/sum(wtDict.values()) for k in wtDict}   #to ensure that the weights sum to 1
   for row in range(img_arr.shape[0]):
     for col in range(img_arr.shape[1]):
      output[row, col] = np.floor(img_arr[row,col]/step)*(255/(n_levels-1)) #quantize
      error = img_arr[row, col] - output[row, col]  #calculate error
     for key in wtDictNormalized:  #spread error to neighbours
       if inRange(row+key[0], 0, img_arr.shape[0]) and inRange(col+key[1], 0, img_arr.shape[1]):  #take care of image border
        output[row+key[0], col+key[1]] += error*wtDictNormalized[key]
   return Image.fromarray(np.floor(output).astype(np.uint8), "L")