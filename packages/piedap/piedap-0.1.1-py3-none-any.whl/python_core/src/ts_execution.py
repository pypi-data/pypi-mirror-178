from operator import mod
import sys
from pathlib import Path
import os
ROOT_DIR = str(Path(__file__).parent.parent.parent.parent)
os.chdir(ROOT_DIR)
sys.path.append(ROOT_DIR+"\\")
sys.path.append(ROOT_DIR+"\\piap\\")
from os.path import exists
import subprocess
from datetime import datetime
import pytest
import glob
import shutil
import time
from python_core.utils.readingData import XLSReader
from python_core.config import constants
from python_core.src.ts_generator import TS_generator
from python_core.utils import historical_report_gen
from python_core.utils.keepReport import latest_report

# function to search for xpath.properties file application level
def find_files(filename, search_path):
   result = []
   # Walking top-down from the root
   for root, dir, files in os.walk(search_path):
      if filename in files:
         result.append(os.path.join(root, filename))
   return result


class Test_execution:
    
    def test_execution():

     appn_xlsPath=ROOT_DIR+"\\project_exco\\application_controller.xlsx"
     app_xls=XLSReader(appn_xlsPath)
     try:
        app_row=app_xls.rowCount("application_controller")
        for app_num in range(1,app_row):
            appName=app_xls.getCellDataByColName("application_controller",app_num,"TestApplication")
            apprunmod=app_xls.getCellDataByColName("application_controller",app_num,"RunMode")
            print("\n Application name is",appName," with Runmode --", apprunmod)
            if apprunmod == "Y":
                
                print("\nTest module invoked...\n")
                mod_xlsPath=ROOT_DIR+"\\project_exco\\"+appName+"\\module_controller.xlsx"
                print("\n module controller xlsx path ",mod_xlsPath,"\n")
                mod_xls=XLSReader(mod_xlsPath)
                mrow=mod_xls.rowCount("Sheet1")
                dict={}
                m=0
                
                for rNum in range(1, mrow):
                    mName = mod_xls.getCellDataByColName("Sheet1", rNum, "TestModule")
                    print("\n The module name is ==> ", mName,"\n")
                    mrunmod=mod_xls.getCellDataByColName("Sheet1", rNum, "RunMode")
                    print("Module name and Runmode")
                    # constants.log_write2("Module name %s",mName)
                    # constants.log_write2("Runmode %s",mrunmod)
                    print("\n",mName, mrunmod)
                    s=0 
                    if mrunmod=="Y":
                        try:
                                print("\n",mName," is executing ---\n")
                                mod_dir=ROOT_DIR+"\\project_exco\\"+appName+"\\"+mName
                                print("\n Module directory",mod_dir,"\n")
                                #constants.log_write2("Module directory is called %s",mod_dir)
                                os.chdir(mod_dir)
                            
                                temp_script_path=ROOT_DIR+"\\project_exco\\"+appName+"\\"+mName+"\\testscripts"
                                if os.path.exists(temp_script_path):
                                    t = ROOT_DIR+"\\project_exco\\"+appName+"\\"+mName+"\\testscripts\\__pycache__"
                                    files = glob.glob(ROOT_DIR+"\\project_exco\\"+appName+"\\"+mName+"\\testscripts"+"/*")
                                    for f in files:
                                        if f == t:
                                            print("\n --- Previous testscripts cleared --- for ",mName)
                                        else:    
                                            os.remove(f)
                                else:
                                    os.mkdir(temp_script_path)
                                    print("\n Testcripts folder created for --", mName)
                                    
                                
                                mast_xls=XLSReader(ROOT_DIR+"\\project_exco\\"+appName+"\\"+mName+"\\testsuites\\MasterSuite.xlsx")
                                mast_row=mast_xls.rowCount("MasterSuite")
                                print("\n Master suite row count",mast_row)
                                log_mastrow=str(mast_row)
                                #constants.log_write2("Master suite row count %s",log_mastrow)
                                for masNum in range(1,mast_row):
                                    mastName=mast_xls.getCellDataByColName("MasterSuite",masNum,"TestSuite")
                                    mastrunmod=mast_xls.getCellDataByColName("MasterSuite",masNum,"RunMode")
                                    print("\nMaster suite name and runmode")
                                    # constants.log_write2("Master suite name %s",mastName)
                                    # constants.log_write2("runmode %s",mastrunmod)
                                    print("\n",mastName,mastrunmod)
                                    
                                    if mastrunmod=="Y":
                                        
                                        s=s+1
                                        s=str(s)
                                        constants.suite_name=mastName
                                        m=m+1           
                                        
                                        constants.XLS_PATH=(ROOT_DIR+"\\project_exco\\"+appName+"\\"+mName+"\\testsuites"+"\\"+"t_suite"+"\\"+mastName+".xlsx")
                                        suite_xls=XLSReader(constants.XLS_PATH)
                                        suite_row=suite_xls.rowCount("testsuite")
                                        i=1
                                        for suite_num in range(1,suite_row):
                                            tcid=suite_xls.getCellDataByColName("testsuite",suite_num,"TCID")
                                            tc_runmod=suite_xls.getCellDataByColName("testsuite",suite_num,"RunMode")
                                            tc_order=suite_xls.getCellDataByColName("testsuite",suite_num,"RunSequence")
                                            tdid=suite_xls.getCellDataByColName("testsuite",suite_num,"TDID")
                                            print("\nTest case id and Runmode")
                                            # constants.log_write2("Test case id %s",tcid)
                                            # constants.log_write2("runmode %s",tc_runmod)
                                            print("\nthe tc , and td are ---->",tcid,tc_runmod,tdid)
                                            if tc_runmod=='Y':
                                              try:
                                                # test data path
                                                td_path = find_files(tdid+".xlsx", mod_dir)
                                                print("\nTestdata path",td_path)
                                                
                                                #x_path=obj_path
                                                app_path = ROOT_DIR+"\\project_exco\\"+appName
                                                x_path = find_files("xpath.properties",app_path)

                                                print("\nthe tested xpath is  ", x_path )
                                                
                                                
                                                # test-script generation
                                                TS_generator.generator(td_path, x_path, appName, mName, mastName, tcid, tc_runmod, tdid, tc_order)  
                                              except: 
                                                print("\n Error occured ---> for ",tcid," test case in ", mName,"\n")
                                        
                                        #execution of testscripts based on suite
                                        print("\n\npytest started :----")  
                                        allure_report_path = "--alluredir="+ROOT_DIR+"\\piap\\temp\\allure-report"              
                                        pytest.main(["-x",temp_script_path,allure_report_path])
                        except:
                              print("\n Error occured ---> for ",mName," in ",appName," folder\n")
        
        
        
        print("\n calling hist_rep() ----\n ")
        historical_report_gen.hist_rep()
        
        print("\n Calling latest report function :--->")
        latest_report()

     except:
        
        print("\n--- ERROR OCCURED IN EXECUTION SCRIPT ---- \n")
                                          
 # function calling for test execution       
Test_execution.test_execution()