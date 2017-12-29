import zipfile
import os
import shutil
import glob
import datetime
import time
import sys
from subprocess import Popen
import xml.etree.ElementTree as ET
import subprocess
from distutils.dir_util import copy_tree
from tempfile import mkstemp
from shutil import move
from os import remove, close
from pathlib import Path



'''
def reFileNameOnly(sPath, sPrefixName):
'''


#globle varible
lastMP_UIPath = r"D:\\MP_UI_RENAME\\MP_UI_unzipFile\\MP_UI_V1.55.2017.1213\\"


#sample function
# def replaceBinFile():
# 	print('replaceBinFile start ..'.format('-'))
# 	try:
# 		print('replaceBinFile start ..'.format('-'))
# 	except:	       
# 		print('replaceBinFile except')

# 	print('replaceBinFile End ..'.format('-'))
# 	return 0

def reFileNameOnly(sPath, sPrefixName):
    print('{:<10s}reFileNameOnly  ..'.format('start'))
    os.chdir(sPath)
    listFolderInfo = []
    for allfiles in os.listdir(sPath):
        if (allfiles.startswith("V1.") or
        	allfiles.startswith("v1.") or
        	allfiles.startswith("1.")
        	):

	            newName = sPrefixName + allfiles
	            os.rename(allfiles, newName)
	            print('old name = {}, new name = {} ok'.format(allfiles, newName))

    print('{:<10s}reFileNameOnly  ..'.format('End'))
    return 0



def reFolderNameOnly(sPath):
    print('{:<10s}reFolderNameOnly  ..'.format('start'))
    os.chdir(sPath)
    listFolderInfo = []
    for folders in os.listdir(sPath):
        if (folders.startswith("V1.") or
        	folders.startswith("v1.")) and not folders.endswith(".zip") :

	            newDirectorieName = "MP_UI_" + folders
	            os.rename(folders, newDirectorieName)
	            print('old name = {}, new name = {} ok'.format(folders, newDirectorieName))

    print('{:<10s}reFolderNameOnly  ..'.format('End'))
    return 0


def copyTimeStamp(sSrc, sDes): 
    try:
        if os.path.exists(sSrc) and os.path.exists(sDes) :
           shutil.copystat(sSrc, sDes)

	# print('{:<10s}copyTimeStamp  end'.format('start'))
    # print("copyTimeStamp end")
    except:
        print("!!! except in copyTimeStamp")


def syncTimeStamp(sDes):
    print('start syncTimeStamp {}'.format("="))

    global lastMP_UIPath
    srcbinfilepath = ""
    desbinfilepath = ""
    sSrcBin =  os.path.join(lastMP_UIPath, "bin")
    sDesBin =  os.path.join(sDes, "bin")
    for root, dirs, files in os.walk(sSrcBin):
        for srcbinfile in files:
            if (srcbinfile.endswith(".bin")):
                srcbinfilepath = os.path.join(root, srcbinfile)
                for desRoot, desDirs, desFiles in os.walk(sDesBin):
                    for desbinfile in desFiles:
                    	if (srcbinfile == desbinfile):
                        # if (desbinfile.endswith(".bin")):
                            desbinfilepath = os.path.join(desRoot, desbinfile)
                            print('got it\nsrcbinfilepath = {}\ndesbinfilepath = {}'.format(srcbinfilepath, desbinfilepath))
                            copyTimeStamp(srcbinfilepath, desbinfilepath)
                            # print('copy file, timestamp ok = \nMP:{}\nUI:{}'.format(srcbinfilepath, binPath))



def syncTimeStampII(sSrc, sDes):
    print('start syncTimeStampII \nsSrc = {}, sDes = {}'.format(sSrc, sDes))

    global lastMP_UIPath
    srcbinfilepath = ""
    desbinfilepath = ""
    # sSrcBin =  os.path.join(lastMP_UIPath, "bin")
    sDesBin =  os.path.join(sDes, "bin")
    for root, dirs, files in os.walk(sSrc):
        for srcbinfile in files:
            # print('srcbinfile = {}, path = {}'.format(srcbinfile, root))
        	#check src bin file in windwos folder, not adata folder
            if (srcbinfile.endswith(".bin")) and (root.find("windows") > 0)  and (root.find("ADATA") == -1) :
                srcbinfilepath = os.path.join(root, srcbinfile)
                # print('syncTimeStampII: binFile = {},  srcbinfilepath = {}'.format(srcbinfile, srcbinfilepath))
                for desRoot, desDirs, desFiles in os.walk(sDesBin):
                    for desbinfile in desFiles:
                    	if (srcbinfile == desbinfile):
                        # if (desbinfile.endswith(".bin")):
                            desbinfilepath = os.path.join(desRoot, desbinfile)
                            # print('get:\nsrcbinfilepath = {}\ndesbinfilepath = {}'.format(srcbinfilepath, desbinfilepath))
                            copyTimeStamp(srcbinfilepath, desbinfilepath)
                            print('sync ok:\nsrcbinfilepath = {}\ndesbinfilepath = {}'.format(srcbinfilepath, desbinfilepath))
                            # print('copy file, timestamp ok = \nMP:{}\nUI:{}'.format(srcbinfilepath, binPath))


