from email.policy import default
from pickle import FALSE
from flask import Flask, render_template, request, redirect, url_for, flash, abort, current_app
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, func, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime as dt
from flask_ckeditor import CKEditor
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, login_user, UserMixin
import uuid

from send_mail import send_reset_mail



#   FLASK
app = Flask(__name__)
app.config['SECRET_KEY']='iloveyounidawhyyoublockedme'


#   CKEditor
ckeditor = CKEditor(app)

#   Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


login_manager.login_view = 'login'


##################################################################################
#
#           DATABASE
#
##################################################################################
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogs.db'
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    #   default 
    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    secret_key = db.Column(db.String(250), default=uuid.uuid4().hex, nullable=False)
    created_date = db.Column(db.String(250), nullable=False)
    last_login = db.Column(db.String(250), nullable=False)
    #   user will give input
    firstName = db.Column(db.String(250), nullable=False)
    lastName = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    profile_image = db.Column(db.String(500), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    
    #   contact relation
    contacts_info = db.relationship("Contact", back_populates="user")

    #   bookmark relation
    bookmark_info = db.relationship("Bookmark", back_populates="user")

    #   comment relation
    comment_info = db.relationship("Comment", back_populates="user")


class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(250), nullable=False)
    message = db.Column(db.Text, nullable=False)
    send_date = db.Column(db.String(250), default=dt.now().strftime("%H:%M | %d %B %Y"), nullable=False)
    status = db.Column(db.Boolean, default=False, nullable=False)

    #   user relation
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    user = db.relationship("User", back_populates="contacts_info")


class Post(db.Model):
    __tablename__ = "posts"
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
    
    #   post relation
    post_info = db.relationship("Bookmark", back_populates="post")

    #   comment relation
    comment_post_info = db.relationship("Comment", back_populates="post")


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text_comment = db.Column(db.Text, nullable=False)
    date_comment = db.Column(db.String(250), default=dt.now().strftime("%H:%M | %d %B %Y"), nullable=False)

    #   user
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    user = db.relationship("User", back_populates="comment_info")
    
    #   comment 
    post_id = db.Column(db.Integer, ForeignKey('posts.id'))
    post = db.relationship("Post", back_populates="comment_post_info")

class Bookmark(db.Model):
    __tablename__ = "bookmarks"
    id = db.Column(db.Integer, primary_key=True)
    bookmark_date = db.Column(db.String(250), default=dt.now().strftime("%H:%M | %d %B %Y"), nullable=False)

    #   user
    user_id = db.Column(db.Integer, ForeignKey("users.id"))
    user = db.relationship("User", back_populates="bookmark_info")

    #   post
    post_id = db.Column(db.Integer, ForeignKey("posts.id"))
    post = db.relationship("Post", back_populates="post_info")


db.create_all()


##################################################################################
#
#            login
#
##################################################################################
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.admin != True:
            # return abort(403)
            return render_template("errors/403.html")
        return f(*args, **kwargs)
    return decorated_function


 
#   NEW (  For admin routes and page setup  )
##################################################################################
#
#           ADMIN ROUTES
#
##################################################################################
@app.route("/admin/")
@login_required
@admin_only
def dashboard():
    posts = Post.query.order_by(desc(Post.updated_date)).all()[:5]
    #   GET CATEGORIES WITH COUNT   
    categories_with_numbers = Post.query.with_entities(Post.category, func.count(Post.category)).group_by(Post.category).all()

    return render_template("admin/pages/index.html", path=request.path, posts=posts, chart_data=categories_with_numbers)


@app.route("/admin/get-all-post")
@login_required
@admin_only
def get_all_post():
    posts = Post.query.order_by(desc(Post.updated_date)).all()
    return render_template("admin/pages/posts.html", path=request.path, posts=posts)


@app.route("/admin/new-post", methods=["GET", "POST"])
@login_required
@admin_only
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

    return render_template("admin/pages/new-post.html", path=request.path)


@app.route("/admin/update-post/<int:post_id>", methods=["GET", "POST"])
@login_required
@admin_only
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

    return render_template("admin/pages/update-post.html", post=post)


@app.route("/admin/delete-post/<int:post_id>")
@login_required
@admin_only
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for("get_all_post"))



