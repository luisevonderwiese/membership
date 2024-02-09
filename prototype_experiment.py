import os
import pandas as pd
import numpy as np

import lingdata.database as database

import code.raxmlng as raxmlng
import code.distances as distances
import code.pythia as pythia
import code.util as util
import matplotlib.pyplot as plt




def run_raxml_ng(df):
    for (i, row) in df.iterrows():
        raxmlng.run_search1(row["msa_paths"]["prototype"], row["MULTI_xGTR_prototype"], util.prefix(results_dir, row, "raxmlng", "prototype"))

def write_results_df(df):
    sampled_difficulties = []
    for i, row in df.iterrows():
        df.at[i, "difficulty"] = pythia.get_difficulty(util.prefix(results_dir, row, "pythia", "prototype"))
        df.at[i, "rate_matrix"] = raxmlng.get_matrix(util.prefix(results_dir, row, "raxmlng", "prototype"))
    print_df = df[["ds_id", "source", "ling_type", "family", "difficulty", "rate_matrix"]]
    print(print_df)
    print_df.to_csv(os.path.join(results_dir, "prototype_results.csv"), sep = ";")


def run_pythia(df):
    for (i, row) in df.iterrows():
        pythia.run_with_padding(row["msa_paths"]["prototype"], util.prefix(results_dir, row, "pythia", "prototype"))

def to_matrix(rates, x):
    matrix = [[0 for i in range(x)] for j in range(x)]
    for col_idx in range(x):
        for row_idx in range(col_idx):
            idx = sum(range(x-row_idx, x)) + col_idx - row_idx - 1
            rate = rates[idx]
            matrix[col_idx][row_idx] = rate
            matrix[row_idx][col_idx] = rate
    return matrix

def plot_heatmaps(df):
    for i,row in df.iterrows():
        rates = raxmlng.substitution_rates(util.prefix(results_dir, row, "raxmlng", "prototype"))
        rate_matrix = to_matrix(rates, row["max_values_prototype"])
        rate_matrix = np.array(rate_matrix)
        plt.imshow(rate_matrix)
        plt.colorbar()
        plt.savefig(os.path.join(plots_dir, row["ds_id"] + "_rates.png"))
        plt.clf()



raxmlng.exe_path = "./bin/raxml-ng"
pythia.raxmlng_path = "./bin/raxml-ng"
pythia.predictor_path = "predictors/latest.pckl"
distances.exe_path = "./bin/qdist"
config_path = "prototype_lingdata_config.json"
results_dir = "data/results"
plots_dir = os.path.join(results_dir, "heatmaps")
if not os.path.isdir(plots_dir):
    os.makedirs(plots_dir)



database.read_config(config_path)
#database.download()
database.compile()
df = database.data()
pd.set_option('display.max_rows', None)
print(df)

run_raxml_ng(df)
plot_heatmaps(df)
