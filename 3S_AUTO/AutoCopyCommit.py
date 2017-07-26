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

    
def runGitCommit(sGitPath, testFile, sTestName):
    print('runGitCommit[{}] start ..'.format('-'))

    try:
        sCmd = 'git commit -m {}[{}]{}{}'.format("\"",sTestName, testFile, "\"")  
        # sMsg = 'a'
        print("sCmd:", sCmd)
        # print(sMsg)

        print('sGitPath = {}'.format(sGitPath))
        os.chdir(sGitPath)
        os.system("git add .")
        os.system(sCmd)
    except:
        print('!!!except runGitCommit End ..\n ')        

    print('runGitCommit[{}] End ..\n '.format('-'))
    return 0

def runCopyFolder(sSrc, sDet):
    # ignore_dirs = shutil.ignore_patterns( '.gitignore', '.git')
    ignore_dirs = shutil.ignore_patterns( '.gitignore', '.git')
    print('runCopyFolder from {} to {} ok'.format(sSrc, sDet))
    if not (os.path.exists(sSrc)):
        print('[Err] runCopyFolder not exist {}'.format(sSrc))
    if os.path.exists(sDet):
        print('[Err] runCopyFolder exit {}'.format(sDet))
        return -1

    shutil.copytree(sSrc, sDet, ignore=ignore_dirs)

    return 0

# # 1.remove exist folder
# # 2.copy folder
# def runCopyFromWorkPath(sXmlPath, sTestFile):
#     tree = ET.parse(sXmlPath)
#     root = tree.getroot()   
#     try:
#         print('runCopyFromWorkPath[{}] start ..'.format('-'))
#         for neighbor in root.iter('PATHObjects'):
#             sPath1 = neighbor.find('PCWorkPath').text
#             sPath2 = neighbor.find('PCSEToolPath').text

#         print('sPath1 = {}, sPath2 = {}'.format(sPath1, sPath2))

#         if os.path.exists(sPath2):
#             shutil.rmtree(sPath2) 
#             print('{}{}'.format(sPath2, ", rmtree ok"))
            

#         det_file = os.path.join(sPath1, sTestFile) 
#         # print('det_file = {}'.format(det_file))
#         if not (os.path.exists(det_file)):
#             print('[Err] not exist, det_file = {}'.format(det_file))
#             retur -1
#         else:
#             print(os.listdir(det_file))

#         for root, directories, files in os.walk(det_file):
#             for subfolder in directories:
#                 if (subfolder.find("bin") != -1 ):
#                     sFolderPathSrc = os.path.join(root, subfolder)
#                     sFolderPathDet = os.path.join(sPath2, subfolder)
#                     print('subfolder = {}, path = {}'.format(subfolder, sFolderPathSrc))
#                     runCopyFolder(sFolderPathSrc, sFolderPathDet)

#                 elif (subfolder.find("src") != -1 ):
#                     sFolderPathSrc = os.path.join(root, subfolder)
#                     sFolderPathDet = os.path.join(sPath2, subfolder)
#                     print('subfolder = {}, path = {}'.format(subfolder, sFolderPathSrc))
#                     runCopyFolder(sFolderPathSrc, sFolderPathDet)

#                 elif (subfolder.find("package") != -1 ):
#                     sFolderPathSrc = os.path.join(root, subfolder)
#                     sFolderPathDet = os.path.join(sPath2, subfolder)
#                     print('subfolder = {}, path = {}'.format(subfolder, sFolderPathSrc))
#                     runCopyFolder(sFolderPathSrc, sFolderPathDet)
#     except:
#         print('!!!excpet in runCopyFromWorkPath\n')            
#         return -1

#     print('runCopyFromWorkPath[{}] End ..\n '.format('-'))
#     return 0

