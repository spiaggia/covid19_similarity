import pandas as pd

dist_df = pd.read_csv('results/log_20200517_231124.csv', index_col=0)

ddf = dist_df.groupby('version1')
network_df = dist_df.loc[ddf['dist'].idxmax(),:]
#network_df = pd.concat([network_df, dist_df[dist_df['dist'] > dist_df["dist"].quantile(0.8)]])
network_df = pd.concat([network_df, dist_df[dist_df['dist'] > 0.999]])

print(network_df)

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

network_df["node1"] =  network_df["version1"] + "-" +  network_df["country_code1"]
network_df["node2"] =  network_df["version2"] + "-" +  network_df["country_code2"]

feature_1 = network_df["node1"]
feature_2 = network_df["node2"]
dist = network_df["dist"]

df = pd.DataFrame({'f1': feature_1, 'f2': feature_2, 'score': dist})
print(df)

G = nx.from_pandas_edgelist(df=df, source='f1', target='f2', edge_attr='score')
pos = nx.spring_layout(G)  # For better example looking
nx.draw(G, pos, with_labels=True)
labels = {e: G.edges[e]['score'] for e in G.edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size = 6)
plt.show()
