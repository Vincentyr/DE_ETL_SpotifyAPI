import pandas as pd
import os

# inputs  
# File path for local machine
company = "Facebook_Inc"
local_path = "C:/Users/Yong Ren/Documents/Investment/Database/SEC_Edgar_Data_Extraction/SEC_Edgar_Data_Extraction"
company_path = "/".join([local_path, company])
sheetnumber = 3

# fixed variable 
# the base dataframe sheet name for 10-K form
sheetname = []

# set a base dataframe for to merge all other files so we will have a base dataframe to merge all others later
file_dir = os.listdir(path=company_path)
# as the file are arranged in order, we will always extract the first file as our base dataframe
file_path = company_path + "/" + file_dir[0]
df = pd.read_excel(file_path, None)
for i in df.keys():
    sheetname.append(i)

# [To be editted] Dataframe variable - You have to look through the financial report.xslx manually and select which sheet to look at
# For our Fundamental analysis, reports vary from company to company but we are looking at the following statements :
# 1. Balance Sheet
# 2. Income Statement
# 3. Cashflow
df_income_base = pd.read_excel(file_path, sheetname[sheetnumber]).fillna("")

# check if there is unnamed column based on the format of the 10-K sheet and rearrange the column naming convention
if any(df_income_base.columns.str.match('Unnamed')):
    columnheader = list(df_income_base.loc[0])
    rename = [x.split(",")[-1].replace(" ", "") for x in columnheader]
    rename[0] = columnheader[0]
    # i have rearrange the order of the balance sheet from descending to ascending so that it will continue during the merging function
    rename =  [rename[0]] + rename[len(rename):0:-1]
    df_income_base.columns = rename
else:
    next

# Create a loop for the rest of the files within the local machine
for i in range(1,len(file_dir)):
    # this steps is a duplicate of the code used to generate base dataframe
    new_file_path = company_path + "/" + file_dir[i]
    df_temp = pd.read_excel(new_file_path, None)
    # we have to declare the temp list here so it will can be overwrite in each cycle
    sheetname_temp = []
    for i in df_temp.keys():
        sheetname_temp.append(i)
    df_income = pd.read_excel(new_file_path, sheetname_temp[sheetnumber]).fillna("")

    # checking if we have an invalid columns name due to the format in sheet such as income statement
    if any(df_income.columns.str.match('Unnamed')):
        columnheader_temp = list(df_income.loc[0])
        rename_temp = [x.split(",")[-1].replace(" ", "") for x in columnheader_temp]
        rename_temp[0] = columnheader_temp[0]
        df_income.columns = rename_temp

    # we will take the base dataframe description as master and drop any subsequent description
    df_income = df_income.drop(df_income.columns[0], axis=1)
    print(df_income_base.columns)

    # [To be editted] inserting new row with no value in dataframe. For FB income statement, we see that there is addition column at interest and other income and added new rows
    df_income.loc[9.1] = ["","",""]
    df_income.loc[9.2] = ["","",""]
    df_income = df_income.sort_index().reset_index(drop=True)

    # merging the dataframe together via the outer merge and we will use suffixes to rename duplicate comlumn so we can filter away any duplicate
    df_income_base = df_income_base.merge(df_income,left_index=True, right_index=True, how='inner', suffixes=('', '_DROP')).filter(regex='^(?!.*_DROP)')

# save the dataframe to local machine
current_dir = os.listdir(path=company_path)
# we have to replace the "." in order to avoid creating a mess in filenaming convention. If you try to add a "." to window file directory, it will directly be omitted, and when you download files again, the directory is not able to match the file name
companyname = company.replace(" ", "_").replace(".","") + "_Compiled_Data"
if companyname not in current_dir:
    os.mkdir("/".join([company_path, companyname]))
else:
    next
new_dir = "/".join([company_path, companyname])
os.chdir(new_dir)

filename = company + "_compiled.xlsx"
file_path = "/".join([company_path, companyname, filename])
df_income_base.to_excel(file_path, sheet_name = sheetname[sheetnumber])