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

"""
Achive_Folder_To_ZIP: 壓縮資料夾，排除git檔，上傳至網芳
removeFolder:刪除特定資料夾
removeFile:刪除特定檔案
copyTo3800:將資料夾上傳至網芳
copyRelease note:
"""
sPCS3800_SSD_MPPath = ''
sPC_NewMPUI_Path = ''
sPC_NewMPUI_Name = ''
sRemote3800_NewMPUI_Path = ''
sRemoteDepAp_NewMPUI_Path = ''

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


def removeFolder(sPath):
    sDestinationPath = os.path.join(sPath,"src\debug")
    if (os.path.isdir(sDestinationPath)):
        print("remove folder = ", sDestinationPath)
        shutil.rmtree(sDestinationPath)

    sDestinationPath = os.path.join(sPath,"src\Release")
    if (os.path.isdir(sDestinationPath)):
        print("remove folder = ", sDestinationPath)
        shutil.rmtree(sDestinationPath)    

    sDestinationPath = os.path.join(sPath,"src\Setting")
    if (os.path.isdir(sDestinationPath)):
        print("remove folder = ", sDestinationPath)
        shutil.rmtree(sDestinationPath)    

    sDestinationPath = os.path.join(sPath,"bin\Log")
    if (os.path.isdir(sDestinationPath)):
        print("remove folder = ", sDestinationPath)
        shutil.rmtree(sDestinationPath)    

    sDestinationPath = os.path.join(sPath,"bin\\table")
    if (os.path.isdir(sDestinationPath)):
        print("remove folder = ", sDestinationPath)
        shutil.rmtree(sDestinationPath)    

    sDestinationPath = os.path.join(sPath,"bin\\UI_Log")
    if (os.path.isdir(sDestinationPath)):
        print("remove folder = ", sDestinationPath)
        shutil.rmtree(sDestinationPath)            

    sDestinationPath = os.path.join(sPath,"bin\\data")
    if (os.path.isdir(sDestinationPath)):
        print("remove folder = ", sDestinationPath)
        shutil.rmtree(sDestinationPath)    

    print("removeFolder done!")

def removeFile(sPath):
    for currentFile in glob.glob( os.path.join(sPath, '*') ):
        if os.path.isdir(currentFile):
            #print ("got a directory: ", currentFile)
            removeFile(currentFile)
        #print ("processing file: ", currentFile)

        ncb = "ncb";
        opt = "opt";
        plg = "plg";
        if currentFile.endswith(ncb) or currentFile.endswith(opt) or currentFile.endswith(plg):
            print ("remove file: ", currentFile)
            os.remove(currentFile)

def copyOneFile(src_file, det_file):        
    print('{}-\n{:120}-from \n{:120}-to'.format("prepare to copyOneFile ",src_file, det_file))
    shutil.copy2(src_file, det_file)
    



def B2HEX_MP(sXmlPath):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()     
    global sPCS3800_SSD_MPPath
    global sPC_NewMPUI_Path

    print('{}'.format("B2HEX_MP start .."))
    
    for neighbor in root.iter('PATHObjects'):
        sPath1 = neighbor.find('Bin2HexExePath').text
        sPath2 = os.path.join(sPCS3800_SSD_MPPath, "windows\\3S_SSD_MP.exe")
        sPath1Hex =  sPath1.replace("BIN2HEX.exe","3S_SSD_MP.hex")
        

        print('{} = {}'.format("sPath1 ", sPath1 ))
        print('{} = {}'.format("sPath2 ", sPath2 ))
        print('{} = {}'.format("sPath1Hex ", sPath1Hex ))

    sCmd = sPath1 + " " + sPath2 +  " " + sPath1Hex
    print('{} = {}'.format("sCmd ",sCmd ))
    p=subprocess.Popen(sCmd, shell=True)  
    p.wait() 

    print('{} = {}'.format("sCmd ",sCmd ))


    print('copy to src\MP'.format("-"))
    sPath3 = os.path.join(sPC_NewMPUI_Path, "src\\MP") 
    copyOneFile(sPath1Hex, sPath3)



    print('{}\n'.format("B2HEX_MP End .."))
    
