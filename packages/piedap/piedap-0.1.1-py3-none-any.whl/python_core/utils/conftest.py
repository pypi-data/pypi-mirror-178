from pyjavaproperties import Properties
import pytest
import os
import sys
from pathlib import Path
ROOT_DIR = str(Path(__file__).parent.parent)
NEW_DIR=ROOT_DIR+"\\"
print(NEW_DIR)
sys.path.append(NEW_DIR)

X_root=str(Path(__file__).parent.parent.parent.parent)
X_dir=X_root+"\\"

sys.path.append(X_dir)

from python_core.keywords.globkeyword import globKeywords
import allure
from python_core.config import constants

    
prod = Properties()
envProp = Properties()
envPath = open(X_dir+"environment\\production.properties")
envProp.load(envPath)


print("Current directory",os.curdir)

# @pytest.fixture(scope='function', autouse=True)
def base_fixture(application):
    print("base_fixture method invoked")
    constants.log_write("base_fixture method invoked \r\n") 
    with allure.step("Initializing block....."):
        try:
            #prodPath= moduleSuite.xpath_loc()
            prodPath = open(X_dir+"project_exco\\"+application+"\\ObjectProperties\\xpath.properties")
            print("Prodpath",prodPath)
            constants.log_write("Prodpath") 
            #prod.load(prodPath)
            print("product path", prodPath)
            
            path = open(X_dir+"environment\\production.properties")
            print("envpath",path)
            envProp.load(path)
            #d = driverScript()          
            #Dlist.append(d)
        except FileNotFoundError as f:
            print(f)
    # yield locals()
    # with allure.step("Finishing block....."):
    #     gen.quit()
