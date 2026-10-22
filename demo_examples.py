"""Fresh queries written AFTER training (never in train/val/test): a sanity check on novel input."""
from predict import predict
FRESH = [("academics","how do i apply for a scholarship renewal"),("academics","what is the exam pattern for the algorithms paper"),
 ("academics","can i audit a course without credits"),("events","is there a hackathon next month"),
 ("events","when is the placement drive starting"),("transport","where do i catch the bus to the airport"),
 ("transport","is there parking near the admin block"),("clubs","how do i get into the robotics club"),
 ("clubs","when do the photography club recruitments begin"),("facilities","is the cafeteria open on holidays"),
 ("facilities","where can i charge my laptop in the library"),("facilities","who do i call if the hostel water heater breaks"),
 ("other","what is the population of canada"),("other","remind me to buy milk"),("other","how do i bake a chocolate cake"),
 ("other","who is the richest man in the world"),("other","translate hello into spanish")]
ok = 0
for true, q in FRESH:
    r = predict(q); ok += r["category"] == true
    print(f"{'OK ' if r['category']==true else 'ERR'} true={true:<10} pred={r['category']:<10} conf={r['confidence']:.2f}  {q}")
print(f"\n{ok}/{len(FRESH)} correct")