def buildFileDateInfo(sPath):

    # print('{:<10s}buildFileDateInfo, {}  ..'.format('start', sPath))

    # build from file info 
    file_paths = []  # List which will store all of the full filepaths.
    listFileInfo =[]
    # Walk the tree.
    os.chdir(sPath)
    for root, directories, files in os.walk(sPath):
        for fileName in files:            
        	if fileName.endswith(".bin") and fileName.startswith("3S") :
	            filePath = os.path.join(root, fileName)
	            relativefilePath = os.path.relpath(filePath)
	            # print("file path = {}".format(filePath))
	            # print('fileName = {}\n path1 = {},\n path2 = {} '.format(fileName, filePath, relativefilePath))

	            # tupleFileInfo[0] = file name
	            # tupleFileInfo[1] = file path
	            fileTimeInfo = os.path.getmtime(filePath)
	            # tupleFileInfo = (fileName, relativefilePath, fileTimeInfo) #save file name , path into tuple
	            tupleFileInfo = (fileName, filePath, fileTimeInfo) #save file name , path into tuple
	            listFileInfo.append(tupleFileInfo)  # Add it to the list.            
	            # print('fileName = {}\n path1 = {},\n path2 = {} '.format(fileName, relativefilePath, fileTimeInfo))


    # print('{:<10s}buildFileInfo  ..'.format('End'))
    return listFileInfo


def buildFolderInfo(sPath, sFolderType):

    print('{:<10s}buildFolderInfo  ..'.format('start'))

    # build from folder info 
    file_paths = []  # List which will store all of the full filepaths.
    listFolderInfo = []
    listBinFileInfo = []
    # Walk the tree.
    os.chdir(sPath)
    for root, directories, files in os.walk(sPath):
        for directorieName in directories:            
            folderPath = os.path.join(root, directorieName)
            relativefolderPath = os.path.relpath(folderPath)
            
            # print('folderName = {}\n path1 = {},\n path2 = {} '.format(directorieName, folderPath, relativefolderPath))

            # tupleFileInfo[0] = folder name
            # tupleFileInfo[1] = folder path
            tupleFileInfo = (directorieName, relativefolderPath) #save folder name , path into tuple
            listFolderInfo.append(tupleFileInfo)  # Add it to the list.            

    #.................
    #create folder info
    #.................
    print('create folder info start ..'.format('-'))

    iIndex = 0
    for x, y in listFolderInfo:
    	# for only bin folder 
    	if x == sFolderType:
	        print('{:<5d}, listFolderInfo, name = {} path = {} sFolderType = {}'.format(iIndex, x, y, sFolderType))
	        sPath1 = os.path.join(sPath, y)
	        listBinFileInfo = buildFileDateInfo(sPath1)
	        iIndex += 1

    
    # for x, y, z in listBinFileInfo:
    #     print('listFileInfo, name = {} path = {} date = {}'.format(x, y, z))


    # print('{:<10s}buildFolderInfo  ..'.format('End'))
    return listBinFileInfo



def runCompressFile(sWorkFolder, sNewZipFolder, sName):

	# print("runCompressFile start")
    print('runCompressFile start \n{}\n{}\n{}'.format(sWorkFolder, sNewZipFolder, sName))
    sRemoteFileName = sName + ".zip"
    sRemoteFolderName = sName
    

    dest = os.path.join(sWorkFolder, sRemoteFileName) 
    if (os.path.isfile(dest)):
        print('{}{}'.format(dest, "   exist !! remove it ?"))
        os.remove(dest)
        print('{}{}'.format(dest, ", remove ok"))

    # else:        
        # print('{}{}'.format(dest, "  do not exist"))
            
    zf = zipfile.ZipFile(dest, mode='w')

    print('chdir to {}'.format(sNewZipFolder))
    os.chdir(sNewZipFolder)


    for root, folders, files in os.walk(".\\"):
    	for sfile in files:
		    aFile = os.path.join(root, sfile)
		    sTmpPath = os.path.join(sRemoteFolderName, aFile)
	    
	 
		    # print('runCompressFile add [{}] '.format(aFile))
		    zf.write(aFile, sTmpPath, compress_type=zipfile.ZIP_BZIP2)

    zf.close()
    print('runCompressFileEnd ..[{}]\n '.format(dest))



