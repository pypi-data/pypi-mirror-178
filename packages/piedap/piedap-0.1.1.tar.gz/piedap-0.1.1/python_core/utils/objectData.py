from pyjavaproperties import Properties
prod = Properties()

class Read_obj_data:
    
    def read_obj_data(self,xpath):
        try:
            print(" read_obj_data function is running\n")
            prodPath = open(xpath)
            prod.load(prodPath)
            #print("\nxpath.properties are => ", prod)
            return prod
        except:
            print("Error in reading object data from ", xpath)


