from dotenv import load_dotenv
load_dotenv()
from app import app, db, Challenge

challenges = [
    "Beställa mat eller dryck på finska",
    "Övertyga busschauffören om en \"pissi-pausi\"",
    "Taktik-spy för att kunna dricka mer",
    "Turkdusch innan buffén",
    "Få en autograf från en landslagslöpare (på valfri kroppsdel)",
    "Presentera dig själv på knagglig finska för en främling",
    "Skriv en egen hejaramsa och få tre andra att sjunga med",
    "Måla naglarna i klubbens färger",
    "Ta en selfie med en finsk funktionär",
    "Köp något från taxfreen som inte går att konsumera",
    "Ge dricks till buskern på båten",
    "Basta 2 gånger med minst 1 timmes mellanrum"
]

with app.app_context():
    for title in challenges:
        db.session.add(Challenge(title=title, points=2))
    db.session.commit()
    print("✅ 2-poängare inlagda!")
