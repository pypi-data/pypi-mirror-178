import shutil
from datetime import datetime
from pathlib import Path
import os,glob
import time
import sys
from pathlib import Path
ROOT_DIR = str(Path(__file__).parent.parent.parent.parent)
os.chdir(ROOT_DIR)
sys.path.append(ROOT_DIR+"\\")
from python_core.config import constants


def hist_rep():
               
        try:    
                print("\n Historic report generation invoked -->\n")
            # allure path initialized
                src_dir = constants.allure_dir
                files=os.listdir(src_dir)
                print("This is new dir path in historic report generation", ROOT_DIR)
                current_datetime = datetime.now().strftime("%Y-%m-%d-%H.%M.%S")
                str_current_datetime = str(current_datetime)
                
                
                print("datetime created")
                if (os.path.exists(ROOT_DIR+"\\piam\\test_reports\\web_automation\\test_report1")):
                    print("test_report1 exist")
                    os.rmdir(ROOT_DIR+"\\piam\\test_reports\\web_automation\\test_report1")
                    print("test_report1 is removed")
        

                #temporary hist report folder is created
                dir_path=ROOT_DIR+"\\piam\\test_reports\\web_automation\\test_report1"
                os.mkdir(dir_path)
                new_dest=ROOT_DIR+"\\piam\\test_reports\\web_automation\\test_report1"
                
                # path to destination directory
                dest_dir = new_dest
                        
                #
                # print("test report1 directory created")
                    
                print("test report1 directory created")
                for fname in files:
                    shutil.copy2(os.path.join(src_dir,fname), dest_dir)
                            
                        
                print(str_current_datetime,type(str_current_datetime))
                os.chdir(ROOT_DIR+'\\piam\\test_reports\\web_automation')
                test_rep="test_report1"
                        
                    #timestamp rename
                os.rename(test_rep,current_datetime)
                        
                del_dir=constants.allure_dir
                print("delete directory",del_dir)
                filelist = glob.glob(os.path.join(del_dir, "*"))
                for f in filelist:
                    os.remove(f)
                        
                os.system("allure serve "+ROOT_DIR+"\\piam\\test_reports\\web_automation"+"\\"+current_datetime)
        
        except:
            print("\n Action occured in historic report gen file \n")
       
        