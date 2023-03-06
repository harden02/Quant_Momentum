# -*- coding: utf-8 -*-
"""
Analysis of Results
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import stats

sourcefile = pd.read_csv('MomentumReturnsModular.txt', skipinitialspace=True)
sourcefile.set_index('use_gradient', inplace= True)
gradients = sourcefile.loc[sourcefile.index == True]
increases = sourcefile.loc[sourcefile.index == False]


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(25, 16))
ax1.hist(gradients['strategyreturn'])
ax1.set(title='exponential gradient method', xlabel = 'raw return')
ax2.hist(increases['strategyreturn'])
ax2.set(title='raw formation return method', xlabel = 'raw return')




