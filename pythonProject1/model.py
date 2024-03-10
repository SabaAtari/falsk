from __init__  import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(100),unique=True)
    username= db.Column(db.String(60))
    password_hash =db.Column(db.String(130))
    posts = db.relationship('Post',backref='user',lazy='dynamic')
    comments=db.relationship('Comment',backref='user',lazy='dynamic')
    likes = db.relationship('Like', backref='user', lazy='dynamic')

    def __init__(self,email,username,password):
        self.email=email
        self.username =username
        self.password_hash=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

class Post(db.Model):
    __tablename__='posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    content = db.Column(db.String())
    tags = db.Column(db.String())
    user_id = db.Column(db.ForeignKey('users.id'))
    likes = db.Column(db.Integer, default=0)
    comments=db.relationship('Comment',backref='post',lazy='dynamic')
    likes = db.relationship('Like', backref='post', lazy='dynamic')

    def __init__(self,title,content,tags,user_id):
        self.title=title
        self.content=content
        self.tags=tags
        self.user_id=user_id


    def __repr__(self):
        return self.content

class Comment(db.Model):
    __tablename__='comments'
    id = db.Column(db.Integer, primary_key=True)
    content=db.Column(db.String)
    post_id=db.Column(db.ForeignKey('posts.id'))
    user_id=db.Column(db.ForeignKey('users.id'))

    def __init__(self,content,post_id,user_id):
        self.content=content
        self.user_id=user_id
        self.post_id=post_id

class Like(db.Model):
    __tablename__='likes'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.ForeignKey('posts.id'))
    user_id = db.Column(db.ForeignKey('users.id'))

    def __init__(self, post_id, user_id):
        self.post_id = post_id
        self.user_id = user_id