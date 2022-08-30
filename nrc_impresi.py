#%%
import os, pandas as pd, numpy as np, itertools, sys
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

#%%
df_affective = pd.read_excel('adjective.xlsx','affective_space2')
df_nrc = pd.read_excel('nrc_bahas.xlsx','Metadata1')
# %%

# %%
temp = df_nrc.groupby("Indonesian (id)").sum()
temp[temp>=1] = int(1)
temp.to_excel("nrc_bahasa_unique.xlsx")
# %%
df_nrc = pd.read_excel('nrc_bahasa_unique.xlsx')
concat = df_nrc[df_nrc["Indonesian (id)"].isin(df_affective['value'].values)]
concat.to_excel("nrc_impresi.xlsx",index=False)
# %%
df_nrc = pd.read_excel('nrc_bahasa_unique.xlsx','Metadata1')

factory = StemmerFactory()
stemmer = factory.create_stemmer()
for x in df_nrc.index:
    df_nrc["Indonesian (id)"][x] = stemmer.stem(df_nrc["Indonesian (id)"][x])

# %%
df_nrc.to_excel("nrc_stemming.xlsx",index=False)