import pandas as pd
import matplotlib.pyplot as plt

thisdir = "/home/krose/iHeart/"

#load the three tables
df1 = pd.read_table(thisdir + "users.tsv")
df2 = pd.read_table(thisdir + "listens.tsv")
df3 = pd.read_table(thisdir + "artists.tsv")

#join list of users with their listens (inner join to get only active users)
df4 = pd.merge(df1, df2, on='profile_id', how='inner')

#now join artist seeds with artists by artist_id to get genres for each listen
df5 = pd.merge(df4, df3, how='left', left_on='artist_seed', right_on='artist_id') 

#Get list of top 10 genres
top10genres = df5.groupby('genre').count().sort_values('profile_id', ascending=False).head(10).index.tolist()

#extract non-null entries of age and gender
df5_with_ages = df5.loc[df5['age'].notnull()]
df5_with_genders = df5.loc[df5['gender'].notnull()]

#Make containers for extracted data
#unique = unique profile id
unique_male = dict()
unique_female = dict()
all_male = dict()
all_female = dict()

unique_ages = dict()
total_ages = dict()

#Extract age and gender by genre
for this_genre in top10genres:
    df5_with_genders_thisgenre = df5_with_genders.loc[df5_with_genders['genre']==this_genre]

    total_with_genders = float(len(df5_with_genders_thisgenre.profile_id.tolist()))
    unique_with_genders = float(len(df5_with_genders_thisgenre.profile_id.unique().tolist()))

    unique_male[this_genre] = len(df5_with_genders_thisgenre.loc[df5_with_genders_thisgenre['gender']=='MALE'].profile_id.unique().tolist()) / unique_with_genders
    unique_female[this_genre] = len(df5_with_genders_thisgenre.loc[df5_with_genders_thisgenre['gender']=='FEMALE'].profile_id.unique().tolist()) / unique_with_genders

    all_male[this_genre] = len(df5_with_genders_thisgenre.loc[df5_with_genders_thisgenre['gender']=='MALE'].profile_id.tolist()) / total_with_genders
    all_female[this_genre] = len(df5_with_genders_thisgenre.loc[df5_with_genders_thisgenre['gender']=='FEMALE'].profile_id.tolist()) / total_with_genders


    df5_with_ages_thisgenre = df5_with_ages.loc[df5_with_ages['genre']==this_genre]
    
    total_ages[this_genre] = df5_with_ages_thisgenre['age'].tolist()
    unique_ages[this_genre] = df5_with_ages_thisgenre.drop_duplicates(subset='profile_id')['age'].tolist()


#Save visualization of unique listens by genre and gender
p1 = plt.bar(range(len(unique_male)), unique_male.values(), align='center')
p2 = plt.bar(range(len(unique_male)), unique_female.values(), bottom=unique_male.values(), color='#d62728')
plt.ylabel('Fraction of total unique')
plt.title('Fraction of unique listeners by genre and gender')
plt.legend((p1[0], p2[0]), ('MALE', 'FEMALE'))
plt.xticks(range(len(unique_male)), unique_male.keys(), rotation=25)
plt.savefig(thisdir+"fraction_of_unique_by_gender.pdf")

plt.close()

#total listens by genre and gender
p3 = plt.bar(range(len(all_male)), all_male.values(), align='center')
p4 = plt.bar(range(len(all_male)), all_female.values(), bottom=all_male.values(), color='#d62728')
plt.ylabel('Fraction of total listens')
plt.title('Fraction of total listeners by genre and gender')
plt.legend((p3[0], p4[0]), ('MALE', 'FEMALE'))
plt.xticks(range(len(all_male)), all_male.keys(), rotation=25)
plt.savefig(thisdir+"fraction_of_total_by_gender.pdf")

plt.close()
#total listens by age and genre
b1 = plt.boxplot(total_ages.values(), showfliers=False)
plt.ylabel('Age of all listeners by genre')
plt.xticks(range(len(total_ages)), total_ages.keys(), rotation=25)
plt.savefig(thisdir+"age_of_total_by_genre.pdf")

plt.close()
#unique listens by age and genre
b2 = plt.boxplot(unique_ages.values(), showfliers=False)
plt.ylabel('Age of unique listeners by genre')
plt.xticks(range(len(unique_ages)), unique_ages.keys(), rotation=25)
plt.savefig(thisdir+"age_of_unique_by_genre.pdf")

