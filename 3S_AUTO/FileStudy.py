
import os
import shutil
import glob
import datetime
import sys
import xml.etree.ElementTree as ET
from distutils.dir_util import copy_tree
from os import remove, close
from collections import Counter
from operator import itemgetter

"""
1.show diff file size, file name
2.Sync Folder(copy extra folder, remove extra folder)
3.Sync File by Name(copy extra file, remove extra)
4.Sync File by Date(copy lastest file, remove old file  )
last update 2017.4.12 Rex at Zhupei

"""

def rawInputTest():
    sYesNo = input(">>> Input, YES/NO: ")
    if ("YES" in sYesNo):
        print ("ans = ", sYesNo)
        return 1
    elif ("NO" in sYesNo):
        print ("ans = ", sYesNo)
        return 0
    else:
        print("wrong answer , do nothing")
        return -1

def buildFileDateInfo(sPath):

    print('{:<10s}buildFileDateInfo  ..'.format('start'))

    # build from file info 
    file_paths = []  # List which will store all of the full filepaths.
    listFileInfo =[]
    # Walk the tree.
    os.chdir(sPath)
    for root, directories, files in os.walk(sPath):
        for fileName in files:            
            filePath = os.path.join(root, fileName)
            relativefilePath = os.path.relpath(filePath)
            
            # print('fileName = {}\n path1 = {},\n path2 = {} '.format(fileName, filePath, relativefilePath))

            # tupleFileInfo[0] = file name
            # tupleFileInfo[1] = file path
            fileTimeInfo = os.path.getmtime(filePath)
            tupleFileInfo = (relativefilePath, fileTimeInfo) #save file name , path into tuple
            listFileInfo.append(tupleFileInfo)  # Add it to the list.            
            # print('fileName = {}\n path1 = {},\n path2 = {} '.format(fileName, relativefilePath, fileTimeInfo))


    print('{:<10s}buildFileInfo  ..'.format('End'))
    return listFileInfo

def runSyncFileByDate(sXmlPath, inParameter):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()   

    print('{:<10s}runSyncFileByDate  ..'.format('start'))

    for neighbor in root.iter('PATHObjects'):
        sPath1 = neighbor.find('SyncFolderFrom').text
        sPath2 = neighbor.find('SyncFolderTo').text

    
    listFileFrom = buildFileDateInfo(sPath1)
    listFileTo = buildFileDateInfo(sPath2)

    nPara = int(inParameter)
    #remove older File
    if ( nPara > 0):
        iIndex = 0
        iFileInfoSize = len(listFileFrom)
        while iFileInfoSize > 0:
            iFileInfoSize -= 1
            if (listFileFrom[iFileInfoSize][1] > listFileTo[iFileInfoSize][1]):
                iIndex += 1
                sFullPathSrc = os.path.join(sPath1, listFileFrom[iFileInfoSize][0])                
                sFullPathDes = os.path.join(sPath2, listFileTo[iFileInfoSize][0])
                
                removeFile(sFullPathDes)
                shutil.copy2(sFullPathSrc, sFullPathDes)
                print('{:<5d}, CopyFile OK\nsFullPathSrc = {} \nsFullPathDes = {} '.format(iIndex, sFullPathSrc, sFullPathDes))

            # print("{},{},{}", iFileInfoSize, listFileFrom[iFileInfoSize][0], listFileFrom[iFileInfoSize][1]  )


    print('{:<10s}runSyncFileByDate..'.format('End'))
    return 0

def buildFileInfo(sPath):

    print('{:<10s}buildFileInfo  ..'.format('start'))

    # build from file info 
    file_paths = []  # List which will store all of the full filepaths.
    listFileInfo =[]
    # Walk the tree.
    os.chdir(sPath)
    for root, directories, files in os.walk(sPath):
        for fileName in files:            
            filePath = os.path.join(root, fileName)
            relativefilePath = os.path.relpath(filePath)
            
            # print('fileName = {}\n path1 = {},\n path2 = {} '.format(fileName, filePath, relativefilePath))

            # tupleFileInfo[0] = file name
            # tupleFileInfo[1] = file path
            tupleFileInfo = (fileName, relativefilePath) #save file name , path into tuple
            listFileInfo.append(tupleFileInfo)  # Add it to the list.            

            # tupleFileInfo = (folderName, relativefilePath) #save file name , path into tuple
            # listFileInfo.append(tupleFileInfo)  # Add it to the list.                        
    # iIndex = 0
    # for x, y in listFileInfo:
    #     print('{:<5d}, listFileInfo, name = {} path = {} '.format(iIndex, x, y))
    #     iIndex += 1


    print('{:<10s}buildFileInfo  ..'.format('End'))
    return listFileInfo


