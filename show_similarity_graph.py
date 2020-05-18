import os
import datetime
from glob import glob
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

now = datetime.datetime.now()
filename = './image/log_' + now.strftime('%Y%m%d_%H%M%S') + '.png'

def get_latest_modified_file_path(dirname):
  target = os.path.join(dirname, '*')
  files = [(f, os.path.getmtime(f)) for f in glob(target)]
  latest_modified_file_path = sorted(files, key=lambda files: files[1])[-1]
  print(latest_modified_file_path[0])
  return latest_modified_file_path[0]

dist_df = pd.read_csv(get_latest_modified_file_path("results"))
print(dist_df)

ddf = dist_df.groupby('version1')
network_df = dist_df.loc[ddf['dist'].idxmax(),:]
print(network_df)
# network_df = dist_df
network_df = network_df[network_df['dist'] > 0.9]
network_df = pd.concat([network_df, dist_df[dist_df['dist'] > 0.999]])



network_df["source"] =  network_df["version1"] + "-" +  network_df["country_code1"]
network_df["target"] =  network_df["version2"] + "-" +  network_df["country_code2"]
network_df["weight"] =  network_df["dist"] **10 * 100


print(network_df.sort_values("weight"))


G = nx.from_pandas_edgelist(network_df, edge_attr=True)

plt.figure(figsize=(50,50))
pos = nx.spring_layout(G, k=1)

nx.draw_networkx_nodes(G, pos, node_color='w',alpha=0.6, node_size=2)
nx.draw_networkx_labels(G, pos, fontsize=14, font_family="Yu Gothic", font_weight="bold")

nx.draw_networkx_edges(G, pos, alpha=0.4, edge_color='C', width=1)

plt.axis('off')
plt.savefig(filename)
os.system('open ' + get_latest_modified_file_path("image"))
# plt.show()

