import numpy as np

def erode(img,size=3):
    output = np.zeros_like(np.array(img))
    height = output.shape[0]
    width = output.shape[1]
    #Create extended image
    extend_by = (size-1)//2
    padded_img = np.pad(img, extend_by, 'edge')
    for i in range(extend_by, height+extend_by):
        for j in range(extend_by, width+extend_by):
            img_patch = padded_img[i-extend_by:i+extend_by+1, j-extend_by:j+extend_by+1]
            output[i-extend_by, j-extend_by] = img_patch.min()
    return output

def dilate(img,size=3):
    output = np.zeros_like(np.array(img))
    height = output.shape[0]
    width = output.shape[1]
    #Create extended image
    extend_by = (size-1)//2
    padded_img = np.pad(img, extend_by, 'edge')
    for i in range(extend_by, height+extend_by):
        for j in range(extend_by, width+extend_by):
            img_patch = padded_img[i-extend_by:i+extend_by+1, j-extend_by:j+extend_by+1]
            output[i-extend_by, j-extend_by] = img_patch.max()
    return output

def opening(img,size=3):
    eroded = erode(img,size)
    return dilate(eroded, size)

def closing(img,size=3):
    dilated = dilate(img,size)
    return erode(dilated, size)

def median2d(img,size=3):
    output = np.zeros_like(np.array(img))
    height = output.shape[0]
    width = output.shape[1]
    #Create extended image
    extend_by = (size-1)//2
    padded_img = np.pad(img, extend_by, 'edge')
    for i in range(extend_by, width):
        for j in range(extend_by, height):
            img_patch = padded_img[j-extend_by:j+extend_by+1, i-extend_by:i+extend_by+1]
            output[j, i] = np.median(img_patch)
    return output

def edge_int(img,size=3):
    return (np.array(img)-erode(img,size)).clip(0,255)

def edge_ext(img,size=3):
    return (dilate(img,size)-np.array(img)).clip(0,255)

def top_hat(img,size=3):
    return (np.array(img)-opening(img,size)).clip(0,255)