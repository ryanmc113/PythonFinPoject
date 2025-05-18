from numbers_parser import Document
doc = Document("/Users/ryanmcumber/Documents/Finances.numbers")


sheets = doc.sheets
tables = sheets[0].tables
rows = tables[0].rows()

def findNonEmptyCells(rows):
    finalArr = []
    for cell in rows:
        nestArr = []
        for values in cell:
            nestArr.append(values.value)
        finalArr.append(nestArr)

    return finalArr
    
print(findNonEmptyCells(rows))
