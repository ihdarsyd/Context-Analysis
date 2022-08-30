#%%
import os, pandas as pd, numpy as np, itertools, sys

df_kamus = pd.read_excel('NRC.xlsx')

kamus_bahasa = df_kamus.loc[:, ['Indonesian (id)', 'Anger','Anticipation','Disgust',	'Fear',	'Joy',	'Sadness',	'Surprise',	'Trust']]
kamus_bahasa.to_excel("nrc_bahas.xlsx",index=False)
# %%
