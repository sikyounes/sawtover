from flask import Blueprint, render_template
from models import mongo

blog_bp = Blueprint('blog', __name__, template_folder='../templates/blog')

@blog_bp.route('/')
def index():
    posts = mongo.db.posts.find().sort("created_at", -1) # Sort by creation date
    return render_template('index.html', posts=posts)

@blog_bp.route('/post/<slug>')
def view_post(slug):
    post = mongo.db.posts.find_one_or_404({'slug': slug})
    return render_template('view_post.html', post=post)
