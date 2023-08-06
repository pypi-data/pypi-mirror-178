from lib2to3.pgen2 import driver
from _overlapped import NULL
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import allure
from selenium.webdriver import Edge
from msedge.selenium_tools import EdgeOptions
from allure_commons.types import AttachmentType
import logging
from datetime import datetime
import sys
import os
from pathlib import Path
ROOT_DIR = str(Path(__file__).parent.parent.parent)
NEW_DIR=ROOT_DIR+"\\"
sys.path.append(NEW_DIR)
CUR_DIR = str(Path(__file__).parent.parent.parent.parent)
N_DIR=CUR_DIR+"\\"
sys.path.append(N_DIR)
from python_core.config import constants
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from pyjavaproperties import Properties
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


config=Properties()
path=constants.config_path
config.load(open(path))

envconfig=Properties()
envpath=constants.env_Path
envconfig.load(open(envpath))


class globKeywords:
    
    def __init__(self):
        print("globalKeywords init --- method invoked")
        self.driver = NULL
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
          

    
    def openBrowser(self, browsername = "Edge"):
       
        with allure.step("Open browser --> "+ browsername): 
          try:  
                constants.log_write2("Browser name running currently: ",browsername) 
                print("open browser is getting called", browsername)
                print("Value of self.envProp ==> ", envconfig['GridRun'])              
                

                # If Grid run = Y --> execution in remote node
                if (envconfig['GridRun'] == constants.Y):
                    print(" grid run => ", (envconfig['GridRun']))
                    if (browsername == constants.CHROME):
                        print("Chrome browser is invoked")
                        my_options = webdriver.ChromeOptions()
                        my_options.add_argument("--disable-notifications")
                        my_options.add_argument("--start-maximized")
                        my_options.add_argument("--disable-infobars")
                        my_options.page_load_strategy="normal" 
                        my_options.set_capability("browser_version","107.0")
                        my_options.set_capability("platform_name", "Linux")
                        capability=DesiredCapabilities.CHROME
                    
                    elif (browsername == constants.FIREFOX):
                        print("Firefox browser is invoked")
                        my_options = webdriver.FirefoxOptions()
                        my_options.add_argument("--disable-notifications")
                        my_options.add_argument("--start-maximized")
                        my_options.add_argument("--disable-infobars")
                        my_options.page_load_strategy="normal" 
                        my_options.set_capability("browser_version","107.0")
                        my_options.set_capability("platform_name", "Linux")
                        capability=DesiredCapabilities.FIREFOX
                    
                    elif (browsername == constants.EDGE):
                        print("Edge browser is invoked")
                        my_options = webdriver.EdgeOptions()
                        my_options.add_argument("--disable-notifications")
                        my_options.add_argument("--start-maximized")
                        my_options.add_argument("--disable-infobars")
                        my_options.page_load_strategy="normal" 
                        capability=DesiredCapabilities.EDGE

                    elif (browsername == "Safari"):
                        print("Safari browser invoked -- ")
                        my_options = webdriver.Safari()
                        capability = DesiredCapabilities.SAFARI
                    try:  # Remote system  ->  "http://165.232.190.219:4444"
                        self.driver = webdriver.Remote( command_executor="http://165.232.190.219:4444",
                                                        desired_capabilities=capability,
                                                        options=my_options  )
                        
                        print(" session id for self.driver is: => ", self.driver)
                    except Exception as e:
                        print("\nException occured in open browser--",e)
                
                # If Grid Run is N --> execution in local system
                else:
                   
                    print("\nExecution of test script in local machine\n")
                    
                    if (browsername == constants.CHROME):
                        options = webdriver.ChromeOptions()
                        options.add_argument("--disable-infobars")
                        options.add_argument("--disable-notifications")
                        options.add_argument("--start-maximized")
                        options.page_load_strategy="normal"
                        self.driver = webdriver.Chrome(options=options,executable_path=constants.chrome_path) 
                    
                    elif (browsername == constants.FIREFOX):
                        options = webdriver.FirefoxOptions()
                        options.add_argument("--disable-infobars")
                        options.add_argument("--disable-notifications")
                        options.add_argument("--start-maximized")
                        options.page_load_strategy="normal"
                        self.driver = webdriver.Firefox(options=options,executable_path=constants.firefox_path)
                    
                    elif (browsername == constants.EDGE):
                        print("edge browser invoked......")
                        options = webdriver.EdgeOptions()
                        options.add_argument("--disable-infobars")
                        options.add_argument("--disable-notifications")
                        options.add_argument("--start-maximized")
                        options.page_load_strategy="normal"
                        self.driver = webdriver.Edge(options=options,executable_path=constants.edge_path)
                
                
                self.takeScreenshot()
          except:
                 self.reportFailure("Error in invoking browser")



    def navigate(self, dataField,dataFieldName):
        try:
            
            print("URL is --->",dataField)
            with allure.step("Navigating to - " + dataFieldName):
                self.driver.get(dataField)
                self.takeScreenshot()
        except:
            self.reportFailure("Failed to Navigate to URL")
        
        
    def click(self, objectName,objectN):
        with allure.step("Clicking on -"+ objectN):
            try:
                constants.log_write2("Click on parameter ",objectName)     
                print("parameter is",objectName)
                #self.driver.find_element_by_xpath(objectName).click()
                self.driver.find_element(By.XPATH, objectName).click()
                #self.driver.findElement(By.xpath(objectName)).click()o
                self.takeScreenshot()
                
            except:
                constants.log_write2("Failed for parameter",objectName)     
                self.reportFailure("Failed while trying to click on:"+ objectName)   

    def typing(self, objectName, dataField,objectN,dataName):
        with allure.step("Typing in - " + objectN + " with - " + dataName):
            self.getElement(objectName).send_keys(dataField)
            self.takeScreenshot()

    def enter(self, objectName, dataField,objectN,dataName):
        with allure.step("Pressing Enter Key in - " + objectN + " with - " + dataName):
            self.getElement(objectName).send_keys(dataField)
            self.takeScreenshot()

    
    def type(self, objectName, dataField,objectN,dataName):
        self.intervalWait(2)
        dataField = str(dataField)
        with allure.step("Typing in - "+ objectN +" with - " + dataName):
            try:
                print("entering type function")
                objectName = str(objectName)
                #self.driver.find_element_by_xpath(objectName).send_keys(dataField)
                self.driver.find_element(By.XPATH, objectName).send_keys(dataField)
                #self.driver.findElement(By.xpath(objectName)).send_keys(dataField)
                self.takeScreenshot()
            except:
                    self.reportFailure("Failed while trying to type:"+ dataField +" in:"+ objectName)     

    # common utility functions
    def waitForPageToBeLoaded(self):
       with allure.step(" Wait for page to be loaded -"): 
        i = 1
        while (i != 10):
            load_status = self.driver.execute_script("return document.readyState")
            if (load_status == 'complete'):
                break
            else:
                time.sleep(2)

    def isElementPresent(self, objectName,objectN):
       with allure.step("Is Element Present -"+ objectN): 
        wait = WebDriverWait(self.driver, 20)
        elementList = []
        obj = self.prod[objectName]
        self.waitForPageToBeLoaded()
        if (objectName.endswith('_xpath')):
            elementList = wait.until(EC.presence_of_all_elements_located((By.XPATH, obj)))
        elif (objectName.endswith('_id')):
            elementList = wait.until(EC.presence_of_all_elements_located((By.ID, obj)))
        elif (objectName.endswith('_name')):
            elementList = wait.until(EC.presence_of_all_elements_located((By.NAME, obj)))
        elif (objectName.endswith('_cssSelector')):
            elementList = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, obj)))
        else:
            elementList = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, obj)))

        if (len(elementList) == 0):
            return False
        else:
            return True

    def isElementVisible(self, objectName,objectN):
       with allure.step(" Is element visible -", + objectN): 
        wait = WebDriverWait(self.driver, 20)
        elementList = []
        obj = self.prod[objectName]
        self.waitForPageToBeLoaded()
        if (objectName.endswith('_xpath')):
            elementList = wait.until(EC.visibility_of_all_elements_located((By.XPATH, obj)))
        elif (objectName.endswith('_id')):
            elementList = wait.until(EC.visibility_of_all_elements_located((By.ID, obj)))
        elif (objectName.endswith('_name')):
            elementList = wait.until(EC.visibility_of_all_elements_located((By.NAME, obj)))
        elif (objectName.endswith('_cssSelector')):
            elementList = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, obj)))
        else:
            elementList = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, obj)))

        if (len(elementList) == 0):
            return False
        else:
            return True

    def getElement(self, objectName,objectN):
       with allure.step(" Get element -", + objectN): 
        obj = self.prod[objectName]
        element = NULL
        if (self.isElementPresent(objectName) and self.isElementVisible(objectName)):
            try:
                if (objectName.endswith('_xpath')):
                    element = self.driver.find_element_by_xpath(obj)
                elif (objectName.endswith('_id')):
                    element = self.driver.find_element_by_id(obj)
                elif (objectName.endswith('_name')):
                    element = self.driver.find_element_by_name(obj)
                elif (objectName.endswith('_cssSelector')):
                    element = self.driver.find_element_by_css_selector(obj)
                elif (objectName.endswith('_className')):
                    element = self.driver.find_element_by_class_name(obj)
                else:
                    print("XPATH name undefined")
                    return False
                return element
            except Exception:
                self.reportFailure("The element -" + objectName + " not found")
        else:
            self.reportFailure("The element -" + objectName + " not present/ visible")



    def takeScreenshot(self):
        
        self.wait()
        allure.attach(self.driver.get_screenshot_as_png(), "Screenshot taken at : " + str(datetime.now()),
                      AttachmentType.PNG)

    def reportFailure(self, message):
       with allure.step(" Report failure -" +message): 
        self.wait()
        self.takeScreenshot()
        assert False, message

    def reportSuccess(self, message):
       with allure.step(" Report success - " + message): 
        self.takeScreenshot()
        self.logging(message)
        assert True

    def logging(self, message):
       with allure.step("Logging - " + message): 
        self.logger.info(message)

    def wait(self):
       with allure.step(" Wait -"): 
        time.sleep(2)
    
    def intervalWait(self, dataField):
        print("Interval wait given --", dataField, " seconds") 
        with allure.step("Interval wait --"):
         time.sleep(dataField)
    
