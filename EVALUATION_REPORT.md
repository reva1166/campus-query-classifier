# Evaluation Report – Campus Query Classifier

**Run configuration:** own hand-written queries only (240 rows; offline sandbox, CLINC150 not downloaded – see README §"CLINC150 step").
Random seed = 42 everywhere. Split 60/20/20 stratified → train 144 / validation 48 / test 48 (8 per class in test).
Cleaning removed 0 rows (no duplicates / empties among the 240 unique queries).

## 1. Model comparison (held-out test set, macro-averaged)

| Model | Accuracy | Precision | Recall | F1 | 5-fold CV acc (all 240) |
|---|---|---|---|---|---|
| **TF-IDF (word+char) + Logistic Regression** (selected) | 0.646 | 0.701 | 0.646 | **0.661** | 0.704 |
| TF-IDF (word+char) + LinearSVC (calibrated) | 0.646 | 0.701 | 0.646 | 0.653 | 0.713 |

The two are a statistical tie (differences < 1 point; 1 test query = 2.1 points). LR was kept for its natively probabilistic output. Other variants (word-only, Naive Bayes) scored 53–60 % in repeated CV and were dropped (`reports/model_sweep_cv.txt`; tuned on train+validation only, never on test).

## 2. Per-class results (selected model, test)

| Class | Precision | Recall | F1 |
|---|---|---|---|
| academics | 0.67 | 0.50 | 0.57 |
| events | 0.40 | 0.50 | 0.44 |
| transport | 0.78 | 0.88 | 0.82 |
| clubs | 1.00 | 0.62 | 0.77 |
| facilities | 0.36 | 0.50 | 0.42 |
| other | 1.00 | 0.88 | 0.93 |

Confusion matrix: `reports/confusion_matrix.png`.

## 3. Examples

Correct (highest confidence): "is the toastmasters club active in our college" → clubs (0.85); "where is the bus pickup point for the south campus" → transport (0.81); "what are the library opening hours" → facilities (0.81).

Incorrect (full list in `reports/examples_incorrect.csv`):

| Query | True | Predicted | Conf. |
|---|---|---|---|
| does the campus have a pharmacy | facilities | transport | 0.60 |
| is there a late night transport for the library users | transport | facilities | 0.48 |
| how do i request maintenance for the air conditioner | facilities | events | 0.46 |
| is there a seminar on entrepreneurship | events | facilities | 0.47 |
| what clubs are available for first year students | clubs | events | 0.30 |
| how is the cgpa calculated | academics | facilities | 0.36 |
| who invented the telephone | other | events | 0.21 |

## 4. Error analysis

* **events ↔ facilities and academics → facilities are the main confusions.** Events queries about a *place* ("what's on at the auditorium", "seminar on …") and facilities queries phrased as a *time/schedule* share vocabulary (when/where/is there). With ~24 training examples per class, the model keys on surface words rather than intent.
* **clubs → events (3 of 8 clubs test items).** Recruitment/enrollment language ("enrollment start", "clubs for first-year students", "list of societies") overlaps with orientation-style events. Clubs precision is perfect (1.00) but recall only 0.62: the model is conservative about predicting clubs.
* **Real label ambiguity.** "late night transport for library users", "seminar on entrepreneurship" and "physics lecture on Monday" arguably belong to two categories; some "errors" are boundary cases in the taxonomy, not model failures.
* **`other` is the easiest class** (P 1.00, R 0.88): off-topic vocabulary (weather, jokes, trivia) is very distinct. The one miss ("who invented the telephone") came with the lowest confidence of all errors (0.21).
* **Cause:** the dominant factor is data volume (144 training rows). Cross-validated accuracy (≈0.70) agrees with the test result (0.65) given the tiny test set (95 % interval roughly ±13 points).

## 5. Confidence and unknown handling

* Confidence = max class probability. Mean confidence is 0.56 on correct vs 0.38 on wrong predictions – informative, but the distributions overlap.
* Unknown handling is two-layered: (1) an explicit trained `other` class; (2) an optional low-confidence fallback to `other`. The threshold was tuned on the validation set and **0.0 was selected** – i.e. the fallback did not help. The test sweep confirms it (`reports/threshold_sweep.csv`): threshold 0.3 → accuracy 0.625, 0.4 → 0.604, 0.5 → 0.458, because correct in-domain answers on such small data are often below 0.5 confidence, so thresholding pushes them wrongly to `other`. With CLINC150 added (more data → sharper probabilities) this should be re-tuned (it is automatic in `train.py`).

## 6. Sanity check on fresh queries

`demo_examples.py`: 17 new queries written after training → 15/17 correct (both misses are `other` queries: "who is the richest man in the world", "translate hello into spanish"). **Caveat:** I wrote these myself in the same style as the training queries, so this is optimistic; treat the 65–70 % figure as the realistic estimate and the 15/17 as a smoke test.

## 7. Limitations

* All results above are on synthetic, author-written queries – not real student traffic.
* Test set is only 48 items; small differences are noise.
* The CLINC150 path (`--use-clinc`) was written against the dataset card's schema but **could not be run in the offline sandbox**; it is untested. The first run will print a warning if any intent name in `INTENT_MAP` isn't found.
