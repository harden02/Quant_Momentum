# -*- coding: utf-8 -*-
"""
Analysis of Results
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import stats

source_file = pd.read_csv('MomentumReturnsModular.txt', skipinitialspace=True)
source_file.set_index('use_gradient', inplace=True)
gradients = source_file.loc[source_file.index == True]
increases = source_file.loc[source_file.index == False]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(25, 16))
ax1.hist(gradients['strategy_return'])
ax1.set(title='exponential gradient method', xlabel='raw return')
ax2.hist(increases['strategy_return'])
ax2.set(title='raw formation return method', xlabel='raw return')