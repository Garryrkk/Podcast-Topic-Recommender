from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import spacy

nlp = spacy.load("en_core_web_sm")

def clean_texts(texts):
    return [" ".join([token.lemma_ for token in nlp(text.lower()) if not token.is_stop and token.is_alpha]) for text in texts]

def get_clusters(texts, n_clusters=5):
    cleaned = clean_texts(texts)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(cleaned)
    model = KMeans(n_clusters=n_clusters)
    model.fit(X)
    labels = model.labels_
    clusters = {i: [] for i in range(n_clusters)}
    for i, label in enumerate(labels):
        clusters[label].append(texts[i])
    return clusters
