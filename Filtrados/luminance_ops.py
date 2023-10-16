import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

FORMATS=["YIQ promedio", "YIQ clamp", "RGB promedio", "RGB clamp"]

def rgb_to_yiq(rgb_img):
  norm_img = rgb_img/255
  result = np.zeros(rgb_img.shape)
  height = rgb_img.shape[0]
  width = rgb_img.shape[1]
  mat = np.array([
      [0.299, 0.587, 0.114],
      [0.595716, -0.274453, -0.321263],
      [0.211456, -0.522591, 0.311135]
  ])
  for i in range(height):
    for j in range(width):
      result[i,j,:] = np.matmul(mat, norm_img[i,j])
  return result

def yiq_to_rgb(yiq_img):
  result = np.zeros(yiq_img.shape)
  height = yiq_img.shape[0]
  width = yiq_img.shape[1]
  mat = np.array([
      [1, 0.9563, 0.6210],
      [1, -0.2721, -0.6474],
      [1, -1.1070, 1.7046]
  ])
  for i in range(height):
    for j in range(width):
      result[i,j,:] = np.matmul(mat, yiq_img[i,j])
  return result*255

def pow2_ilum(img):
    yiq_img = rgb_to_yiq(np.array(img))
    yiq_img[:,:,0] = yiq_img[:,:,0]**2
    return Image.fromarray( yiq_to_rgb(yiq_img).astype(np.int8), mode="RGB" )

def sqrt_ilum(img):
    yiq_img = rgb_to_yiq(np.array(img))
    yiq_img[:,:,0] = np.sqrt(yiq_img[:,:,0])
    return Image.fromarray( yiq_to_rgb(yiq_img).astype(np.int8), mode="RGB" )

def lineal_ilum(img, ymin=0.2, ymax=1):
    yiq_img = rgb_to_yiq(np.array(img))
    output = yiq_img.copy()
    output[:,:,0] = (yiq_img[:,:,0]-ymin)/(ymax-ymin)
    #Saturate
    output[yiq_img[:,:,0]<ymin] = 0 
    output[yiq_img[:,:,0]>ymax] = 1
    return Image.fromarray( yiq_to_rgb(output).astype(np.int8), mode="RGB" )

def equalize_ilum(img):
    yiq_img = rgb_to_yiq(np.array(img))
    output = yiq_img.copy()
    img_counts, bins = np.histogram(yiq_img[:,:,0], bins=50, density=True)
    cum_hist = np.cumsum(img_counts)
    # use linear interpolation of cdf to find new pixel values
    image_equalized = np.interp(yiq_img[:,:,0].flatten(), bins[:-1], cum_hist)
    
    output[:,:,0] = image_equalized.reshape(output[:,:,0].shape)
    return Image.fromarray( yiq_to_rgb(output).astype(np.int8), mode="RGB" )

