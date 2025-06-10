from flask import Flask, render_template, abort

app = Flask(__name__)

# Sample blog post data (in-memory list of dictionaries)
posts_data = [
    {
        'id': 1,
        'title': 'First Post',
        'content': 'This is the full content of my very first blog post! Welcome to my minimal blog.'
    },
    {
        'id': 2,
        'title': 'Second Post',
        'content': 'This is another interesting article. I am exploring how to build a simple blog with Flask.'
    },
    {
        'id': 3,
        'title': 'A Day in the Life',
        'content': 'Today I woke up, coded a blog, and then wrote a post about it. It was a good day for coding and sharing.'
    }
]

@app.route('/')
def index():
    return render_template('index.html', posts=posts_data)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = next((post for post in posts_data if post['id'] == post_id), None)
    if post is None:
        abort(404) # Not found
    return render_template('post.html', post=post)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) # Added host and port for clarity
