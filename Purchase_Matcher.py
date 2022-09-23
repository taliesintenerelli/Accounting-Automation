#imports
import re
#import parse
import pdfplumber
import pandas as pd
from collections import namedtuple

#Line Creation
Line = namedtuple('Line', 'date company_name purchase_amount')

#Line Finder
G1_re = re.compile(r'(\d{1}/\d{2}) Purchase (.*) (\d{2}/\d{2}) (.*)(Olive Garden|Best Buy|Early Bird|Pizza Hut|Mc Donolds)')
G2_re = re.compile(r'\d{1,3}\.\d{2}')

#Tell it what file to use
file = r'C:\Users\tdten\Desktop\_021522 WellsFargo (1).pdf'

#Make "Lines" (different from "line") as an empty set
lines = []
total_check = 0

#Open the file, iterate through the pages, put it in a text file called "text", and make new line at the end of each line
with pdfplumber.open(file) as pdf:
    pages = pdf.pages
    for page in pdf.pages:
        text = page.extract_text()
        for line in text.split('\n'):
#Check if condisitons for the regular expressions are met
            date_and_name = G1_re.search(line)
            amount = G2_re.search(line)
#Define date, cmpany_name, and purchase_amount
            if date_and_name:
                date, company_name = date_and_name.group(3), date_and_name.group(5)
                purchase_amount = amount.group(0)
#Put the values into "Lines"
                lines.append(Line(date, company_name, purchase_amount))

#put in pandas
df = pd.DataFrame(lines)
df.head()

#print(df.info)

#convert purchase_amount from a string to a float
df['purchase_amount'] = df['purchase_amount'].map(lambda x: float(str(x).replace(',', '')))

#export as CSV
df.to_csv('Pmatch.csv', index=False)