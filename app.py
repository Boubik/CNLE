import subprocess
from flask import Flask, render_template, request
import os

debug = 0

# Create folders if they don't exist
folders = ['tmp', 
           'tmp/count', 
           'tmp/data']

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    
# Check if the file exists
if not os.path.isfile('sendgrid.env'):
    print("File 'sendgrid.env' does not exist. Exiting...")
    exit()

app = Flask(__name__)

# Home page route
@app.route('/')
def home():
    return render_template('home.html')

# send route
@app.route('/send', methods=['POST'])
def sendPage():
    # Retrieve the data from the form
    data = {}
    data['link'] = request.form['linkInput']
    data['email'] = request.form['email']
    if 'deduplication' in request.form:
        data['deduplication'] = request.form['deduplication']
    else:
        data['deduplication'] = "off"
    data['exportOptions'] = request.form['exportOptions']
    command = ["nohup", "venv/bin/python3", "extractor.py", data['link'], data['email'], data['deduplication'], data['exportOptions'], str(debug)]
    # Start the subprocess with nohup
    subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    return render_template('send.html', data=data)

if __name__ == "__main__":
    app.run(debug=bool(debug))
