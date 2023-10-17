import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

PHASE_MIN = -np.pi
PHASE_MAX = np.pi

SPECTRUM_MIN = -60

def fourier_transform(img, phase=None):
    img_spectrum = 20*np.log10( np.abs(np.fft.fftshift(np.fft.fft2(np.array(img)))) )
    img_spectrum = img_spectrum - SPECTRUM_MIN
    img_phase = np.angle(np.fft.fftshift(np.fft.fft2(np.array(img))))
    img_phase = 255*(img_phase - PHASE_MIN)/(PHASE_MAX-PHASE_MIN) #Take to 0-255 range
    return Image.fromarray( img_spectrum.astype(np.uint8), mode="L" ).resize((600,600)), Image.fromarray( img_phase.astype(np.uint8), mode="L" ).resize((600,600))

def inv_fourier(img_spectrum, img_phase):
    #Denorm spectrum
    spectrum_denorm = np.array(img_spectrum)+SPECTRUM_MIN
    img_amp = 10**(spectrum_denorm/20)
    #Denorm phase
    phase_denorm = np.array(img_phase)*(PHASE_MAX-PHASE_MIN)/255+PHASE_MIN
    #Reconstruct fourier transform
    img_fft = img_amp*(np.cos(phase_denorm)+1j*np.sin(phase_denorm))
    img = np.abs( np.fft.ifft2(np.fft.ifftshift(img_fft)) )
    img = 255*(img-img.min())/(img.max()-img.min())
    return Image.fromarray( img.astype(np.uint8), mode="L" ).resize((600,600)), img_phase