from app import app, db, Challenge

challenges = [
    ("Ha med sig stövlar, paraply eller stol (-1)", -1),
    ("Gå direkt till jobbet på måndag morgon(-2)", -2),
    ("Spy i bussen, på båten eller annan inomhus plats (-3)", -3),
    ("Missa målgång för ditt lag (-4)", -4),
    ("Missa båten hem (-5)", -5)
]

with app.app_context():
    for title, points in challenges:
        db.session.add(Challenge(title=title, points=points))
    db.session.commit()
    print("✅ Minuspoäng inlagda!")
