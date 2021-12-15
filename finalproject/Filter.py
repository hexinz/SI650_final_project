import sqlite3
import numpy as np
import pandas as pd
from tqdm import tqdm

def load_mat():
    connection = sqlite3.connect("db.sqlite3")
    cursor = connection.cursor()
    query_user = "SELECT id, username FROM auth_user"
    query_rating = "SELECT * FROM searchengine_fav"
    users = cursor.execute(query_user).fetchall()
    ratings = cursor.execute(query_rating).fetchall()
    connection.close()

    user_id, user_name = [], []
    for i in users:
        user_id.append(i[0])
        user_name.append(i[1])
    users_df = pd.DataFrame({'user_id': user_id, 'user_name': user_name})

    episode_id, user_id_fk, rating = [], [], []
    for i in ratings:
        episode_id.append(i[2])
        user_id_fk.append(i[3])
        rating.append(i[1])
    ratings_df = pd.DataFrame({'episode_id': episode_id, 'user_id': user_id_fk, 'rating': rating})

    data = users_df.merge(ratings_df, on='user_id', how='left')
    origin_mat = data.pivot(index='episode_id', columns='user_name', values='rating').T
    new_mat = data.pivot(index='episode_id', columns='user_name', values='rating').T
    for i in range(new_mat.shape[1]):
        new_mat[i] = new_mat[i].apply(lambda x: x - np.mean(new_mat[i]))
    return data, origin_mat, new_mat

def Item_Item_Cos_Sim(mat):
    cosine_similarity = np.zeros((mat.shape[1], mat.shape[1]))
    for i in tqdm(range(mat.shape[1])):
        for j in range(mat.shape[1]):
            if i < j:
                temp = mat[[i, j]].dropna(axis=0)
                a = np.array(temp[i])
                b = np.array(temp[j])
                if np.sum(a) != 0 and np.sum(b) != 0:
                    cosine_similarity[i][j] = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
                else:
                    cosine_similarity[i][j] = None
    return cosine_similarity.T + cosine_similarity

data, origin_mat, new_mat = load_mat()
cosine_similarity = Item_Item_Cos_Sim(new_mat)

def Item_Item_Filter(username):
    result = np.zeros(new_mat.shape[1])
    for i in range(new_mat.shape[1]):
        isfull = 1
        if np.isnan(origin_mat.loc[username, i]):
            isfull = 0
            coeff,cos_sim = [],[]
            for idx, j in enumerate(cosine_similarity[i]):
                if j > 0.5 and not np.isnan(origin_mat.loc[username,idx]):
                    coeff.append(origin_mat.loc[username,idx])
                    cos_sim.append(j)
            if coeff != [] and cos_sim != []:
                result[i] = np.dot(np.array(coeff),np.array(cos_sim)) / np.sum(cos_sim)
    return result.argsort()[::-1][:5]


# Item_Item_Filter('Cora')
