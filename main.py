from flask import Flask, render_template,request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

app.secret_key = "my_top_secret_123"
BASE_DIR =os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app )

class Card(db.Model):
    __tablename__ = "cards"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    user_email = db.Column(db.String(20), nullable=False)


    def __repr__(self):
        return f'<Card {self.id}>'

# Görev #1. Kullanıcı tablosunu oluşturun.
class User(db.Model):
    __tablename__= "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email= db.Column(db.String(35), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Card {self.id}>'
    
with app.app_context():
    db.create_all()

# İçerik sayfasını başlatma
@app.route('/', methods=['GET','POST'])
def login():
    error = ''
    if request.method == 'POST':
        form_login = request.form['email']
        form_password = request.form['password']
            
        # Görev #4. Kullanıcı doğrulamasını uygulayın
        users_db = User.query.all()
        for user in users_db:
            if form_login==user.email and form_password== user.password:
                session["user_email"]=user.email
                return redirect('/index')
            else:
                error = 'invalid username or passsword'
                return render_template('login.html', error = error)

     
    else:
        return render_template('login.html')



@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Görev #3. Kullanıcı doğrulamasını uygulayın
        user= User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        
        return redirect('/')
    
    else:    
        return render_template('registration.html')



@app.route('/index')
def index():
    email=session.get('user_email')
    cards =Card.query.filter_by(user_email=email).all()

    return render_template('index.html',
                           cards=cards
                           )

@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get_or_404(id)

    return render_template('card.html', card=card)


@app.route('/create')
def create():
    return render_template('create_card.html')


@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']

        email = session['user_email']
        card= Card(title=title,subtitle=subtitle,text=text,user_email=email)
        db.session.add(card)
        db.session.commit()
       
        return redirect('/')
    else:
        return render_template('create_card.html')


if __name__ == "__main__":
    app.run(debug=True)