@app.route("/admin/profile")
@login_required
@admin_only
def admin_profile():
    return render_template("admin/auth/profile.html", path=request.path)


@app.route("/admin/contacts")
@login_required
@admin_only
def admin_contact():
    contacts = Contact.query.order_by(Contact.send_date).all()

    return render_template("admin/pages/contact.html", path=request.path, contacts=contacts)


@app.route("/admin/done-contact/<contact_id>")
@login_required
@admin_only
def done_contact(contact_id):

    contact = Contact.query.get(contact_id)

    if contact == None:
        return redirect(url_for("admin_contact"))

    if contact.status == True:
        contact.status = False
    else:
        contact.status = True
    
    db.session.add(contact)
    db.session.commit()

    return redirect(url_for("admin_contact"))


@app.route("/admin/comments")
@login_required
@admin_only
def admin_comments():
    comments = Comment.query.order_by(Comment.date_comment).all()
    return render_template("/admin/pages/comments.html", comments=comments, path=request.path)


@app.route("/admin/delete-comments/<comment_id>")
@login_required
@admin_only
def admin_delete_comments(comment_id):
    comment = Comment.query.get(comment_id)

    if comment == None:
        return redirect(url_for("admin_comments"))
    
    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for("admin_comments"))


@app.route("/admin/users")
@login_required
@admin_only
def admin_users():
    users = User.query.order_by(User.created_date).all()
    return render_template("admin/pages/users.html", path=request.path, users=users)


@app.route("/admin/delete-users/<user_id>")
@login_required
@admin_only
def admin_delete_users(user_id):
    user = User.query.get(user_id)

    if user == None:
        return redirect(url_for("admin_users"))
    
    if user.active == True:
        user.active = False
    elif user.active == False:
        user.active = True

    db.session.add(user)
    db.session.commit()

    return redirect(url_for("admin_users"))



@app.route("/admin/register", methods=["GET", "POST"])
def admin_register():
    # if user is logged in then redirect to home page
    if current_user.is_active == True:
        return redirect(url_for("home"))

    if request.method == "POST":
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        email = request.form["email"]
        phone = request.form["phone"]
        profile_image = request.form["profile_image"]
        password = request.form["password"]
        confirmPassword = request.form["confirmPassword"]

        # password equal check
        if password != confirmPassword:
            flash("Password and Confirm Password is did not match, Please enter same password")
            return redirect(url_for("admin_register"))
        
        # search exists email or phone
        if User.query.filter_by(email=email).first():
            flash("Email already register, Please enter anthor email address.")
            return redirect(url_for("admin_register"))
        elif User.query.filter_by(phone=phone).first():
            flash("Phone already register, Please enter anthor Phone address.")
            return redirect(url_for("admin_register"))
        
        # create new account
        hash_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=10)
        new_user = User(firstName=firstName,lastName=lastName,email=email,phone=phone,profile_image=profile_image,password=hash_password,admin=True,created_date=dt.now().strftime("%H:%M | %d %B %Y"), last_login=dt.now().strftime("%H:%M | %d %B %Y"))
        db.session.add(new_user)
        db.session.commit()

        # login user & redirect to dashboard
        login_user(new_user)
        return redirect(url_for("dashboard"))

    return render_template("admin/auth/register.html", path=request.path)


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    # #   if user is logged in then redirect to home
    if current_user.is_active == True:
        return redirect(url_for('home'))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        #   check user is exists or not
        if user == None:
            flash("User does not exist, Please create new account.")
            return redirect(url_for('admin_register'))

        #   check user is admin or not
        if user.admin == False:
            flash("Invalid user, You do not have permission to login here.")
            return redirect(url_for('login'))

        #   login user

        if check_password_hash(pwhash=user.password, password=password):
            #   update user last login
            user.last_login = dt.now().strftime("%H:%M | %d %B %Y")
            db.session.add(user)
            db.session.commit()

            # login user
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Wrong password, Please enter correct password")
            return redirect(url_for("admin_login"))

    return render_template("admin/auth/login.html", path=request.path)


