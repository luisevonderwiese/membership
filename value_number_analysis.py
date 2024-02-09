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
    matrix_string = row["value_number_matrix"]
    matrix = []
    for el in matrix_string[2:-2].split("], ["):
        if el == "[]" or el == "":
            matrix.append([])
        else:
            matrix.append([int(inner_el) for inner_el in el.split(", ")])

    #matrix = [[] if el == "[]" else [int(inner_el) for inner_el in el.split(", ")] for el in matrix_string.strip("[]").split("], [")]
    while len(big_matrix) < len(matrix):
        big_matrix.append([])
    for i, counts in enumerate(matrix):
        while len(counts) >= len(big_matrix[i]):
            big_matrix[i].append(0)
        for j, count in enumerate(counts):
            big_matrix[i][j] += count

print(big_matrix)
fig,ax = plt.subplots(figsize=(40, 30))
#cm = plt.get_cmap('gist_rainbow')
#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.set_prop_cycle(color=[cm(1.*i/len(big_matrix)) for i in range(len(big_matrix))])
x = range(len(big_matrix))
print(len(big_matrix))
max_len = max([len(el) for el in big_matrix])
print(max_len)
y_old = [0 for el in x]
for count in range(max_len):
    y_new = []
    for group in big_matrix:
        if count >= len(group):
            y_new.append(0)
        else:
            y_new.append(group[count])
    #ax.bar(x, y_new, bottom=y_old, color=cm(1.*count/len(big_matrix)))
    ax.bar(x, y_new, bottom=y_old, label = str(count))
    for i in range(len(big_matrix)):
        y_old[i] = y_old[i] + y_new[i]
ax.legend()
plt.savefig(os.path.join(plots_dir, "stacked.png"))
plt.clf()

all_counts = [row["value_number_counts"] for i,row in df.iterrows()]
max_num = max([len(counts) for counts in all_counts])
fig,ax = plt.subplots(figsize=(40, 30))
x = range(len(all_counts))
y_old = [0 for el in x]
for num in range(max_num):
    y_new = [counts[num] for counts in all_counts]
    ax.bar(x, y_new, bottom=y_old, label = str(num))
    for i in x:
        y_old[i] = y_old[i] + y_new[i]
ax.legend()
plt.savefig(os.path.join(plots_dir, "stacked_per_dataset.png"))
plt.clf()
