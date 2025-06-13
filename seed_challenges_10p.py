from dotenv import load_dotenv
load_dotenv()
from app import app, db, Challenge

challenges = [
    "Riva en annan klubbs militärtält utan att upptäckas",
    "Streaka framför damstarten",
    "Överleva hela resan utan att sova en blund",
    "Bli intervjuad av lokalmedia",
    "Klara hela resan utan att använda mobilen en enda gång"
]

with app.app_context():
    for title in challenges:
        db.session.add(Challenge(title=title, points=10))
    db.session.commit()
    print("✅ 10-poängare inlagda!")
