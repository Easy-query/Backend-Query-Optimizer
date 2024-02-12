import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

queries_df = pd.read_csv("./queries.csv")


# Define function to preprocess SQL queries
def clean_query(query):
    # Normalize spaces
    query = re.sub(r'\s+', ' ', query)

    # Lowercase the query
    query = query.lower()

    # Replace variable values (e.g., numbers and strings) with placeholders
    query = re.sub(r'\b\d+\b', '<NUM>', query)
    query = re.sub(r"'(.*?)'", '<STRING>', query)

    return query


# Preprocess SQL queries

""" create search function
    == compute the similarity between the term we entered and the movie list"""


def search(query):
    queries_df["clean_query"] = queries_df["unoptimized_query"].apply(clean_query)

    # instantiating the class
    vectorized = TfidfVectorizer(ngram_range=(1, 2))  # looking at groups of 1 and 2 words

    # creating a matrix of vector for each query
    tfidf = vectorized.fit_transform(queries_df["clean_query"])

    query = clean_query(query)
    query_vec = vectorized.transform([query])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -3)[-3:]
    results = queries_df.iloc[indices][::-1]
    return results
