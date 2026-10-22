import pandas as pd, numpy as np
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import ComplementNB, MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.model_selection import StratifiedKFold, cross_val_score, RepeatedStratifiedKFold
df = pd.read_csv("data/campus_dataset.csv"); tv = df[df.split!="test"]   # exclude test from tuning
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=42)
W = lambda **k: TfidfVectorizer(ngram_range=(1,2), sublinear_tf=True, **k)
C = lambda: TfidfVectorizer(analyzer="char_wb", ngram_range=(2,5), sublinear_tf=True, min_df=2)
cands = {
 "word+char LR C=10": Pipeline([("f",FeatureUnion([("w",W()),("c",C())])),("m",LogisticRegression(C=10,max_iter=2000))]),
 "word LR C=10": Pipeline([("f",W()),("m",LogisticRegression(C=10,max_iter=2000))]),
 "word LR C=100": Pipeline([("f",W()),("m",LogisticRegression(C=100,max_iter=2000))]),
 "word uni LR C=30": Pipeline([("f",TfidfVectorizer(sublinear_tf=True)),("m",LogisticRegression(C=30,max_iter=2000))]),
 "word SVC C=1": Pipeline([("f",W()),("m",LinearSVC(C=1))]),
 "word+char SVC C=0.5": Pipeline([("f",FeatureUnion([("w",W()),("c",C())])),("m",LinearSVC(C=0.5))]),
 "word ComplementNB": Pipeline([("f",W()),("m",ComplementNB(alpha=0.3))]),
 "count MultinomialNB": Pipeline([("f",CountVectorizer(ngram_range=(1,2))),("m",MultinomialNB(alpha=0.3))]),
}
for k,m in cands.items():
    s = cross_val_score(m, tv.text, tv.label, cv=cv, scoring="accuracy"); print(f"{k:24s} {s.mean():.3f} ± {s.std():.3f}")