# def runCopyFromWorkPath(sXmlPath, sTestFile):
def runCopyFromWorkPath_EX(sSrcFolder, sSrcFile, sDesFolder):
    try:
        print('runCopyFromWorkPath_EX[{}] start ..'.format('-'))
        
        print('sSrcFolder = {}, sSrcFile = {}, sDesFolder = {}'.format(sSrcFolder, sSrcFile, sDesFolder))

        sDesPath = os.path.join(sDesFolder, sSrcFile)
        if os.path.exists(sDesFolder):
            print('{}{}'.format(sDesFolder, ", prepare rmtree "))
            shutil.rmtree(sDesFolder,  ignore_errors=True)                         
            # shutil.rmtree(sFolderPath) 
            print('{}{}'.format(sDesFolder, ", rmtree done"))
        else:
            print('not exist, {}'.format(sDesFolder))

        sSrcPath = os.path.join(sSrcFolder, sSrcFile) 
        print('sSrcPath = {}'.format(sSrcPath))
        if not (os.path.exists(sSrcPath)):
            print('[Err] not exist, det_file = {}'.format(sSrcPath))
            retur -1
        else:
            print(os.listdir(sSrcPath))

        for root, directories, files in os.walk(sSrcPath):
            for subfolder in directories:
                if (subfolder.find("bin") != -1 ):
                    sFolderPathSrc = os.path.join(root, subfolder)
                    sFolderPathDet = os.path.join(sDesFolder, subfolder)
                    print('subfolder = {}, path = {}'.format(subfolder, sFolderPathSrc))
                    runCopyFolder(sFolderPathSrc, sFolderPathDet)

                elif (subfolder.find("src") != -1 ):
                    sFolderPathSrc = os.path.join(root, subfolder)
                    sFolderPathDet = os.path.join(sDesFolder, subfolder)
                    print('subfolder = {}, path = {}'.format(subfolder, sFolderPathSrc))
                    runCopyFolder(sFolderPathSrc, sFolderPathDet)

                elif (subfolder.find("package") != -1 ):
                    sFolderPathSrc = os.path.join(root, subfolder)
                    sFolderPathDet = os.path.join(sDesFolder, subfolder)
                    print('subfolder = {}, path = {}'.format(subfolder, sFolderPathSrc))
                    runCopyFolder(sFolderPathSrc, sFolderPathDet)
    except:
        print('!!!excpet in runCopyFromWorkPath_EX\n')            
        return -1

    print('runCopyFromWorkPath_EX[{}] End ..\n '.format('-'))
    return 0



# def runCopyFromDEPAP(sXmlPath, sTestFile):
#     tree = ET.parse(sXmlPath)
#     root = tree.getroot()   

#     global sPC_NewMPUI_Path
#     global sPC_NewMPUI_Name

#     print('CopyFromDEPAP[{}] start ..'.format('-'))

#     try:
#         for neighbor in root.iter('PATHObjects'):
#             sPath1 = neighbor.find('DEPAP_SSD_Path').text
#             sPath2 = neighbor.find('PCWorkPath').text

#         det_file = os.path.join(sPath1, sTestFile) 
#         if os.path.exists(det_file):
#             print('{}{}'.format(det_file, ", exist"))

#         sPath3 = os.path.join(sPath2, sTestFile) 
#         if os.path.exists(sPath3):
#             print('{}{}'.format(sPath3, ",exist , remove now"))        
#             os.remove(sPath3)

        
#         print('copy from [{}] to [{}] ok'.format(det_file, sPath2))

#         # shutil.copytree(sPath1, sPath2, ignore=ignore_dirs)

#         shutil.copy(det_file, sPath2)

#         if os.path.exists(sPath3):
#             zf = zipfile.ZipFile(sPath3)

#             print('{}{}'.format(sPath3, ", ready to Extract "))        
#             zf.extractall(path=sPath2, members=None, pwd=None)
#             zf.close()
#         else:
#             print('{}{}'.format(sPath3, "not exist , do nothing"))        
#     except:
#         print('!!!except in runCopyFromDEPAP\n')        

#     print('CopyFromDEPAP[{}] End ..\n '.format('-'))
#     return 0