def B2HEX_KEYPRO(sXmlPath):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()     

    print('{}'.format("B2HEX_KEYPRO start .."))

    for neighbor in root.iter('PATHObjects'):
        sPath1 = neighbor.find('Bin2HexExePath').text
        sPath2 = neighbor.find('Bin2HexKeyProDLLPath').text
        sPath1Hex =  sPath1.replace("BIN2HEX.exe","KeyProGen.hex")
        #sPath3 = neighbor.find('Bin2HexKeyProDLLHexPath').text
        
        print('{} = {}'.format("sPath1 ",sPath1 ))
        print('{} = {}'.format("sPath2 ",sPath2 ))
        print('{} = {}'.format("sPath1Hex ", sPath1Hex ))

    sCmd = sPath1 + " " + sPath2 +  " " + sPath1Hex
    print('{} = {}'.format("sCmd ",sCmd ))
    p=subprocess.Popen(sCmd, shell=True)  
    p.wait() 

    print('{} = {}'.format("sCmd ",sCmd ))
    print('{}\n '.format("B2HEX_KEYPRO End .."))

def writeBat(sXmlPath):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()   

    global sPC_NewMPUI_Path

    print('writeBat[{}] start ..'.format('-'))
    for neighbor in root.iter('PATHObjects'):
        sReadPath1 = neighbor.find('PC3SAutoPath').text
        sWritePath1 = neighbor.find('pythonWorkingPath').text

    sReadPath1 = os.path.join(sReadPath1, "BUILD_MP_UI.bat") 
    sWritePath1 = os.path.join(sWritePath1, "autobuild.bat") 
    print(sReadPath1)
    print(sWritePath1) 

    sSourceCodePath = os.path.join(sPC_NewMPUI_Path, "src")
    sCmd = 'cd {}\n'.format(sSourceCodePath)
    print(sCmd)
    

    wF = open(sWritePath1, 'w')  
    wF.writelines(sCmd)

    rF = open(sReadPath1, 'r')  
    result = list()  
    for line in rF.readlines():                          #依次读取每行  
        line = line.strip()                             #去掉每行头尾空白  
        if not len(line) or line.startswith('#'):       #判断是否是空行或注释行  
            continue      
        result.append(line) 
        result.append('\n') 

    wF.writelines(result)      
    wF.close()
    rF.close()
 

    print('{}\n'.format("writeBat End .."))


def runVC6AutoBuild(sXmlPath):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()   
    global sPC_NewMPUI_Path

    print('{}'.format("runVC6AutoBuild start .."))

    writeBat(sXmlPath)

    for neighbor in root.iter('PATHObjects'):
        sPath1 = neighbor.find('pythonWorkingPath').text
    sPath1 = os.path.join(sPath1, "autobuild.bat") 

    p = subprocess.Popen(sPath1, shell=True)    
    p.wait() 
    

    #copy to uac folder
    print('{}'.format("copy to uac folder"))
    sReleaseFolder = os.path.join(sPC_NewMPUI_Path,"src\\Release\\SSDMP.exe")
    sUacFolder = os.path.join(sPC_NewMPUI_Path,"src\\UAC")
    copyOneFile(sReleaseFolder, sUacFolder)

    print('{}\n'.format("runVC6AutoBuild End .."))

def runUacBat(sXmlPath):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()   

    global sPC_NewMPUI_Path

    print('{}'.format("runUacBat start .."))

    sUacFolder = os.path.join(sPC_NewMPUI_Path,"src\\UAC")

    os.chdir(sUacFolder)
    os.system("uac.bat")

    #copy to bin
    print('{}'.format("copy to bin"))
    sUacFolder = os.path.join(sPC_NewMPUI_Path,"src\\UAC\\SSDMP.exe")
    sBinFolder = os.path.join(sPC_NewMPUI_Path,"bin")
    copyOneFile(sUacFolder, sBinFolder)

    print('{},{}\n'.format("runUacBat End ..", sUacFolder))


def runCopySSD_MP_tool_EV(sXmlPath):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()   

    print('runCopySSD_MP_tool_EV[{}] start ..'.format('-'))
    for neighbor in root.iter('PATHObjects'):
        sPath1 = neighbor.find('pythonWorkingPath').text
        sPath2 = neighbor.find('S3800_SSD_MPPath').text
    
    listFolderName = sPath2.split(os.sep)
    iCount = len(listFolderName)
    #print(sFolderName[iCount-1])

    sPath1 = os.path.join(sPath1, listFolderName[iCount-1])
    copy_tree(sPath2, sPath1)

    global sPCS3800_SSD_MPPath
    sPCS3800_SSD_MPPath = sPath1

    print('copy_tree from [{}] to [{}] ok'.format(sPath2, sPath1))
    print('runCopySSD_MP_tool_EV[{}] End ..\n '.format('-'))


