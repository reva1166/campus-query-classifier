"""Dataset-generation script.

Sources
  1. own      : 240 hand-written campus queries (campus_queries.py), 40 / category
  2. clinc150 : (optional, needs internet) DeepPavlov/clinc150, intents mapped to
                campus categories by INTENT_MAP below. Out-of-scope (label=null)
                utterances and unrelated intents feed the 'other' class.

Usage:
  python build_dataset.py                 # own queries only (offline)
  python build_dataset.py --use-clinc     # own + mapped CLINC150

Output: data/campus_dataset.csv  (text, label, source, split)
"""
import argparse, re, random, json
import pandas as pd
from sklearn.model_selection import train_test_split
from campus_queries import QUERIES

SEED = 42
CATEGORIES = ["academics", "events", "transport", "clubs", "facilities", "other"]

# --- CLINC150 intent -> campus category (judgement calls, documented in README) ---
# 'clubs' has NO defensible CLINC intent, so it comes from own queries only.
INTENT_MAP = {
    "academics":  ["definition", "spelling", "calculator", "measurement_conversion"],
    "events":     ["calendar", "calendar_update", "schedule_meeting", "meeting_schedule",
                   "next_holiday", "reminder", "reminder_update"],
    "transport":  ["directions", "traffic", "uber", "distance", "gas", "gas_type",
                   "current_location", "share_location"],
    "facilities": ["restaurant_suggestion", "restaurant_reviews", "restaurant_reservation",
                   "nutrition_info"],
    "other":      ["weather", "tell_joke", "flip_coin", "roll_dice", "play_music", "greeting",
                   "goodbye", "thank_you", "what_are_your_hobbies", "how_old_are_you",
                   "fun_fact", "meaning_of_life", "who_made_you", "what_is_your_name",
                   "exchange_rate", "stock", "book_hotel", "book_flight", "credit_score",
                   "bill_balance", "recipe", "cook_time", "alarm", "timer", "time"],
}
CLINC_CAP_TRAIN = {"academics": 120, "events": 120, "transport": 120, "facilities": 120,
                   "other": 200}          # per category, so CLINC doesn't swamp own data
CLINC_CAP_EVAL = 25                        # per category for val and test each


def clean(text: str) -> str:
    """lowercase, drop URLs/control chars, strip punctuation except apostrophes, squeeze spaces"""
    t = str(text).lower()
    t = re.sub(r"https?://\S+", " ", t)
    t = re.sub(r"[\x00-\x1f\x7f]", " ", t)
    t = re.sub(r"[^a-z0-9' ]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def own_frame():
    rows = [(q, c) for c, qs in QUERIES.items() for q in qs]
    df = pd.DataFrame(rows, columns=["text", "label"])
    df["source"] = "own"
    # stratified 60/20/20 split with fixed seed
    tr, tmp = train_test_split(df, test_size=0.4, stratify=df.label, random_state=SEED)
    va, te = train_test_split(tmp, test_size=0.5, stratify=tmp.label, random_state=SEED)
    return pd.concat([tr.assign(split="train"), va.assign(split="validation"), te.assign(split="test")])


def clinc_frame():
    from datasets import load_dataset
    raw = load_dataset("DeepPavlov/clinc150", "default")           # utterance, label (null = OOS)
    intents = load_dataset("DeepPavlov/clinc150", "intents")["intents"]
    id2name = {int(r["id"]): r["name"] for r in intents}
    name2cat = {n: c for c, ns in INTENT_MAP.items() for n in ns}
    missing = sorted(set(name2cat) - set(id2name.values()))
    if missing:
        print("WARNING intent names not found in dataset (check INTENT_MAP):", missing)
    rng = random.Random(SEED)
    parts = []
    for split in ["train", "validation", "test"]:
        d = raw[split].to_pandas()
        d["intent"] = d["label"].map(lambda x: None if pd.isna(x) else id2name[int(x)])
        d["cat"] = d["intent"].map(name2cat)
        d.loc[d["intent"].isna(), "cat"] = "other"                 # out-of-scope -> other
        d = d.dropna(subset=["cat"])
        cap = CLINC_CAP_TRAIN if split == "train" else {c: CLINC_CAP_EVAL for c in CLINC_CAP_TRAIN}
        d = pd.concat([g.sample(min(len(g), cap[c]), random_state=SEED) for c, g in d.groupby("cat")])
        parts.append(pd.DataFrame({"text": d["utterance"], "label": d["cat"],
                                   "source": "clinc150", "split": split}))
    return pd.concat(parts)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--use-clinc", action="store_true")
    args = ap.parse_args()
    df = own_frame()
    if args.use_clinc:
        df = pd.concat([df, clinc_frame()])
    n0 = len(df)
    df["text"] = df["text"].map(clean)
    df = df[df.text.str.len() >= 3]                                 # drop empty / degenerate
    df = df.drop_duplicates(subset="text", keep="first")            # no leakage across splits
    stats = {"rows_before_cleaning": n0, "rows_after_cleaning": len(df),
             "removed": n0 - len(df),
             "counts": df.groupby(["split", "label"]).size().unstack(fill_value=0).to_dict("index"),
             "by_source": df.source.value_counts().to_dict()}
    df.to_csv("data/campus_dataset.csv", index=False)
    json.dump(stats, open("data/dataset_stats.json", "w"), indent=2)
    print(json.dumps(stats, indent=2))