def runCopyFromDEPAP_EX(sSrcFolder, sSrcFile, sDesFolder):   

    print('runCopyFromDEPAP_EX[{}] start ..'.format('-'))

    try:
        sSrcPath = os.path.join(sSrcFolder, sSrcFile) 
        if os.path.exists(sSrcPath):
            print('{}{}'.format(sSrcPath, ", exist ok"))

        sPath3 = os.path.join(sDesFolder, sSrcFile) 
        if os.path.exists(sPath3):
            print('{}{}'.format(sPath3, ",exist , remove now"))        
            os.remove(sPath3)

        
        print('copy from [{}] to [{}] ok'.format(sSrcPath, sDesFolder))

        # shutil.copytree(sPath1, sPath2, ignore=ignore_dirs)

        shutil.copy(sSrcPath, sDesFolder)

        if os.path.exists(sPath3):
            zf = zipfile.ZipFile(sPath3)

            print('{}{}'.format(sPath3, ", ready to Extract "))        
            zf.extractall(path=sDesFolder, members=None, pwd=None)
            zf.close()
            print('{}{}'.format(sPath3, ", Extract done"))        
        else:
            print('{}{}'.format(sPath3, "not exist , do nothing"))        
    except:
        print('!!!except in runCopyFromDEPAP_EX\n')        

    print('runCopyFromDEPAP_EX[{}] End ..\n '.format('-'))
    return 0


def findFile(sPath, sFileName):
    print('findFile Start sPath = {}, name = {}'.format(sPath, sFileName))
    for file in os.listdir(sPath):
        if file.startswith(sFileName):
            print('GetIt = [{}] '.format(file))
            return file
    print('findFile [{}] End ..\n '.format("-"))
    return -1

def findFile_Ex(sPath, sStartStr, sEndStr):
    try:
        print('findFile_Ex Start sPath = {}, sStartStr = {}, sEndStr = {}'.format(sPath, sStartStr, sEndStr))
        for file in os.listdir(sPath):
            if file.startswith(sStartStr):
                if file.endswith(sEndStr):
                    print('GetIt = [{}] '.format(file))
                    return file
        print('findFile_Ex [{}] End ..\n '.format("-"))
    except:
        print(' findFile_Ex except [{}] End ..\n '.format("-"))  
    return -1


# def runCopyMP(sXmlPath, sTestName, sParameter):
#     tree = ET.parse(sXmlPath)
#     root = tree.getroot()   

#     print('CopyFromDEPAP start \nsPath = {}\nsTestName = {}\nsParameter = {}'.format(sXmlPath, sTestName, sParameter))
    
#     try:
#         for neighbor in root.iter('PATHObjects'):
#             sPath1 = neighbor.find('DEPAP_SSD_Path').text
#             sPath3 = neighbor.find('PCSEToolPath').text
            
#         # sMpVersion = "v1." + sVersion
#         # sReturnFileName = findFile(sPath1 ,sMpVersion)
#         # if ( sReturnFileName == -1):
#         #     print ('nothing in {}'.format(sReturnFileName))
#         # else:
#         #     print ('get it in {}'.format(sReturnFileName))

#         #update all new version 
#         bFlag = True
#         bRes = False
#         while (bFlag):
#             sMpVersion = "v1." + sParameter
#             print ('sMpVersion, {}'.format(sMpVersion))
#             sReturnFileName = findFile(sPath1 ,sMpVersion)
            
#             if ( sReturnFileName == -1):
#                 print ('nothing in {}'.format(sReturnFileName))
#                 bFlag = False
#             else:
#                 sReturnFileNameZip = sReturnFileName + ".zip"    
#                 # sDesPath = os.path.join(sPath1, sReturnFileNameZip)
#                 print ('sDesPath {}'.format(sReturnFileNameZip))
#                 if (runCopyFromDEPAP(sXmlPath, sReturnFileNameZip) != 0):
#                     return -1
#                 if (runCopyFromWorkPath(sXmlPath, sReturnFileName) != 0):
#                     return -1
#                 if (runGitCommit(sPath3, sReturnFileName) != 0):
#                     return -1
#                 sParameter = str( int(sParameter) + 1)
#                 bRes = True
#         if (bRes):
#             #update xml 
#             for child in root.iter('Item'):
#                 testName = child.get('Name')
#                 testPara = child.get('Parameter')
#                 if (testName == "CopyMP") and (testPara != sVersion):
#                     child.set('Parameter', sParameter)
#                     tree.write(sXmlPath)
#                     print ('wirte xml  {}'.format(sXmlPath))

