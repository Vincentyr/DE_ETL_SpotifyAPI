# SEC Annual Report Data Extraction

This is a Data pipeline that aimed to extract SEC Edgar data using the API and automate the extraction process from the start and end off with a company dashboard that provide both overview and in depth data.

## First Step - Web Scraping to Extract the Annual Report URL

Referring to edgar.py, we have automate the extraction of the Financial Report.xslx document into our local machine of a single company. By changing the company name and year variable at the start of the script, we can easily download the files into our local machine for processing in BI tools (e.g. Tabelau / powerBI). You may refer to the sample - Facebook_Inc where we have extracted 10 years worth of data

## Second Step - Data Transform of the data within the excel

Next, we will have a number of annual report excel that we have in hand. This part will mainly be relying on using pandas dataframe so we can transform the data in the format that we can use. After much effort and searching on the Great Google, different company report their financial data differently. Hence, we will generalise the approach to transform the tables but we will still need customise some of the transformation after making sense of the data. You can refer to the transformation code to see the editable section where you will need to understand the financial report excel before committing 

