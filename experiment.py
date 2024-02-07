import os
import pandas as pd
import numpy as np

import lingdata.database as database

import code.raxmlng as raxmlng
import code.distances as distances
import code.pythia as pythia
import code.util as util
from ete3 import Tree




def run_raxml_ng(df):
    for (i, row) in df.iterrows():
        raxmlng.run_inference(row["msa_paths"]["bin"], "BIN+G", util.prefix(results_dir, row, "raxmlng", "bin"))
        raxmlng.run_inference(row["msa_paths"]["membership"], "BIN+G", util.prefix(results_dir, row, "raxmlng" , "membership"), "--prob-msa on")

def write_results_df(df):
    sampled_difficulties = []
    for i, row in df.iterrows():
        alpha = raxmlng.alpha(util.prefix(results_dir, row, "raxmlng", "bin"))
        df.at[i, "alpha"] = alpha
        if alpha < 20:
            df.at[i, "heterogenity"] = 1
        else:
            df.at[i, "heterogenity"] = 0
        df.at[i, "difficulty"] = pythia.get_difficulty(util.prefix(results_dir, row, "pythia", "bin"))
        glottolog_tree_path = row["glottolog_tree_path"]
        bin_tree_path = raxmlng.best_tree_path(util.prefix(results_dir, row, "raxmlng", "bin"))
        membership_tree_path = raxmlng.best_tree_path(util.prefix(results_dir, row, "raxmlng", "membership"))
        df.at[i, "gq_glottolog_bin"] = distances.gq_distance(glottolog_tree_path, bin_tree_path)
        df.at[i, "gq_glottolog_membership"] = distances.gq_distance(glottolog_tree_path, membership_tree_path)
        if not os.path.isfile(bin_tree_path) or not os.path.isfile(membership_tree_path):
            df.at[i, "rf_bin_membership"] = float('nan')
        else:
            df.at[i, "rf_bin_membership"] = distances.rf_distance(Tree(bin_tree_path), Tree(membership_tree_path))
    print_df = df[["ds_id", "source", "ling_type", "family", "alpha", "heterogenity", "difficulty", "gq_glottolog_bin", "gq_glottolog_membership", "rf_bin_membership"]]
    print(print_df)
    print_df.to_csv(os.path.join(results_dir, "results.csv"), sep = ";")


def run_pythia(df):
    for (i, row) in df.iterrows():
        pythia.run_with_padding(row["msa_paths"]["bin"], util.prefix(results_dir, row, "pythia", "bin"))



raxmlng.exe_path = "./bin/raxml-ng"
pythia.raxmlng_path = "./bin/raxml-ng"
pythia.predictor_path = "predictors/latest.pckl"
distances.exe_path = "./bin/qdist"
config_path = "membership_lingdata_config.json"
results_dir = "data/results"



database.read_config(config_path)
#database.download()
#database.compile()
df = database.data()
pd.set_option('display.max_rows', None)
print(df)

#run_raxml_ng(df)
#run_pythia(df)
write_results_df(df)
