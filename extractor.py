import os
from functions import loadAllData, saveData, PrepareData, sendMail
import sys
import random
import string
import zipfile
import shutil
import time
import datetime
from config import get_config

config = get_config

start_time = time.time()

if not config["local"]:
    email = sys.argv[2]
else:
    email = None
    
url = sys.argv[1]
deduplicate = sys.argv[3]
exportOptions = sys.argv[4]
debug = config["debug"]

# Generate random folder name
folder_path = "tmp/" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=12)) + '/'
os.makedirs(folder_path, exist_ok=True)
csv_file = open(folder_path + 'output.csv', 'w', newline='')
csv_full_file = open(folder_path + 'output_full.csv', 'w', newline='')
txt_file = open(folder_path + 'output.txt', 'w', newline='')
log = open(folder_path + 'log.log', 'w', newline='')
log.write(f"Started at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
# write to log
if not config["local"]:
    log.write(f"local: True\ndeduplicate: {deduplicate}\npath: {folder_path}\nexportOption: {exportOptions}\ndebug: {debug}\nurl: {url}\n\n")
else:
    log.write(f"local: False\nemail: {email}\ndeduplicate: {deduplicate}\npath: {folder_path}\nexportOption: {exportOptions}\ndebug: {debug}\nurl: {url}\n\n")

# get all data posible
data = loadAllData(url, log, csv_file, csv_full_file)
# write to log
log.write("All data loaded\n\n")

    
# remove duplicates
newData = {}
for url, html in data.items():
    newData = PrepareData(log, newData, html, url, deduplicate)
# write to log
log.write("\nAll data deduplicated\n\n")

# save data
for url, data in newData.items():
    saveData(data, csv_file, csv_full_file, txt_file)
# write to log
log.write("\nAll data saved\n\n")
csv_file.close()
csv_full_file.close()
txt_file.close()
log.flush()

# create a zip file
with zipfile.ZipFile(folder_path + 'data.zip', 'w') as zip_file:
    # add the csv file to the zip
    zip_file.write(folder_path + 'output.csv', 'output.csv')
    # add the full csv file to the zip
    zip_file.write(folder_path + 'output_full.csv', 'output_full.csv')
    # add the txt file to the zip
    zip_file.write(folder_path + 'output.txt', 'output.txt')
    # add the log file to the zip if debug is enabled
    if debug:
        zip_file.write(folder_path + 'log.log', 'log.log')

zip_file.close()
# write to log
log.write("\nZip file created\n\n")

if exportOptions == "FullCSV":
    file = 'output_full.csv'
    file_type = 'text/csv'
elif exportOptions == "CSV":
    file = 'output.csv'
    file_type = 'text/csv'
elif exportOptions == "TXT":
    file = 'output.txt'
    file_type = 'text/plain'
else:
    file = 'data.zip'
    file_type = 'application/zip'


# send mail
if config["local"]:
    log.write("\nLocal mode enabled, skipping mail sending\n\n")
    # move file to current working directory
    shutil.move(folder_path + file, os.path.join(os.getcwd(), file))
else:
    sendMail(log, email, folder_path + file, file, file_type)
    log.write("\nMail sent\n\n")

end_time = time.time()
execution_time = end_time - start_time
log.write(f"\nScript execution time: {execution_time} seconds")

log.close()


# Remove the folder and its contents
if not debug:
    shutil.rmtree(folder_path[:-1])