import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

ratings = pd.read_csv("toy_dataset.csv", index_col=0)
ratings = ratings.fillna(0)


def standardize(row):
    new_row = (row - row.mean()) / (row.max() - row.min())
    return new_row


ratings_std = ratings.apply(standardize)

item_similarity = cosine_similarity(ratings_std.T)
print(item_similarity)

item_similarity_df = pd.DataFrame(item_similarity, index=ratings.columns, columns=ratings.columns)


def get_similar_movies(movie_name, user_rating):
    similar_score = item_similarity_df[movie_name] * (user_rating - 2.5)
    similar_score = similar_score.sort_values(ascending=False)

    return similar_score


action_lover = [("action1", 5), ("romantic2", 1), ("romantic3", 1)]

similar_movies = pd.DataFrame()

for movie, rating in action_lover:
    similar_movies = similar_movies.append(get_similar_movies(movie, rating), ignore_index=True)