def removeFile(sPath):
    try:
        print('removeFile/Folder path, {} '.format(sPath))
        if os.path.isfile(sPath):
            os.remove(sPath)  # remove the file
        elif os.path.isdir(path):
             shutil.rmtree(path)  # remove dir and all contains
    except OSError:
        print('OSError, {} '.format(sPath))        
    return 0



def runSyncFileByFileName(sXmlPath, inParameter):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()   

    print('{:<10s}runSyncFileByFileName  ..'.format('start'))

    for neighbor in root.iter('PATHObjects'):
        sPath1 = neighbor.find('SyncFolderFrom').text
        sPath2 = neighbor.find('SyncFolderTo').text

    
    listFileFrom = buildFileInfo(sPath1)
    listFileTo = buildFileInfo(sPath2)

    nPara = int(inParameter)
    #remove older File
    if ( nPara > 0):
        iIndex = 0
        for x, y in listFileTo:
            bExistFile = 0
            for x1, y1 in listFileFrom:
                if (y == y1 ):
                    bExistFile = 1

            if (bExistFile == 0): # extra File, need remove
                iIndex += 1
    
                sFullPathDes = os.path.join(sPath2, y)
                print('{:<5d},kill bExtraFile, name = {} path = {},{} '.format(iIndex, x, y, sFullPathDes))
                
                if os.path.exists(sFullPathDes):  # make exist File
                    removeFile(sFullPathDes)



    # copy File
    iIndex = 0
    for x, y in listFileFrom:
        iIndex += 1
        bExistFile = 0
        for x1, y1 in listFileTo:
            if (y in y1 ):
                bExistFile = 1

        if (bExistFile == 0): # not exist File, copyFile
            sFullPathSrc = os.path.join(sPath1, y)
            sFullPathDes = os.path.join(sPath2, y)
            
            # print('show path, \n{}\n{}'.format(sFullPathSrc, sFullPathDes))

            if not os.path.exists(sFullPathDes):
                # print(os.path.dirname(sFullPathDes))
                # make new  folder
                if not os.path.exists(os.path.dirname(sFullPathDes)):
                    try:
                        print('makedirs OK, {}'.format(sFullPathDes))
                        os.makedirs(os.path.dirname(sFullPathDes))
                    except OSError as exc: # Guard against race condition
                        print("OSError")

                # copy file start 
                shutil.copy2(sFullPathSrc, sFullPathDes)
                print('{:<5d}, CopyFile OK\nsFullPathSrc = {} \nsFullPathDes = {} '.format(iIndex, sFullPathSrc, sFullPathDes))


    print('{:<10s}runSyncFileByFileName..'.format('End'))
    return 0



def buildFolderInfo(sPath):

    print('{:<10s}buildFolderInfo  ..'.format('start'))

    # build from folder info 
    file_paths = []  # List which will store all of the full filepaths.
    listFileInfo =[]
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
            listFileInfo.append(tupleFileInfo)  # Add it to the list.            

    # iIndex = 0
    # for x, y in listFileInfo:
    #     print('{:<5d}, listFileInfo, name = {} path = {} '.format(iIndex, x, y))
    #     iIndex += 1


    print('{:<10s}buildFolderInfo  ..'.format('End'))
    return listFileInfo



