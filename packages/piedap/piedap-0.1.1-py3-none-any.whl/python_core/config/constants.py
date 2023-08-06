import os
from datetime import datetime
import sys
from pathlib import Path

ROOT_DIR = str(Path(__file__).parent.parent.parent)
NEW_DIR=ROOT_DIR+"\\"

X_root=str(Path(__file__).parent.parent.parent.parent)
X_dir=X_root+"\\"


DATASHEET = "DataSheet"
TESTCASESHEET = "TestCase"
KEYWORDSHEET = "Keyword"

TESTSUITE="TestSuite"

TCID = "TCID"
RUNMODE = "RunMode"
KEYWORD = "Keyword"
OBJECT = "Object"
DATA = "Data"

RUNMODE_YES = "Y"
RUNMODE_NO = "N"

CHROME='Chrome'
FIREFOX='Firefox'
EDGE='Edge'
IE='IE'

Y='Y'
N='N'
DIR_CLR_FLAG = 'Y'
flag=0
keyflag=0
allure_dir=X_dir+"piap\\temp\\allure-report"


chrome_path=NEW_DIR+'drivers\\Browsers\\chromedriver.exe'
edge_path=NEW_DIR+'drivers\\Browsers\\msedgedriver.exe'
firefox_path=NEW_DIR+'drivers\\Browsers\\geckodriver.exe'

rep_flag=0

order_dict={}

def log_write2(log_var,log_var2):
    f= open(X_dir+"\\piam\\logs\\log.txt","a+")
    f.write("\n\r"+log_var+"%"+log_var2+"\n\r")
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    f.write("Current date and time: %s"%dt_string)
    f.close
    
    
def log_write(log_var):
    
    f= open(X_dir+"\\piam\\logs\\log.txt","a+")
    f.write(log_var+"\n\r")
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    f.write("Current date and time: %s"%dt_string)
    f.close
run_order=0

config_path=X_dir+"piam\\userconfigurations\\web_automation\\config.properties"
env_Path = X_dir+"environment\\production.properties"

