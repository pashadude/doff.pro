import math
from sklearn.feature_extraction.text import TfidfVectorizer


class SimilarityMeasures:
    def jaccard_similarity(self, vector1, vector2):
        intersection_cardinality = len(set.intersection(*[set(vector1), set(vector2)]))
        union_cardinality = len(set.union(*[set(vector1), set(vector2)]))
        return intersection_cardinality / float(union_cardinality)

    def cosine_similarity(self, vector1, vector2):
        dot_product = sum(p * q for p, q in zip(vector1, vector2))
        magnitude = math.sqrt(sum([val ** 2 for val in vector1])) * math.sqrt(sum([val ** 2 for val in vector2]))
        if not magnitude:
            return 0
        return dot_product / magnitude

    def tf_idf(self, documents):
        tfidf = TfidfVectorizer().fit_transform(documents)
        return tfidf

    def tf_idf_cosine(self, tfidf):
        tf_idf_cosine_results = []
        for count_0, doc_0 in enumerate(tfidf.toarray()):
            for count_1, doc_1 in enumerate(tfidf.toarray()):
                tf_idf_cosine_results.append((self.cosine_similarity(doc_0, doc_1), count_0, count_1))
        return tf_idf_cosine_results
