from selenium import webdriver
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup

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

def PrepareData(newData, html, url, deduplicate):
    # Filter HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Get all data from filtered HTML
    table = soup.find('table', id='short_table', cellspacing='2', border='0', width='100%')
    try:
        tableRows = table.find_all('tr')
    except AttributeError:
        print('Error did not find tableRows: ' + str(url))
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
        
        if deduplicate:
            for key, inDbData in newData.items():
                if inDbData[2] == cells[2].text and inDbData[3] == cells[3].text and inDbData[4] == cells[4].text and inDbData[5] == cells[5].text and inDbData[6] == cells[6].text and inDbData[7] == cells[7].text:
                    print('Alredy in: ' + str(cells[2].text) + '; ' + str(cells[3].text) + '; ' + str(cells[4].text) + '; ' + str(cells[5].text) + '; ' + str(cells[6].text) + '; ' + str(cells[7].text))
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

def loadAllData(url, csv_file, csv_full_file):            

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
    print(f"Max Filters: {len(filters)}")
    k = 1
    for filterUrl in filters:
        print("")
        html = getHtmlFromInternet(filterUrl)
        soup = BeautifulSoup(html, 'html.parser')
        print(f"Filter {k} of {len(filters)}")
        try:
            url = soup.find('a', title='Next')['href'][:-6]
            for i in range(1, maxCount + 1, 10):
                html = getHtmlFromInternet(url + str(i).zfill(6))
                print(f"URL: {url + str(i).zfill(6)}")
                soup = BeautifulSoup(html, 'html.parser')
                data[url + str(i).zfill(6)] = html
        except TypeError:
            url = None
        k+=1
        
        
    return data