def runSyncFolder(sXmlPath, inParameter):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()   

    print('{:<10s}runSyncFolder  ..'.format('start'))

    for neighbor in root.iter('PATHObjects'):
        sPath1 = neighbor.find('SyncFolderFrom').text
        sPath2 = neighbor.find('SyncFolderTo').text


    listFolderFrom = buildFolderInfo(sPath1)
    listFolderTo = buildFolderInfo(sPath2)

    #print folder list 
    # iIndex = 0
    # for x, y in listFolderFrom:
    #     print('{:<5d}, listFolderFromInfo, name = {} path = {} '.format(iIndex, x, y))
    #     iIndex += 1

    # iIndex = 0
    # for x, y in listFolderTo:
    #     print('{:<5d}, listFolderToInfo, name = {} path = {} '.format(iIndex, x, y))
    #     iIndex += 1

    
    #remove oldr folder
    if (inParameter == "1"):
        iIndex = 0
        for x, y in listFolderTo:
            
            bExistFolder = 0
            for x1, y1 in listFolderFrom:
                if (y in y1 ):
                    bExistFolder = 1

            if (bExistFolder == 0): # exist folder, need remove
                iIndex += 1
                # print('{:<5d},kill bExistFolder, name = {} path = {} '.format(iIndex, x, y))
    
                sFullPathDes = os.path.join(sPath2, y)
                
                if os.path.exists(sFullPathDes):  # make exist folder
                    shutil.rmtree(sFullPathDes)
                    print('{:<5d}, rmtree OK, {} '.format(iIndex, sFullPathDes))


    # copy folder
    iIndex = 0
    for x, y in listFolderFrom:
        iIndex += 1
        bExistFolder = 0
        for x1, y1 in listFolderTo:
            if (y in y1 ):
                bExistFolder = 1

        if (bExistFolder == 0): # not exist folder, copyFolder
            # print('{:<5d}, bExistFolder, name = {} path = {} '.format(iIndex, x, y))
            sFullPathSrc = os.path.join(sPath1, y)
            sFullPathDes = os.path.join(sPath2, y)
            
            
            if not os.path.exists(sFullPathDes):
                shutil.copytree(sFullPathSrc, sFullPathDes)
                print('{:<5d}, CopyTree OK\nsFullPathSrc = {} \nsFullPathDes = {} '.format(iIndex, sFullPathSrc, sFullPathDes))


    print('{:<10s}runSyncFolder..'.format('End'))
    return 0

# def runSortFileList(inListFile):
#     for f1, f2, f3, f4 in inListFile:
#         for f_1, f_2, f_3, f_4 in inListFile:


#     return outlistFile

def runSameFile(sXmlPath, inParameter):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()   


    print('runSameFile[{}] start ..'.format('-'))

    for neighbor in root.iter('PATHObjects'):
        sPath1 = neighbor.find('Folder_Path').text
        # sPath2 = neighbor.find('PCWorkPath').text    


    file_paths = []  # List which will store all of the full filepaths.
    listFileInfo =[]
    # Walk the tree.
    for root, directories, files in os.walk(sPath1):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.            

            # tupleFileInfo[0] = file name
            # tupleFileInfo[1] = file path
            # tupleFileInfo[2] = file size 
            tupleFileInfo = (filename, filepath, os.path.getsize(filepath))
            listFileInfo.append(tupleFileInfo)
            
            # print('tupleFileInfo = {} \n '.format(tupleFileInfo))
            # print('t0 = {}\n t1 = {} \n t2 = {} \n '.format(tupleFileInfo[0], tupleFileInfo[1], tupleFileInfo[2]))
            
    print("build listFileInfo done")
    # print("======================================\n")
    
    countFileName = [] # count same file by file name
    countFileSize = [] # count same file by file size 
    for x, y, z in listFileInfo:
        countFileName = Counter(elem[0] for elem in listFileInfo) # elem[0] = file name 
        countFileSize = Counter(elem[2] for elem in listFileInfo) # elem[2] = file size

    # for letter, count in countFileName.most_common(1):
    #     print('countFileName, letter = {} count = {} \n '.format(letter, count))

    # for letter, count in countFileSize.most_common(2):
    #     print('countFileSize, letter = {} count = {} \n '.format(letter, count))
        

    print("count file name, size done ")
    # print("======================================\n")

    # made new list
    # x = file name
    # y = file path
    # z = file size 
    listFileInfo2 = [] # new file list for same file name
    listFileInfo3 = [] # new file list for same file size 
    for x, y, z in listFileInfo:
        for letter, count in countFileName.most_common(int(inParameter)):
            if letter == x:
                # tupleFileInfo = (x, y, z, count)
                y =  y.replace("\\","/")
                tupleFileInfo = (count, z, x, y) 

                listFileInfo2.append(tupleFileInfo)        
                # print('countFileName tupleFileInfo = {} \n '.format(tupleFileInfo))
        for letter1, count1 in countFileSize.most_common(int(inParameter)):
            if letter1 == z:
                # tupleFileInfo1 = (x, y, z, count1)
                y =  y.replace("\\","/")
                tupleFileInfo1 = (count1, z, x, y) 
                # tupleFileInfo1 = (x, z, count1, y)
                listFileInfo3.append(tupleFileInfo1)  
                # print('countFileSize tupleFileInfo = {} \n '.format(tupleFileInfo1))

    print("made new file list1,2  done ")
    # print("======================================\n")

    sortlistFileInfo2 = sorted(listFileInfo2,  key=itemgetter(2)) # order by file name
    sortlistFileInfo3 = sorted(listFileInfo3,  key=itemgetter(1)) # order by file  size 

    
    print("sort file list1,2  done ")
    # print("\n Show listFile2 result (same file name) :")
    # print("Index, Title, FileName, FileSize, Filecount, FilePath")
    print('\n\n{:10s},{:10s},{:5s},{:25s},{:20s} , Show listFile2 result (same file name) :'.format("Index", "Filecount", "FileSize", 'FileName', "FilePath"))
    nIndex = 0
    for item in sortlistFileInfo2:
        print('{:<7d}, {}'.format(nIndex, item))
        nIndex += 1


    # print("\n Show listFile3 result (same file size) :")
    # print("Index, Title, FileName, FileSize, Filecount, FilePath")
    print('\n\n{:10s},{:10s},{:5s},{:25s},{:20s} , Show listFile3 result (same file size) :'.format("Index", "Filecount", "FileSize", 'FileName', "FilePath"))
    nIndex = 0
    for item1 in sortlistFileInfo3:
        print('{:<7d}, {}'.format(nIndex, item1))        
        nIndex += 1


    print('\n runSameFile[{}] End ..\n '.format('-'))

    return 0
    #debug code , no use
    print('listFileInfo len = {} \n '.format(len(listFileInfo)))
    print('L0 = {}\n L1 = {} \n L2 = {} \n\n '.format(listFileInfo[0], listFileInfo[1], listFileInfo[2]))
    print('L00 = {}\n L10 = {} \n L20 = {} \n '.format(listFileInfo[0][0], listFileInfo[1][0], listFileInfo[6][0]))
    

    print('count[0] = {}\n \n '.format(Counter(elem[0] for elem in listFileInfo)))
    print('count[2]= {}\n \n '.format(Counter(elem[2] for elem in listFileInfo)))
    


