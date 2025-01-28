from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify

app = Flask(__name__, template_folder='src/templates')
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)