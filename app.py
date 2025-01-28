from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from authlib.integrations.flask_client import OAuth
import os
from dotenv import load_dotenv

app = Flask(__name__, template_folder='src/templates')
app.secret_key = 'your_secret_key'

oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/login/google")
def login_google():
    redirect_uri = url_for('google_auth_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route("/auth/google/callback")
def google_auth_callback():
    token = google.authorize_access_token()
    if token is None:
        return "Login failed or denied.", 400

    user_info = token.get('userinfo')
    if user_info:
        session['user'] = user_info

    return redirect(url_for('profile'))

@app.route("/profile")
def profile():
    user = session.get("user")
    if not user:
        return redirect(url_for('index'))
    return (
        f"<h2>Welcome, {user.get('name')}!</h2>"
        f"<p>Email: {user.get('email')}</p>"
        "<p><a href='/logout'>Logout</a></p>"
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)