def getNewMPUI_Name(sOldName, sVer):
    datetime.datetime.now()

    sMonth = time.strftime("%m") 
    iMonth = int(sMonth)
    sYear  = time.strftime("%Y")
    sDate  = time.strftime("%d")

    listFileName = sOldName.split('.')
    #listFileName[1] = int(listFileName[1]) + 1
    listFileName[1] = sVer
    
    
    NewMPUIName = '{}.{}.{}.{}{}'.format(listFileName[0], listFileName[1], sYear, iMonth, sDate)

    print("NewMPUIName:", NewMPUIName)
    return NewMPUIName
    


def runCopyFromGit(sXmlPath):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()   

    global sPC_NewMPUI_Path
    global sPC_NewMPUI_Name

    print('runCopyFromGit[{}] start ..'.format('-'))
    for neighbor in root.iter('PATHObjects'):
        sPath1 = neighbor.find('PCSourceCodeGitPath').text
        sPath2 = neighbor.find('PCSourceCodePath').text

    if os.path.exists(sPath2):
        shutil.rmtree(sPath2) 
        print('{}{}'.format(sPath2, ", rmtree ok"))

    ignore_dirs = shutil.ignore_patterns( '.gitignore', '.git', 'workHistory', 'MP_UI_DOC', 'src.7z')
    print('copy_tree from [{}] to [{}] ok'.format(sPath1, sPath2))
    shutil.copytree(sPath1, sPath2, ignore=ignore_dirs)



    print('runCopyFromGit[{}] End ..\n '.format('-'))

def runCopySSD_MP_UI(sXmlPath):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()   

    global sPC_NewMPUI_Path
    global sPC_NewMPUI_Name

    print('runCopySSD_MP_UI[{}] start ..'.format('-'))
    for neighbor in root.iter('PATHObjects'):
        sPath1 = neighbor.find('PCSourceCodePath').text
        sToolVersion = neighbor.find('ToolVersion').text

    listFolderName = sPath1.split(os.sep)
    iCount = len(listFolderName)
    sNewFolder = listFolderName[iCount-1]
    #print(listFolderName[iCount-1])
    sNewName = getNewMPUI_Name(listFolderName[iCount-1], sToolVersion)
    sPath2 = sPath1.replace(listFolderName[iCount-1], sNewName)

    if os.path.exists(sPath2):
        shutil.rmtree(sPath2) 
        print('{}{}'.format(sPath2, ", rmtree ok"))
        
    copy_tree(sPath1, sPath2)
    sPC_NewMPUI_Name = sNewName
    sPC_NewMPUI_Path = sPath2

    print('sPC_NewMPUI_Name = [{}] , sPC_NewMPUI_Path =  [{}]'.format(sPC_NewMPUI_Name, sPC_NewMPUI_Path))

    print('copy_tree from [{}] to [{}] ok'.format(sPath1, sPath2))

    print('runCopySSD_MP_UI[{}] End ..\n '.format('-'))



def runCopyToGitbin(sXmlPath):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()   

    global sPC_NewMPUI_Path
    global sPC_NewMPUI_Name

    print('runCopyToGitbin[{}] start ..'.format('-'))
    
    for neighbor in root.iter('PATHObjects'):
        sPathGit = neighbor.find('PCSourceCodeGitPath').text
        det_file = os.path.join(sPathGit, "bin")  

    removeFolder(sPC_NewMPUI_Path) # remove specific folder
    removeFile(sPC_NewMPUI_Path) # remove specific folder

    # det_file = os.path.join(sPath1, sPC_NewMPUI_Name) 
    src_file = os.path.join(sPC_NewMPUI_Path, 'bin')
    #print(det_file)
    print('src = {}', src_file)
    print('det = {}', det_file)

    if os.path.exists(det_file):
        print('{}{}'.format(det_file, "   exist !! remove it ?"))
        sYesNo = rawInputTest()
        if (sYesNo == 1):
            shutil.rmtree(det_file) 
            print('{}{}'.format(det_file, ", remove ok"))
        elif(sYesNo == 0):
            print("skip")
            sys.exit(0)
        
    shutil.copytree(src_file, det_file)
    print('runCopyToGitbin, {} end ..'.format(det_file))