def runPause():
    print('runPause {} {}'.format("-", "-"))
    sYesNo = rawInputTest()
    if (sYesNo == 1):
        print('{}{}'.format(sYesNo, "-"))
    elif(sYesNo == 0):
        print("skip")
        sys.exit(0)
    print('EndPause {} {}'.format("-", "-"))        
    


def parseXML(sXmlPath):

    ListCount = 0
    ListItem = ['']
    ListState = ['','','','','']


    tree = ET.parse(xmlPath)
    root = tree.getroot()     

    for child in root.iter('Item'):
        testName = child.get('Name')
        testState = child.get('Enabled')
        inParameter = child.get('Parameter')
        # print('testName:{:>25}, testState:{:>8}'.format(testName, testState ))

        if (testState == 'TRUE'):
            if ( testName == 'FileSize'):
                runSameFile(xmlPath, inParameter)                                                                 
            if ( testName == 'SyncFolder'):
                runSyncFolder(xmlPath, inParameter)                                                                                 
            if ( testName == 'SyncFileByFileName'):
                runSyncFileByFileName(xmlPath, inParameter) 
            if ( testName == 'SyncFileByDate'):
                runSyncFileByDate(xmlPath, inParameter)                 

            if ( testName == 'Pause'):
                runPause()                                                
                          
            ListItem.insert(ListCount, testName)
            ListCount +=1

    print('\n-------------------------------------------------------------------\n')

    nfinishList = 0 
    for finishList in ListItem:
        print('finishList[{}]:{:>25}'.format(nfinishList, finishList))
        nfinishList += 1
        

    print('\n-------------------excellent you are---------------------------------\n')
    return 0


if __name__ == "__main__":

    xmlPath = "D:\\3S_PC\\python\\3S_AUTO\\FileStudy.xml"

    sStartTime = datetime.datetime.now()
    print('StartTime:{} ..\n '.format(sStartTime))
    try:

        parseXML(xmlPath)

        sEndTime = datetime.datetime.now()        
        print('EndTime:{}, Total:{} ..'.format(sEndTime, (sEndTime-sStartTime)))        

    except:
        print('!!! exception happen in', xmlPath)

	
    sys.exit(0)