from selenium import webdriver
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import concurrent.futures

def getHtmlFromInternet(url):
    # Define the Chrome webdriver options
    options = webdriver.ChromeOptions() 
    options.add_argument("--headless") # Set the Chrome webdriver to run in headless mode for scalability

    # By default, Selenium waits for all resources to download before taking actions.
    # However, we don't need it as the page is populated with dynamically generated JavaScript code.
    #options.page_load_strategy = "none"

    # Pass the defined options objects to initialize the web driver 
    driver = Chrome(options=options) 
    # Set an implicit wait of 5 seconds to allow time for elements to appear before throwing an exception
    #driver.implicitly_wait(5)

    driver.get(url)
    #time.sleep(5)

    # Print the value of the JavaScript variable

    # Get HTML from URL using Selenium
    return driver.page_source

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
    # write to log
    log.write(f"Max Filters: {len(filters)}\n")
    k = 1
    for filterUrl in filters:
        print("")
        html = getHtmlFromInternet(filterUrl)
        soup = BeautifulSoup(html, 'html.parser')
        # write to log
        log.write(f"Filter {k} of {len(filters)}\n")
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
        k+=1
    return data

def loadAllDataMulti(url, log, csv_file, csv_full_file):

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
    # write to log
    log.write(f"Max Filters: {len(filters)}\n")
        
    # Using ThreadPoolExecutor to execute the function in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Map each filterUrl in filters to the getHtmlByFilter function call
        # Assign a unique k value to each call using enumerate
        future_to_url = {executor.submit(getHtmlByFilter, filterUrl, log, k+1, maxCount): filterUrl for k, filterUrl in enumerate(filters)}

        # Dictionary to store the combined results from all URLs
        combined_results = {}

        # Collecting results
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()  # This will be the dictionary returned by getHtmlByFilter
                combined_results.update(data)  # Merge the dictionary into the combined_results
                print(f"Data received from {url}: {data}")
            except Exception as exc:
                print(f'{url} generated an exception: {exc}')
            
            
    return combined_results

def getHtmlByFilter(filterUrl, log, k, maxCount):
    data = {}
    print("")
    html = getHtmlFromInternet(filterUrl)
    soup = BeautifulSoup(html, 'html.parser')
    # write to log
    log.write(f"Filter {k} started\n")
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
    k+=1
    
    return data
    

def sendMail(log, email, full_path, file_name, file_type):
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