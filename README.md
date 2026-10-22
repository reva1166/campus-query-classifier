# Campus Query Classifier

Classifies student queries into **academics, events, transport, clubs, facilities, other**.
TF-IDF (word + char n-grams) → Logistic Regression, compared against a calibrated LinearSVC. Seed fixed (42).

## Results (own-query run, offline)
| | Accuracy | Macro P | Macro R | Macro F1 |
|---|---|---|---|---|
| Logistic Regression (selected) | 0.646 | 0.701 | 0.646 | 0.661 |
| LinearSVC (calibrated) | 0.646 | 0.701 | 0.646 | 0.653 |

5-fold CV accuracy ≈ 0.70 for both. Test set = 48 queries, so expect ±~13 points. Full details, confusion matrix and error analysis: **EVALUATION_REPORT.md**.
Accuracy is modest because only 144 training queries are used; adding CLINC150 (below) is the main lever for improvement.

## How the six categories are obtained (both sources)
1. **Own queries (always used):** 40 hand-written queries per category (`campus_queries.py`), 240 total. The only source for *clubs* – CLINC150 has no intent that fits.
2. **CLINC150 mapping (optional, `--use-clinc`):** selected intents are mapped to categories in `INTENT_MAP` (`build_dataset.py`), e.g. calendar/reminder/next_holiday → events; directions/traffic/uber/distance → transport; restaurant_* → facilities (dining); definition/spelling/calculator → academics (study help). `other` = CLINC out-of-scope (null label) plus unrelated intents (weather, jokes, music…). The mapping is a judgement call and CLINC's phrasing is generic (not campus-specific), so each category is capped (120 train / 25 val / 25 test per category) to keep it from drowning out the campus-specific queries.

## Setup & run
```bash
pip install -r requirements.txt
python build_dataset.py              # own queries only  (add --use-clinc to include CLINC150; needs internet)
python train.py                      # trains both models, writes models/ and reports/
python predict.py "when does the next college bus leave"     # CLI (no args = interactive)
python app.py                        # web UI at http://127.0.0.1:5000 ; API: POST /predict {"query": "..."}
python demo_examples.py              # fresh-query smoke test
```
API example: `curl -X POST localhost:5000/predict -H 'Content-Type: application/json' -d '{"query":"is the gym open on sundays"}'`
→ `{"category":"facilities","confidence":0.9,"top":[...]}`

## Pipeline
* **Cleaning:** lowercase, strip URLs/control chars/punctuation (keep apostrophes), collapse whitespace, drop <3-char rows, de-duplicate across all splits (no leakage). Counts in `data/dataset_stats.json`.
* **Split:** stratified 60/20/20 for own queries (CLINC uses its own train/validation/test). Threshold tuned on validation; final model refit on train+validation; test used once.
* **Metrics:** accuracy, macro precision/recall/F1, per-class report, 5-fold CV.
* **Unknown class:** explicit `other` class + optional confidence threshold (tuned automatically; currently 0.0 – see report §5).

## Files
`campus_queries.py` data · `build_dataset.py` dataset generation · `train.py` training/eval · `sweep_models.py` CV model sweep · `predict.py` CLI · `app.py` web UI/API · `demo_examples.py` · `data/` · `models/` · `reports/` (metrics.json, confusion_matrix.png, examples_*.csv, threshold_sweep.csv, model_sweep_cv.txt)

## Honest caveats
CLINC150 loading is **untested** (sandbox had no internet). Queries are author-written, not real student data. Small test set.
