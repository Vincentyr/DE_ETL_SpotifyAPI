import requests
import pandas as pd
import os

# inputs - Look up the company name in https://www.sec.gov/edgar/searchedgar/companysearch.html
# the company name have to be exact in cap and special charactor such as "."
company = ["Facebook Inc"]
# input the latest year you want it to be
latestyear = 2021
# the no. of year you want to backdate
yearstobackdate = 10
year = sorted([latestyear-x for x in range(yearstobackdate)])
# year = ['2015','2016','2017','2018','2019','2020','2021']
# writing files into local machine and change to your own directory
base_path = 'C:/Users/Yong Ren/Documents/Investment/Database/SEC_Edgar_Data_Extraction/SEC_Edgar_Data_Extraction' 

# fixed variable
quarter = ['QTR1','QTR2','QTR3','QTR4']
base_url = r"https://www.sec.gov/Archives/"
headers = {'User-Agent' : 'Mozilla/5.0'} # declare the user agent which is necessary to grant the right to using requests.get(), see SEC edgar documentation

# empty list for storing the master.idx data
fulldata = []
# we will extract all the data from QTR 1-4 in master.idx as they are not file accordingly to years
for years in year:
    for qtr in quarter:
        # unicode error have appear for some of the files, so we will skip those files
        try:
            # download
            index = requests.get(f'https://www.sec.gov/Archives/edgar/full-index/{years}/{qtr}/master.idx', headers=headers).content
            # NOTE! UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc3 in position 8510740: invalid continuation byte. perhaps do an exceptionerror line to avoid corrupted files
            data = index.decode('utf-8')
        except UnicodeDecodeError:
            print("UnicodeDecodeError, " + str(years) + str(qtr) + " file is not downloaded")
        newdata = data.split("\n")
        # through manual interpretation of master.idx file downloaded to determine the slicing but the rows headers that we slice off is standardise throughout all files
        newdata = newdata[11:]
        for item in newdata:
            fulldata.append(item.split("|"))
        print("Dowload done for " + str(years) + qtr)

# we will loop through all the company 
for companies in company:
    # Creating Dataframe to organise the data 
    df = pd.DataFrame(fulldata, columns=["CIK","Company Name","Form Type","Date Filed","File Name"])
    df10_K = df[(df['Company Name'] == companies) & (df["Form Type"] == '10-K')]
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
    
    current_dir = os.listdir(path=base_path)
    # we have to replace the "." in order to avoid creating a mess in filenaming convention. If you try to add a "." to window file directory, it will directly be omitted, and when you download files again, the directory is not able to match the file name
    companyname = companies.replace(" ", "_").replace(".","")
    if companyname not in current_dir:
        os.mkdir("/".join([base_path, companyname]))
    else:
        next

    #change directory 
    company_path = base_path + "/" + companyname
    os.chdir(company_path)

    # creating the filename for each download and check if file already exist. Finally, download the 10-K files
    file_dir = os.listdir(path=company_path)

    # finding the year for the finanical report to cater for newer company to use for our file naming
    # since edgar start filling in 1994/1995, we need to beware of files created in 1990s
    firstyear = int(allof10_K[0].split("-")[1])
    if firstyear > 93:
        yearinfull = int(str(19)+str(firstyear))
    else:
        yearinfull = int(str(20)+str(firstyear))

    for years, url in enumerate(new_url, yearinfull):
        filename = companyname + str(years) + "_AnnualReport.xlsx"
        if os.path.exists(filename) == True:
            next
        else:
            r = requests.get(url, headers=headers)
            # this will write the file into the current directory with the filename we created
            with open(filename, "wb") as f:
                f.write(r.content)
                f.close()
    print("All files downloaded for " + companies)
