#!/usr/bin/env python3.6
import os
import pandas as pd
from wordcloud import WordCloud
from common import *
import nltk
nltk.download('wordnet')

# better to test with: https://towardsdatascience.com/k-means-clustering-8e1e64c1561c

#### Useful functions

def preprocessSpelling(input_list, split_by_comma=True, camel_case_to_spaces=True, spaces_to_underscores=True,
                        to_lowercase=True):
    if split_by_comma:
        output_list = [s.split(',') for s in input_list if s not in ['-', '']]  # split by comma
        output_list = [item for sublist in output_list for item in sublist]  # flatten list of list
    if camel_case_to_spaces:
        output_list = [camel_case_split(s) for s in output_list]  # resolve camel case into spaces
    # if spaces_to_underscores:
    #     output_list = [n.strip().replace(' ', '_') for n in output_list]  # replace spaces with underscores
    if to_lowercase:
        output_list = [s.lower() for s in output_list]  # make all lower case
    return output_list


#### Read file with dataframe
resultsFile = "skill-taxonomy-extraction/data/in/20220118_skillTaxonomy.csv"

taxonomy = pd.read_csv(resultsFile, delimiter=';')

print(taxonomy.columns)

#### Preprocess the data by cleaning and lematization

v_lemmatizer = np.vectorize(lemmatizer)

outputList = preprocessSpelling(input_list=taxonomy['Identified primitives'].dropna())
lemmaOutputList  = v_lemmatizer(outputList)
print(lemmaOutputList)

#### Find optimal K for the KNN algorithm - NOT WORKING ON TEXT

# from sklearn.cluster import KMeans

# Sum_of_squared_distances = []
# K = range(1,150)
# for k in K:
#     km = KMeans(n_clusters=k)
#     km = km.fit(outputList)
#     Sum_of_squared_distances.append(km.inertia_)


# import matplotlib.pyplot as plt

# plt.plot(K, Sum_of_squared_distances, 'bx-')
# plt.xlabel('k')
# plt.ylabel('Sum_of_squared_distances')
# plt.title('Elbow Method For Optimal k')
# plt.show()

#### Apply clustering with optimal K
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(outputList)

true_k = 4
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
    print("Cluster %d:" % i),
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind]),
    print