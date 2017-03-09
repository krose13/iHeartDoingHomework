import pandas as pd

thisdir = "/home/krose/iHeart/"

#load the tables tables
df1 = pd.read_table(thisdir + "users.tsv")
df2 = pd.read_table(thisdir + "listens.tsv")

df3 = pd.merge(df1, df2, on='profile_id', how='inner')

print len(df1.profile_id.unique()), len(df2.profile_id.unique()), len(df3.profile_id.unique())
