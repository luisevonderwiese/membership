import pandas as pd
import os
import matplotlib.pyplot as plt
from tabulate import tabulate
import math
from scipy import stats
import numpy as np

from lingdata import database

import code.distances as distances
import code.util as util




results_dir = "data/results"
plots_dir = os.path.join(results_dir, "plots")
if not os.path.isdir(plots_dir):
    os.makedirs(plots_dir)

pd.set_option('display.max_rows', None)

config_path = "membership_lingdata_config.json"

database.read_config(config_path)
df = database.data()

big_matrix = []
for i,row in df.iterrows():
    matrix = row["value_number_matrix"]
    while len(counts) < len(matrix):
        big_matrix.append([])
    for i, counts in enumerate(matrix):
        while len(counts) >= len(big_matrix[i]):
            big_matrix[i].append(0)
        for j, count in enumerate(counts):
            big_matrix[i][j] += count

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_prop_cycle(color=[cm(1.*i/len(big_matrix)) for i in range(len(big_matrix))])
x = len(big_matrix)
y_old = [0 for in in range(len(big_matrix))]
for count in range(len(big_matrix)):
    y_new = []
    for group in big_matrix:
        if count >= len(group):
            y_new.append(0)
        else:
            y_new.append(group[count])
    ax.bar(x, y_new, bottom=y_old, color=ccm(1.*count/len(big_matrix)))
    for i in range(len(big_matrix)):
        y_old[i] = y_old[i] + y_new[i]
plt.savefig(os.path.join(plots_dir, "stacked.png"))
plt.clf()
