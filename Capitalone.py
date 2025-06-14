import PyPDF2

# importing date class from datetime module
from datetime import date
import re
import os
from dotenv import load_dotenv
import GoogleSheetsReport
import errno
import traceback

load_dotenv()


def read_pdf(file_path):
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(reader.pages)):
                if page_num > 1:
                    page = reader.pages[page_num]
                    text += page.extract_text()
            return text
    except OSError as err:
        if err.errno == errno.ENOENT:
            print("File not found")
        elif err.errno == errno.EACCES:
            print(
                f"[Errno {err.errno} ({errno.errorcode[err.errno]})] {os.strerror(err.errno)}"
            )
        else:
            print(err.errno)
    except Exception as e:
        print(traceback.format_exc())


def moneyFinder(text):

    # regex pattern for all payments.
    money_pattern = r"\$\d+(?:,\d{3})*(?:\.\d{2})"
    # regex pattern for all payments made, not spent
    money_pattern_payment = r"\-\s\$\d+(?:,\d{3})*(?:\.\d{2})"
    money = re.findall(money_pattern, text)
    money_paid = re.findall(money_pattern_payment, text)
    length_of_money_paid = len(money_paid)
    final_money = money[length_of_money_paid:]
    return final_money


def nameFinder(text):

    name_pattern = r"(?<=\d\s)(.*?)(?=\s\$)"
    name = re.findall(name_pattern, text)
    return name


def capitalOneMain():
    capital_one_file_path = os.getenv("capital_one_file_path")
    text = read_pdf(capital_one_file_path)
    moneyList = moneyFinder(text)
    totalMoneySpent = totalMoney(moneyList)
    GoogleSheetsReport.rowBuilder(
        removePayment(nameFinder(text)), moneyList, "CapitalOne"
    )
    return totalMoneySpent


finalTransactionNameArr = []


# removes names of the payments made from the list of bought items
def removePayment(transactionNamesArr):
    for transaction in transactionNamesArr:
        if "PYMTAuthDate" not in transaction:
            finalTransactionNameArr.append(transaction)
    return finalTransactionNameArr


def totalMoney(moneyList):
    total = 0
    for money in moneyList:
        total += float(money)

    return total
