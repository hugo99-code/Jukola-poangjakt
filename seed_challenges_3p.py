from dotenv import load_dotenv
load_dotenv()
from app import app, db, Challenge

challenges = [
    "Få med sig en lokal skylt hem med obegriplig text",
    "Dansa tango med en Finsk dam",
    "Svepa en öl direkt efter målgång",
    "Leda allsången i bussen",
    "Äta minst 10 stycken grilli makkara under resan",
    "Spring din sträcka med 2 olika skor",
    "Sov i en annan klubbs tält",
    "Drick ett glas av varje alkoholhaltig dryck på buffén",
    "Få en finne att sjunga en sång på svenska",
    "Var först ut på dansgolvet"
]

with app.app_context():
    for title in challenges:
        db.session.add(Challenge(title=title, points=3))
    db.session.commit()
    print("✅ 3-poängare inlagda!")