def runArtemisCopyTo3SPC(sXmlPath):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()   

    global sPC_NewMPUI_Path
    global sPC_NewMPUI_Name

    print('runCopy3SPC[{}] start ..'.format('-'))
    
    for neighbor in root.iter('PATHObjects'):
        sPath1 = neighbor.find('PC_SSD_tools').text
        sPath2 = neighbor.find('SDEPAP_SSD_libraryPath').text
        det_file = os.path.join(sPath1, "artemis")  
        src_file = os.path.join(sPath2, "artemis")  

    #removeFolder(sPC_NewMPUI_Path) # remove specific folder
    # removeFile(sPC_NewMPUI_Path) # remove specific folder

    # det_file = os.path.join(sPath1, sPC_NewMPUI_Name) 
    
    #print(det_file)
    print('src = {}'.format(src_file))
    print('det = {}'.format(det_file))

    if os.path.exists(det_file):
        print('{}{}'.format(det_file, "   exist !! remove it ?"))
        sYesNo = rawInputTest()
        if (sYesNo == 1):
            shutil.rmtree(det_file) 
            print('{}{}'.format(det_file, ", remove ok"))
        elif(sYesNo == 0):
            print("skip")
            sys.exit(0)
        
    shutil.copytree(src_file, det_file)
    print('runCopy3SPC, {} end ..'.format(det_file))



def runGitCommit(sXmlPath):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()   

    print('runGitCommit[{}] start ..'.format('-'))

    for neighbor in root.iter('PATHObjects'):
        # sPath1 = neighbor.find('PCWorkPath').text
        sPath2 = neighbor.find('PC_SSD_tools').text
        sPath3 = (os.path.abspath(os.path.join(sPath2, os.pardir)))

    sStartTime = datetime.datetime.now()

    sCmd = 'git commit -m {}{}{}'.format("\"", sStartTime, "\"")  
    # sMsg = 'a'
    print("sCmd:", sCmd)
    # print(sMsg)
    
    print('sPath2 = {} , {}'.format(sPath2, sPath2))
    
    os.chdir(sPath2)
    os.system("git add .")
    os.system(sCmd)


    print('runGitCommit[{}] End ..\n '.format('-'))

def get_filepaths(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.


def parseXML():

    xmlPath = r"D:\\3S_PC\\python\\3S_AUTO\\Sync_3S.xml"

    ListCount = 0
    ListItem = ['']
    ListState = ['','','','','']


    tree = ET.parse(xmlPath)
    root = tree.getroot()     

    for child in root.iter('Item'):
        testName = child.get('Name')
        testState = child.get('Enabled')
        print('testName:{:>25}, testState:{:>8}'.format(testName, testState ))

        if (testState == 'TRUE'):
            if ( testName == 'artemisCopyToPC'):
                runArtemisCopyTo3SPC(xmlPath)                                                                 
            if ( testName == 'GitCommit'):
                runGitCommit(xmlPath)             

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

    # xmlPath = r"D:\\3S_PC\\python\\3S_AUTO\\Sync_3S.xml"
    cmd = "D:\\3S_PC\sourceCode\SSD\VS2008\BIN2HEX\Release\BIN2HEX.exe D:\\3S_PC\\sourceCode\\SSD\\VS2008\\BIN2HEX\\Debug\\3S_SSD_MP.exe D:\\3S_PC\\sourceCode\\SSD\\VS2008\\BIN2HEX\\Release\\3S_SSD_MP.hex"

    sStartTime = datetime.datetime.now()
    print('StartTime:{} ..\n '.format(sStartTime))
    try:
        #ok
        #B2HEX_MP(xmlPath)
        #B2HEX_KEYPRO(xmlPath)

        parseXML()

        sEndTime = datetime.datetime.now()        
        print('EndTime:{}, Total:{} ..'.format(sEndTime, (sEndTime-sStartTime)))        

        #tree.write(data,"UTF-8")
    except:
        print('!!! exception happen in')


	
    sys.exit(0)