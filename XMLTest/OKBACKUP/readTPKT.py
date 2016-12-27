import os
import glob
import numpy as np

#for root, dirs, files in os.walk("./20160719/"):
    #print (root)
    #for f in files:
        #print (os.path.join(root, f))
        #file1 = os.path.join(root, f)
        #print (file1)
        #glob.glob(' *.text ')
        
        #if (file1)

#f1 = glob.glob(r'./20160719/*.log')
#f1 = glob.glob(r'./**/*.log')
listError = []
nListErrCount = []
nTotal = 0

def showList():
	for index, item in enumerate(listError):
		#if "Rex" in item:
		print("showList index = {}, item = {}, nListErrCount = {}".format(index,item, nListErrCount[index]))

def runList(sString, nErrNumber):
	#print("runList get data sString = {}, nErrNumber = {}".format(sString, nErrNumber))
	if sString in listError: 
		#print("sameErr: {0}".format(sString))
		#print("sameErr")
		for index, item in enumerate(listError):
			if sString in item:
				#print("runList before index = {}, item = {}, nErrNumber = {}".format(index,item, nErrNumber))
				nListErrCount[index] = int(nListErrCount[index]) + int(nErrNumber)
				#print("runList after add index = {}, item = {}, addNErrNumber = {} , after sum = {}".format(index,item, int(nErrNumber) , int(nListErrCount[index])))
				break						
		 
	else:
		listError.append(sString)
		nListErrCount.append(int(nErrNumber))
		#showList()

def printList():
	open("resultPython.txt", "w",newline=None)
		#wFile1.write("Total file = {} \n".format(nTotal))

	for index, item in enumerate(listError):
		if "Rex" in item:
			print("printList index = {}, item = {}, nErrNumber = {}".format(index,item, nListErrCount[index]))
		with open("resultPython.txt", "a",newline=None) as wFile:
			#wFile.write("printList index = {}, item = {}, nErrNumber = {} \n".format(index,item, nListErrCount[index]))
			wFile.write("[{}],{},{} \n".format(index,item, int(nListErrCount[index])))

	with open("resultPython.txt", "a",newline=None) as wFile1:
		wFile1.write("Total file = {} \n".format(nTotal))

	

#'C:\Log\APOLLO\BURNIN\20161025\*.CSV'
#'\\\\qthfbliu\\QA_log\\Error_Log\\**\\*.CSV'
#_1024 18:18:38.886371] ADB OK,  reboot
#_1024 18:18:48.962474] ADB OK,  devices
str1 = "ADB OK,  reboot"
str2 = "ADB OK,  devices"
for filename in glob.iglob('\\\\p10backup\\MTY1\\Production_Test_Data\\ApolloTestData\\NeilTestLog\\APOLLO\\QTYMTYT2IPC010\\**\\*.log', recursive=True):
	try:
		if (filename.find("TPKT") != -1) and (filename.find("N2007") != -1):
			print(filename)
			nTotal = nTotal + 1
			with open(filename,  encoding = 'utf-8-sig') as f2:		
			    for line in f2:
			    	if ("ADB OK,  reboot" in line) or ("ADB OK,  devices" in line) :
			    		print (line)
			    	#if (str1 in line) or (str2 in line):
			    		
			f2.close()
			print("read ok, {}".format(filename))
			#print('\n'.join('{}: {}'.format(*k) for k in enumerate(listError)))
	except OSError as err:
	    print("OS error: {0}".format(err))
	except ValueError:
	    print("Could not convert data to an integer.")
	    print("line = ", sum_lines)
	except:
	    print("Unexpected error:", sys.exc_info()[0])
	    raise

#listError.sort()
printList()	    