def parseTXT():
	global lastMP_UIPath

	print('parseTXT start ..'.format('-'))
	
	stxtPath = r"D:\\MP_UI_RENAME\\MP_UI_zipFile\\zipList.txt"
	sZipFolder = r"D:\\MP_UI_RENAME\\MP_UI_zipFile\\"
	sDesFolder = r"D:\\MP_UI_RENAME\MP_UI_unzipFile\\"
	sMPFolder =  r"D:\\MP_UI_RENAME\\MP_Folder\\"
	listSourceCodeBinInfo = []
	listMPBinInfo = [] 

	listZipFileInfo =[]
	oldFolderName = ""
	NewFolderName = ""
	try:
		#read txt file
		rF = open(stxtPath, 'r') 
		for line in rF.readlines():
			line = line.strip()

			if not len(line) or line.startswith('#'): 
				continue 
			# print('{} '.format(line))
			lineList = line.split(',')
			# print('{} -> {} '.format(lineList[0], lineList[1]))
			listZipFileInfo.append(lineList)

		#un source code zip
		iCount = 0 
		for x1, y1 in listZipFileInfo:
			# print('{} -> {} '.format(x1, y1))

			# proc MP_UI
			sPath3 = os.path.join(sZipFolder, x1) 
			oldFolderName = x1.replace(".zip","")
			NewFolderName = "MP_UI_" + oldFolderName

			
			print('\nRound[{}], {}, oldFolderName = {}, NewFolderName = {} '.format(iCount, sPath3, oldFolderName, NewFolderName))
			iCount = iCount + 1

			if os.path.exists(sPath3):
				zf = zipfile.ZipFile(sPath3)
				# print('{}{}'.format(sPath3, ", ready to Extract "))
				zf.extractall(path=sDesFolder, members=None, pwd=None)

				zf.close()
				# print('{}{} '.format(sPath3, ", Extract done"))
 

			try:
				#check , rename extract folder
				extractFolderPath = os.path.join(sDesFolder, oldFolderName)
				newExtractFolderPath = os.path.join(sDesFolder, NewFolderName)
				print('oldPath = {} \nnewPath = {}'.format(extractFolderPath, newExtractFolderPath))
				if os.path.exists(extractFolderPath):
					os.chdir(sDesFolder)
					os.rename(extractFolderPath, newExtractFolderPath)
					print('rename ok, old = {} new = {}'.format( extractFolderPath, newExtractFolderPath))
					
					#sync timestamps
					# if (newExtractFolderPath != lastMP_UIPath):
					# 	print('newExtractFolderPath = {} lastMP_UIPath = {}'.format( newExtractFolderPath, lastMP_UIPath))
					# syncTimeStamp(newExtractFolderPath)
					# lastMP_UIPath = newExtractFolderPath
						
				else:
					print('!!! exception extractFolderPath = {} '.format(extractFolderPath))

			except:
				print("Unexpected error:", sys.exc_info()[0])
				print('!!! except #check , rename extract folder')

			# break

			
			#proc MP_UI 
			listSourceCodeBinInfo = buildFolderInfo(newExtractFolderPath, "bin")

			sPathMPFolder = os.path.join(sMPFolder, y1) 
			sPathMPFolder = os.path.join(sPathMPFolder, "windows")

			# syncTimeStamp
			syncTimeStampII(sPathMPFolder, newExtractFolderPath)

			#for bin in proc MP_Folder
			for binName, binPath, z in listSourceCodeBinInfo:
				# print('listFileInfo, name = {} path = {} date = {}'.format(binName, binPath, z))

				#find bin file in mp
				bGetBin = False
				if os.path.exists(sPathMPFolder):

					# print('sPathMPFolder = {} '.format(sPathMPFolder))		
					for root, dirs, files in os.walk(sPathMPFolder):
					    for bfile in files:
					        if (bfile == binName) and (root.find("ADATA") == -1):
					        	mpFilePath = os.path.join(root, bfile)
					        	# print("get it")
					        	print('got it, mpFilePath = {}, root = {}'.format(mpFilePath, root))
					        	bGetBin = True
					        	# print("ready to remove ")
					        	# os.remove(binPath)
					        	shutil.copy(mpFilePath, binPath)
					        	copyTimeStamp(mpFilePath, binPath)
					        	print('copy file, timestamp ok = \nMP:{}\nUI:{}'.format(mpFilePath, binPath))

			runCompressFile(sDesFolder, newExtractFolderPath, NewFolderName)
			# if bGetBin == False:
			# 	print('!!! cant find, MP_UI binName = {}'.format(binName))

				             # print(os.path.join(root, file))				
		# listMPBinInfo = buildFolderInfo(sMPFolder, "HUATOOP")
		#proc MP
	except:	       
		print('parseTXT except')
    
        

	return 0     


if __name__ == "__main__":

    sStartTime = datetime.datetime.now()
    print('StartTime:{} ..\n '.format(sStartTime))

    sPath = r"D:\\MP_UI_RENAME\newtest"
    try:
     	
     	#re folder name only , ok 20171228
     	# reFolderNameOnly(sPath)

     	reFileNameOnly(sPath, "BIN_GRADE_")

     	#copyTime stamp
     	#copyTimeStamp()
    	# parseTXT()
        #tree.write(data,"UTF-8")
    except:
        print('!!! exception happen in')

    sEndTime = datetime.datetime.now()        
    print('EndTime:{}, Total:{} ..'.format(sEndTime, (sEndTime-sStartTime)))   

    sys.exit(0)                        