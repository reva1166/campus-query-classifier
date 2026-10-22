"""CLI: python predict.py "how do i join the coding club" ["another query" ...]
        python predict.py            (interactive; empty line quits)"""
import sys, joblib, numpy as np
from build_dataset import clean

_bundle = joblib.load("models/campus_classifier.joblib")

def predict(text: str, top_k: int = 3) -> dict:
    model, thr = _bundle["model"], _bundle["threshold"]
    proba = model.predict_proba([clean(text)])[0]
    order = np.argsort(proba)[::-1]
    label, conf = model.classes_[order[0]], float(proba[order[0]])
    low_conf = conf < thr
    return {"query": text, "category": "other" if low_conf else label, "confidence": round(conf, 3),
            "routed_to_other_by_threshold": bool(low_conf),
            "top": [{"category": model.classes_[i], "prob": round(float(proba[i]), 3)} for i in order[:top_k]]}

if __name__ == "__main__":
    qs = sys.argv[1:]
    if qs:
        for q in qs: r = predict(q); print(f"{r['category']:<11} conf={r['confidence']:.2f}  <- {q}")
    else:
        while (q := input("query> ").strip()):
            r = predict(q); print(f"  -> {r['category']} (conf {r['confidence']:.2f})  top3: {r['top']}")
