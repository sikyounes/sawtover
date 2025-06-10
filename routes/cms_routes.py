from flask import Blueprint, render_template, request, redirect, url_for, flash
from functools import wraps
from models import mongo
from bson.objectid import ObjectId
import cloudinary.uploader
import cloudinary.api
from config import CMS_USER, CMS_PASSWORD
from datetime import datetime
import re

cms_bp = Blueprint('cms', __name__, template_folder='../templates/cms')

# Decorator for basic authentication
def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth or not (auth.username == CMS_USER and auth.password == CMS_PASSWORD):
            return ('Unauthorized', 401, {'WWW-Authenticate': 'Basic realm=Login Required'})
        return f(*args, **kwargs)
    return decorated_function

def generate_slug(title):
    slug = re.sub(r'[^\w\s-]', '', title).strip().lower()
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug

@cms_bp.route('/')
@auth_required
def index():
    return redirect(url_for('cms.list_posts'))

@cms_bp.route('/posts')
@auth_required
def list_posts():
    posts = mongo.db.posts.find().sort(created_at, -1)
    return render_template('list_posts.html', posts=posts)

@cms_bp.route('/posts/new', methods=['GET', 'POST'])
@auth_required
def add_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        image = request.files.get('image')

        image_url = None
        public_id = None

        if not title or not content:
            flash('Title and content are required.', 'error')
            return render_template('add_post.html', title=title, content=content) # Pass current values back

        slug = generate_slug(title)
        if mongo.db.posts.find_one({'slug': slug}):
            flash(f"A post with slug '{slug}' already exists. Please choose a different title.", 'error')
            return render_template('add_post.html', title=title, content=content) # Pass current values back

        if image and image.filename != '':
            try:
                upload_result = cloudinary.uploader.upload(image)
                image_url = upload_result['secure_url']
                public_id = upload_result['public_id']
            except Exception as e:
                flash(f'Error uploading image: {e}', 'error')

        now = datetime.utcnow()
        post_data = {
            'title': title,
            'content': content,
            'slug': slug,
            'image_url': image_url,
            'public_id': public_id,
            'created_at': now,
            'updated_at': now
        }

        mongo.db.posts.insert_one(post_data)
        flash('Post created successfully!', 'success')
        return redirect(url_for('cms.list_posts'))
    # This is for GET request
    return render_template('add_post.html')

@cms_bp.route('/posts/edit/<post_id>', methods=['GET', 'POST'])
@auth_required
def edit_post(post_id):
    post = mongo.db.posts.find_one_or_404({'_id': ObjectId(post_id)})
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        image = request.files.get('image')

        if not title or not content:
            flash('Title and content are required.', 'error')
            return render_template('edit_post.html', post=post)

        new_slug = generate_slug(title)
        if post['slug'] != new_slug and mongo.db.posts.find_one({'slug': new_slug, '_id': {'$ne': ObjectId(post_id)}}):
            flash(f"A post with slug '{new_slug}' already exists. Please choose a different title.", 'error')
            return render_template('edit_post.html', post=post, title=title, content=content) # Pass current values back

        update_data = {
            'title': title,
            'content': content,
            'slug': new_slug,
            'updated_at': datetime.utcnow()
        }

        if image and image.filename != '':
            if post.get('public_id'):
                try:
                    cloudinary.uploader.destroy(post['public_id'])
                except Exception as e:
                    flash(f'Error deleting old image: {e}', 'warning')

            try:
                upload_result = cloudinary.uploader.upload(image)
                update_data['image_url'] = upload_result['secure_url']
                update_data['public_id'] = upload_result['public_id']
            except Exception as e:
                flash(f'Error uploading new image: {e}', 'error')

        mongo.db.posts.update_one({'_id': ObjectId(post_id)}, {'$set': update_data})
        flash('Post updated successfully!', 'success')
        return redirect(url_for('cms.list_posts'))

    # This is for GET request
    return render_template('edit_post.html', post=post)

@cms_bp.route('/posts/delete/<post_id>', methods=['POST'])
@auth_required
def delete_post(post_id):
    post = mongo.db.posts.find_one_or_404({'_id': ObjectId(post_id)})

    if post.get('public_id'):
        try:
            cloudinary.uploader.destroy(post['public_id'])
        except Exception as e:
            flash(f'Error deleting image from Cloudinary: {e}', 'warning')

    mongo.db.posts.delete_one({'_id': ObjectId(post_id)})
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('cms.list_posts'))