@app.route("/admin/logout")
@login_required
@admin_only
def admin_logout():
    logout_user()
    return redirect(url_for("home"))


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
        return render_template("blog/pages/search.html", path=request.path, posts=search_posts, sidebar=sidebar, logged_in=current_user.is_authenticated)

    #   get posts by category
    category = request.args.get("category")
    if category != None:
        category_posts = Post.query.filter_by(category=category).all()
        return render_template("blog/pages/search.html", path=request.path, posts=category_posts, sidebar=sidebar, logged_in=current_user.is_authenticated)
    
    # get posts by tag
    query_tag = request.args.get("tag")
    if query_tag != None:        
        posts_list = Post.query.all()
        tag_posts = []
        for post in posts_list:
            tag = post.tags
            if query_tag in tag:
                tag_posts.append(post)
        return render_template("blog/pages/search.html", path=request.path, posts=tag_posts, sidebar=sidebar, logged_in=current_user.is_authenticated)
    
    return render_template("blog/pages/index.html", path=request.path, posts=posts, sidebar=sidebar, logged_in=current_user.is_authenticated)


@app.route("/blog")
def blog():
    posts = Post.query.order_by(desc(Post.updated_date)).all()
    
    #   SEARCH RESULTS
    search = request.args.get("search")
    if search != None:
        search_posts = Post.query.filter(Post.title.contains(search)).all()
        return render_template("blog/pages/search.html", path=request.path, posts=search_posts, sidebar=sidebar, logged_in=current_user.is_authenticated)

    #   get posts by category
    category = request.args.get("category")
    if category != None:
        category_posts = Post.query.filter_by(category=category).all()
        return render_template("blog/pages/search.html", path=request.path, posts=category_posts, sidebar=sidebar, logged_in=current_user.is_authenticated)
    
    # get posts by tag
    query_tag = request.args.get("tag")
    if query_tag != None:        
        posts_list = Post.query.all()
        tag_posts = []
        for post in posts_list:
            tag = post.tags
            if query_tag in tag:
                tag_posts.append(post)
        return render_template("blog/pages/search.html", path=request.path, posts=tag_posts, sidebar=sidebar, logged_in=current_user.is_authenticated)

    return render_template("blog/pages/blogs.html", path=request.path, posts=posts, sidebar=sidebar, logged_in=current_user.is_authenticated)  
    

@app.route("/post-detail/<int:post_id>", methods=["GET","POST"])
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
        return render_template("blog/pages/search.html", path=request.path, posts=search_posts, sidebar=sidebar, logged_in=current_user.is_authenticated)

    #   get posts by category
    category = request.args.get("category")
    if category != None:
        category_posts = Post.query.filter_by(category=category).all()
        return render_template("blog/pages/search.html", path=request.path, posts=category_posts, sidebar=sidebar, logged_in=current_user.is_authenticated)
    
    # get posts by tag
    query_tag = request.args.get("tag")
    if query_tag != None:        
        posts_list = Post.query.all()
        tag_posts = []
        for post in posts_list:
            tag = post.tags
            if query_tag in tag:
                tag_posts.append(post)
        return render_template("blog/pages/search.html", path=request.path, posts=tag_posts, sidebar=sidebar, logged_in=current_user.is_authenticated)
    
    # bookmark icon
    saved = True
    total_bookmark = 0

    if current_user.is_authenticated != True:
        saved = False

    if current_user.is_authenticated == True:
        bookmark = Bookmark.query.filter_by(user_id=current_user.id, post_id=post.id).first()
        if bookmark == None:
            saved = False
    
    # count total bookmark
    count_bookmark = Bookmark.query.filter_by(post_id=post_id).all()
    total_bookmark = len(count_bookmark)
    

    #   add new comment
    if request.method == "POST":
        if current_user.is_authenticated == False:
            flash("Please login to submit contact information.")
            return redirect(url_for("login"))

        text = request.form["comment"]
        new_comment = Comment(text_comment=text, user=current_user, post=post)
        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for("post_detail", post_id=post_id))
    
    #   users comment display
    # comments = Comment.query.filter_by(post_id=post_id).all()
    comments = Comment.query.order_by(Comment.date_comment).filter_by(post_id=post_id).all()

    return render_template("blog/pages/post-detail.html", post=post, sidebar=sidebar, logged_in=current_user.is_authenticated, saved=saved, total_bookmark=total_bookmark, comments=comments, total_comments=len(comments), user=current_user)


