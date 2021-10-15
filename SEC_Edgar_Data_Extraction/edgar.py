import bs4 as bs 
import requests
import pandas as pd
import os

# inputs - Look up the company name in https://www.sec.gov/edgar/searchedgar/companysearch.html
company = "MICROSOFT CORP"
year = ['2018','2019','2020','2021']

# fixed variable
quarter = ['QTR1','QTR2','QTR3','QTR4']
base_url = r"https://www.sec.gov/Archives/"
headers = {'User-Agent' : 'Mozilla/5.0'} # declare the user agent which is necessary to grant the right to using requests.get()

# empty list for storing the data
fulldata = []
# we will extract all the data from QTR 1-4 in master.idx so we can the specific filing for the entire year
for years in year:    
    for qtr in quarter:
        # download
        index = requests.get(f'https://www.sec.gov/Archives/edgar/full-index/{years}/{qtr}/master.idx', headers=headers).content
        data = index.decode('utf-8')
        newdata = data.split("\n")
        newdata = newdata[11:]
        for item in newdata:
            fulldata.append(item.split("|"))
        print("Dowload done for " + years + qtr)

# Creating Dataframe to organise the data 
df = pd.DataFrame(fulldata, columns=["CIK","Company Name","Form Type","Date Filed","File Name"])
df10_K = df[(df['Company Name'] == company) & (df["Form Type"] == '10-K')]
# converting the filename dataframe into a list
allof10_K = df10_K['File Name'].values.tolist()

# transforming the URL to the annual report directory
# from this : 'https://www.sec.gov/Archives/edgar/data/789019/0001564590-18-019062.txt'
# to this: 'https://www.sec.gov/Archives/edgar/data/789019/000156459018019062'
new_url = []
for item in allof10_K:
    # remove "-"
    newc = [item.replace("-", "")]
    # remove .txt
    newnewc = newc[0].replace(".txt", "")
    new_url.append(base_url+newnewc+"/Financial_Report.xlsx")
    
# writing files into local machine
base_path = 'C:/Users/Yong Ren/Documents/Investment/Database/edgar' #<-change to your own directory
current_dir = os.listdir(path=base_path)
companyname = company.replace(" ", "_")
if companyname not in current_dir:
    os.mkdir("/".join([base_path, companyname]))

#change directory 
company_path = base_path + "/" + companyname
os.chdir(company_path)

# creating the filename for each download and check if file already exist. Finally, download the 10-K files
file_dir = os.listdir(path=company_path)

for year, url in enumerate(new_url, int(year[0])):
    filename = companyname + str(year) + "_AnnualReport.xlsx"
    if os.path.exists(filename) == True:
        next
    else:
        r = requests.get(url, headers=headers)
        with open(filename, "wb") as f:
            f.write(r.content)
            f.close()
    print("All files downloaded")
