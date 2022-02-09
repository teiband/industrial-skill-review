# Code for extraction of clusters and information
This folder provides the code used for extracting the information from the review table. 

## Preprocessing
In order to run the clustering and extract information from the review table which is saved under `data/in` you need to run the `pre_processing.py`. While you run the code you can select which column to extract and where to save the information.

## Wordcloud generation
After the data have been processed you can also generate your own wordcloud depending on the column you are interested of. For doing so run the script `create_wordcloud.py`.

## Clustering
If you want to perform some clustering from the extracted keywords you can use the supporting jupyter notebooks which can be found under the folder [`FaissSearch`](FaissSearch/) if you would like to perform searches and clusterings using [faiss](https://github.com/facebookresearch/faiss). Otherwise, you can use the [`taxonomySearch`](taxonomySearch/) in case you would like to cluster with [scikit-learn](https://scikit-learn.org/stable/). For the paper outcomes `scikit-learn` has been used. Within this folder three clustering approaches are available, one with [HDBSCAN](https://hdbscan.readthedocs.io/en/latest/how_hdbscan_works.html), one with [Kmeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html) and one for hierarcical clustering. Feel free to choose the one you like the most.