# NEEDS MODIFICATION BASED ON USAGE
    def selectDate(self):
        with allure.step("Selecting date : " + self.data['ClosingDate']):
            date = self.data['ClosingDate']
            dt = datetime.strptime(date, "%d-%m-%Y")
            year = dt.year
            month = dt.strftime("%B")
            day = dt.day
            desired_date = month + " " + str(year)
            while True:
                displayed_date = self.driver.find_element_by_xpath("//*[@id='calenDiv']/div/div[1]/div/span[3]").text
                if (desired_date > displayed_date):
                    self.driver.find_element_by_id("nm").click()
                    self.driver.find_element_by_xpath("//td[text()=" + str(day) + "]").click()
                    break
                elif (desired_date < displayed_date):
                    self.driver.find_element_by_id("pm").click()
                    self.driver.find_element_by_xpath("//td[text()=" + str(day) + "]").click()
                    break

    def validateTitle(self, objectName,objectN):
        with allure.step("Validating URL Title...",objectN):
            expectedTitle = self.prod[objectName]
            actualTitle = self.driver.title
            if (expectedTitle == actualTitle):
                self.reportSuccess("Title Validation successful")
            else:
                self.reportFailure(
                    "Title Validation Failed...Got title as " + actualTitle + " instead of " + expectedTitle)

    def validateLogin(self, objectName, dataField,objectN,dataName):
        with allure.step("Validating login...."):
            element = self.getElement(objectName)
            if (element.is_displayed() and dataField == 'Success'):
                self.reportSuccess("Login Successful")
            else:
                self.reportFailure("Login Failed")

