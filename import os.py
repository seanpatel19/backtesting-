# https://medium.com/swlh/how-to-build-quant-algorithmic-trading-model-in-python-12abab49abe3


import os
from zipline.data import bundles

BUNDLE_NAME = 'eod-quotemedia'
os.environ['ZIPLINE_ROOT'] = os.path.join(os.getcwd(), 'data', 'zipline')
ingest_func = bundles.csvdir.csvdir_equities(['daily'], BUNDLE_NAME)
bundles.register(BUNDLE_NAME, ingest_func)
bundle_data = bundles.load(BUNDLE_NAME)

# Import common data science libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from tqdm import tqdm



