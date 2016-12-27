import os
import sys

file1 = os.path.join('C:\Python34\FileTest\VPro20160623131244B')
file2 = os.path.join('C:\\Python34\FileTest\VPro20160623114153Aansi')
file3 = os.path.join('C:\Python34\FileTest\VPro20160623114153B')
file4 = os.path.join('C:\Python34\FileTest\VPro20160623131244A')
file5 = os.path.join('C:\Python34\FileTest\VPro20160623114153Aansi')

print("file path:", file1)
print('file size is :' , os.path.getsize(file1))


# Initialize counter for line number
sum_lines = 0 
line_Prink = 0
line_ScanProcessController = 0 
line_ParametersController = 0


try:
	with open(file1) as f:
	    for line in f:
	        if "PrintK" in line:
	            line_Prink += 1
	        if "ScanProcessController" in line:
	            line_ScanProcessController += 1
	        if "ParametersController" in line:
	            line_ParametersController += 1
	        sum_lines += 1
	        

		        #print(line_no)
	  
	f.close()
except OSError as err:
    print("OS error: {0}".format(err))
except ValueError:
    print("Could not convert data to an integer.")
    print("line = ", sum_lines)
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise



print('number of line :' ,sum_lines)
print("Number of PrintK:", line_Prink)
print("{0:<20}{1:1.2f}".format('ratio of Prink:',  (line_Prink / float(sum_lines))))

print("Number of line_ScanProcessController:", line_ScanProcessController)
print("{0:<20}{1:1.2f}".format('ratio of ScanProcessController:',  (line_ScanProcessController / float(sum_lines))))

print("Number of line_ParametersController:", line_ParametersController)
print("{0:<20}{1:1.2f}".format('ratio of ParametersController:',  (line_ParametersController / float(sum_lines))))
print("{0:<50}".format("=================================="))

print("file path:", file2)
print('file size is :' , os.path.getsize(file2))


# Initialize counter for line number
sum_lines = 0 
line_Prink = 0
line_ScanProcessController = 0 
line_ParametersController = 0


try:
	with open(file2) as f:
	    for line in f:
	        if "PrintK" in line:
	            line_Prink += 1
	        if "ScanProcessController" in line:
	            line_ScanProcessController += 1
	        if "ParametersController" in line:
	            line_ParametersController += 1
	        sum_lines += 1
	        

		        #print(line_no)
	  
	f.close()
except OSError as err:
    print("OS error: {0}".format(err))
except ValueError:
    print("Could not convert data to an integer.")
    print("line = ", sum_lines)
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise



print('number of line :' ,sum_lines)
print("Number of PrintK:", line_Prink)
print("{0:<20}{1:1.2f}".format('ratio of Prink:',  (line_Prink / float(sum_lines))))

print("Number of line_ScanProcessController:", line_ScanProcessController)
print("{0:<20}{1:1.2f}".format('ratio of ScanProcessController:',  (line_ScanProcessController / float(sum_lines))))

print("Number of line_ParametersController:", line_ParametersController)
print("{0:<20}{1:1.2f}".format('ratio of ParametersController:',  (line_ParametersController / float(sum_lines))))
print("{0:<50}".format("=================================="))

print("file path:", file3)
print('file size is :' , os.path.getsize(file3))


# Initialize counter for line number
sum_lines = 0 
line_Prink = 0
line_ScanProcessController = 0 
line_ParametersController = 0


try:
	with open(file3) as f:
	    for line in f:
	        if "PrintK" in line:
	            line_Prink += 1
	        if "ScanProcessController" in line:
	            line_ScanProcessController += 1
	        if "ParametersController" in line:
	            line_ParametersController += 1
	        sum_lines += 1
	        

		        #print(line_no)
	  
	f.close()
except OSError as err:
    print("OS error: {0}".format(err))
except ValueError:
    print("Could not convert data to an integer.")
    print("line = ", sum_lines)
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise



print('number of line :' ,sum_lines)
print("Number of PrintK:", line_Prink)
print("{0:<20}{1:1.2f}".format('ratio of Prink:',  (line_Prink / float(sum_lines))))

print("Number of line_ScanProcessController:", line_ScanProcessController)
print("{0:<20}{1:1.2f}".format('ratio of ScanProcessController:',  (line_ScanProcessController / float(sum_lines))))

print("Number of line_ParametersController:", line_ParametersController)
print("{0:<20}{1:1.2f}".format('ratio of ParametersController:',  (line_ParametersController / float(sum_lines))))
print("{0:<50}".format("=================================="))

print("file path:", file4)
print('file size is :' , os.path.getsize(file4))


# Initialize counter for line number
sum_lines = 0 
line_Prink = 0
line_ScanProcessController = 0 
line_ParametersController = 0


try:
	with open(file4) as f:
	    for line in f:
	        if "PrintK" in line:
	            line_Prink += 1
	        if "ScanProcessController" in line:
	            line_ScanProcessController += 1
	        if "ParametersController" in line:
	            line_ParametersController += 1
	        sum_lines += 1
	        

		        #print(line_no)
	  
	f.close()
except OSError as err:
    print("OS error: {0}".format(err))
except ValueError:
    print("Could not convert data to an integer.")
    print("line = ", sum_lines)
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise



print('number of line :' ,sum_lines)
print("Number of PrintK:", line_Prink)
print("{0:<20}{1:1.2f}".format('ratio of Prink:',  (line_Prink / float(sum_lines))))

print("Number of line_ScanProcessController:", line_ScanProcessController)
print("{0:<20}{1:1.2f}".format('ratio of ScanProcessController:',  (line_ScanProcessController / float(sum_lines))))

print("Number of line_ParametersController:", line_ParametersController)
print("{0:<20}{1:1.2f}".format('ratio of ParametersController:',  (line_ParametersController / float(sum_lines))))
print("{0:<50}".format("=================================="))
