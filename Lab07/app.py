from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'saikrishnaraoyadagiri'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, primary_key=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@app.route('/')
def signIn():
    return render_template('signIn.html')

@app.route('/signUp')
def signUp():
    return render_template('signUp.html')

def is_email_unique(email):
    existing_user = User.query.filter_by(email=email).first()
    return existing_user is None


@app.route('/validateSignup', methods=['POST'])
def validate_password():
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')
    password = request.form.get('password')
    confirmPassword=request.form.get('confirmPassword')

    

    conditions_not_met = []

    if password != confirmPassword:
        conditions_not_met.append('Password & Confirm Password did not match.')
    
    if not is_email_unique(email) :
        conditions_not_met.append("Email ID is already used")

    if not any(s.islower() for s in password):
        conditions_not_met.append("Password should have at least one lowercase letter.")
    
    if not any(s.isupper() for s in password):
        conditions_not_met.append("Password should have at least one uppercase letter.")
    
    if not password[-1].isdigit():
        conditions_not_met.append("Password should have a number at the end.")
    
    if len(password) < 8:
        conditions_not_met.append("Password should have at least 8 characters.")
    
    if len(conditions_not_met) == 0:
        user = User(firstname=firstname,lastname=lastname,email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('thankyou', firstname=firstname,lastname=lastname))
    else:
        flash(conditions_not_met, 'error')
        return render_template('signUp.html',conditions_not_met=conditions_not_met)


@app.route('/validateSignIn', methods=['POST'])
def validate_signin():
    username=request.form.get('username')
    password=request.form.get('password')
    user = User.query.filter_by(email=username, password=password).first()
    if user:
        return render_template('secretPage.html')
    else:
        error='Invalid email or password.'
        return render_template('signIn.html', error=error)


        
@app.route('/thankyou/<firstname>/<lastname>')
def thankyou(firstname,lastname):
    return render_template('thankyou.html', firstname=firstname, lastname=lastname)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

