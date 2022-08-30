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
collection = mongodb.data_user
tweets = collection.find()

sanitized = json.loads(json_util.dumps(tweets))
normalized = pd.json_normalize(sanitized)
df_tweets = pd.DataFrame(normalized)

#%%
df_tweets = df_tweets['user.screen_name'].value_counts()
df_tweets.to_excel("count_user.xlsx")


# %%
