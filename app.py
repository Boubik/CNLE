from flask import Flask, render_template, request, redirect, url_for
import subprocess

app = Flask(__name__)

# Home page route
@app.route('/')
def home():
    message = "Here's a message passed from the Flask route to this home template."
    return render_template('home.html', message=message)

# send route
@app.route('/send', methods=['POST'])
def sendPage():
    # Retrieve the data from the form
    data = {}
    data['link'] = request.form['linkInput']
    data['email'] = request.form['email']
    data['deduplication'] = request.form['deduplication']
    data['exportOptions'] = request.form['exportOptions']
    data['message'] = f"Vaše žádost byla úspěšně odeslána. Informace budou zaslány na e-mailovou adresu ({data['email']}). Proces zpracování může trvat několik minut. Děkujeme za vaši trpělivost."
    # Assuming you want to pass two parameters: 'param1' and 'param2'
    command = ["nohup", "venv/bin/python3", "test.py", data['link'], data['email'], data['deduplication'], data['exportOptions']]
    # Start the subprocess with nohup
    #subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    # Replace 'your_script.py' with the script you want to run, along with any necessary arguments
    #data['resault'] = subprocess.run(["venv/bin/python3", "test.py", "param1", "param2"], capture_output=True, text=True)
    return render_template('send.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)
