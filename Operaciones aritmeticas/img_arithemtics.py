import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

FORMATS=["YIQ promedio", "YIQ clamp", "RGB promedio", "RGB clamp"]

def rgb_to_yiq(rgb_img):
  norm_img = rgb_img/255.0
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
      [1, 0.9663, 0.6210],
      [1, -0.2721, -0.6474],
      [1, -1.1070, 1.7046]
  ])
  for i in range(height):
    for j in range(width):
      result[i,j,:] = np.matmul(mat, yiq_img[i,j])
  return result*255

def cuasi_sum(img1, img2, format):
    """This function performs pixel-by-pixel sum of images according to format

    Args:
        img1 (PIL image): First image to be summed
        img2 (PIL image): Second image to be summed
        format (str): Possible values are those in FORMATS

    Returns:
        PIL image of img1+img2
    """
    if format == "YIQ promedio":
        yiq1 = rgb_to_yiq(np.array(img1))
        yiq2 = rgb_to_yiq(np.array(img2))
        output = (yiq1 + yiq2)/2.0
        #Calcualte I and Q values
        output[:,:,1] = ((yiq1[:,:,0]*yiq1[:,:,1])+(yiq2[:,:,0]*yiq2[:,:,1])) / (yiq1[:,:,0]+yiq2[:,:,0])
        output[:,:,2] = ((yiq1[:,:,0]*yiq1[:,:,2])+(yiq2[:,:,0]*yiq2[:,:,2])) / (yiq1[:,:,0]+yiq2[:,:,0])
        return Image.fromarray(yiq_to_rgb(output).astype(np.int8), mode="RGB")
    elif format == "YIQ clamp":
        yiq1 = rgb_to_yiq(np.array(img1))
        yiq2 = rgb_to_yiq(np.array(img2))
        output = (yiq1 + yiq2).clip(0,1)
        #Calcualte I and Q values
        output[:,:,1] = ((yiq1[:,:,0]*yiq1[:,:,1])+(yiq2[:,:,0]*yiq2[:,:,1])) / (yiq1[:,:,0]+yiq2[:,:,0])
        output[:,:,2] = ((yiq1[:,:,0]*yiq1[:,:,2])+(yiq2[:,:,0]*yiq2[:,:,2])) / (yiq1[:,:,0]+yiq2[:,:,0])
        return Image.fromarray(yiq_to_rgb(output).astype(np.int8), mode="RGB")
    elif format == "RGB promedio":
        output = (np.array(img1)+np.array(img2))//2
        return Image.fromarray(output.astype(np.int8), mode="RGB")
    elif format == "RGB clamp":
        output = (np.array(img1)+np.array(img2)).clip(0,255)
        return Image.fromarray(output.astype(np.int8), mode="RGB")
    
def cuasi_diff(img1, img2, format):
    """This function performs pixel-by-pixel substraction of images according to format

    Args:
        img1 (PIL image): First image to which substraction is performed
        img2 (PIL image): Second image used in substraction
        format (str): Possible values are those in FORMATS

    Returns:
        PIL image of img1-img2
    """
    if format == "YIQ promedio":
        yiq1 = rgb_to_yiq(np.array(img1))
        yiq2 = rgb_to_yiq(np.array(img2))
        output = (yiq1 - yiq2)/2.0
        #Calcualte I and Q values
        output[:,:,1] = ((yiq1[:,:,0]*yiq1[:,:,1])+(yiq2[:,:,0]*yiq2[:,:,1])) / (yiq1[:,:,0]+yiq2[:,:,0])
        output[:,:,2] = ((yiq1[:,:,0]*yiq1[:,:,2])+(yiq2[:,:,0]*yiq2[:,:,2])) / (yiq1[:,:,0]+yiq2[:,:,0])
        return Image.fromarray( ((yiq_to_rgb(output)+255)/2).astype(np.int8), mode="RGB" )
    elif format == "YIQ clamp":
        yiq1 = rgb_to_yiq(np.array(img1))
        yiq2 = rgb_to_yiq(np.array(img2))
        output = (yiq1 - yiq2).clip(0,1)
        #Calcualte I and Q values
        output[:,:,1] = ((yiq1[:,:,0]*yiq1[:,:,1])+(yiq2[:,:,0]*yiq2[:,:,1])) / (yiq1[:,:,0]+yiq2[:,:,0])
        output[:,:,2] = ((yiq1[:,:,0]*yiq1[:,:,2])+(yiq2[:,:,0]*yiq2[:,:,2])) / (yiq1[:,:,0]+yiq2[:,:,0])
        return Image.fromarray(yiq_to_rgb(output).astype(np.int8), mode="RGB")
    elif format == "RGB promedio":
        output = (np.array(img1)-np.array(img2)+255)//2
        return Image.fromarray(output.astype(np.int8), mode="RGB")
    elif format == "RGB clamp":
        output = (np.array(img1)-np.array(img2)).clip(0,255)
        return Image.fromarray(output.astype(np.int8), mode="RGB")
    
def if_lighter(img1, img2, format):
    """Outputs image made from brightest pixels between the 2 inputs

    Args:
        img1 (PIL image): First image
        img2 (PIL image): Second image
        format (str): Possible values are those in FORMATS

    Returns:
        PIL image with brightest pixels
    """
    if format == "YIQ promedio" or format == "YIQ clamp":
        yiq1 = rgb_to_yiq(np.array(img1))
        yiq2 = rgb_to_yiq(np.array(img2))
        output = yiq2
        output[yiq1[:,:,0]>yiq2[:,:,0]] = yiq1[yiq1[:,:,0]>yiq2[:,:,0]]
        return Image.fromarray(yiq_to_rgb(output).astype(np.int8), mode="RGB")
    elif format == "RGB promedio" or format == "RGB clamp":
        output = np.array(img2)
        mag1 = img1.convert("L")
        mag2 = img2.convert("L")
        output[np.array(mag1)>np.array(mag2)] = np.array(img1)[np.array(mag1)>np.array(mag2)]
        return Image.fromarray(output.astype(np.int8), mode="RGB")
    
def if_darker(img1, img2, format):
    """Outputs image made from darkest pixels between the 2 inputs

    Args:
        img1 (PIL image): First image
        img2 (PIL image): Second image
        format (str): Possible values are those in FORMATS

    Returns:
        PIL image with darkest pixels
    """
    if format == "YIQ promedio" or format == "YIQ clamp":
        yiq1 = rgb_to_yiq(np.array(img1))
        yiq2 = rgb_to_yiq(np.array(img2))
        output = yiq2
        output[yiq1[:,:,0]<yiq2[:,:,0]] = yiq1[yiq1[:,:,0]<yiq2[:,:,0]]
        return Image.fromarray(yiq_to_rgb(output).astype(np.int8), mode="RGB")
    elif format == "RGB promedio" or format == "RGB clamp":
        output = np.array(img2)
        mag1 = img1.convert("L")
        mag2 = img2.convert("L")
        output[np.array(mag1)<np.array(mag2)] = np.array(img1)[np.array(mag1)<np.array(mag2)]
        return Image.fromarray(output.astype(np.int8), mode="RGB")