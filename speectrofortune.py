import picamera.array
from picamera import PiCamera
from time import sleep
import time
from fractions import Fraction

import numpy as np
from matplotlib import pyplot as plt
import sklearn
import sklearn.preprocessing

from scipy.interpolate import interp1d

CALIBRATE = False

RED_MAX_WAVELENGTH = 611.6
GREEN_MAX_WAVELENGTH = 546.5
BLUE_MAX_WAVELENGTH = 436.6

AWB_MODE = 'sunlight'
BRIGHTNESS = 50
CONTRAST = 0
EXPOSURE_MODE = 'auto'
#FRAMERATE = Fraction(10,1)
FRAMERATE = 10
SHUTTER_SPEED = int(5*1000000) #microseconds

timestamp = time.strftime("%Y%m%d-%H%M%S")

camera = PiCamera()

camera.awb_mode = AWB_MODE
camera.brightness = BRIGHTNESS
camera.contrast = CONTRAST
camera.exposure_mode = EXPOSURE_MODE
#camera.framerate = FRAMERATE
#camera.shutter_speed = SHUTTER_SPEED


camera.start_preview()
input("klik enter to continue pls")
#camera.exposure_mode = 'off'
#sleep(3)


with picamera.array.PiRGBArray(camera) as output:
    camera.capture(output, 'rgb')
    
    center_col_num = int(output.array.shape[1]/2)
    cross_sec_col = output.array[:,center_col_num]
    
    if CALIBRATE:
        max_red, _, max_blue = np.argmax(cross_sec_col, axis=0)
        func = interp1d([max_red, max_blue], [RED_MAX_WAVELENGTH, BLUE_MAX_WAVELENGTH], fill_value='extrapolate')
        wavelengths = func(list(range(output.array.shape[0])))
    else:
        wavelengths = np.genfromtxt('calibration.csv', delimiter=',')

    intensities = np.zeros([len(wavelengths), 2])
    for i in range(len(wavelengths)):
        intensity = np.mean(cross_sec_col[i])
        wl = wavelengths[i]
        intensities[i, :] = ([wl, intensity])
        
    intensities[:,1] = sklearn.preprocessing.MinMaxScaler().fit_transform(intensities[:,1].reshape(-1, 1)).squeeze()
    
    
    plt.plot([intensities[i][0] for i in range(len(intensities))], [intensities[i][1] for i in range(len(intensities))])
    
    if CALIBRATE:
        plt.savefig('calibration_plot.png')
        np.savetxt('calibration.csv', wavelengths, delimiter=',')
        np.savetxt('calibration_intensities.csv', intensities, delimiter=',')
        camera.capture('calibration.jpg')
        
    else:
        plt.savefig('runs/' + timestamp + '_plot.png')
        np.savetxt('runs/' + timestamp + '.csv', intensities)
        camera.capture('runs/' + timestamp + '.jpg')

        
    plt.show()


    #print(intensities)
    
    

camera.stop_preview()


        