# NEEDS MODIFICATION BASED ON USAGE# 
    def getRowCount(self, name):
        with allure.step("Get row count...."):
            rows = self.driver.find_elements_by_xpath(self.prod['allLeads_xpath'])
            for i in range(0, len(rows)):
                if ((rows[i].text) == name):
                    return i + 1
            return -1

    

    def acceptingAlert(self):
       with allure.step(" Accepting alert -"): 
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.alert_is_present())
        a = self.driver.switch_to.alert
        print(a.text)
        a.accept()
        self.driver.switch_to.default_content()

    
            
    def submit(self):
        with allure.step("Submitting -"):
            try:
                action =ActionChains(self.driver) 
                action.send_keys(Keys.ENTER).perform()
                self.takeScreenshot()
            except:
                self.reportFailure("Submit has failed")
            
    def dropDown(self):
       with allure.step("Drop down menu - "): 
        try:
            action =ActionChains(self.driver) 
            action.send_keys(Keys.ARROW_DOWN+Keys.ENTER).perform()
            self.takeScreenshot()
        except:
            self.reportFailure("dropDown has failed")  
            
    def refresh(self):
       with allure.step(" Refreshing the page - "): 
        try:
            self.driver.refresh() 
            self.takeScreenshot()  
        except:
            self.reportFailure("refresh has failed")  
            
    def moveNext(self):
       with allure.step("Move to next - "): 
        try:
            action =ActionChains(self.driver)   
            action.send_keys(Keys.TAB).perform()
            self.takeScreenshot()
        except:
            self.reportFailure("moveNext has failed")  
            
    def scrollDown(self):
       with allure.step(" Scroll down - "): 
        try:
            html = self.driver.find_element_by_tag_name('html')   
            html.send_keys(Keys.PAGE_DOWN)
            # self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
            self.takeScreenshot()
        except:
            self.reportFailure("scrolldown has failed") 
            
    def scrollUp(self):
       with allure.step(" Scroll up - "):  
        try:
            html = self.driver.find_element_by_tag_name('html')   
            html.send_keys(Keys.PAGE_UP)
            self.takeScreenshot()
        except:
            self.reportFailure("scrollup has failed") 
    
    def movePrevious(self):
       with allure.step(" Move to previous page - "):  
        try:
            action =ActionChains(self.driver) 
            action.send_keys(Keys.LEFT_SHIFT+Keys.TAB).perform()   
            self.takeScreenshot()
        except:
            self.reportFailure("movePrevious has failed")
    
    def selectText(self):
       with allure.step(" Selecting the text - "):  
        try:
            action=ActionChains(self.driver)    
            action.send_keys(Keys.SHIFT + Keys.HOME).perform()
            self.takeScreenshot()
        except:
            self.reportFailure("selectText has failed")       
    
    def deleteText(self):
       with allure.step(" Deleting the text- "):  
        try:
            action=ActionChains(self.driver) 
            action.send_keys(Keys.SHIFT + Keys.HOME).perform()
            action.send_keys(Keys.DELETE).perform()
            self.takeScreenshot()
        except:
             self.reportFailure("deleteText has failed")   
            
                
    def uploadingImage(self, objectName, dataField,objectN,dataName):
       print("uploading function running ----")  
       with allure.step(" Uploading image - path  "+objectN+ " in "+dataName):  
        try:
            infile = os.path.abspath(dataField)
            upload_file = self.driver.find_element(By.XPATH, objectName)
            upload_file.send_keys(infile)
            self.takeScreenshot()
        except:
           self.reportFailure("uploadingImage has failed")
    
    
    def arrowDown(self):
       with allure.step(" Arrow down - "):  
        try:
            action =ActionChains(self.driver)
            action.send_keys(Keys.ARROW_DOWN).perform()
            self.takeScreenshot()
        except:
            self.reportFailure("arrowDown has failed")

    
    def select(self, objectName, dataField, objectN,dataName):
        dataField = str(dataField)
        with allure.step("select one data from select tag dropown"+ objectN +" with - "+ dataName):
            try:
                objectName = str(objectName)
                self.driver.find_element(By.XPATH, objectName).send_keys(dataField)
                self.takeScreenshot()

            except:
                self.reportFailure("Failed while trying to selecct on: "+ dataField +" in: "+ objectName)    
    

    def pageUp(self):
        with allure.step("Page Down - "):
            try:
                self.driver.execute_script("window.scrollTo(0, 0)")

            except:
                self.reportFailure("PageDown has failed")
    
    def driverClose(self):
        with allure.step("closing the driver after test execution -- "):
            self.driver.quit()