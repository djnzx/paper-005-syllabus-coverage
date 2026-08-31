import os

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer


# Install:
# pip3 install -U sentence-transformers pandas numpy

# Run:
# python3 match.py

# Optional model override:
# MODEL_NAME=intfloat/multilingual-e5-base python3 match.py


MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
)

REQUIREMENTS_CSV = "requirements.csv"
SYLLABUS_CSV = "syllabus.csv"

MATCHES_CSV = "matches.csv"
SIMILARITY_MATRIX_CSV = "similarity_matrix.csv"
RANK_MATRIX_CSV = "rank_matrix.csv"
ROW_RELATIVE_MATRIX_CSV = "row_relative_matrix.csv"

TOP_K = 3


def classify(score: float) -> str:
    if score >= 0.70:
        return "strong"
    if score >= 0.55:
        return "partial"
    if score >= 0.40:
        return "weak"

    return "missing"


def read_requirements(path: str) -> pd.DataFrame:
    """
    Supports either:

    requirement_id,requirement_text

    or:

    n,name
    """

    df = pd.read_csv(path, skipinitialspace=True)
    df.columns = [str(column).strip() for column in df.columns]

    if {"requirement_id", "requirement_text"}.issubset(df.columns):
        result = df[["requirement_id", "requirement_text"]].copy()

    elif {"n", "name"}.issubset(df.columns):
        result = df[["n", "name"]].copy()
        result = result.rename(
            columns={
                "n": "requirement_id",
                "name": "requirement_text",
            }
        )

    else:
        raise ValueError(
            "requirements.csv must contain either "
            "'requirement_id,requirement_text' or 'n,name'. "
            f"Found columns: {list(df.columns)}"
        )

    result["requirement_id"] = result["requirement_id"].astype(str).str.strip()
    result["requirement_text"] = result["requirement_text"].astype(str).str.strip()

    return result


def read_syllabus(path: str) -> pd.DataFrame:
    """
    Supports either:

    lecture_id,lecture_text

    or no-header format:

    L1,Вектори ...
    L2,Системи ...
    """

    first_try = pd.read_csv(path, skipinitialspace=True)
    first_try.columns = [str(column).strip() for column in first_try.columns]

    if {"lecture_id", "lecture_text"}.issubset(first_try.columns):
        result = first_try[["lecture_id", "lecture_text"]].copy()

    else:
        result = pd.read_csv(
            path,
            header=None,
            names=["lecture_id", "lecture_text"],
            skipinitialspace=True,
        )

    result["lecture_id"] = result["lecture_id"].astype(str).str.strip()
    result["lecture_text"] = result["lecture_text"].astype(str).str.strip()

    return result


def encode_texts(
        model: SentenceTransformer,
        texts: list[str],
        kind: str,
) -> np.ndarray:
    """
    For ordinary sentence-transformer models, text is passed as-is.

    For E5 models, use:

    query:   requirement text
    passage: lecture text
    """

    model_name_lower = MODEL_NAME.lower()

    if "e5" in model_name_lower:
        if kind == "requirement":
            texts = ["query: " + text for text in texts]

        elif kind == "lecture":
            texts = ["passage: " + text for text in texts]

    return model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True,
    )


def build_rank_matrix(
        similarity: np.ndarray,
        requirement_ids: list[str],
        lecture_ids: list[str],
) -> pd.DataFrame:
    """
    For each requirement row:

    rank 1 = best lecture
    rank 2 = second-best lecture
    etc.
    """

    rank_matrix = np.zeros_like(similarity, dtype=int)

    for i in range(similarity.shape[0]):
        order = np.argsort(similarity[i])[::-1]

        for rank, j in enumerate(order, start=1):
            rank_matrix[i, j] = rank

    return pd.DataFrame(
        rank_matrix,
        index=requirement_ids,
        columns=lecture_ids,
    )


def main() -> None:
    requirements_df = read_requirements(REQUIREMENTS_CSV)
    syllabus_df = read_syllabus(SYLLABUS_CSV)

    requirement_ids = requirements_df["requirement_id"].tolist()
    lecture_ids = syllabus_df["lecture_id"].tolist()

    requirements = requirements_df["requirement_text"].tolist()
    lectures = syllabus_df["lecture_text"].tolist()

    print(f"Requirements: {len(requirements)}")
    print(f"Lectures:     {len(lectures)}")
    print(f"Model:        {MODEL_NAME}")
    print()

    model = SentenceTransformer(MODEL_NAME)

    print("Encoding requirements...")
    requirement_embeddings = encode_texts(
        model=model,
        texts=requirements,
        kind="requirement",
    )

    print("Encoding lectures...")
    lecture_embeddings = encode_texts(
        model=model,
        texts=lectures,
        kind="lecture",
    )

    # Embeddings are normalized, so dot product == cosine similarity.
    similarity = requirement_embeddings @ lecture_embeddings.T

    matrix_df = pd.DataFrame(
        similarity,
        index=requirement_ids,
        columns=lecture_ids,
    ).round(3)

    matrix_df.columns.name = None
    matrix_df.index.name = None

    matrix_df.to_csv(SIMILARITY_MATRIX_CSV)

    rank_matrix_df = build_rank_matrix(
        similarity=similarity,
        requirement_ids=requirement_ids,
        lecture_ids=lecture_ids,
    )

    rank_matrix_df.columns.name = None
    rank_matrix_df.index.name = None

    rank_matrix_df.to_csv(RANK_MATRIX_CSV)

    row_means = similarity.mean(axis=1, keepdims=True)
    row_relative = similarity - row_means

    row_relative_df = pd.DataFrame(
        row_relative,
        index=requirement_ids,
        columns=lecture_ids,
    ).round(3)

    row_relative_df.columns.name = None
    row_relative_df.index.name = None

    row_relative_df.to_csv(ROW_RELATIVE_MATRIX_CSV)

    rows = []

    for i, requirement_id in enumerate(requirement_ids):
        scores = similarity[i]
        top_indices = np.argsort(scores)[::-1][:TOP_K]
        best_score = float(scores[top_indices[0]])

        for rank, j in enumerate(top_indices, start=1):
            rows.append(
                {
                    "requirement_id": requirement_id,
                    "requirement_text": requirements[i],
                    "rank": rank,
                    "lecture_id": lecture_ids[j],
                    "lecture_text": lectures[j],
                    "score": round(float(scores[j]), 4),
                    "best_score_for_requirement": round(best_score, 4),
                    "coverage": classify(best_score),
                }
            )

    matches_df = pd.DataFrame(rows)
    matches_df.to_csv(MATCHES_CSV, index=False)

    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 300)
    pd.set_option("display.precision", 3)

    print()
    print("Full similarity matrix:")
    print(matrix_df)

    print()
    print("Rank matrix, where 1 = best lecture for this requirement:")
    print(rank_matrix_df)

    print()
    print("Top matches:")
    print(matches_df)

    print()
    print("Saved files:")
    print(f"  {SIMILARITY_MATRIX_CSV}")
    print(f"  {RANK_MATRIX_CSV}")
    print(f"  {ROW_RELATIVE_MATRIX_CSV}")
    print(f"  {MATCHES_CSV}")


if __name__ == "__main__":
    main()