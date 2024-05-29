import numpy as np
import pandas as pd
import ast

movie = pd.read_csv("Movies.csv")

movie.head(2)

credit = pd.read_csv("Credits.csv")

credit.head(2)

total= movie.merge(credit, on="title")

total.head(2)

#Selecting rows

total.columns

total = total[['movie_id','title','overview','genres','keywords','cast','crew']]
total.head(3)

total.isnull().sum()

total.dropna(inplace=True)

total.isnull().sum()

total.duplicated().sum()

def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

import ast
# ast.literal_eval(total['genres'][0])[0]

convert(total['genres'][0])

total['genres'] = total['genres'].apply(convert)

total['keywords'] = total['keywords'].apply(convert)

total['keywords']

total.head()

def convert2(obj):
    L = []
    flag = 0
    for i in ast.literal_eval(obj):
        if flag != 3:
#             print(i['name'])
            L.append(i['name'])
            flag += 1
#             print(flag)
        else:
            break
    return L

# convert2(total['cast'][0])

total['cast'] = total['cast'].apply(convert2)

def convert3(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i['job'] == "Director":
            L.append(i['name'])
    return L

total['crew'] = total['crew'].apply(convert3)

total.head(3)

total['overview'] = total['overview'].apply(lambda x: x.split())    

total['genres'] = total['genres'].apply(lambda x:[i.replace(" ","") for i in x])
total['keywords'] = total['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
total['cast'] = total['cast'].apply(lambda x:[i.replace(" ","") for i in x])
total['crew'] = total['crew'].apply(lambda x:[i.replace(" ","") for i in x])

total.head(3)

total['tags'] =total['overview'] + total['genres'] + total['keywords'] + total['cast'] + total['crew']

total.head(3)

movie_df = total[['movie_id','title','tags']]

movie_df['tags'] = movie_df['tags'].apply(lambda x:" ".join(x))

movie_df['tags'][0]

movie_df['tags'] = movie_df['tags'].apply(lambda x:x.lower())

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 5000, stop_words = "english")

vectors = cv.fit_transform(movie_df['tags']).toarray()

vectors[0]

cv.get_feature_names()

import nltk

from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

def stem(obj):
    L = []
    for i in obj.split():
        L.append(ps.stem(i))
    return ' '.join(L)

movie_df['tags'] = movie_df['tags'].apply(stem)

vectors = cv.fit_transform(movie_df['tags']).toarray()

cv.get_feature_names()

from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity(vectors)

similarity[0]

movie_df[movie_df['title'] == 'Evan Almighty'].index[0]

sorted(list(enumerate(similarity[0])), reverse=True,key = lambda x:x[1])

def recommend(movie):
    movie_index = movie_df[movie_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True,key = lambda x:x[1])[1:6]
    
    for i in movie_list:
        print(movie_df.iloc[i[0]].title)

recommend("Noah")

import pickle

pickle.dump(movie_df, open('movies.pkl','wb'))

pickle.dump(movie_df.to_dict(), open('movie_dict.pkl','wb'))

pickle.dump(similarity, open('similarity.pkl','wb'))



