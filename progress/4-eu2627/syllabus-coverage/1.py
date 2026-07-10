from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

requirements = [
"R1. Students should understand vectors in R^n, including vector addition, scalar multiplication, linear combinations, span, and geometric interpretation.",
"R2. Students should be able to represent systems of linear equations using matrices and solve them using row reduction and matrix algebra.",
"R3. Students should understand linear independence, dependence, basis, dimension, and the relationship between these concepts and solution spaces.",
"R4. Students should understand matrices as linear transformations and be able to interpret matrix multiplication as composition of transformations.",
"R5. Students should understand dot products, norms, angles, orthogonality, projections, and orthogonal decompositions in Euclidean spaces.",
"R6. Students should be able to apply least squares methods to overdetermined systems and interpret least squares as an orthogonal projection problem.",
"R7. Students should understand eigenvalues, eigenvectors, eigenspaces, and their role in describing invariant directions of linear transformations.",
"R8. Students should be able to use diagonalization and symmetric matrix properties to analyze quadratic forms and optimization problems.",
"R9. Students should understand singular value decomposition and its applications to low-rank approximation, data compression, and dimensionality reduction.",
"R10. Students should be able to apply linear algebra concepts to modern applications such as linear regression, Markov chains, PageRank, and data analysis."
]

lectures = [
"L1. Вектори в R^n: координатне подання, додавання векторів, множення на скаляр, геометричний зміст векторів у дво-, три- та багатовимірному просторі.",
"L2. Лінійні комбінації та лінійна оболонка: поняття span, породжені підпростори, опис множин розв’язків через лінійні комбінації векторів.",
"L3. Системи лінійних рівнянь: матричний запис систем, розширена матриця, елементарні перетворення рядків та метод Гауса.",
"L4. Матриці та матрична алгебра: операції над матрицями, добуток матриць, одинична матриця, обернена матриця та властивості матричних обчислень.",
"L5. Ранг матриці та простори розв’язків: ведучі змінні, вільні змінні, нульовий простір, простір стовпців та інтерпретація розв’язності систем.",
"L6. Лінійна незалежність, базис і розмірність: критерії незалежності векторів, мінімальні породжувальні системи, координати вектора в заданому базисі.",
"L7. Лінійні відображення: матриця лінійного перетворення, образ і ядро, геометричні приклади поворотів, проєкцій, масштабувань і відображень.",
"L8. Композиція лінійних перетворень: зв’язок між композицією відображень і множенням матриць, некомутативність добутку матриць, зміна базису.",
"L9. Скалярний добуток і норма: довжина вектора, кут між векторами, ортогональність, нормування векторів і геометрія евклідового простору.",
"L10. Ортогональні проєкції: проєкція вектора на пряму та підпростір, ортогональне розкладання, відстань від вектора до підпростору.",
"L11. Ортогональні базиси та процес Грама — Шмідта: побудова ортонормованого базису, QR-розклад і застосування до чисельних обчислень.",
"L12. Метод найменших квадратів: перевизначені системи, нормальні рівняння, геометрична інтерпретація як ортогональна проєкція на простір стовпців.",
"L13. Лінійна регресія як задача найменших квадратів: матриця ознак, вектор параметрів, помилки моделі, інтерпретація коефіцієнтів регресії.",
"L14. Власні значення і власні вектори: характеристичне рівняння, власні простори, інваріантні напрями та геометричний зміст власних векторів.",
"L15. Діагоналізація матриць: умови діагоналізовності, базис із власних векторів, степені матриць і спрощення лінійних динамічних моделей.",
"L16. Симетричні матриці та спектральна теорема: ортогональні власні вектори, ортогональна діагоналізація, додатно визначені матриці.",
"L17. Квадратичні форми та оптимізація: матричне подання квадратичних функцій, головні осі, класифікація критичних точок, зв’язок із власними значеннями.",
"L18. Марковські ланцюги: стохастичні матриці, стаціонарні розподіли, довгострокова поведінка систем і приклади з динаміки популяцій.",
"L19. PageRank і мережеві моделі: графи як матриці переходів, власні вектори у ранжуванні сторінок, інтерпретація стаціонарного стану.",
"L20. Сингулярний розклад матриці: SVD, сингулярні значення, низькорангове наближення, стиснення зображень, тематичне моделювання та зменшення розмірності."
]

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

req_embeddings = model.encode(requirements, normalize_embeddings=True)
lec_embeddings = model.encode(lectures, normalize_embeddings=True)

similarity = cosine_similarity(req_embeddings, lec_embeddings)

df = pd.DataFrame(
    similarity,
    index=[f"R{i+1}" for i in range(len(requirements))],
    columns=[f"L{j+1}" for j in range(len(lectures))]
)

print(df.round(3))