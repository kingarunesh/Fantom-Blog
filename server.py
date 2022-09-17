from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt


app = Flask(__name__)


##################################################################################
#
#           DATABASE
#
##################################################################################
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogs.db'
db = SQLAlchemy(app)


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(250), nullable=False)
#     email = db.Column(db.String(250), unique=True, nullable=False)
#     password = db.Column(db.String(250), nullable=False)
#     phone = db.Column(db.String(15), unique=True, nullable=False)
#     admin = db.Column(db.Boolean, default=False, nullable=False)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), unique=True, nullable=False)
    subtitle = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(250), nullable=False)
    tags = db.Column(db.String(500), nullable=False)
    total_view = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.String(250), nullable=False)
    updated_date = db.Column(db.String(250), nullable=False)


db.create_all()

##################################################################################
#
#           ADMIN ROUTES
#
##################################################################################
@app.route("/admin")
def dashboard():
    return render_template("admin/index.html", path=request.path)


@app.route("/admin/new-post", methods=["GET", "POST"])
def new_post():

    if request.method == "POST":
        title = request.form["title"]
        subtitle = request.form["subtitle"]
        description = request.form["description"]
        image_url = request.form["image_url"]
        category = request.form["category"]
        tags = request.form["tags"]
        created_date = dt.now().strftime("%d %B %Y")
        updated_date = dt.now().strftime("%d %B %Y")
        total_view = 1

        add_post = Post(
            title=title,
            subtitle=subtitle,
            description=description,
            image_url=image_url, 
            category=category, 
            tags=tags,
            created_date=created_date,
            updated_date=updated_date,
            total_view=total_view
            )

        db.session.add(add_post)
        db.session.commit()

        return redirect(url_for('get_all_post'))

    return render_template("admin/new-post.html", path=request.path)


@app.route("/admin/get-all-post")
def get_all_post():
    return render_template("admin/posts.html", path=request.path)


@app.route("/admin/profile")
def admin_profile():
    return render_template("admin/profile.html", path=request.path)


@app.route("/admin/contact")
def admin_contact():
    return render_template("admin/contact.html", path=request.path)


@app.route("/admin/register")
def admin_register():
    return render_template("admin/register.html", path=request.path)


@app.route("/admin/login")
def admin_login():
    return render_template("admin/login.html", path=request.path)



##################################################################################
#
#           BLOG ROUTES
#
##################################################################################
@app.route("/")
def home():
    return render_template("blog/index.html", path=request.path)


@app.route("/blog")
def blog():
    return render_template("blog/blogs.html", path=request.path)


@app.route("/post-detail")
def post_detail():
    return render_template("blog/post-detail.html")


@app.route("/about")
def about():
    return render_template("blog/about.html", path=request.path)


@app.route("/contact")
def contact():
    return render_template("blog/contact.html", path=request.path)


@app.route("/register")
def register():
    return render_template("blog/register.html", path=request.path)


@app.route("/login")
def login():
    return render_template("blog/login.html", path=request.path)


@app.route("/logout")
def logout():
    pass


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")