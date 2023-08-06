from piap.python_core.utils.readData import Read_data


def data_ts():
  try:
        print("\ndata_ts function is running --- ")
        data = Read_data() 
        mylist = []
        mylist.append(data)
        return  data
  except:
        print("\n Error in sending data object from data_ts function\n")

# value = data_ts()
# print("\n The elements are ",value)