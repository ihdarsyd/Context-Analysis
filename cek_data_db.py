#%%
from _helpers.secret import *
from _helpers.dbconn import mongodb
from datetime import timedelta
import pandas as pd

collection = mongodb.tweet
tweets = collection.find()

if tweets.count()==0:
    print("Empty Cursor")
else:
    print("Cursor is Not Empty")
    df_tweets = pd.DataFrame(tweets)
# %%
