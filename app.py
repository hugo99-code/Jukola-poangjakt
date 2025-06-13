from dotenv import load_dotenv
load_dotenv()
import os  # Viktigt att detta importeras före os-användning
print("📂 Current working directory:", os.getcwd())
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Du kan ersätta med en säkrare nyckel i en riktig miljö

database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

print("▶ DATABASE_URL =", database_url)
db = SQLAlchemy(app)

# --- MODELLER ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    total_points = db.Column(db.Integer, default=0)

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    points = db.Column(db.Integer, nullable=False)

class UserChallenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'))

# --- ROUTES ---
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            name = request.form['name']
            password = generate_password_hash(request.form['password'])
            if User.query.filter_by(name=name).first():
                return render_template('register.html', error='Användarnamnet är redan taget.')
            user = User(name=name, password_hash=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            print("❌ Fel vid registrering:", e)
            return render_template('register.html', error='Något gick fel. Se loggen.')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        if name == 'admin' and password == 'deargerard2022':
            session['admin'] = True
            return redirect(url_for('admin'))
        user = User.query.filter_by(name=name).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Fel användarnamn eller lösenord.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    challenges = Challenge.query.order_by(Challenge.points, Challenge.title).all()
    completed_ids = {uc.challenge_id for uc in UserChallenge.query.filter_by(user_id=user.id).all()}
    leaderboard = User.query.order_by(User.total_points.desc()).all()
    return render_template('dashboard.html', user=user, challenges=challenges, completed_ids=completed_ids, leaderboard=leaderboard)

@app.route('/check_challenge/<int:challenge_id>', methods=['POST'])
def check_challenge(challenge_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    if not UserChallenge.query.filter_by(user_id=user_id, challenge_id=challenge_id).first():
        challenge = Challenge.query.get(challenge_id)
        db.session.add(UserChallenge(user_id=user_id, challenge_id=challenge_id))
        user = User.query.get(user_id)
        user.total_points += challenge.points
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/uncheck_challenge/<int:challenge_id>', methods=['POST'])
def uncheck_challenge(challenge_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    record = UserChallenge.query.filter_by(user_id=user_id, challenge_id=challenge_id).first()
    if record:
        challenge = Challenge.query.get(challenge_id)
        db.session.delete(record)
        user = User.query.get(user_id)
        user.total_points -= challenge.points
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))
    challenges = Challenge.query.order_by(Challenge.points.desc(), Challenge.title).all()
    users = User.query.order_by(User.total_points.desc()).all()
    if request.method == 'POST':
        title = request.form['title']
        points = int(request.form['points'])
        db.session.add(Challenge(title=title, points=points))
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('admin.html', challenges=challenges, users=users)

@app.route('/admin/delete/<int:challenge_id>', methods=['POST'])
def delete_challenge(challenge_id):
    if not session.get('admin'):
        return redirect(url_for('login'))
    challenge = Challenge.query.get(challenge_id)
    if challenge:
        db.session.delete(challenge)
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/edit/<int:challenge_id>', methods=['GET', 'POST'])
def edit_challenge(challenge_id):
    if not session.get('admin'):
        return redirect(url_for('login'))
    challenge = Challenge.query.get(challenge_id)
    if request.method == 'POST':
        challenge.title = request.form['title']
        challenge.points = int(request.form['points'])
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('edit_challenge.html', challenge=challenge)

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if not session.get('admin'):
        return redirect(url_for('login'))
    user = User.query.get(user_id)
    if user:
        UserChallenge.query.filter_by(user_id=user.id).delete()
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/reset_password/<int:user_id>', methods=['GET', 'POST'])
def reset_password(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        new_password = request.form['new_password']
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        flash('Lösenordet har uppdaterats!')
        return redirect(url_for('admin'))
    return render_template('reset_password.html', user=user)

if os.getenv("FLASK_ENV") != "production":
    with app.app_context():
        db.create_all()

# --- INIT ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))