from app import app, db, Challenge

challenges = [
    "Basta efter din sträcka",
    "Bjuda coach/ledare på en öl",
    "Gå till duschen med efterföljande sträckas löpare",
    "Hitta ett ledigt bord vid frukosten på båten",
    "Ta en selfie i en Baja-Maja",
    "Prata med en finsk löpare om terrängen",
    "Drick en finsk dryck du inte kan uttala namnet på",
    "Läsa högt ur PM med en finsk brytning",
    "Fråga vad \"makkara\" kostar – trots att det står på skylten",
    "Vinn två vänd-10 omgångar i rad",
    "Låna tvål och shampoo av en främling i Jukola-duschen",
    "Packa något onödigt som du aldrig använder under helgen",
    "Smuggla med ett par mackor från frukost-buffén"
]

with app.app_context():
    for title in challenges:
        db.session.add(Challenge(title=title, points=1))
    db.session.commit()
    print("✅ Utmaningar inlagda!")
