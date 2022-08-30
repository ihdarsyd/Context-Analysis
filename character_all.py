#%%
import os, pandas as pd, numpy as np, itertools, sys
from datetime import datetime
import matplotlib.pyplot as plt

from _helpers.secret import *
from _helpers.dbconn import mongodb
from datetime import timedelta

from bson import json_util, ObjectId
import json
#%%
def menghitung_threshold(df, jumlah_data):
    df_data = pd.DataFrame(df.sum(axis = 0, skipna = True))
    t = []
    n = 8
    N = jumlah_data
    e = 0
    for x in df_data.index:
        e = e + (df_data[0][x]/n)
    return (e/N)
#%%
def inner_product(df1, df2, five_personality):
    tot = 0
    for idx in df1.index:
        tot += (df1[0][idx]*df2[five_personality][idx])
    return tot
#%%
collection = mongodb.data_user
tweets = collection.find()

sanitized = json.loads(json_util.dumps(tweets))
normalized = pd.json_normalize(sanitized)
df_tweets = pd.DataFrame(normalized)

df_nrc = pd.read_excel('nrc_bahasa_unique.xlsx','Metadata1')
df_five = pd.read_excel('nrc_bahasa_unique.xlsx','Metadata2')
df_five = df_five.set_index("Trait")

group_user = df_tweets.groupby('user.screen_name')
character_all_user = pd.DataFrame()
# %%
for group_name, df_group in group_user:
    df_tweets['character'] = 0
    index = []
    #df = df.iloc[0:3,:]
    df_average = pd.DataFrame()
    for x in df_group.index:
        df_keywords = pd.DataFrame()
        for keyword in df_tweets['keywords'][x]:
            temp = df_nrc.loc[df_nrc['Indonesian (id)'] == keyword]
            if(len(temp) != 0 ):
                df_keywords = df_keywords.append(temp, sort=False, ignore_index=True)
        if(len(df_keywords)!=0):
            index.append(x)
            df_keywords = pd.DataFrame(df_keywords.sum(axis = 0, skipna = True)).T
            df_keywords.drop('Indonesian (id)', inplace=True, axis=1)
            df_average = df_average.append(df_keywords, ignore_index=False)
    df_average.index = index
    t = menghitung_threshold(df_average, len(df_tweets))
    df_average = pd.DataFrame(df_average.mean())
    df_average.loc[df_average[0] < t] = 0
    df_average.loc[df_average[0] >= t] = 1

    five_personality = ['Openness', 'Conscientiousness', 'Extraversion','Agreeableness', 'Neuroticism']
    result = []
    for i in range(len(five_personality)):
        result.append(inner_product(df_average,df_five.sort_index(),five_personality[i]))

    personality = pd.DataFrame(result, index=five_personality)
    # personality = personality.sort_values(by=[0], ascending=False)
    # print(personality.iloc[0].to_numpy())
    personality = personality.T
    personality.index = [group_name]
    character_all_user = character_all_user.append(personality)
# %%
character_all_user.to_excel("all_character_user.xlsx")

# %%
