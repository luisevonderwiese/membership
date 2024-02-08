import os
import shutil

results_dir = "data/results/raxmlng/"
for identifier in os.listdir(results_dir):
    best_tree_path = os.path.join(results_dir, identifier, "bin.raxml.bestTree")
    if os.path.isfile(best_tree_path):
        print(identifier)
        dest_path = os.path.join("trees", identifier + ".tree")
        shutil.copyfile(best_tree_path, dest_path)
