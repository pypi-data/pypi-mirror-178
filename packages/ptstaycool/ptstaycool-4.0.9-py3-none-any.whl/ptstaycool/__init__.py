import os
from time import sleep
import sys



desktop = os.path.join(os.path.expanduser('~/Documents/'))+'Hkk_output/'

try :
    os.mkdir(desktop)
except FileExistsError:
    pass