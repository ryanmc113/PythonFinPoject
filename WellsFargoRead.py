import PyPDF2
# importing date class from datetime module 
from datetime import date 
import re 
import os 
from dotenv import load_dotenv
import GoogleSheetsReport

load_dotenv()

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            # if page_num > 1:
            page = reader.pages[page_num]
            text += page.extract_text()
        return text
    
def moneyFinder(text):
    #regex pattern for all payments.
    money_pattern = r'(?<=\s{5})\d+(?:,\d{3})*(?:\.\d{2})'
    moneyList = re.findall(money_pattern,text)
    return moneyList

def nameFinder(text):
    name_pattern = r'(?:\bPurchase)(.*)'
    nameList = re.findall(name_pattern, text)
    return nameList

def wellsFargoMain():
    wells_fargo_file_path = os.getenv('wells_fargo_file_path')
    text = read_pdf(wells_fargo_file_path)
    
    moneyList = moneyFinder(text)
    # remove the 'Deposits/Additions' total
    moneyList.pop(0)
    # print(name)
    GoogleSheetsReport.rowBuilder(nameFinder(text), moneyList, 'Wells Fargo')
    




