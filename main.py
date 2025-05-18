import Capitalone
import GoogleSheetsReport
import WellsFargoRead
import customEmailGen
import DAO

#read pdfs
#make google sheets
#send email
#store numbers in database

WellsFargoRead.wellsFargoMain()
Capitalone.capitalOneMain()
customEmailGen.emailGenerator()