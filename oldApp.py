from functions import loadAllData, saveData, PrepareData

deduplicate = False
url = "https://aleph.nkp.cz/F/6ACPY7ICL1CMUCTN8C2M9JFLY879P1XVVG4UD83BE9YQ3UJJH2-11132?func=find-b&find_code=WRD&x=22&y=12&request=Matematika&filter_code_1=WTP&filter_request_1=BK&filter_code_2=WLN&filter_request_2=cze&adjacent=N"
csv_file = open('output.csv', 'w', newline='')
csv_full_file = open('output_full.csv', 'w', newline='')
txt_file = open('output.txt', 'w', newline='')

# get all data posible
data = loadAllData(url, csv_file, csv_full_file)
print("\nAll data loaded\n\n")

    
# remove duplicates
newData = {}
for url, html in data.items():
    newData = PrepareData(newData, html, url, deduplicate)
print("\nAll data deduplicated\n\n")

# save data
for url, data in newData.items():
    saveData(data, csv_file, csv_full_file, txt_file)
print("\nAll data saved\n\n")
    
# Show some stats
print(f"Count of data: {len(newData)}")