@app.route("/bookmark")
def bookmark():
    if current_user.is_authenticated != True:
        flash("Please login to bookmark post.")
        return redirect(url_for("login"))

    post = request.args.get("post_id")
    current_post = Post.query.get(post)

    #   check if user doese not have already bookmark this post
    bookmark = Bookmark.query.filter_by(user_id=current_user.id, post_id=current_post.id).first()
    if bookmark == None:
        #   save post
        new_bookmark = Bookmark(user=current_user, post=current_post)
        db.session.add(new_bookmark)
        db.session.commit()
        return redirect(url_for("post_detail", post_id=current_post.id))
    #   if user have already bookmark then remove post from bookmark
    else:
        #   remove bookmark post
        db.session.delete(bookmark)
        db.session.commit()

        return redirect(url_for("post_detail", post_id=current_post.id))


@app.route("/about")
def about():
    return render_template("blog/pages/about.html", path=request.path, logged_in=current_user.is_authenticated)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        if current_user.is_authenticated:
            subject = request.form["subject"]
            message = request.form["message"]

            new_contact = Contact(subject=subject, message=message, user=current_user)

            db.session.add(new_contact)
            db.session.commit()

            flash("Your message sent successfully.")
            return redirect(url_for("contact"))
        else:
            flash("Please login")
            return redirect(url_for("login"))
    
    return render_template("blog/pages/contact.html", path=request.path, logged_in=current_user.is_authenticated)


@app.route("/register", methods=["GET", "POST"])
def register():
    #   if user logged in then redirect to profile page
    if current_user.is_active == True:
        return redirect(url_for('profile'))

    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    confirmPassword = request.form.get("confirmPassword")
    profile_image = request.form.get("image")

    #   check email or phone in database exists
    if User.query.filter_by(email=email).first():
        flash("'Email' already exists, Please select different email address")
        return redirect(url_for("register"))
    elif User.query.filter_by(phone=phone).first():
        flash("'Contact Number' already exists, Please select different phone number")
        return redirect(url_for("register"))
    
    #   save data in database
    if request.method == "POST":
        if password == confirmPassword:
            #   generate hash password
            password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=10)

            new_user = User(firstName=firstName,lastName=lastName,email=email,phone=phone,password=password,profile_image=profile_image, created_date=dt.now().strftime("%H:%M | %d %B %Y"), last_login=dt.now().strftime("%H:%M | %d %B %Y"))

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)

            return redirect(url_for("home"))
        else:
            flash("'Password' not match with 'Confirm Password', Please enter same password.")
            return redirect(url_for("register"))

    return render_template("blog/auth/register.html", path=request.path)


@app.route("/login", methods=["GET", "POST"])
def login():
    #   if user logged in then redirect to profile page
    if current_user.is_active == True:
        return redirect(url_for('profile'))

    #   login user
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        #   user not exists
        if user == None:
            flash("'Email' doesn't exists, Please create new account")
            return redirect(url_for("register"))

        #   if user delete account redirect to register
        if user.active != True:
            flash("Please create new account")
            return redirect(url_for("register"))
        
        #   if user is admin then return, user does not exists becuase this form valid only for normal users
        if user.admin == True:
            flash("User not valid, Please create new account")
            return redirect(url_for("register"))

        #   if user exists then login user
        if user != None:
            if check_password_hash(pwhash=user.password, password=password):
                #   update last login time
                user.last_login = dt.now().strftime("%H:%M | %d %B %Y")
                db.session.add(user)
                db.session.commit()

                #   login 
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash("Wrong Password, Please enter correct password.")
                return redirect(url_for("login"))

    return render_template("blog/auth/login.html", path=request.path)


@app.route("/profile")
@login_required
def profile():
    #   contact
    contacts = Contact.query.all()
    contact_list = []
    for contact in (contacts):
        if contact.user_id == current_user.id:
            contact_list.append(contact)    
    
    #   bookmark
    # bookmarks_posts = Bookmark.query.filter_by(user_id=current_user.id).all()
    bookmarks_posts = Bookmark.query.order_by(desc(Bookmark.bookmark_date)).filter_by(user_id=current_user.id).all()

    #   comments
    comments = Comment.query.order_by(Comment.date_comment).filter_by(user_id=current_user.id).all()

    return render_template("blog/auth/profile.html", path=request.path, logged_in=current_user.is_authenticated, user=current_user, contact_list=contact_list, bookmarks_posts=bookmarks_posts, comments=comments)


