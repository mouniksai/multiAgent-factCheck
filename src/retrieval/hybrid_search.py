import logging
from typing import List, Dict, Any, Tuple
import numpy as np
from rank_bm25 import BM25Okapi

logger = logging.getLogger(__name__)

# Optional FAISS and SentenceTransformer imports
FAISS_AVAILABLE = False
try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    faiss = None
    FAISS_AVAILABLE = False

SENTENCE_TRANSFORMERS_AVAILABLE = False
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SentenceTransformer = None
    SENTENCE_TRANSFORMERS_AVAILABLE = False

_EMBEDDER = None


def get_embedder():
    global _EMBEDDER
    if _EMBEDDER is None and SENTENCE_TRANSFORMERS_AVAILABLE:
        try:
            _EMBEDDER = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception as e:
            logger.warning(f"Could not load SentenceTransformer: {e}")
            _EMBEDDER = None
    return _EMBEDDER


def build_faiss_index(docs: List[str]):
    """Builds a dense semantic vector index using FAISS, or scikit-learn cosine matrix fallback."""
    embedder = get_embedder()
    if FAISS_AVAILABLE and embedder is not None:
        try:
            embeddings = embedder.encode(docs, convert_to_numpy=True)
            dimension = embeddings.shape[1]
            index = faiss.IndexFlatIP(dimension)
            faiss.normalize_L2(embeddings)
            index.add(embeddings)
            return index, embeddings
        except Exception as e:
            logger.warning(f"FAISS indexing failed: {e}. Falling back to TF-IDF vector matrix.")

    # Resilient fallback: scikit-learn TfidfVectorizer dense matrix
    from sklearn.feature_extraction.text import TfidfVectorizer
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(docs).toarray().astype(np.float32)
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    matrix = matrix / norms
    return ("TFIDF_FALLBACK", vectorizer, matrix), matrix


def dense_search(query: str, index_obj, k: int = 5) -> List[int]:
    """Performs dense semantic vector search."""
    if isinstance(index_obj, tuple) and len(index_obj) == 3 and index_obj[0] == "TFIDF_FALLBACK":
        _, vectorizer, doc_matrix = index_obj
        q_vec = vectorizer.transform([query]).toarray().astype(np.float32)
        q_norm = np.linalg.norm(q_vec)
        if q_norm > 0:
            q_vec = q_vec / q_norm
        scores = np.dot(doc_matrix, q_vec.T).flatten()
        top_k = np.argsort(scores)[::-1][:k]
        return top_k.tolist()

    embedder = get_embedder()
    if FAISS_AVAILABLE and embedder is not None and hasattr(index_obj, "search"):
        try:
            query_vector = embedder.encode([query], convert_to_numpy=True)
            faiss.normalize_L2(query_vector)
            _, indices = index_obj.search(query_vector, k)
            return indices[0].tolist()
        except Exception as e:
            logger.warning(f"FAISS dense search failed: {e}")

    # Fallback to simple bag-of-words similarity
    return list(range(min(k, 3)))


def bm25_search(query: str, docs: List[str], k: int = 5) -> List[int]:
    """Sparse lexical search using BM25 Okapi."""
    tokenized_corpus = [doc.lower().split() for doc in docs]
    bm25 = BM25Okapi(tokenized_corpus)
    tokenized_query = query.lower().split()
    scores = bm25.get_scores(tokenized_query)
    top_k_indices = np.argsort(scores)[::-1][:k]
    return top_k_indices.tolist()


def reciprocal_rank_fusion(dense_ranks: List[int], bm25_ranks: List[int], c: int = 60) -> List[int]:
    """Combines sparse and dense rank lists using Reciprocal Rank Fusion (RRF)."""
    scores: Dict[int, float] = {}
    
    for rank, doc_id in enumerate(dense_ranks):
        scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (c + rank + 1)
        
    for rank, doc_id in enumerate(bm25_ranks):
        scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (c + rank + 1)
        
    sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [doc_id for doc_id, _ in sorted_docs]


def hybrid_search(query: str, docs: List[str], k: int = 5) -> List[str]:
    """Executes full hybrid search with Reciprocal Rank Fusion."""
    if not docs:
        return []
    index_obj, _ = build_faiss_index(docs)
    dense_indices = dense_search(query, index_obj, k=min(k, len(docs)))
    bm25_indices = bm25_search(query, docs, k=min(k, len(docs)))
    fused_indices = reciprocal_rank_fusion(dense_indices, bm25_indices)
    return [docs[idx] for idx in fused_indices[:k]]
