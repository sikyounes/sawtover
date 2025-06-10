from flask import Flask, render_template # Added render_template for context processor
from routes.cms_routes import cms_bp
from routes.blog_routes import blog_bp
from models import init_app as init_db
from config import MONGODB_URI, CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, FLASK_SECRET_KEY
import cloudinary
from datetime import datetime # Added for context processor

app = Flask(__name__)
app.config['SECRET_KEY'] = FLASK_SECRET_KEY
app.config['MONGO_URI'] = MONGODB_URI

# Initialize extensions
init_db(app) # Initialize DB

# Configure Cloudinary
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

# Register blueprints
app.register_blueprint(cms_bp, url_prefix='/cms')
app.register_blueprint(blog_bp, url_prefix='/')

# Context processor to inject 'now' for templates
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) # Added host and port for clarity
