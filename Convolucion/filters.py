import numpy as np
from scipy.ndimage import rotate

dir_dict = {"N":0, "NE":-45, "E":-90, "SE":-135,
                    "S":180, "SW":135, "W":90, "NW": 45}

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

def conv2d(kernel, img):
  output = np.zeros_like(np.array(img)).astype(np.float64)
  width, height = img.size
  kernel_size = kernel.shape[0]
  #Create extended image
  extend_by = (kernel_size-1)//2
  padded_img = np.pad(img, extend_by, 'edge').astype(np.float64)
  for i in range(extend_by, width):
    for j in range(extend_by, height):
        img_patch = padded_img[j-extend_by:j+extend_by+1, i-extend_by:i+extend_by+1]
        output[j, i] = (img_patch*kernel).sum()
  return output.clip(0,255)

def constant_kernel(size):
    return np.ones((size,size)) / (size**2)

def bartlett_kernel(size):
    a = np.arange(1,(size//2)+2)
    a = np.concatenate((a,a[-2::-1])).reshape(-1,1)
    kernel = np.matmul(a,a.reshape(1,-1))
    return kernel/kernel.sum()

def gaussian_kernel(size):
    kernel = None
    if size == 5:
      a = np.array([1,4,6,4,1]).reshape(-1,1)
      b = np.array([1,2,3,2,1]).reshape(1,-1)
      result = np.matmul(a,b)
      kernel = result/result.sum()
    elif size == 7:
      a = np.array([1,6,15,20,15,6,1]).reshape(-1,1)
      b = np.array([1,2,3,4,3,2,1]).reshape(1,-1)
      result = np.matmul(a,b)
      kernel = result/result.sum()
    return kernel

def bandpass_kernel():
    a = np.array([-1,0,2,0,-1]).reshape(-1,1)
    b = np.array([1,2,3,2,1]).reshape(1,-1)
    return np.matmul(a,b)

def highpass_kernel(fc):
    kernel = None
    if fc==0.2:
      a = np.array([-1,-4,10,-4,-1]).reshape(-1,1)
      b = np.array([1,2,3,2,1]).reshape(1,-1)
      kernel = np.matmul(a,b)
    elif fc== 0.4:
      a = np.array([1,-4,6,-4,1]).reshape(-1,1)
      b = np.array([1,2,3,2,1]).reshape(1,-1)
      kernel = np.matmul(a,b)
    return kernel

def laplace_kernel(version):
    laplaciano = None
    if version == "4":
      laplaciano = np.array([
                    [0, -1, 0],
                    [-1, 4, -1],
                    [0, -1, 0]
                ])
    elif version == "8":
      laplaciano = np.array([
                    [-1, -1, -1],
                    [-1, 8, -1],
                    [-1, -1, -1]
                ])
    return laplaciano

def directional_kernel(angle):
   n_kernel = np.array([
                      [1,2,1],
                      [0,0,0],
                      [-1,-2,-1]
                      ])
   return rotate(n_kernel, angle, reshape=False)
