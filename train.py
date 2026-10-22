"""Train + evaluate two models (seed fixed), tune the unknown-threshold, write report artifacts.

  Model A: TF-IDF (word 1-2gram + char 2-5gram) -> Logistic Regression
  Model B: same features                         -> LinearSVC (probability-calibrated)
"""
import json, random
import numpy as np, pandas as pd, joblib
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import (accuracy_score, precision_recall_fscore_support,
                             classification_report, confusion_matrix)

SEED = 42
random.seed(SEED); np.random.seed(SEED)
LABELS = ["academics", "events", "transport", "clubs", "facilities", "other"]


def features():
    return FeatureUnion([
        ("word", TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, min_df=1)),
        ("char", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), sublinear_tf=True, min_df=2)),
    ])

def make(name):
    clf = (LogisticRegression(C=10, max_iter=2000, random_state=SEED) if name == "logreg"
           else CalibratedClassifierCV(LinearSVC(C=0.5, random_state=SEED), cv=3, method="sigmoid"))
    return Pipeline([("tfidf", features()), ("clf", clf)])

def apply_threshold(proba, classes, t):
    """argmax, but fall back to 'other' when confidence < t  (unknown handling)"""
    classes = np.array(classes)
    pred = classes[proba.argmax(1)].astype(object)
    pred[proba.max(1) < t] = "other"
    return pred, proba.max(1)

def scores(y, p):
    pr, rc, f1, _ = precision_recall_fscore_support(y, p, labels=LABELS, average="macro", zero_division=0)
    return {"accuracy": accuracy_score(y, p), "precision_macro": pr, "recall_macro": rc, "f1_macro": f1}

df = pd.read_csv("data/campus_dataset.csv")
tr, va, te = (df[df.split == s] for s in ["train", "validation", "test"])
results, fitted = {}, {}

for name in ["logreg", "linearsvc"]:
    # 1) tune confidence threshold on VALIDATION set only
    m = make(name).fit(tr.text, tr.label)
    pv = m.predict_proba(va.text)
    grid = np.arange(0.0, 0.81, 0.05)
    f1s = [scores(va.label, apply_threshold(pv, m.classes_, t)[0])["f1_macro"] for t in grid]
    t_best = float(grid[int(np.argmax(f1s))]) if max(f1s) > f1s[0] + 1e-9 else 0.0
    # 2) refit on train+validation, evaluate once on the untouched TEST set
    full = pd.concat([tr, va])
    m = make(name).fit(full.text, full.label)
    pt = m.predict_proba(te.text)
    pred_plain = np.array(m.classes_)[pt.argmax(1)]
    pred_thr, conf = apply_threshold(pt, m.classes_, t_best)
    # 3) 5-fold CV on all own+clinc data for a stabler estimate
    cv = StratifiedKFold(5, shuffle=True, random_state=SEED)
    cvp = cross_val_predict(make(name), df.text, df.label, cv=cv)
    sc = scores(te.label, pred_plain)
    results[name] = {"threshold": t_best, "test": sc,
                     "test_with_threshold": scores(te.label, pred_thr),
                     "cv5_accuracy": float((cvp == df.label).mean()),
                     "cv5_f1_macro": scores(df.label, cvp)["f1_macro"],
                     "per_class": classification_report(te.label, pred_plain, labels=LABELS,
                                                        output_dict=True, zero_division=0)}
    fitted[name] = (m, pred_plain, conf, pt)
    print(f"{name}: test acc={sc['accuracy']:.3f} f1={sc['f1_macro']:.3f} | cv5 acc={results[name]['cv5_accuracy']:.3f} | thr={t_best}")

best = max(results, key=lambda k: (results[k]["test"]["f1_macro"], results[k]["cv5_f1_macro"]))
model, pred, conf, proba = fitted[best]
results["best_model"] = best
joblib.dump({"model": model, "threshold": results[best]["threshold"], "labels": LABELS}, "models/campus_classifier.joblib")
json.dump(results, open("reports/metrics.json", "w"), indent=2)

# confusion matrix
cm = confusion_matrix(te.label, pred, labels=LABELS)
fig, ax = plt.subplots(figsize=(6.5, 5.5)); ax.imshow(cm, cmap="Blues")
ax.set_xticks(range(6)); ax.set_xticklabels(LABELS, rotation=45, ha="right"); ax.set_yticks(range(6)); ax.set_yticklabels(LABELS)
for i in range(6):
    for j in range(6): ax.text(j, i, cm[i, j], ha="center", va="center", color="white" if cm[i, j] > cm.max() / 2 else "black")
ax.set_xlabel("predicted"); ax.set_ylabel("true"); ax.set_title(f"Confusion matrix - {best} (test)")
plt.tight_layout(); plt.savefig("reports/confusion_matrix.png", dpi=140)

# examples: correct & incorrect
ex = te.assign(pred=pred, confidence=conf.round(3))
ex[ex.label == ex.pred].sort_values("confidence", ascending=False).head(8).to_csv("reports/examples_correct.csv", index=False)
ex[ex.label != ex.pred].sort_values("confidence", ascending=False).to_csv("reports/examples_incorrect.csv", index=False)
# calibration-ish stat: confidence of right vs wrong
print("best:", best, "| mean conf correct %.2f wrong %.2f" % (conf[pred == te.label].mean(),
      conf[pred != te.label].mean() if (pred != te.label).any() else float("nan")))
print(ex[ex.label != ex.pred][["text", "label", "pred", "confidence"]].to_string(index=False))
print(pd.DataFrame(cm, index=LABELS, columns=LABELS))

# unknown-handling analysis: effect of the confidence threshold on the TEST set
rows = []
for t in [0.0, 0.3, 0.4, 0.5, 0.6]:
    p, _ = apply_threshold(proba, model.classes_, t)
    s = scores(te.label, p)
    rej = (proba.max(1) < t)
    rows.append({"threshold": t, "accuracy": round(s["accuracy"], 3), "f1_macro": round(s["f1_macro"], 3),
                 "share_routed_to_other": round(float(rej.mean()), 3),
                 "in_domain_wrongly_routed_to_other": int(((p == "other") & (te.label != "other")).sum())})
pd.DataFrame(rows).to_csv("reports/threshold_sweep.csv", index=False)
print(pd.DataFrame(rows).to_string(index=False))
