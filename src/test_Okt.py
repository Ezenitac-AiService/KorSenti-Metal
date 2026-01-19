import re
import json
import numpy as np
import pandas as pd
import h5py
import logging
from konlpy.tag import Okt
from tqdm import tqdm
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import concurrent.futures
import matplotlib.pyplot as plt
from konlpy.tag import Okt
import jpype

if not jpype.isJVMStarted():
    jpype.startJVM()

okt = Okt()
print(okt.morphs("테스트 문장입니다."))
