import pandas as pd
from scipy.stats import ks_2samp

df1 = pd.read_table("/home/krose/iHeart/users.tsv")
df2 = pd.read_table("/home/krose/iHeart/listens.tsv")

df3 = pd.merge(df1, df2, on='profile_id', how='left')

#Separate users into active and inactive based on existence of an entry
#in the listens table

df_active = df3.loc[df3['listen_date'].notnull()]
df_inactive = df3.loc[df3['listen_date'].isnull()]

#Screen out any entries where the user does not have an age, also select
#only one entry for each profile_id

df_active_ages = df_active.loc[df_active['age'].notnull()].drop_duplicates(subset='profile_id')
df_inactive_ages = df_inactive.loc[df_inactive['age'].notnull()].drop_duplicates(subset='profile_id')


#Fetch mean ages
print df_active_ages['age'].mean(), df_inactive_ages['age'].mean()

#Do Kolmogorov-Smirnov testing between compatibility of each dataset
print ks_2samp(df_active_ages['age'], df_inactive_ages['age'])
