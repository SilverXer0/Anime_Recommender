import pandas as pd 
import embeddinghub as eh

#current issue with the import statement - not running

anime_list = pd.read_csv('anime.csv')  # loads csv file into dataframe to be read

genre_df= anime_list["genre"].str.get_dummies(sep=",")
num_genres = len(genre_df.columns)

# embeds genres as one hot encoding - allows for better results/predictions to be made

genre_df = pd.merge(anime_list[['anime_id','name']] , genre_df , left_index=True, right_index=True)

# Note: dimension # of each embedding is the total number of collumns(which is number of genres)
# add anime id to and the anime's name to the variable genre_df

genre_df = genre_df.head(2000)

# Note: there is an issue with embeddinghub that limits the maximum number of elements in a vector space
# Therefore, only the first 2000 animes are considered, hence the code above

hub = eh.connect(eh.LocalConfig("data/"))

space = hub.create_space("anime", dims=num_genres)

# creates vector space with dimension equal to the number of genres
# Represents the one hot encoding of the different anime
#Note: Localconfig is being used, which means that the embeddings are stored and indexed locally.
# Can use 'docker run featureformcom/embeddinghub -p 7462:7462' and 'hub = eh.connect(eh.Config())' which will run embeddinghub as a docker

emb = {}
# embeddinghub needs the embeddings in the form of a hashmap/dictionary

for idx,anime in genre_df.iterrows():
    key = anime['name']
    embedding = anime.to_list()[2:]
    emb[key] = embedding

space.multiset(emb)

# keeps embeddings in bulk

neighbors = space.nearest_neighbors(key="Kizumonogatari II: Nekketsu-hen", num=5)

print(
    anime_list[anime_list['name'] == 'Kizumonogatari II: Nekketsu-hen']['genre']
)

# tested for that anime

for neighbor in neighbors:
    print(neighbor)
    print(
    anime_list[anime_list['name'] == neighbor]['genre']
)