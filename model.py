"""Game Recommendation System Model"""

import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from scipy.sparse import hstack

# Read the CSV file with the correct encoding and quoting
dataset1 = pd.read_csv('games.csv', index_col=False, sep=",")
dataset1 = dataset1[:20000]

# Select needed columns
needed_columns = ['AppID', 'Name', 'Release date', 'Tags', 'Genres', 'Supported languages']
dataset1 = dataset1[needed_columns]
dataset1 = dataset1.rename(columns={
    'Supported languages': 'Description'
})

# Fill NaN values and clean the text fields
dataset1['Tags'] = dataset1['Tags'].fillna('')
dataset1['Tags'] = dataset1['Tags'].apply(
    lambda tag: ' '.join(f'"{t.strip()}"' for t in sorted(tag.split(',')))
)

dataset1['Genres'] = dataset1['Genres'].fillna('')
dataset1['Genres'] = dataset1['Genres'].apply(
    lambda genre: ' '.join(f'"{g.strip()}"' for g in sorted(genre.replace('"', '').split(',')))
)

dataset1['Description'] = dataset1['Description'].fillna('')

# Create TF-IDF vectors
tfid = TfidfVectorizer(token_pattern=r'"[^"]+"')
tfid2 = TfidfVectorizer(token_pattern=r'"[^"]+"')
tfid3 = TfidfVectorizer(stop_words='english')

# Create matrices
matrix_tag = tfid.fit_transform(dataset1['Tags'])
matrix_genre = tfid2.fit_transform(dataset1['Genres'])
matrix_desc = tfid3.fit_transform(dataset1['Description'])

# Combine matrices of tags and genres
combined_sparse_matrix = hstack([matrix_tag, matrix_genre])

# Calculate similarity matrices
cosine_sim_tag = linear_kernel(matrix_tag, matrix_tag)
cosine_sim_genre = linear_kernel(matrix_genre, matrix_genre)
cosine_sim_desc = linear_kernel(matrix_desc, matrix_desc) 
cosine_sim_combined = linear_kernel(combined_sparse_matrix, combined_sparse_matrix)

indices = pd.Series(dataset1.index, index=dataset1['Name']).drop_duplicates()

def get_all_game_names():
    return dataset1['Name'].unique()

def get_all_tags():
    tag_list = set()
    for tags in dataset1['Tags']:
        matched = re.findall(r'"([^"]+)"', tags)
        tag_list.update(matched)
    sorted_tag_list = sorted(list(tag_list))
    return sorted_tag_list

def get_all_genres():
    genre_list = set()
    for genre in dataset1['Genres']:
        matched = re.findall(r'"([^"]+)"', genre)
        genre_list.update(matched)
    sorted_genre_list = sorted(list(genre_list))
    return sorted_genre_list

def recommend(name, cosine_):
    """Recommend games based on game name"""
    idx = indices[name]
    
    sim_scores = list(enumerate(cosine_[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    
    max_score = cosine_.max()

    game_indices = [i[0] for i in sim_scores]
    
    result = dataset1[['Name', 'Tags', 'Genres', 'Description']].iloc[game_indices].copy()
    
    max_score = cosine_.max()
    result['Score(%)'] = [((score / max_score) * 100).round(2) for _, score in sim_scores]
    
    return result


def recommend_by(data, current_tfid, matrix_):
    """Recommend games based on genres (tags)"""

    data = ' '.join(f'"{a}"' for a in sorted(data))
    
    current_matrix = current_tfid.transform([data])
    
    current_cosine_ = linear_kernel(current_matrix, matrix_)
    
    sim_scores = list(enumerate(current_cosine_[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    
    game_indices = [i[0] for i in sim_scores]
    
    result = dataset1[['Name', 'Tags', 'Genres', 'Description']].iloc[game_indices].copy()
    
    max_score = current_cosine_.max()
    result['Score(%)'] = [((score / max_score) * 100).round(2) for _, score in sim_scores]
    
    return result

def recommend_by_description(description_text):
    """Recommend games based on description text."""

    desc_vector = tfid3.transform([description_text])
    cosine_scores = linear_kernel(desc_vector, matrix_desc)

    sim_scores = list(enumerate(cosine_scores[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:21]
    
    game_indices = [i[0] for i in sim_scores]
    result = dataset1[['Name', 'Tags', 'Genres', 'Description']].iloc[game_indices].copy()
    
    max_score = cosine_scores.max()
    result['Score(%)'] = [((score / max_score) * 100).round(2) for _, score in sim_scores]

    return result



# game_to_test = "Dungeonball"
# print(f'Tag dari "{game_to_test}" adalah: {dataset1["Tags"][indices[game_to_test]]}\n\nHasil rekomendasi:')
# print(recommend(game_to_test, cosine_sim_tag))

# print(f'Genre dari "{game_to_test}" adalah: {dataset1["Genres"][indices[game_to_test]]}\n\nHasil rekomendasi:')
# print(recommend(game_to_test, cosine_sim_genre))

# print(f'Hasil rekomendasi combined dari "{game_to_test}":')
# print(recommend(game_to_test, cosine_sim_combined).head())

# tags = ["Adventure", "Action", "Indie", "Casual", "Simulation", "RPG", "Racing"]
# print(f'Hasil rekomendasi dari tag "{tags}"')
# recommend_by(tags, tfid, matrix_tag)

# genre = ["Co-op", "Multi-player"]
# print(f'Hasil rekomendasi dari genre "{genre}"')
# recommend_by(genre, tfid2, matrix_genre)

# strings = 'A game about a cat'
# print(f'Recommendations based on description: {strings}')
# print(recommend_by_description(strings))