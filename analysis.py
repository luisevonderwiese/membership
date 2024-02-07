import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from tabulate import tabulate
import math
from scipy import stats
import numpy as np

from lingdata import database
from lingdata.categorical import CategoricalData

import code.distances as distances
from code.distances import DistanceMatrixIO
import code.util as util




results_dir = "data/results"
plots_dir = os.path.join(results_dir, "plots")
if not os.path.isdir(plots_dir):
    os.makedirs(plots_dir)

pd.set_option('display.max_rows', None)

config_path = "membership_lingdata_config.json"

database.read_config(config_path)
df = database.data()

results_df = pd.read_csv(os.path.join(results_dir, "results.csv"), sep = ";")
df = pd.merge(df, results_df, how = 'left', left_on=["ds_id", "source", "ling_type", "family"], right_on = ["ds_id", "source", "ling_type", "family"])
print(df)

plt.axline([0, 0], slope=1, color = 'lightgray', linewidth = 1, linestyle = "--")
plt.scatter(df["gq_glottolog_bin"], df["gq_glottolog_membership"], s=10)
plt.xlabel('bin')
plt.ylabel('membership')
plt.savefig(os.path.join(plots_dir, "scatter_gq.png"))
plt.clf()
