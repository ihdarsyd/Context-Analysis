#%%
import os, pandas as pd, numpy as np, itertools, sys
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from numpy.random import RandomState
from sklearn.cluster import AgglomerativeClustering

df = pd.read_excel('all_character_user.xlsx','Sheet1',index_col=0)

# %%
k = 5
p = 10
data_centroid=[]
for x in range(p):
    kmeans = KMeans(n_clusters=k, random_state= RandomState())
    kmeans.fit(df)
    data_centroid.append(kmeans.cluster_centers_[0])
    data_centroid.append(kmeans.cluster_centers_[1])
    data_centroid.append(kmeans.cluster_centers_[2])
    data_centroid.append(kmeans.cluster_centers_[3])
    data_centroid.append(kmeans.cluster_centers_[4])

# %%
#Hierarchical clustering menggunakan dataset centroid(20)
clustering = AgglomerativeClustering(n_clusters = k).fit(data_centroid)
y_pred = clustering.fit_predict(data_centroid)

#Mencari centroid dari hasil Hierarchical clustering
centroid_data = pd.DataFrame(data_centroid)
centroid_data.insert(0,'class',y_pred)
new_centroid = centroid_data.groupby("class").mean().values

# Kmeans akhir
kmeans_new = KMeans(n_clusters=k, init=new_centroid)
kmeans_new.fit(df)
kmeans_new.predict(df)
new_label = kmeans_new.labels_

df['cluster_label'] = new_label
df.to_excel("character_cluster.xlsx")
# %% Groupby Cluster
group_label = pd.read_excel('character_cluster.xlsx',index_col=0)

x = group_label.groupby('cluster_label')
label_0 = len(x.get_group(0))
label_1 = len(x.get_group(1))
label_2 = len(x.get_group(2))
label_3 = len(x.get_group(3))
label_4 = len(x.get_group(4))
# %%
x.size().plot(kind = "bar")
group_label['cluster_label'].value_counts()
# %%
