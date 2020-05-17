import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

dist_df = pd.read_csv('results/log_20200517_231124.csv', index_col=0)

ddf = dist_df.groupby('version1')
network_df = dist_df.loc[ddf['dist'].idxmax(),:]
network_df = pd.concat([network_df, dist_df[dist_df['dist'] > 0.999]])

print(network_df)


network_df["node1"] =  network_df["version1"] + "-" +  network_df["country_code1"]
network_df["node2"] =  network_df["version2"] + "-" +  network_df["country_code2"]

feature_1 = network_df["node1"]
feature_2 = network_df["node2"]
dist = network_df["dist"]

df = pd.DataFrame({'f1': feature_1, 'f2': feature_2, 'score': dist})
print(df)

G = nx.from_pandas_edgelist(df=df, source='f1', target='f2', edge_attr='score')

plt.figure(figsize=(15,15))
pos = nx.spring_layout(G, k=0.3)

nx.draw_networkx_nodes(G, pos, node_color='w',alpha=0.6, node_size=2)
nx.draw_networkx_labels(G, pos, fontsize=14, font_family="Yu Gothic", font_weight="bold")

nx.draw_networkx_edges(G, pos, alpha=0.4, edge_color='C', width=1)

plt.axis('off')
plt.savefig("g2.png")
plt.show()
