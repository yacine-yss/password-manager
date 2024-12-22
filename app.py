from flask import Flask, flash, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = "this is secret"
db = SQLAlchemy(app)

# Model
class PasswordManager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(555), nullable=False)
    url = db.Column(db.String(555), nullable=False)
    password = db.Column(db.String(555), nullable=False)

    def __repr__(self):
        return f'<PasswordManager {self.email}>'

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form['email']
        url = request.form['url']
        password = request.form['password']

        new_entry = PasswordManager(email=email, url=url, password=password)
        db.session.add(new_entry)
        db.session.commit()

    password_list = PasswordManager.query.all()
    return render_template('index.html', passwordlist=password_list)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = PasswordManager.query.get_or_404(id)

    if request.method == 'POST':
        task.email = request.form['email']
        task.url = request.form['url']
        task.password = request.form['password']
        try:
            db.session.commit()
            flash("Password Updated")
            return redirect('/')
        except:
            flash("There was an issue updating your task")
            return redirect('/')
    
    
    return render_template('update.html', task=task)


@app.route('/delete/<int:id>')
def delete (id):
    new_password_to_delete=PasswordManager.query.get_or_404(id)
    try:
        db.session.delete(new_password_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return("there is an error ")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
