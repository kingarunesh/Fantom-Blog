from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, func
from datetime import datetime as dt
from flask_ckeditor import CKEditor



app = Flask(__name__)

app = Flask(__name__)
ckeditor = CKEditor(app)


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
 
#   NEW (  For admin routes and page setup  )
##################################################################################
#
#           ADMIN ROUTES
#
##################################################################################
@app.route("/admin")
def dashboard():
    posts = Post.query.order_by(desc(Post.updated_date)).all()[:5]
    return render_template("admin/index.html", path=request.path, posts=posts)


@app.route("/admin/get-all-post")
def get_all_post():
    posts = Post.query.order_by(desc(Post.updated_date)).all()
    return render_template("admin/posts.html", path=request.path, posts=posts)


@app.route("/admin/new-post", methods=["GET", "POST"])
def new_post():

    if request.method == "POST":
        title = request.form["title"]
        subtitle = request.form["subtitle"]
        # description = request.form["description"]
        description = request.form.get("ckeditor")
        image_url = request.form["image_url"]
        category = request.form["category"]
        tags = request.form["tags"]
        created_date = dt.now().strftime("%H:%M | %d %B %Y")
        updated_date = dt.now().strftime("%H:%M | %d %B %Y")
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


@app.route("/admin/update-post/<int:post_id>", methods=["GET", "POST"])
def update_post(post_id):
    post = Post.query.get(post_id)

    if request.method == "POST":
        post.title = request.form["title"]
        post.subtitle = request.form["subtitle"]
        # post.description = request.form["description"]
        post.description = request.form.get("ckeditor")
        post.image_url = request.form["image_url"]
        post.category = request.form["category"]
        post.tags = request.form["tags"]
        post.updated_date = dt.now().strftime("%H:%M | %d %B %Y")

        db.session.add(post)
        db.session.commit()

        return redirect(url_for("get_all_post"))

    return render_template("admin/update-post.html", post=post)


@app.route("/admin/delete-post/<int:post_id>")
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for("get_all_post"))



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


#   NEW (  For normal user routes and page setup  )
##################################################################################
#
#           CATEGORIES, TAGS
#
##################################################################################
#   GET CATEGORIES WITH COUNT   
categories_with_numbers = Post.query.with_entities(Post.category, func.count(Post.category)).group_by(Post.category).all()


#   tags
posts = Post.query.all()
# all tags
tag_list = []
for post in posts:
    tag = post.tags.split(',')
    for t in tag:
        tag_list.append(t)
 
# unique tags
unique_tags = []
for tag in tag_list:
    if tag not in unique_tags:
        unique_tags.append(tag)

# get top 5 popular post by post view count
popular_posts = Post.query.order_by(desc(Post.total_view))[:5]


sidebar = {
    "categories_with_numbers":categories_with_numbers,
    "tags":unique_tags,
    "popular_posts":popular_posts
}

##################################################################################
#
#           BLOG ROUTES
#
##################################################################################
@app.route("/")
def home():
    #   get all post by updated_date - order
    posts = Post.query.order_by(desc(Post.updated_date)).all()

    #   SEARCH RESULTS
    search = request.args.get("search")
    if search != None:
        search_posts = Post.query.filter(Post.title.contains(search)).all()
        return render_template("blog/search.html", path=request.path, posts=search_posts, sidebar=sidebar)
    
    return render_template("blog/index.html", path=request.path, posts=posts, sidebar=sidebar)


@app.route("/blog")
def blog():
    posts = Post.query.order_by(desc(Post.updated_date)).all()

    #   SEARCH RESULTS
    search = request.args.get("search")
    if search != None:
        search_posts = Post.query.filter(Post.title.contains(search)).all()
        return render_template("blog/search.html", path=request.path, posts=search_posts, sidebar=sidebar)

    return render_template("blog/blogs.html", path=request.path, posts=posts, sidebar=sidebar)  
    

@app.route("/post-detail/<int:post_id>")
def post_detail(post_id):
    post = Post.query.get(post_id)

    # increase post view number
    post.total_view += 1
    db.session.add(post)
    db.session.commit()

    #   SEARCH RESULTS
    search = request.args.get("search")
    if search != None:
        search_posts = Post.query.filter(Post.title.contains(search)).all()
        return render_template("blog/search.html", path=request.path, posts=search_posts, sidebar=sidebar)

    return render_template("blog/post-detail.html", post=post, sidebar=sidebar)


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
