"""Encode clause and outcome texts into a shared space with a pinned encoder.

Implements manuscript Sec. 6.2: one encoder phi: Text -> R^d, mean pooling,
L2-normalised output so cosine == dot product. Embeddings are cached on disk by
sha1(text|model|revision) so a re-run is deterministic and fast.
"""
from __future__ import annotations

import hashlib
import os

import numpy as np

from common import RESULTS, DEFAULT_MODEL

_CACHE = os.path.join(RESULTS, "emb_cache.npz")


def _key(text: str, model: str, revision: str) -> str:
    return hashlib.sha1(f"{model}@{revision}\n{text}".encode("utf-8")).hexdigest()


def load_encoder(model_name: str = DEFAULT_MODEL):
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(model_name)
    # Resolve a revision string for reproducibility (best effort).
    revision = getattr(model, "model_card_data", None)
    revision = getattr(revision, "base_model_revision", None) or "unpinned"
    return model, str(revision)


def encode(texts: list[str], model_name: str = DEFAULT_MODEL,
           encoder=None) -> np.ndarray:
    """Return an (n, d) array of L2-normalised embeddings, using a disk cache."""
    if encoder is None:
        model, revision = load_encoder(model_name)
    else:
        model, revision = encoder

    cache: dict[str, np.ndarray] = {}
    if os.path.exists(_CACHE):
        with np.load(_CACHE, allow_pickle=True) as z:
            cache = {k: z[k] for k in z.files}

    keys = [_key(t, model_name, revision) for t in texts]
    missing = [(t, k) for t, k in zip(texts, keys) if k not in cache]
    if missing:
        vecs = model.encode([t for t, _ in missing], normalize_embeddings=True,
                            show_progress_bar=False)
        for (_, k), v in zip(missing, vecs):
            cache[k] = np.asarray(v, dtype=np.float32)
        np.savez(_CACHE, **cache)

    return np.vstack([cache[k] for k in keys])
