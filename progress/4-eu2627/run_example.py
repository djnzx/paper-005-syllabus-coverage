import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/LaBSE")

clauses = {
    "c1 A.5.1 policy": "Information security policy defined and communicated",
    "c2 A.5.7 threat intel": "Threat intelligence collected and analysed",
    "c3 A.5.24 incident mgmt": "Incident management planned and prepared",
    "c4 NIS2 supply chain": "Supply-chain security addressed",
    "c5 NIS2 hygiene & training": "Basic cyber hygiene and training provided",
    "c6 NIS2 MFA": "Multi-factor authentication used",
}
outcomes = {
    "l1": "Explain the organisation's information security policy and staff duties",
    "l2": "Recognise phishing and report incidents to the service desk",
    "l3": "Apply strong passwords and multi-factor authentication",
    "l4": "Follow good cyber-hygiene habits in daily work",
    "l5": "Describe how personal data is backed up",
}

cl_keys = list(clauses)
lo_keys = list(outcomes)
C = model.encode([clauses[k] for k in cl_keys], normalize_embeddings=True)
L = model.encode([outcomes[k] for k in lo_keys], normalize_embeddings=True)
sim = C @ L.T  # cosine, since normalized

print("FULL MATRIX (rows=clauses, cols=l1..l5)")
header = "                            " + "  ".join(f"{k:>5}" for k in lo_keys)
print(header)
for i, ck in enumerate(cl_keys):
    row = "  ".join(f"{sim[i,j]:.2f}" for j in range(len(lo_keys)))
    print(f"{ck:<27} {row}")

print("\nBEST MATCH PER CLAUSE")
for i, ck in enumerate(cl_keys):
    j = int(np.argmax(sim[i]))
    print(f"{ck:<27} best={lo_keys[j]}  s={sim[i,j]:.2f}")

# Ukrainian cross-lingual check on one outcome
ua = "Застосовувати надійні паролі та багатофакторну автентифікацію"
v = model.encode([ua], normalize_embeddings=True)
print(f"\nCross-lingual check: UA 'strong passwords + MFA' vs c6 MFA = {(C[5] @ v[0]):.2f}")