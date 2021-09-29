from flask import render_template, Flask, url_for, request
import requests
import smtplib

MY_EMAIL = "anushajain.bang@yahoo.com"
PASSWORD = "xcjohaogktvrkata"

app = Flask(__name__)


@app.route("/")
def home():
    response = requests.get(url="https://api.npoint.io/645becfd899dc55f10c5")
    all_posts = response.json()
    return render_template("index.html", blog_posts=all_posts)


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact_page():
    if request.method == "POST":
        data = request.form
        send_email(data["username"], data["email_id"], data["phone_no"], data["user_message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


def send_email(username, email_id, phone_no, user_message):
    with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject: Blog Mail from Booting Coffee!\n\nName: {username}\nEmail id: {email_id}\nPhone no: {phone_no}\nMessage : {user_message}"
        )


@app.route('/post/<int:blog_id>')
def get_blog(blog_id):
    response = requests.get(url="https://api.npoint.io/645becfd899dc55f10c5")
    return render_template("post.html", blog=response.json()[blog_id - 1],
                           pic=url_for('static', filename=f'img/post{blog_id}-bg.jpg'))


if __name__ == "__main__":
    app.run(debug=True)
