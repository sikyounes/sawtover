import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')
CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
CMS_USER = os.getenv('CMS_USER')
CMS_PASSWORD = os.getenv('CMS_PASSWORD')
