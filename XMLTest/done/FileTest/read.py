import os

file1 = os.path.join('C:\Python34\FileTest\VPro20160608162138B')
print('file size is :' , os.path.getsize('C:\Python34\FileTest\VPro20160608162138B'))

num_lines = sum(1 for line in open('VPro20160608162138B'))
print('number of line :' ,num_lines)

search_str = "Printk"
fo = open('VPro20160608162138B','r')
# Read the first line from the file
line = fo.readline()

# Initialize counter for line number
line_Prink = 0
line_ScanProcessController = 0 
line_ParametersController = 0

with open('VPro20160608162138B') as f:
    for line in f:
        if "PrintK" in line:
            line_Prink += 1
        if "ScanProcessController" in line:
            line_ScanProcessController += 1
        if "ParametersController" in line:
            line_ParametersController += 1
            #print(line_no, line)
            
        #print(line_no)
print("Number of PrintK:", line_Prink)
#print("ratio :", line_Prink / float(num_lines))
print("{0:<20}{1:1.2f}".format('ratio of Prink:',  (line_Prink / float(num_lines))))

print("Number of PrintK:", line_ScanProcessController)
print("{0:<20}{1:1.2f}".format('ratio of ScanProcessController:',  (line_ScanProcessController / float(num_lines))))

print("Number of PrintK:", line_ParametersController)
print("{0:<20}{1:1.2f}".format('ratio of ParametersController:',  (line_ParametersController / float(num_lines))))