from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("MY_SECRET")
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config["MAIL_USERNAME"] = "codymilliron.testing@gmail.com"
app.config["MAIL_PASSWORD"] = os.getenv("GMAIL_SECRET")

db = SQLAlchemy(app)
mail = Mail(app)


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
        date = request.form["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form["occupation"]
        print(first_name,last_name, email, date, occupation)
        form = Form(first_name=first_name,
                    last_name=last_name,
                    email=email,
                    date=date_obj,
                    occupation=occupation)
        db.session.add(form)
        db.session.commit()

        message_body = f"{first_name}, thank you for your submission. " \
                       f"Here is your information:{first_name} {last_name}\nStart Date {date}" \
                       f"Current status: {occupation}"

        message = Message(subject="New Form Submission",
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[email],
                          body=message_body)

        mail.send(message)

        flash("You form was submitted succesfully!", "success")
    return render_template('index.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)

