import importlib
import os
import sys
import time
from pathlib import Path
import pandas as pd
import pandas as st
ROOT_DIR = str(Path(__file__).parent.parent.parent.parent)
os.chdir(ROOT_DIR)
sys.path.append(ROOT_DIR+"\\")
sys.path.append(ROOT_DIR+"\\piap\\")
sys.path.append(ROOT_DIR+"\\project_exco\\")
from pyjavaproperties import Properties
from python_core.config import constants
from python_core.keywords.globkeyword import globKeywords
from project_exco.python_custom.custkeyword import custKeywords

config=Properties()
path=constants.config_path
config.load(open(path))
BrowserList = config['Browser'] 
BrowserList = list(BrowserList.split())
browsername = []
for brow in range(len(BrowserList)): 
    browsername.append(BrowserList[brow])
index = 0


class TS_generator:
    
    
    
    def generator(argtd_path, argxpath, appName, modName, tc_suiteName, tcid, tc_runmode, tdid, tc_order):
        
        global index

        print("\n Browser list is ===>\t",browsername[index::])
        print("\nGenerator invoked ----> \n Parameter for generator calling are:----> \n ", argtd_path, argxpath,appName, modName, tc_suiteName, sep="\n")
        print("\n",tcid," is running \n runmode: '" ,tc_runmode,"' \n run sequence as:" ,tdid, tc_order)
        
      # test case folder path
        tc_folder_path = ROOT_DIR+"\\project_exco\\"+appName+"\\"+modName+"\\testcases"
        
      # check runmode of test case if 'Y' then start test script generation 
        if tc_runmode == 'Y':
            print("\n",tcid," test case is running \n")
            try:

                    print("\n Test Script Generation-- Started for -> ",tcid)

                    # open a temp text file to store test scripts temporarily
                    temp_test_file = open(ROOT_DIR+"\\piap\\temp\\ts_gen\\temp_text_file.txt", 'w')
                    
                    # read template text file and write in temp text file
                    with open(ROOT_DIR+"\\piap\\blueprint\\ts\\ts_template.txt", 'r') as template:
                        for line in template:
                          temp_test_file.write(line)

                    # declare class name based on test_case name
                    temp_test_file.write("\n\n\nclass Test_"+tcid[3::] + ":")
                    temp_test_file.write("\n   @pytest.mark.parametrize("+"'datalist'"+",[(data_ts(), "+"'Success'"")] )")
                    temp_test_file.write("\n   def test_"+tcid+"(self, datalist):")
                    temp_test_file.write("\n    "+"glob = globKeywords()")
                    temp_test_file.write("\n    "+"data = datalist[0]")
                    
                    xpath = str(argxpath[0])
                    print("\n The xpath in generator is -- ", xpath)
                    temp_test_file.write("\n    "+"obj = Read_obj_data()")
                    temp_test_file.write("\n    "+"Obj = obj.read_obj_data(r'"+xpath+"')")
                    #temp_test_file.write("\n    "+"ObjCust = obj.read_obj_data(r'"+xpath+"')")
                    td_path = str(argtd_path[0])
                    print("\n The td path in generator is -- ", td_path)
                    temp_test_file.write("\n    Data = data.read_data(r'"+td_path+"')")
                    temp_test_file.write("\n    cust = custKeywords()")
                    temp_test_file.write("\n    browsername = '"+browsername[index]+"'")
                    temp_test_file.write("\n\n        # test script steps begins here")
                    
                    # index for browser 
                    if index < 2:
                        index+=1
                    
                    else:
                        index=0                  
                    
                    try:
                            print("\n Reading test case excel sheet for : ", tcid)  
                            # class definition will be read keyword from test case sheet
                            tcpath = tc_folder_path+"\\"+tcid+".xlsx"

                            # open test case workbook to read tc sheet
                            sheetName = pd.read_excel(tcpath,sheet_name=tcid)
                            sheetName = sheetName.fillna("")   

                            # read keyword, object and data columns from tc sheet
                            tc_row = len(sheetName.index)
                            for row in range(tc_row): 
                                    tc_keyword = sheetName['Keyword'][row]
                                    tc_objectName = sheetName['Object'][row]
                                    tc_objectName = str(tc_objectName)
                                    tc_dataField = sheetName['Data'][row]
                                    tc_dataField = str(tc_dataField)
                                    
                                    do_sheet_path = ROOT_DIR+"\\project_exco\\"+appName+"\\do_sheet.xlsx"
                                    
                                    try: # check keyword in globKeyword
                                        for globword in globKeywords.__dict__.keys():
                                                if (globword == tc_keyword):
                                                         
                                                    # keyword in globKeywords
                                                    if (tc_keyword == "intervalWait")  :
                                                            temp_test_file.write("\n    "+"glob."+tc_keyword+"("+tc_dataField+")")
                                                    elif (tc_objectName=="") and (tc_dataField==""):
                                                            temp_test_file.write("\n    "+"glob."+tc_keyword+"()")
                                                    elif (tc_objectName ==""):
                                                            temp_test_file.write("\n    "+"glob."+tc_keyword+"("+tc_objectName+"Data['"+tc_dataField+"'][0],"+"'"+tc_dataField+"'"+")")
                                                    elif (tc_dataField ==""):
                                                            temp_test_file.write("\n    "+"glob."+tc_keyword+"(Obj['"+tc_objectName+tc_dataField+"'],"+"'"+tc_objectName+"'"+")") 
                                                    else:
                                                            temp_test_file.write("\n    "+"glob."+tc_keyword+"(Obj['"+tc_objectName+"'], Data['"+tc_dataField+"'][0],"+"'"+tc_objectName+"'"+","+"'"+tc_dataField+"'"+")")
                                        else:
                                            # check keyword in custKeyword
                                            for custword in custKeywords.__dict__.keys():
                                                if (custword == tc_keyword):
                                                # keyword in custKeywords
                                                    temp_test_file.write("\n      "+"cust."+tc_keyword+"(glob, Obj )")
                                    except: 
                                            pass     
                                    
                                    finally: # check keyword is user(repeat) function
                                            if (tc_keyword[:9:] == "function_"):
                                                try: 
                                                    print("\n user function keyword found ---> ", tc_keyword)
                                                    # calling user function with  steps 
                                                    temp_test_file.close()
                                                    sheet_read = st.read_excel(do_sheet_path, sheet_name = "function_index")
                                                    sheet_read = sheet_read.fillna("")
                                                    # read steps from sheet
                                                    do_row = len(sheet_read.index)
                                                    for r in range(do_row):
                                                        do_id = sheet_read['TCID'][r]
                                                        fname = sheet_read['FUNCTION_NAME'][r]
                                                    
                                                        # match function name to do_user_function sheet name for respective module
                                                        if (fname == tc_keyword):
                                                        
                                                            #  if function login function called
                                                            if (tc_keyword == "function_do_login"):
                                                                try:
                                                                    print("\n Reading steps for ->",tc_keyword, " from -> ",tc_keyword[9::]," excel sheet\n")
                                                                    sheet_path = ROOT_DIR+"\\project_exco\\"+appName+"\\"+modName+"\\testcases\\do_user_function.xlsx"
                                                                    getting_file_path = ROOT_DIR+"\\project_exco\\python_custom\\user_functions\\"+tcid+"_"+do_id+".py"
                                                                    
                                                                    getting_file = open(getting_file_path,'w')
                                                                    
                                                                    # read get_import_template
                                                                    with open(ROOT_DIR+"\\piap\\blueprint\\ts\\getting_import_template.txt", 'r') as get_template:
                                                                        for line in get_template:
                                                                           getting_file.write(line)
                                                                    
                                                                    # function definition for getting script
                                                                    getting_file.write("\n\n\ndef "+fname+"():\n")
                                                                    getting_file.write("\n        sheet_path = r'"+sheet_path+"'")
                                                                    getting_file.write("\n        print('"+fname+"  is running ---> ')")
                                                                    getting_file.write("\n        sheetName = '"+fname[9::]+"'\n")
                                                                    
                                                                    # read login_template
                                                                    with open(ROOT_DIR+"\\piap\\blueprint\\ts\\login_template.txt", 'r') as get_funct_temp:
                                                                        for l in get_funct_temp:
                                                                            getting_file.write(l)
                                                                    
                                                                    # function calling statement
                                                                    getting_file.write("\n\n"+fname+"()")
                                                                    
                                                                    # getting file closed
                                                                    getting_file.close()
                                                                    
                                                                    print("\n Hence ->",modName[7::],"_",fname[9::],".py ---> is created ---> in python_custom ---> user_functions folder")
                                                                    print("\n Importing",fname,"  dynamically to generator\n ")
                                                                    print("\n Calling --- ", fname,"\n")
                                                                    module = "project_exco.python_custom.user_functions."+tcid+"_do_login"
                                                                    # dynamic import of called user function
                                                                    getattr(importlib.import_module(module), fname)
                                                                    
                                                                
                                                                    # temp text open for appending     
                                                                    temp_test_file = open(ROOT_DIR+"\\piap\\temp\\ts_gen\\temp_text_file.txt", 'r+')
                                                                    temp_test_file.readlines()
                                                                    cur_pos = temp_test_file.tell()
                                                                    temp_test_file.seek(cur_pos, os.SEEK_SET) 
                                                                
                                                                except:
                                                                    print("\n Error occured in ---> do_login -->  Hence script not generated --\n")
                                                            
                                                            # if repeat functions called
                                                            else:
                                                
                                                                try:  
                                                                    print("\n Reading steps for ",fname, " from ",fname[9::]," excel sheet\n")
                                                                    sheet_path = ROOT_DIR+"\\project_exco\\"+appName+"\\"+modName+"\\testcases\\do_user_function.xlsx"
                                                                    getting_file_path = ROOT_DIR+"\\project_exco\\python_custom\\user_functions\\"+tcid+"_"+do_id+".py"
                                                                    
                                                                    getting_file = open(getting_file_path,'w')
                                                                    
                                                                    # read get_import_template
                                                                    with open(ROOT_DIR+"\\piap\\blueprint\\ts\\getting_import_template.txt", 'r') as get_template:
                                                                        for line in get_template:
                                                                            getting_file.write(line)
                                                                    
                                                                    # function definition for getting script
                                                                    getting_file.write("\n\n\ndef "+fname+"():\n")
                                                                    getting_file.write("\n        sheet_path = r'"+sheet_path+"'")
                                                                    getting_file.write("\n        print('"+fname+"  is running ---> ')")
                                                                    getting_file.write("\n        sheetName = '"+fname[9::]+"'")
                                                                    getting_file.write("\n        Iteration = '"+tc_dataField+"'")
                                                                    getting_file.write("\n        if Iteration == '':")
                                                                    getting_file.write("\n             Iteration = 'len(Data.index)'")
                                                                    getting_file.write("\n        else:")
                                                                    getting_file.write("\n             Iteration = str(Iteration)")
                                                                    getting_file.write("\n        tdpath = r'"+ td_path+"'\n")
                                                                    # read get_funct_template
                                                                    with open(ROOT_DIR+"\\piap\\blueprint\\ts\\getting_funct_template.txt", 'r') as get_funct_temp:
                                                                        for l in get_funct_temp:
                                                                            getting_file.write(l)
                                                                    
                                                                    # function calling statement
                                                                    getting_file.write("\n\n"+fname+"()")
                                                                    
                                                                    # getting file closed
                                                                    getting_file.close()
                                                                    
                                                                    print("\n getting_",fname[9::],".py ---> is created ---> in python_custom ---> user_functions folder")
                                                                    print("\n Importing",fname,"  dynamically to generator\n ")
                                                                    print("\n Calling --- ", fname,"\n")
                                                                    module = "project_exco.python_custom.user_functions."+tcid+"_"+do_id
                                                                    # dynamic import of called user function
                                                                    getattr(importlib.import_module(module), fname)
                                                                    
                                                                
                                                                    # temp text open for appending     
                                                                    temp_test_file = open(ROOT_DIR+"\\piap\\temp\\ts_gen\\temp_text_file.txt", 'r+')
                                                                    temp_test_file.readlines()
                                                                    cur_pos = temp_test_file.tell()
                                                                    temp_test_file.seek(cur_pos, os.SEEK_SET)
                                                                
                                                                except:
                                                                        print("\n Error occured in ---> ",fname,"-->  Hence script not generated successfully\n")
                                                except:
                                                    print("\n Error in creating user function for:  ",fname)
                                            
                                            
                                        
                    except:
                            print("\n Error while reading test case sheet for:  ", tcid)


                 
                    # dynamic to test script python file same as test_case name
                    test_script_file = ROOT_DIR+"\\project_exco\\"+appName+"\\"+modName+"\\testscripts\\test_"+tc_order+"_"+tcid+".py"
                    temp_test_file.write("\n    "+"glob.driverClose()")
                    
                    # converting text test file into python file named as test case
                    with open(ROOT_DIR+"\\piap\\temp\\ts_gen\\temp_text_file.txt", 'r') as temp_test_file, open(test_script_file, 'w') as run_tc_file:
                        for lines in temp_test_file:
                            run_tc_file.write(lines)
            except:
                   print("\n--- ERROR OCCURED IN GENERATOR SCRIPT ---- \n")
          
            finally:
                print("\n Test Script Generated -- Completed \n\n")
                
                # delete temporary text file now
                if os.path.exists(ROOT_DIR+"\\piap\\temp\\ts_gen\\temp_text_file.txt"):
                  time.sleep(2)
                  os.remove(ROOT_DIR+"\\piap\\temp\\ts_gen\\temp_text_file.txt")
                  print("\ntemp text file deleted")
        else:
              print("\n",tcid," has runmode = ",tc_runmode)
               