# profilometer
import numpy as np
import pandas as pd
from .misc import *
import mat73
import scipy.io
__all__ = ['parse_oscilloscope_optical']

def read_files(input_path, txt_path):
    try:
        mat = mat73.loadmat(input_path)
    except:
        mat = scipy.io.loadmat(input_path)
    data = {
        "Wavelength (µm)": mat["ref"][:,0],
        "Transmittance (dB)": mat["ref"][:,1],
    }
    df = pd.DataFrame.from_dict(data)
    df.to_csv(txt_path, index=False)

def parse_oscilloscope_optical(**kwargs):
    read_files(kwargs["input_path"], kwargs["txt_path"])
