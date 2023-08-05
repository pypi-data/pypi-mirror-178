import sys
import os
import subprocess

def vector(x):
    try:
        import numpy as np
    except ImportError:
        FNULL = open(os.devnull, 'w')
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-Iv','numpy==1.22.0'], stdout=FNULL, 
        stderr=subprocess.STDOUT)
        import numpy as np

    return np.ones(x)

