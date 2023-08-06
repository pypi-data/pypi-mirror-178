import os
import sys
import shutil
from pathlib import Path
ROOT_DIR = str(Path(__file__).parent.parent.parent.parent)
print("The root dir in keepReport is: ", ROOT_DIR)
os.chdir(ROOT_DIR)
#sys.path.append(ROOT_DIR+"\\piap\\")


def latest_report():
    foldername = ROOT_DIR+"\\piam\\test_reports\\web_automation"
    
    try:    
        for filename in sorted(os.listdir(foldername))[:-10]:
            filename_relPath = os.path.join(foldername,filename)
            #print(filename_relPath, "-- deleted")
            shutil.rmtree(filename_relPath)
        print("Deleted old records except last 10 records from test_reports \n")
    except:
        print("Error in keepReport file ---> old test report did not get deleted")

#print("\n After deletion :---> \n",os.listdir(foldername))