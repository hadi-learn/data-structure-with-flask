from sqlite3 import Connection as SQLite3Connection
from flask import Flask, request, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine
import linked_list
import hash_table
import binary_search_tree
import custom_q
import stack
import random

# app
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configure sqlite3 to enforce foreign key constraints
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

db = SQLAlchemy(app)
now = datetime.now()

# models
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    # posts = db.relationship("BlogPost")
    # without cascade, delete will be prevented because the foreign key constraint defined before
    posts = db.relationship("BlogPost", cascade="all, delete")

class BlogPost(db.Model):
    __tablename__ = "blog_post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

# routes
@app.route("/")
def home():
    return "Welcome"

@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = User(
        name = data["name"],
        email = data["email"],
        address = data["address"],
        phone = data["phone"],
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created"}), 200

@app.route("/user/descending_id", methods=["GET"])
def get_all_user_descending():
    users = User.query.all()
    all_user_ll = linked_list.LinkedList()

    for user in users:
        all_user_ll.insert_beginning(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
            }
        )

    return jsonify(all_user_ll.to_list()), 200

@app.route("/user/ascending_id", methods=["GET"])
def get_all_user_ascending():
    users = User.query.all()
    all_user_ll = linked_list.LinkedList()

    for user in users:
        all_user_ll.insert_at_end(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
            }
        )

    return jsonify(all_user_ll.to_list()), 200

@app.route("/user/<int:user_id>", methods=["GET"])
def get_one_user(user_id):
    users = User.query.all()

    all_users_ll = linked_list.LinkedList()

    for user in users:
        all_users_ll.insert_beginning(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
            }
        )

    user = all_users_ll.get_user_by_id(user_id)

    return jsonify(user), 200

@app.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    user_deleted = user
    db.session.delete(user)
    db.session.commit()
    return jsonify(f"user with id: {user_deleted.id} successfully deleted."), 200

@app.route("/blog_post/<int:user_id>", methods=["POST"])
def create_blog_post(user_id):
    data = request.get_json()

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message": "User does not exist!"}), 400

    ht = hash_table.HashTable(10)

    # print(data)
    ht.add_key_value("title", data["title"])
    ht.add_key_value("body", data["body"])
    ht.add_key_value("date", now)
    ht.add_key_value("user_id", user_id)

    ##### testing the functions
    # ht.print_table()
    # print(ht.get_value("title"))
    # print(ht.get_value("body"))
    # print(ht.get_value("date"))
    # print(ht.get_value("user_id"))

    new_blog_post = BlogPost(
        title = ht.get_value("title"),
        body = ht.get_value("body"),
        date = ht.get_value("date"),
        user_id = ht.get_value("user_id")
    )
    db.session.add(new_blog_post)
    db.session.commit()
    return jsonify({"message": "new blog post created"})


@app.route("/blog_post/<int:blog_post_id>", methods=["GET"])
def get_one_blog_post(blog_post_id):
    blog_posts = BlogPost.query.all()
    random.shuffle(blog_posts)

    bst = binary_search_tree.BinarySearchTree()

    for post in blog_posts:
        bst.insert({
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "date": post.date,
            "user_id": post.user_id,
        })

    post = bst.search(blog_post_id)

    if not post:
        return jsonify({"message": "post not found"}), 400

    return jsonify(post), 200


@app.route("/blog_post/numeric_body", methods=["GET"])
def get_numeric_post_bodies():
    blog_posts = BlogPost.query.all()

    q = custom_q.Queue()

    for post in blog_posts:
        q.enqueue(post)

    return_list = []

    for i in range(len(blog_posts)):
        post = q.dequeue()
        numeric_body = 0
        for char in post.data.body:
            numeric_body += ord(char)

        post.data.body = numeric_body

        return_list.append({
            "id": post.data.id,
            "title": post.data.title,
            "body": post.data.body,
            "user_id": post.data.user_id,
        })

    return jsonify(return_list), 200


@app.route("/blog_post/delete_last_10_posts", methods=["DELETE"])
def delete_last_10_posts():
    blog_posts = BlogPost.query.all()

    st = stack.Stack()

    for post in blog_posts:
        st.push(post)

    for i in range(10):
        posts_to_delete = s.pop()
        db.session.delete(posts_to_delete.data)
        db.session.commit()

    return jsonify({"message": "the last 10 blog posts successfully deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)