@app.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).filter_by(user_id=current_user.id).first()

    post = Post.query.filter_by(id=comment.post_id).first()

    if comment != None:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for("post_detail", post_id=post.id))


@app.route("/change-password", methods=["POST"])
@login_required
def change_password():
    if request.method == "POST":
        # get user data
        user = current_user

        # form data
        current_password = request.form["currentPassword"]
        new_password = request.form["newPassword"]
        confirm_new_password = request.form["confirmNewPassword"]

        if check_password_hash(pwhash=user.password, password=current_password):
            if new_password == confirm_new_password:
                # update password
                user.password = generate_password_hash(password=new_password, method="pbkdf2:sha256", salt_length=8)
                db.session.add(user)
                db.session.commit()

                # logout current user
                logout_user()
                
                # redirect to login page
                return redirect(url_for("login"))
            else:
                flash("New password and Confirm new password, doesn't match, Please enter same password")
                return redirect(url_for("profile"))
        else:
            # redirect to same page
            flash("Current Password is Wrong, Please check once.")
            return redirect(url_for("profile"))


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    #   find user
    user = current_user

    if request.method == "POST":
        # get from form field
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        email = request.form["email"]
        phone = request.form["phone"]
        profile_image = request.form["image"]

        #   update existing user data
        user.firstName = firstName
        user.lastName = lastName
        user.email = email
        user.phone = phone
        user.profile_image = profile_image

        db.session.add(user)
        db.session.commit()        

        #   redirect to profile
        return redirect(url_for("profile"))

    return render_template("blog/auth/profile.html", path=request.path, logged_in=current_user.is_authenticated, user=user)


@app.route("/delete-account")
@login_required
def delete_account():
    #   delete account
    current_user.active = False
    db.session.add(current_user)
    db.session.commit()

    logout_user()

    return redirect(url_for("home"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/forget-password-send", methods=["GET", "POST"])
def forget_password_send():
    if request.method == "POST":
        email = request.form["email"]
        user = User.query.filter_by(email=email).first()

        # if user deleted account
        if user == None or user.active != True:
            flash("User does not exist, Please create new account.")
            return redirect(url_for("register"))
        
        #   if user is admin then return, user does not exists becuase this form valid only for normal users
        if user.admin == True:
            flash("User not valid, Please create new account")
            return redirect(url_for("register"))

        #   generate unique ID for reset password
        secret_key = uuid.uuid4().hex

        #   create reset link
        reset_link = f"http://127.0.0.1:5000/set-new-password/{email}/{secret_key}"

        #   update secret_key and get user secret_key then compare new secret_key to user secret_key
        user.secret_key = secret_key
        db.session.add(user)
        db.session.commit()

        #   send reset link to user email
        send_reset_mail(receiver_email=email, url=reset_link, name=user.firstName)

        flash("Reset password link has sent to you given your email address, go and click there.")
        return redirect(url_for("forget_password_send"))

    return render_template("blog/auth/forget-password-send.html")


@app.route("/set-new-password/<email>/<key>", methods=["GET", "POST"])
def set_new_password(email, key):
    user = User.query.filter_by(email=email).first()

    #   if anyone try to change url by email then redirect
    if user == None:
        return redirect(url_for("register"))

    if request.method == "POST":
        if user.secret_key == key:
            newPassword = request.form["newPassword"]
            confirmNewPassword = request.form["confirmNewPassword"]

            if newPassword == confirmNewPassword:
                # update password
                user.password = generate_password_hash(newPassword, method='pbkdf2:sha256', salt_length=8)

                # uodate secret_key then user can not use again
                user.secret_key = uuid.uuid4().hex

                db.session.add(user)
                db.session.commit()

                return redirect(url_for("login"))
        else:
            return redirect(url_for("register"))

    return render_template("blog/auth/set-new-password.html")



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