#     except:
#         print("!!! except in runCopyMP")
#     return 0


# def runMP(sXmlPath, sTestName, sParameter):
#     tree = ET.parse(sXmlPath)
#     root = tree.getroot()   

#     print('runSSDFA start \nsPath = {}\nsTestName = {}\nsParameter = {}'.format(sXmlPath, sTestName, sParameter))
    
#     try:
#         for neighbor1 in tree.iter('ProcessObject'):
#             if ( neighbor1.get('Name')  == sTestName):
#                 for neighbor1Child in neighbor1:
#                     if(neighbor1Child.tag == 'var1'):
#                         sDesFolder = neighbor1Child.text
#                         print('neighbor1Child.tag(sGitPath) = {}'.format(sDesFolder))
#                     elif(neighbor1Child.tag == 'var2'):
#                         sSrcPath =  neighbor1Child.text
#                         print('neighbor2Child.tag(sSrcPath) = {}'.format(sSrcPath))
#                     elif(neighbor1Child.tag == 'var3'):
#                         sGitWorkPath =  neighbor1Child.text
#                         print('neighbor2Child.tag(sGitWorkPath) = {}'.format(sGitWorkPath))


#         #update all new version 
#         bFlag = True
#         bRes = False
#         while (bFlag):
#             sVersion = "v1." + sParameter
#             print ('sVersion, {}'.format(sVersion))
#             sReturnFileName = findFile_Ex(sSrcPath ,sVersion, ".zip")
            
#             if ( sReturnFileName == -1):
#                 print ('nothing in {}'.format(sReturnFileName))
#                 bFlag = False
#             else:
#                 sReturnFileNameZip = sReturnFileName 
#                 # sDesPath = os.path.join(sPath1, sReturnFileNameZip)
#                 print ('sDesPath {}'.format(sReturnFileNameZip))
#                 if (runCopyFromDEPAP_EX(sSrcPath, sReturnFileNameZip , sGitWorkPath) != 0):
#                     return -1

#                 sReturnFileName = sReturnFileNameZip.replace(".zip", "")
#                 if (runCopyFromWorkPath_EX(sGitWorkPath, sReturnFileName , sDesFolder) != 0):
#                     return -1
#                 if (runGitCommit(sDesFolder, sReturnFileName) != 0):
#                     return -1
#                 sParameter = str( int(sParameter) + 1)
#                 bRes = True

#         if (bRes):
#             #update xml 
#             for child in root.iter('Item'):
#                 testName = child.get('Name')
#                 testPara = child.get('Parameter')
#                 if (testName == "SSDFA") and (testPara != sVersion):
#                     child.set('Parameter', sParameter)
#                     tree.write(sXmlPath)
#                     print ('wirte xml  {}'.format(sXmlPath))

#     except:
#         print("!!! except in runSSDFA")
#     return 0



