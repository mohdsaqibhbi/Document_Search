import math
from collections import defaultdict, Counter

class BM25:
    def __init__(self, documents, preprocessor, k=1.5, b=0.75, delta=0.5):
        
        self.documents = documents
        self.preprocessor = preprocessor
        self.k = k
        self.b = b
        self.delta = delta

        self.doc_tokens = {doc_id: self.preprocessor.preprocess(doc["content"]) for doc_id, doc in self.documents.items()}
        self.doc_lengths = {doc_id: len(tokens) for doc_id, tokens in self.doc_tokens.items()}
        self.avg_doc_length = sum(self.doc_lengths.values()) / len(self.doc_lengths)
        self.inverted_index = self._build_inverted_index()
        self.N = len(self.documents)
        
    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def _build_inverted_index(self):
        index = defaultdict(list)
        for doc_id, tokens in self.doc_tokens.items():
            term_freqs = Counter(tokens)
            for term, freq in term_freqs.items():
                index[term].append((doc_id, freq))
        return index

    def _idf(self, term):
        df = len(self.inverted_index.get(term, []))
        return math.log(1 + (self.N - df + self.delta) / (df + self.delta))

    def score(self, query):
        query_terms = self.preprocessor.preprocess(query)
        scores = defaultdict(float)

        for term in query_terms:
            idf = self._idf(term)
            postings = self.inverted_index.get(term, [])

            for doc_id, freq in postings:
                dl = self.doc_lengths[doc_id]
                tf_component = (freq * (self.k + 1)) / (freq + self.k * (1 - self.b + self.b * dl / self.avg_doc_length))
                scores[doc_id] += idf * tf_component
                
        results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results = [(doc_id, self.sigmoid(score)) for doc_id, score in results]

        return results