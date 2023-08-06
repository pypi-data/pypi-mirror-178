import pandas as pd
import os

class Read_data:
    
    
    def read_data(self,td_path):
        try:
            print(" read_data function is running\n")
            td_path=str(td_path)
            print("The td_path is => ",td_path)
            file_name=os.path.basename(td_path)
            print("file name inside readData file is ", file_name)
            s_name=file_name.replace(".xlsx","")
            print("sheet name inside readData file is ", s_name)
            df=pd.read_excel(td_path, sheet_name=s_name)
            df = df.fillna("")
            print(df)
            return df
        except:
            print("Error in reading data from excel sheet ",s_name)    
        
        