def runSSDFA(sXmlPath, sTestName, sParameter):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()   

    print('runSSDFA start \nsPath = {}\nsTestName = {}\nsParameter = {}'.format(sXmlPath, sTestName, sParameter))
    
    try:
        for neighbor1 in tree.iter('ProcessObject'):
            if ( neighbor1.get('Name')  == sTestName):
                for neighbor1Child in neighbor1:
                    if(neighbor1Child.tag == 'var1'):
                        sDesFolder = neighbor1Child.text
                        print('neighbor1Child.tag(sGitPath) = {}'.format(sDesFolder))
                    elif(neighbor1Child.tag == 'var2'):
                        sSrcPath =  neighbor1Child.text
                        print('neighbor2Child.tag(sSrcPath) = {}'.format(sSrcPath))
                    elif(neighbor1Child.tag == 'var3'):
                        sGitWorkPath =  neighbor1Child.text
                        print('neighbor2Child.tag(sGitWorkPath) = {}'.format(sGitWorkPath))


        #update all new version 
        bFlag = True
        bRes = False
        while (bFlag):
            if(sTestName == "SSDFA"):
                sVersion = "1." + sParameter
            elif(sTestName == "CopyMP"):
                sVersion = "v1." + sParameter
            elif(sTestName == "CheckValidUtility"):
                sVersion = "2." + sParameter

            print ('sVersion, {}'.format(sVersion))
            sReturnFileName = findFile_Ex(sSrcPath ,sVersion, ".zip")
            
            if ( sReturnFileName == -1):
                print ('nothing in {}'.format(sReturnFileName))
                bFlag = False
            else:
                sReturnFileNameZip = sReturnFileName 
                # sDesPath = os.path.join(sPath1, sReturnFileNameZip)
                print ('sDesPath {}'.format(sReturnFileNameZip))
                if (runCopyFromDEPAP_EX(sSrcPath, sReturnFileNameZip , sGitWorkPath) != 0):
                    return -1

                sReturnFileName = sReturnFileNameZip.replace(".zip", "")
                if (runCopyFromWorkPath_EX(sGitWorkPath, sReturnFileName , sDesFolder) != 0):
                    return -1
                if (runGitCommit(sDesFolder, sReturnFileName, sTestName) != 0):
                    return -1
                sParameter = str( int(sParameter) + 1)
                bRes = True

        if (bRes):
            #update xml 
            for child in root.iter('Item'):
                testName = child.get('Name')
                testPara = child.get('Parameter')

                if(testName == sTestName):
                    if (testPara != sVersion):
                        child.set('Parameter', sParameter)
                        tree.write(sXmlPath)
                        print ('wirte xml  {}'.format(sXmlPath))                        

    except:
        print("!!! except in runSSDFA")
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
        runGitCommit(sGitPath, sStartTime, sTestName)      
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
    try:        
        ListCount = 0
        ListItem = ['']
        ListState = ['','','','','']

        tree = ET.parse(xmlPath)
        root = tree.getroot()     

        for child in root.iter('Item'):
            testName = child.get('Name')
            testState = child.get('Enabled')
            parameter = child.get('Parameter')
            print('testName:{:>25}, testState:{:>8}, , parameter:{:>8}'.format(testName, testState, parameter))

            if (testState == 'TRUE'):    
                if ( testName == 'SSDFA'):
                    runSSDFA(xmlPath, testName, parameter)                                                                                                        
                elif ( testName == 'CopyMP'):
                    runSSDFA(xmlPath, testName, parameter)                                                                         
                elif ( testName == 'CheckValidUtility'):
                    runSSDFA(xmlPath, testName, parameter)                                                                                             
                elif ( testName == 'artemisCopyToPC'):
                    runArtemisCopyTo3SPC(xmlPath, testName)                    
                elif ( testName == 'Pause'):
                    runPause()                                                                                                       


                ListItem.insert(ListCount, testName)
                ListCount +=1

        print('\n----------------------------------------------------\n')
        nfinishList = 0 


        for finishList in ListItem:
            if (finishList.find('SSDFA') != -1 ):
                print('finishList[{}]:{:>25}'.format(nfinishList, finishList))
            elif (finishList.find('CopyMP') != -1 ):
                print('finishList[{}]:{:>25} '.format(nfinishList, finishList))            
            elif (finishList.find('CheckValidUtility') != -1 ):
                print('finishList[{}]:{:>25} '.format(nfinishList, finishList))                            
            elif (finishList.find('artemisCopyToPC') != -1 ):
                print('finishList[{}]:{:>25}'.format(nfinishList, finishList))               
            elif (finishList.find('Pause') != -1 ):
                print('finishList[{}]:{:>25}'.format(nfinishList, finishList))               
            else:
                print('finishList[{}]:{:>25}'.format(nfinishList, finishList))
            nfinishList += 1            

        print('\n-------------------excellent you are---------------------------------\n')
    except:
        print('parseXML except')
        return -1
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