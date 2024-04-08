from flask import Flask, render_template

app = Flask(__name__)

# Home page route
@app.route('/')
def home():
    message = "Here's a message passed from the Flask route to this home template."
    return render_template('home.html', message=message)

# Another page route
@app.route('/add')
def another_page():
    message = "Here's a message passed from the Flask route to this add template."
    return render_template('home.html', message=message)

if __name__ == "__main__":
    app.run(debug=True)
