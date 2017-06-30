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

    
def runGitCommit(sGitPath, testFile):
    # tree = ET.parse(sXmlPath)
    # root = tree.getroot()   
    print('runGitCommit[{}] start ..'.format('-'))

    try:
        # for neighbor in root.iter('PATHObjects'):
        #     # sPath1 = neighbor.find('PCWorkPath').text
        #     sPath2 = neighbor.find('PCSEToolPath').text
        #     sPath3 = (os.path.abspath(os.path.join(sPath2, os.pardir)))

        sCmd = 'git commit -m {}{}{}'.format("\"", testFile, "\"")  
        # sMsg = 'a'
        print("sCmd:", sCmd)
        # print(sMsg)

        print('sGitPath = {}'.format(sGitPath))
        os.chdir(sGitPath)
        os.system("git add .")
        os.system(sCmd)
    except:
        print('!!except runGitCommit End ..\n ')        

    print('runGitCommit[{}] End ..\n '.format('-'))
    return 0

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

    print('sPath1 = {}, sPath2 = {}'.format(sPath1, sPath2))

    if os.path.exists(sPath2):
        shutil.rmtree(sPath2) 
        print('{}{}'.format(sPath2, ", rmtree ok"))
        

    det_file = os.path.join(sPath1, sTestFile) 
    print('det_file = {}'.format(det_file))

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


def findFile(sPath, sFileName):
    print('findFile Start sPath = {}, name = {}'.format(sPath, sFileName))
    for file in os.listdir(sPath):
        if file.startswith(sFileName):
            print('GetIt = [{}] '.format(file))
            return file
    print('findFile [{}] End ..\n '.format("-"))
    return -1



def runCopyMP(sXmlPath, sVersion):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()   

    print('CopyFromDEPAP[{}] start ..'.format('-'))
    try:
            

        for neighbor in root.iter('PATHObjects'):
            sPath1 = neighbor.find('DEPAP_SSD_Path').text
            sPath3 = neighbor.find('PCSEToolPath').text
            
        sMpVersion = "v1." + sVersion
        sReturnFileName = findFile(sPath1 ,sMpVersion)
        if ( sReturnFileName == -1):
            print ('nothing in {}'.format(sReturnFileName))
        else:
            print ('get it in {}'.format(sReturnFileName))

        #update all new version 
        bFlag = True
        while (bFlag):
            sMpVersion = "v1." + sVersion
            print ('sMpVersion, {}'.format(sMpVersion))
            sReturnFileName = findFile(sPath1 ,sMpVersion)
            

            if ( sReturnFileName == -1):
                print ('nothing in {}'.format(sReturnFileName))
                bFlag = False
            else:
                sReturnFileNameZip = sReturnFileName + ".zip"    
                # sDesPath = os.path.join(sPath1, sReturnFileNameZip)
                print ('sDesPath {}'.format(sReturnFileNameZip))
                runCopyFromDEPAP(sXmlPath, sReturnFileNameZip)
                runCopyFromWorkPath(sXmlPath, sReturnFileName)
                runGitCommit(sPath3, sReturnFileName)
                sVersion = str( int(sVersion) + 1)

        #update xml 
        for child in root.iter('Item'):
            testName = child.get('Name')
            testFile = child.get('FileName')
            if (testName == "CopyMP") and (testFile != sVersion):
                child.set('FileName', sVersion)
                tree.write(sXmlPath)
                print ('wirte xml  {}'.format(sXmlPath))

    except:
        print("!!! except in runCopyMP")
    return 0

def runArtemisCopyTo3SPC(sXmlPath, sTestName):

    tree = ET.parse(sXmlPath)
    root = tree.getroot()   
    try:
        print('runArtemisCopyTo3SPC start \nsPath = {}\nsTestName = {}'.format(sXmlPath, sTestName))
    
   
        for neighbor in root.iter('PATHObjects'):
            sPath2 = neighbor.find('SDEPAP_SSD_libraryPath').text

        for neighbor1 in tree.iter('ProcessObject'):
            if ( neighbor1.get('Name')  == sTestName):
                for neighbor1Child in neighbor1:
                    if(neighbor1Child.tag == 'var1'):
                        sGitPath = neighbor1Child.text
                        print('neighbor1Child.tag(sGitPath) = {}'.format(sGitPath))
                    elif(neighbor1Child.tag == 'var2'):
                        sSrcPath =  neighbor1Child.text
                        print('neighbor2Child.tag(sSrcPath) = {}'.format(sSrcPath))

        print('src = {}'.format(sSrcPath))
        print('det = {}'.format(sGitPath))

        if os.path.exists(sGitPath):
            print('{}", rmtree ok"'.format(sGitPath))
            shutil.rmtree(sGitPath) 
            
        # ignore_dirs = shutil.ignore_patterns('.txt')
        shutil.copytree(sSrcPath, sGitPath)

        sStartTime = datetime.datetime.now()
        # sCmd = 'git commit -m {}{}{}'.format("\"", sStartTime, "\"")          
        runGitCommit(sGitPath, sStartTime)      
    except OSError as why:
        print('!!!except runArtemisCopyTo3SPC, {}'.format( str(why)))    
    except Error as err:
        print('!!!except runArtemisCopyTo3SPC, {}'.format(errors.extend(err.args[0])) )
    except:    
        print("!!!except")
    print('runArtemisCopyTo3SPC end ..')
    return 0

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
            if ( testName == 'CopyFromDEPAP'):
                runCopyFromDEPAP(xmlPath, testFile)                                                                 
            if ( testName == 'CopyFromWorkPath'):
                runCopyFromWorkPath(xmlPath, testFile)        
            if ( testName == 'CopyMP'):
                runCopyMP(xmlPath, testFile)                                                                         
            if ( testName == 'artemisCopyToPC'):
                runArtemisCopyTo3SPC(xmlPath, testName)                    
            if ( testName == 'Pause'):
                runPause()                                                
            # if ( testName == 'GitCommit'):
            #     runGitCommit(xmlPath, testFile)                                                                                                               
                                                             
            # if ( testName == 'GitCommit'):
            #     runGitCommit(xmlPath)             


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

    xmlPath = "D:\\3S_PC\\python\\3S_AUTO\\AutoCopyCommit.xml"

    sStartTime = datetime.datetime.now()
    print('StartTime:{} ..\n '.format(sStartTime))
    try:

        parseXML(xmlPath)

        sEndTime = datetime.datetime.now()        
        print('EndTime:{}, Total:{} ..'.format(sEndTime, (sEndTime-sStartTime)))        

    except:
        print('!!! exception happen in', xmlPath)

	
    sys.exit(0)