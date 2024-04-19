import subprocess
from flask import Flask, render_template, request
import os
from config import get_config

config = get_config()

# Create folders if they don't exist
folders = ['tmp']

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    
# Check if the file exists
if config["mailProvider"] == "sendgrid" and not os.path.isfile('sendgrid.env'):
    print("File 'sendgrid.env' does not exist. Exiting...")
    exit()

app = Flask(__name__)

# Home page route
@app.route('/')
def home():
    if config["local"]:
        return render_template('home.html', emailClass=" hide")
    else:
        return render_template('home.html', emailClass="")

# send route
@app.route('/send', methods=['POST'])
def sendPage():
    # Retrieve the data from the form
    data = {}
    data['link'] = request.form['linkInput']
    if 'deduplication' in request.form:
        data['deduplication'] = request.form['deduplication']
    else:
        data['deduplication'] = "off"
    data['exportOptions'] = request.form['exportOptions']
    if config["local"]:
        data['message'] = f"Vaše žádost byla úspěšně odeslána. Informace budou uloženy v lokální složce ({os.getcwd()}). Proces zpracování může trvat několik minut (15-25 minut)."
        command = ["nohup", "venv/bin/python3", "extractor.py", data['link'], data['deduplication'], data['exportOptions']]
    else:
        data['message'] = f"Vaše žádost byla úspěšně odeslána. Informace budou zaslány na e-mailovou adresu {request.form['email']}. Proces zpracování může trvat několik minut. Pokud do 15-25 minut nic nepřijde, zkontrolujte prosím složku s nevyžádanou poštou (spam) ve vaší e-mailové schránce. Děkujeme za vaši trpělivost."
        command = ["nohup", "venv/bin/python3", "extractor.py", data['link'], request.form['email'], data['deduplication'], data['exportOptions']]
    # Start the subprocess with nohup
    subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    return render_template('send.html', data=data)

if __name__ == "__main__":
    app.run(debug=config["debug"])
