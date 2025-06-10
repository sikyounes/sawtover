# models.py
from flask_pymongo import PyMongo
from datetime import datetime

mongo = PyMongo()

def init_app(app):
    mongo.init_app(app)

# We will use a collection named "posts".
# Each document in "posts" will represent a blog post and should ideally follow this structure:
# {
#     "title": "String, required",
#     "content": "String, required",
#     "slug": "String, required, unique (derived from title)",
#     "image_url": "String, optional (URL from Cloudinary)",
#     "public_id": "String, optional (Cloudinary public_id for image deletion/replacement)",
#     "created_at": "DateTime, default to now",
#     "updated_at": "DateTime, default to now, updated on edit"
# }

# Example of how to access the posts collection:
# from flask import current_app
# posts_collection = current_app.extensions["pymongo"]["db"].posts
