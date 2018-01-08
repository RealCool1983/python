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
auto git commit from folder to Repository 

1.copy folder 
2.rmtree for bin folder in git 
3.git add . 
4.git commit - m "folder name"

last update 20180108 Rex at Zhupei

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


def findFolder(sPath, sFolderName):
    try:
        print('findFolder Start sPath = {}, sStartStr = {}'.format(sPath, sFolderName))

        for root, dirs, files in os.walk(sPath):  
            for foldername in dirs:
                # print('foldername = [{}] '.format(foldername))
                if (foldername == sFolderName):
                    sFolderPath = os.path.join(root, foldername)
                    print('GetIt = [{}] '.format(sFolderPath))
                    return sFolderPath
        return 0
    except:
        print(' findFile_Ex except [{}] End ..\n '.format("-"))  
    return -1



def runCopyUsb2(sXmlPath, sTestName, sParameter):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()   

    print('runCopyUsb2 start go\nsPath = {}\nsTestName = {}\nsParameter = {}'.format(sXmlPath, sTestName, sParameter))
    
    try:
        for neighbor1 in tree.iter('ProcessObject'):
            if ( neighbor1.get('Name')  == sTestName):
                for neighbor1Child in neighbor1:
                    if(neighbor1Child.tag == 'var1'):
                        sDesPath = neighbor1Child.text
                        
                        print('neighbor1Child.tag(sGitPath) = {}'.format(sDesPath))
                    elif(neighbor1Child.tag == 'var2'):
                        sSrcPath =  neighbor1Child.text
                        print('neighbor2Child.tag(sSrcPath) = {}'.format(sSrcPath))
                    elif(neighbor1Child.tag == 'var3'):
                        sGitWorkPath =  neighbor1Child.text
                        print('neighbor2Child.tag(sGitWorkPath) = {}'.format(sGitWorkPath))

        sDesGitPath = sDesPath
        print ('gogo  {}'.format("go"))
        #update all new version 
        bFlag = True
        bRes = False
        while (bFlag):
            if(sTestName == "CopyUSB2"):
                sVersion = "MP_Ver" + sParameter

            print ('sVersion, {}'.format(sVersion))
            sReturnFolderPath = findFolder(sSrcPath ,sVersion)
            
            if ( sReturnFolderPath == -1) or ( sReturnFolderPath == 0) :
                print ('nothing in {}'.format(sReturnFolderPath))
                bFlag = False
            else:
                # sSrcPath1 = os.path.join(sSrcPath, sReturnFileName)
                
                print ('sReturnFolderPath {}'.format(sReturnFolderPath))

                sDesGitBinPath = os.path.join(sDesGitPath, "bin")
                if os.path.exists(sDesGitBinPath):
                    print('{}", rmtree ok"'.format(sDesGitBinPath))
                    shutil.rmtree(sDesGitBinPath) 
                    
                # ignore_dirs = shutil.ignore_patterns('.txt')
                print ('copytree ok src = {}, des = {}'.format(sReturnFolderPath, sDesGitBinPath))                
                shutil.copytree(sReturnFolderPath, sDesGitBinPath, symlinks=True)
                

                
                if (runGitCommit(sDesPath, sVersion, sTestName) != 0):
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
        print("!!! except in runCopyUsb2")
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
                                                                                                               
                if ( testName == 'CopyUSB2'):
                    runCopyUsb2(xmlPath, testName, parameter)                    
                elif ( testName == 'Pause'):
                    runPause()                                                                                                       

                ListItem.insert(ListCount, testName)
                ListCount +=1

        print('\n----------------------------------------------------\n')
        nfinishList = 0 


        for finishList in ListItem:
            if (finishList.find('CopyUSB2') != -1 ):
                print('finishList[{}]:{:>25}'.format(nfinishList, finishList))

            nfinishList += 1            

        print('\n-------------------excellent you are1---------------------------------\n')
    except:
        print('parseXML except')
        return -1
    return 0


if __name__ == "__main__":

    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # xmlPath = "D:\\3S_PC\\sourceCode\\USB_20\MP\\AutoCopyCommit.xml"
    xmlPath = os.path.join(dir_path, "AutoCopyCommit.xml")

    sStartTime = datetime.datetime.now()
    print('StartTime:{} ..\n '.format(sStartTime))
    try:
        
        if(os.path.exists(xmlPath)):
            parseXML(xmlPath)
        else:
            print('path not exist:{}'.format(xmlPath))            

        sEndTime = datetime.datetime.now()        
        print('EndTime:{}, Total:{} ..'.format(sEndTime, (sEndTime-sStartTime)))        

    except:
        print('!!! exception happen in', xmlPath)

	
    sys.exit(0)