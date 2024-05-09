from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("MY_SECRET")
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))



@app.route("/", methods=["GET", "POST"])
def index():
    print(request.method)
    if request.method == "POST":
        first_name = request.form["first-name"]
        last_name = request.form["last-name"]
        email = request.form["email"]
        date = datetime.strptime(request.form["date"], "%Y-%m-%d")
        occupation = request.form["occupation"]
        print(first_name,last_name, email, date, occupation)
        form = Form(first_name=first_name,
                    last_name=last_name,
                    email=email,
                    date=date,
                    occupation=occupation)
        db.session.add(form)
        db.session.commit()
        flash("You form was submitted succesfully!", "success")
    return render_template('index.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)

