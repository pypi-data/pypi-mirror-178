import pandas as pd
import numpy as np
import streamlit as st
from abydos.distance import Levenshtein 

cmp = Levenshtein()


def add(x,y):
    return st.write(x+y)

def sub(x,y):
    return st.write(x-y)




