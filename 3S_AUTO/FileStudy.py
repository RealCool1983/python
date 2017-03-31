import zipfile
import os
import shutil
import glob
import datetime
import time
import sys
import xml.etree.ElementTree as ET
from distutils.dir_util import copy_tree
from os import remove, close


"""
auto git commit from rar to Repository 

1.copy zip folder from server to pc workFolder
2.extractall 
3.copy src, pbackage bin to pc/SE_TOOLS/MP/MP_V1 
4.git add . 
5.git commit - m "zip file name"

last update 2017.3.24 Rex at Zhupei

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

    
def runGitCommit(sXmlPath, testFile):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()   

    print('runGitCommit[{}] start ..'.format('-'))

    for neighbor in root.iter('PATHObjects'):
        sPath1 = neighbor.find('PCWorkPath').text
        sPath2 = neighbor.find('PCSEToolPath').text
        sPath3 = (os.path.abspath(os.path.join(sPath2, os.pardir)))

    sCmd = 'git commit -m {}{}{}'.format("\"", testFile, "\"")  
    # sMsg = 'a'
    print("sCmd:", sCmd)
    # print(sMsg)

    print('sPath3 = {} , {}'.format(sPath3, sPath3))
    os.chdir(sPath3)
    os.system("git add .")
    os.system(sCmd)


    print('runGitCommit[{}] End ..\n '.format('-'))

def runCopyFolder(sSrc, sDet):
    # ignore_dirs = shutil.ignore_patterns( '.gitignore', '.git')
    ignore_dirs = shutil.ignore_patterns( '.gitignore', '.git')
    print('runCopyFolder from {} to {} ok'.format(sSrc, sDet))
    shutil.copytree(sSrc, sDet, ignore=ignore_dirs)


# 1.remove exist folder
# 2.copy folder
def runCopyFromWorkPath(sXmlPath, sTestFile):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()   

    print('runCopyFromWorkPath[{}] start ..'.format('-'))
    for neighbor in root.iter('PATHObjects'):
        sPath1 = neighbor.find('PCWorkPath').text
        sPath2 = neighbor.find('PCSEToolPath').text

    if os.path.exists(sPath2):
        shutil.rmtree(sPath2) 
        print('{}{}'.format(sPath2, ", rmtree ok"))
        

    det_file = os.path.join(sPath1, sTestFile) 

    print(os.listdir(det_file))


    for root, directories, files in os.walk(det_file):
        for subfolder in directories:
            if (subfolder.find("bin") != -1 ):
                sFolderPathSrc = os.path.join(root, subfolder)
                sFolderPathDet = os.path.join(sPath2, subfolder)
                print('subfolder = {}, path = {}'.format(subfolder, sFolderPathSrc))
                runCopyFolder(sFolderPathSrc, sFolderPathDet)

            elif (subfolder.find("src") != -1 ):
                sFolderPathSrc = os.path.join(root, subfolder)
                sFolderPathDet = os.path.join(sPath2, subfolder)
                print('subfolder = {}, path = {}'.format(subfolder, sFolderPathSrc))
                runCopyFolder(sFolderPathSrc, sFolderPathDet)

            elif (subfolder.find("package") != -1 ):
                sFolderPathSrc = os.path.join(root, subfolder)
                sFolderPathDet = os.path.join(sPath2, subfolder)
                print('subfolder = {}, path = {}'.format(subfolder, sFolderPathSrc))
                runCopyFolder(sFolderPathSrc, sFolderPathDet)
                
            # file_paths.append(filepath)  # Add it to the list.

    # for subfolder in os.listdir(det_file):
    #     if (subfolder.find("bin")):
    #         print('subfolder '.format(subfolder))            


    print('runCopyFromWorkPath[{}] End ..\n '.format('-'))


def get_filepaths(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.


def runFileSize(sXmlPath, sTestFile):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()   


    print('runFileSize[{}] start ..'.format('-'))
    for neighbor in root.iter('PATHObjects'):
        sPath1 = neighbor.find('Folder_Path').text
        # sPath2 = neighbor.find('PCWorkPath').text    
    # print(get_filepaths(sPath1))

    print('path = {}\n '.format(get_filepaths(sPath1)))

    print('runFileSize[{}] End ..\n '.format('-'))


def runCopyFromDEPAP(sXmlPath, sTestFile):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()   

    global sPC_NewMPUI_Path
    global sPC_NewMPUI_Name

    print('CopyFromDEPAP[{}] start ..'.format('-'))
    for neighbor in root.iter('PATHObjects'):
        sPath1 = neighbor.find('DEPAP_SSD_Path').text
        sPath2 = neighbor.find('PCWorkPath').text

    det_file = os.path.join(sPath1, sTestFile) 
    if os.path.exists(det_file):
        print('{}{}'.format(det_file, ", exist"))

    if not (os.path.exists(sPath2)):
        print('{}{}'.format(sPath2, ",exist , remove now"))        
        os.remove(sPath2)

    # ignore_dirs = shutil.ignore_patterns( '.gitignore', '.git')
    print('copy from [{}] to [{}] ok'.format(det_file, sPath2))

    # shutil.copytree(sPath1, sPath2, ignore=ignore_dirs)

    shutil.copy(det_file, sPath2)

    sPath3 = os.path.join(sPath2, sTestFile) 
    zf = zipfile.ZipFile(sPath3)

    print('{}{}'.format(sPath3, ", ready to Extract "))        
    zf.extractall(path=sPath2, members=None, pwd=None)
    zf.close()

    print('CopyFromDEPAP[{}] End ..\n '.format('-'))



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
        testFile = child.get('FileName')
        print('testName:{:>25}, testState:{:>8}'.format(testName, testState ))

        if (testState == 'TRUE'):
            if ( testName == 'FileSize'):
                runFileSize(xmlPath, testFile)                                                                 
            # if ( testName == 'CopyFromWorkPath'):
            #     runCopyFromWorkPath(xmlPath, testFile)        
            # if ( testName == 'GitCommit'):
            #     runGitCommit(xmlPath, testFile)                                                                                                               
        
            if ( testName == 'Pause'):
                runPause()                                                
                          
            ListItem.insert(ListCount, testName)
            ListCount +=1

    print('\n----------------------------------------------------\n')
    nfinishList = 0 
    for finishList in ListItem:
        if (finishList.find('CopySSD_MP_UI') != -1 ):
            print('finishList[{}]:{:>25} : {}'.format(nfinishList, finishList, sPC_NewMPUI_Path))
        elif (finishList.find('CopySSD_MP_tool_EV') != -1 ):
            print('finishList[{}]:{:>25} : {}'.format(nfinishList, finishList, sPCS3800_SSD_MPPath))            
        elif (finishList.find('CopyTo3800') != -1 ):
            print('finishList[{}]:{:>25} : {}'.format(nfinishList, finishList, sRemote3800_NewMPUI_Path))               
        elif (finishList.find('CompressFile') != -1 ):
            print('finishList[{}]:{:>25} : {}'.format(nfinishList, finishList, sRemoteDepAp_NewMPUI_Path))               
        else:
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