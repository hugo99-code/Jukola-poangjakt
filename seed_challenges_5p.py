from dotenv import load_dotenv
load_dotenv()
from app import app, db, Challenge

challenges = [
    "Köpa en Lakka och lyckas få i sig hela själv",
    "Ha en halvtom plastkasse som enda packning",
    "Låna ut sin medhavda kikare under damtävlingen",
    "Övertyga busschauffören om att få sjunga i mikrofonen",
    "Konsekvent ha kortbyxor och T-Shirt hela resan",
    "Streaka på TC",
    "Spring dagsträcka med pannlampa",
    "Sova under bar himmel på TC – utan sovsäck",
    "Spring din sträcka med andra skor än OL-skor",
    "Ha på dig samma par underkläder hela resan"
]

with app.app_context():
    for title in challenges:
        db.session.add(Challenge(title=title, points=5))
    db.session.commit()
    print("✅ 5-poängare inlagda!")
