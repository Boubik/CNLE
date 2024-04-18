from selenium import webdriver
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from config import get_config

def getChrome():
    options = webdriver.ChromeOptions() 
    options.add_argument("--headless")
    return Chrome(options=options)


def getHtmlFromInternet(drriver, url):
    drriver.get(url)
    return drriver.page_source

def PrepareData(log, newData, html, url, deduplicate):
    # Filter HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Get all data from filtered HTML
    table = soup.find('table', id='short_table', cellspacing='2', border='0', width='100%')
    try:
        tableRows = table.find_all('tr')
    except AttributeError:
        # write to log
        log.write('Error did not find tableRows: ' + str(url) + '\n')
        return newData
    

    i=0
    for row in tableRows:
        alredyIn = False
        cells = row.find_all('td', class_='td1')
        if i == 0:
            i += 1
            continue
        else:
            i += 1
        
        if deduplicate == "on":
            for key, inDbData in newData.items():
                if inDbData[2] == cells[2].text and inDbData[3] == cells[3].text and inDbData[4] == cells[4].text and inDbData[5] == cells[5].text and inDbData[6] == cells[6].text and inDbData[7] == cells[7].text:
                    # write to log
                    log.write('Alredy in: ' + str(cells[2].text) + '; ' + str(cells[3].text) + '; ' + str(cells[4].text) + '; ' + str(cells[5].text) + '; ' + str(cells[6].text) + '; ' + str(cells[7].text) + '\n')
                    alredyIn = True
                    break
                
        if not alredyIn:
            data = []
            for cell in cells:
                data.append(cell.text)
            newData[url + " - " + str(i)] = data
        
    return newData

def saveData(data, csv_file, csv_full_file, txt_file):
    
    csv_file.write(f"{data[2]};{data[3]};{data[4]};{data[5]};\n")
    k=0
    for cell in data:
        if k > 1:
            csv_full_file.write(cell + ';')
        k+=1
    csv_full_file.write('\n')
    
    txt_file.write(f"{data[2]}; {data[3]}; {data[4]}; {data[5]}\n")

def getAllSorts(html):
    soup = BeautifulSoup(html, 'html.parser')
    kek = soup.find('div', id='sort_options').findAll('a')
    url = []
    for newurl in kek:
        url.append(newurl['href'])
    return url

def loadAllData(url, log, csv_file, csv_full_file):            

    data = {}
    html = getHtmlFromInternet(url)
    soup = BeautifulSoup(html, 'html.parser')
    maxCount = int(soup.find('td', class_="title", id="bold", width="25%", nowrap="").text.split(' z ')[-1])
    if maxCount > 2500:
        maxCount = 2499
        
    
    table = soup.find('table', id='short_table', cellspacing='2', border='0', width='100%')
    tableLegends = table.find('tr').find_all('th', class_='text3')
    csv_file.write(f"{tableLegends[2].text};{tableLegends[3].text};{tableLegends[4].text};{tableLegends[5].text};\n")
    for cell in tableLegends:
        csv_full_file.write(cell.text + ';')
    csv_full_file.write('\n')
        
        
    filters = getAllSorts(html)
    maxFilters = len(filters)
    # write to log
    log.write(f"Max Filters: {maxFilters}\n")
    
    for filterId in range(0, maxFilters):
        filterUrl = filters[filterId]
        print("")
        html = getHtmlFromInternet(filterUrl)
        soup = BeautifulSoup(html, 'html.parser')
        # write to log
        log.write(f"Filter {filterId+1} of {len(filters)}\n")
        try:
            url = soup.find('a', title='Next')['href'][:-6]
            for i in range(1, maxCount + 1, 10):
                html = getHtmlFromInternet(url + str(i).zfill(6))
                # write to log
                log.write(f"URL: {url + str(i).zfill(6)}\n")
                soup = BeautifulSoup(html, 'html.parser')
                data[url + str(i).zfill(6)] = html
        except TypeError:
            url = None
        filters = getAllSorts(html)
        
        
    return data

def sendMail(log, email, full_path, file_name, file_type):
    config = get_config()
    # Email settings
    smtp_server = config["server"]
    smtp_port = config["port"]
    username = config["username"]
    password = config["password"]
    
    # Email content
    sender_email = username
    subject = 'CNLE - Potvrzení přijetí vašich dat'
    body = 'Dobrý den,\r\n\nVaše data byla úspěšně přijata a jsou přiložena k tomuto e-mailu.\r\n\nS pozdravem,\nCzech National Library Extractor'
    
    # Create MIME multipart message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email
    message['Subject'] = subject

    # Attach the email body
    message.attach(MIMEText(body, 'plain'))

    # Open the file in binary mode
    with open(full_path, "rb") as attachment:
        # Create a MIMEBase instance
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        'Content-Disposition',
        f'attachment; filename= {file_name}',
    )
    
    # Attach the file to the message
    message.attach(part)

    # Send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(username, password)
        text = message.as_string()
        server.sendmail(sender_email, email, text)
        server.quit()
        print("Email sent successfully!")
        log.write("\nEmail sent successfully\n")
    except Exception as e:
        print(f"Failed to send email: {e}")
        log.write(f"\nFailed to send email: {e.message}\n")

def sendMailOld(log, email, full_path, file_name, file_type):
    with open('sendgrid.env', 'r') as file:
        sendGridApiKey = file.read().strip()
    message = Mail(
        from_email='cnle@boubik.cz',
        to_emails=email,
        subject='CNLE - Potvrzení přijetí vašich dat',
        html_content='<p>Dobrý den,<br><br>Vaše data byla úspěšně přijata a jsou přiložena k tomuto e-mailu.<br><br>S pozdravem,<br>Czech National Library Extractor</p>')

    with open(full_path, 'rb') as f:
        data = f.read()
        f.close()
    encoded_file = base64.b64encode(data).decode()
    
    attachedFile = Attachment(
    FileContent(encoded_file),
    FileName(file_name),
    FileType(file_type),
    Disposition('attachment')
    )
    message.attachment = attachedFile
    
    try:
        sg = SendGridAPIClient(sendGridApiKey)
        response = sg.send(message)
        log.write(f"\n{response.status_code}\n")
        log.write(f"{response.body}\n")
        log.write(f"{response.headers}\n")
    except Exception as e:
        print(e.message)
        log.write(f"\n{e.message}\n")
        try:
            message = Mail(
                from_email='cnle@boubik.cz',
                to_emails='cboubik@gmail.com',
                subject='CNLE - Chyba při zpracování dat',
                html_content='<p>Dobrý den,<br><br>omlouváme se, ale nepodařilo se nám získat data z NKP. Prosím, zkuste zadat údaje znovu.<br><br>S pozdravem,<br>Czech National Library Extractor</p>')
        
            sg = SendGridAPIClient(sendGridApiKey)
            response = sg.send(message)
        
        except Exception as e:
            print(e.message)
            log.write(f"\n{e.message}\n")