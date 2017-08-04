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
g_ErrorCode = 0

def showError(sMsg, iErrorCode):
    print("t")
    global g_ErrorCode
    g_ErrorCode = iErrorCode
    print('[{:<5}]showError, {} ..\n '.format(g_ErrorCode, sMsg))
    return 0

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
        sPath2 = os.path.join(sPCS3800_SSD_MPPath, "bin\\3S_SSD_MP.exe")

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
    if os.path.exists(sPath1):
        shutil.rmtree(sPath1) 
        print('{}{}'.format(sPath1, ", rmtree ok"))    
    copy_tree(sPath2, sPath1)

    global sPCS3800_SSD_MPPath
    sPCS3800_SSD_MPPath = sPath1

    print('copy_tree from [{}] to [{}] ok'.format(sPath2, sPath1))
    print('runCopySSD_MP_tool_EVEnd ..[{}]\n '.format('-'))


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



    print('runCopyFromGitEnd ..[{}]\n '.format('-'))

def runCopySSD_MP_UI(sXmlPath):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()   

    global sPC_NewMPUI_Path
    global sPC_NewMPUI_Name

    print('runCopySSD_MP_UI[{}] start ..'.format('-'))
    try:
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

    except:
        showError("!!! runCopySSD_MP_UI except", 3)

    print('runCopySSD_MP_UIEnd ..[{}]\n '.format('-'))
    return 0

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
        shutil.rmtree(det_file) 
        print('{}{}'.format(det_file, ", remove ok"))        
        # sYesNo = rawInputTest()
        # if (sYesNo == 1):
        #     shutil.rmtree(det_file) 
        #     print('{}{}'.format(det_file, ", remove ok"))
        # elif(sYesNo == 0):
        #     print("skip")
        #     sys.exit(0)
        
    shutil.copytree(src_file, det_file)
    print('runCopyToGitbin, {} end ..'.format(det_file))




def runCopyTo3800(sXmlPath):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()   

    global sPC_NewMPUI_Path
    global sPC_NewMPUI_Name
    global sRemote3800_NewMPUI_Path

    print('copyTo3800[{}] start ..'.format('-'))
    
    for neighbor in root.iter('PATHObjects'):
        sPath1 = neighbor.find('S3800_SSD_MPUIPath').text

    removeFolder(sPC_NewMPUI_Path)
    removeFile(sPC_NewMPUI_Path)

    det_file = os.path.join(sPath1, sPC_NewMPUI_Name) 
    src_file = os.path.join(sPC_NewMPUI_Path, 'bin')
    #print(det_file)

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
    sRemote3800_NewMPUI_Path = det_file

    print('copyTo3800, {} end ..'.format(det_file))


#def Achive_Folder_To_ZIP(sFilePath, dest = "", sSequenceNumber = "0"):
def runCompressFile(sXmlPath):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()   

    global sPC_NewMPUI_Path
    global sPC_NewMPUI_Name
    global sRemoteDepAp_NewMPUI_Path

    print('runCompressFile[{}] start ..'.format('-'))
    
    for neighbor in root.iter('PATHObjects'):
        sPath1 = neighbor.find('SDEPAP_SSD_MPUIPath').text

    removeFolder(sPC_NewMPUI_Path)
    removeFile(sPC_NewMPUI_Path)

    sRemoteFileName = sPC_NewMPUI_Name + '.zip'
    sRemoteFolderName = sPC_NewMPUI_Name
    

    dest = os.path.join(sPath1, sRemoteFileName) 
    if (os.path.isfile(dest)):
        print('{}{}'.format(dest, "   exist !! remove it ?"))
        sYesNo = rawInputTest()
        if (sYesNo == 1):
            os.remove(dest)
            print('{}{}'.format(dest, ", remove ok"))
        elif(sYesNo == 0):
            print("skip")
            sys.exit(0)
    else:        
        print('{}{}'.format(dest, "  do not exist"))
            
    zf = zipfile.ZipFile(dest, mode='w')
    os.chdir(sPC_NewMPUI_Path)

    
    #print sFilePath
    for root, folders, files in os.walk(".\\"):
        if ( 'Release' in folders ):
            folders.remove('Release')                 
            print("Achive_Folder_To_ZIP skip Release", folders)  
        if ( 'Debug' in folders ):
            folders.remove('Debug')                 
            print("Achive_Folder_To_ZIP skip Debug", folders)              
        if ( '.git' in folders ):
            folders.remove('.git') 
            print("Achive_Folder_To_ZIP skip .git", folders)         
        if ( 'workingTMP' in folders ):
            folders.remove('workingTMP')                 
            print("Achive_Folder_To_ZIP skip workingTMP", folders)     
        if ( 'table' in folders ):
            folders.remove('table')                 
            print("Achive_Folder_To_ZIP skip table", folders)                           

        for sfile in files:
            stmp = os.path.join(root, sfile) 

            if ('.gitignore' in files):              
                files.remove('.gitignore')                 
                print("Achive_Folder_To_ZIP skip .gitignore", stmp)            
            elif ('reference.txt' in files):              
                files.remove('reference.txt')                 
                print("Achive_Folder_To_ZIP skip ", stmp)                                                    
            # elif ('ChangeList.txt' in files):              
            #     files.remove('ChangeList.txt')                 
            #     print("Achive_Folder_To_ZIP skikp ChangeList.txt", stmp)                                                                    
            else:
                aFile = os.path.join(root, sfile)
                sTmpPath = os.path.join(sRemoteFolderName, aFile)
                
                #zf.write(aFile, compress_type=zipfile.ZIP_DEFLATED)
                print('runCompressFile add [{}] '.format(aFile))
                zf.write(aFile, sTmpPath, compress_type=zipfile.ZIP_BZIP2)

    zf.close()
    sRemoteDepAp_NewMPUI_Path = dest

    #backup to pc release

    sPathPC = os.path.abspath(os.path.join(sPC_NewMPUI_Path, os.pardir))
    sPathPC = os.path.join(sPathPC, "SourceCode")
    print('backup to pc, {}'.format(sPathPC))
    copyOneFile(sRemoteDepAp_NewMPUI_Path, sPathPC)

    print('runCompressFileEnd ..[{}]\n '.format(dest))

def updateIniMPToMP_UI(sFile):
    print('updateIniMPToMP_UI Start sPath = {}'.format(sFile))

    try:
        rF = open(sFile, 'r') 

        for line in rF.readlines():                          #依次读取每行  
            line = line.strip()                             #去掉每行头尾空白  
            if not len(line) or line.startswith('#'):       #判断是否是空行或注释行  
                continue 
            if(line.find("Burner") != -1):#get Burner, need to update 
                sNewLine = line.replace("./", ".\\Setting\\")
                rF.close()
                replaceLine(sFile, line, sNewLine)
                print('replaceLine ok path:{}\n old:{}\n new:{}'.format(sFile, line, sNewLine))

            if(line.find("Recv_Drv_Num_By_UI") != -1):#get Recv_Drv_Num_By_UI, need to update 
                rF.close()
                sNewLine = "Recv_Drv_Num_By_UI=1"
                replaceLine(sFile, line, sNewLine)
                print('replaceLine ok path:{}\n old:{}\n new:{}'.format(sFile, line, sNewLine))

    except:
        print('updateIniMPToMP_UI except')

    print('updateIniMPToMP_UI End ..[{}]\n '.format("-"))
    return 0

def copyIniFile(sSrcPath, sDesPath, sIniEndingName):
    print('copyIniFile Start sSrcPath = {}\nsDesPath = {}\nsIniEndingName = {}'.format(sSrcPath, sDesPath, sIniEndingName))
    try:
        # sDesPath = os.path.join(sDesPath, 'bin\Setting')
        for file in os.listdir(sSrcPath):
            # if file.endswith('TLC_test.ini') or file.endswith('BiCS3_test.ini'):
            if file.endswith(sIniEndingName):
                sFromPath = os.path.join(sSrcPath, file)
                print('GetIt, {}, {} '.format(file, sFromPath))
                
                sToPath = os.path.join(sDesPath, file)

                if os.path.exists(sToPath): # remove old file 
                    print('remove file, {}'.format(sToPath))    
                    os.remove(sToPath) 
                copyOneFile(sFromPath, sDesPath)                       
                updateIniMPToMP_UI(sToPath)
    except:
        showError('!!! except copyIniFile', 4)                        

    print('copyIniFile End ..[{}]\n '.format("-"))
    return 0

def addNewIniSection(sSrcPath, sDesPath, sIniFileType):
    print('addNewIniSection Start sSrcPath = {}\nsDesPath = {}'.format(sSrcPath, sDesPath))
    try:
        for file in os.listdir(sDesPath):
            if file.endswith(sIniFileType):
                sToPath = os.path.join(sDesPath, file)
                print('GetIt, {}, {} '.format(file, sToPath))


                if os.path.exists(sToPath): # remove old file 
                    with open(sToPath, 'a') as outfile:
                        for line in open( sSrcPath, 'r' ):
                            outfile.write(line)
                    outfile.close()
                    print('insert ini section done, {}'.format(sToPath))
    except:
        showError('!!! except addNewIniSection', 11)                        

    print('addNewIniSection End ..[{}]\n '.format("-"))
    return 0


def runHUATOOP(sXmlPath, sH14H16):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()   

    global sPC_NewMPUI_Path
    global sPCS3800_SSD_MPPath

    print('runHUATOOP[{}] start ..'.format(sH14H16))

    try:
        dict_Var = {'var1': '0', 'var2': '0', 'var3': '0', 'var4': '0', 'var5': '0'}

        sPC_NewMPUI_Setting_Path = os.path.join(sPC_NewMPUI_Path, "bin\Setting")

        sFlashType = "[Hynix]"
        if (sH14H16.find("14") != -1):
            sPCS3800_SSD_MP_SettingPath = os.path.join(sPCS3800_SSD_MPPath, "package\windows\H14_TLC\HUATOOP")
        elif (sH14H16.find("16") != -1) and (sH14H16.find("B16A") == -1):
            sPCS3800_SSD_MP_SettingPath = os.path.join(sPCS3800_SSD_MPPath, "package\windows\H16_TLC\HUATOOP")
        elif (sH14H16.find("B0KB") != -1):
            sPCS3800_SSD_MP_SettingPath = os.path.join(sPCS3800_SSD_MPPath, "package\windows\Micron_B0KB")        
            sFlashType = "[Micron]"
        elif (sH14H16.find("B16A") != -1):
            sPCS3800_SSD_MP_SettingPath = os.path.join(sPCS3800_SSD_MPPath, "package\windows\Micron_B16A")     
            sFlashType = "[Micron]"
        elif (sH14H16.find("BiCS3") != -1):
            sPCS3800_SSD_MP_SettingPath = os.path.join(sPCS3800_SSD_MPPath, "package\windows\TSB_BICS")     
            sFlashType = "[Toshiba]" 
        elif (sH14H16.find("T15") != -1):
            sPCS3800_SSD_MP_SettingPath = os.path.join(sPCS3800_SSD_MPPath, "package\windows\T15_TLC")     
            sFlashType = "[Toshiba]"             
        #copy new setting file
        # copyIniFile(sPCS3800_SSD_MP_SettingPath, sPC_NewMPUI_Setting_Path)
        #rewrite setting file

        print('runHUATOOP sPC_NewMPUI_Setting_Path = {}'.format(sPC_NewMPUI_Setting_Path))
        print('runHUATOOP sPCS3800_SSD_MP_SettingPath = {}'.format(sPCS3800_SSD_MP_SettingPath))
        sIniFileName = "NULL"

        for neighbor in tree.iter('ProcessObject'):
            if ( neighbor.get('Name')  == sH14H16):
                for neighborChild in neighbor:
                    dict_Var[neighborChild.tag] = neighborChild.text

                    #------------from MP to MP_UI ------------------------------------#
                    print('compareStart .. [{}] '.format(neighborChild.text))

                    #var4 for another reserve
                    if (neighborChild.tag != "var4"):
                        if (neighborChild.tag == "var1"): #get ini file name 
                            #copy new setting file
                            copyIniFile(sPCS3800_SSD_MP_SettingPath, sPC_NewMPUI_Setting_Path, neighborChild.get('IniFile'))
                            #rewrite setting file                        
                            sIniFileName =  "MP_" + neighborChild.get('IniFile')
                    #sBinName = neighborChild.get('Name') + "_" + neighborChild.text + ".bin"
                        sBinName = neighborChild.get('Name') + neighborChild.text + ".bin"
                        print ('get binName = ', sBinName )

                        if (neighborChild.get('IniFile') == "MTable.set"):
                            # updateMTable(sPC_NewMPUI_Setting_Path, neighborChild.get('IniFile') , neighborChild.get('IniSection'), sBinName, sH14H16 )
                            updateMTable_Ex(sPC_NewMPUI_Setting_Path, neighborChild.get('IniFile') , neighborChild.get('IniSection'), sH14H16, sBinName, sFlashType)
                            
                        else:
                            updateIni(sPC_NewMPUI_Setting_Path, neighborChild.get('IniFile') , neighborChild.get('IniSection'), sBinName, sH14H16 )                    

                        if (findFile(sPCS3800_SSD_MP_SettingPath, sBinName) == 0):
                            print('Get it in [{}] '.format(sPCS3800_SSD_MP_SettingPath))

                            if (findFile(sPC_NewMPUI_Setting_Path ,neighborChild.text) == -1):
                                print ("nothing in sPC_NewMPUI_Setting_Path, copy to")
                                
                                sFromPath = os.path.join(sPCS3800_SSD_MP_SettingPath, sBinName)
                                
                                copyOneFile(sFromPath, sPC_NewMPUI_Setting_Path)
                                #modify setting file 
                            else:
                                print ("already in sPC_NewMPUI_Setting_Path")

                            #remove old file in MP_UI
                            removeDiffFile(sPC_NewMPUI_Setting_Path, neighborChild.get('Name') ,sBinName)
  
                    if(neighborChild.tag == "var4"):
                        print('dict_Var[neighborChild.tag] = {} ..\n '.format(dict_Var[neighborChild.tag]))
                        print('Function = {}, dict_Var4 value =  {}\n '.format(sH14H16, dict_Var['var4']))
                        if( dict_Var['var4'] == 'TRUE'):
                            sInitFullPath = os.path.join(sPC_NewMPUI_Setting_Path, sIniFileName)
                            print('prepare Insert,{},{},{}\n '.format(sInitFullPath, sPC_NewMPUI_Setting_Path, sIniFileName))
                            addNewIniSection("D:\\3S_PC\\python\\3S_AUTO\\newSecton.txt" ,sPC_NewMPUI_Setting_Path, sIniFileName)
                            print('Insert, {}\n '.format(sInitFullPath))


                    #------------Compare MP_UI with MP, delete ------------------------------------#

                    # ok
                    # print ('neighborChild = ', neighborChild)
                    # print ('tag = ', neighborChild.tag)
                    # print ('text = ', neighborChild.text)
                    # print ('attrib = ', neighborChild.attrib)
                    #print ('get = ', neighborChild.get('Editable') )

                print('dict_Var', dict_Var)
        
    except:
        showError("!!!except runHUATOOP ", 5)
    print('runHUATOOPEnd ..[{}]\n '.format(sH14H16))

def updateMTable_Ex(sPath, sIniFile, sIniSection, sH14H16, sFileName, sFlashType):
    #<var1 Name="3S_HNX_14TLC_BNR" IniFile="H14_TLC_test.ini" IniSection="Firmware_Bin_File_Path">3.2.0.51</var1>
    #1.update MTable.set
    print('updateMTable_Ex .. [{}] '.format("-"))
    try:
        for file in os.listdir(sPath):
            #if file.startswith(sFileType):
                #print('GetIt startswith= [{}]'.format(file))
            if (file.find(sIniFile) != -1): 
                print('updateMTable_Ex sIniFile: {}, sIniSection: {}, sFlashType:{}, file:{}, secction:{}'.format(sIniFile, sIniSection, sFlashType, file, sH14H16 ))
                bModifySection = False
                sReadPath1 = os.path.join(sPath, file)

                rF = open(sReadPath1, 'r') 
        
                for line in rF.readlines():                          #依次读取每行  
                    line = line.strip()                             #去掉每行头尾空白  
                    if not len(line) or line.startswith('#'):       #判断是否是空行或注释行  
                        continue 
                    # if(line.find("sFlashType") != -1) and (bModifySection == False):              #get sFlashType section, or skip
                    if(line.find(sFlashType) == -1) and (bModifySection == False):              #get sFlashType section, or skip
                        # print('skip, line:{}'.format(line))
                        continue
                    else:
                        bModifySection = True #get the section
                        # print('updateMTable_Ex sFlashType:{}, read line:{}'.format(sFlashType, line))

                    if(line.find(sFlashType) == -1):
                        if(line.find("[") != -1) and ("]" != -1): # new section start
                            bModifySection = False; # start new section
                            # print('updateMTable_Ex new line:{}'.format(line))
                            break

                            
                    if  (line.find(sIniSection) != -1): #need to replace this line with new setting file 
                        sNewLine = sIniSection + sFileName
                        rF.close()
                        if (line != sNewLine):
                            replaceLine(sReadPath1, line, sNewLine)
                            print('updateMTable_Ex replaceLine ok path:{}\n old:{}\n new:{}'.format(sReadPath1, line, sNewLine))

                rF.close()
    except:
        showError("!!!except updateMTable_Ex", 6)

    print('updateMTable_Ex End {}..\n '.format("-"))    

def updateMTable(sPath, sIniFile, sIniSection, sFileName, sH14H16):
    #<var1 Name="3S_HNX_14TLC_BNR" IniFile="H14_TLC_test.ini" IniSection="Firmware_Bin_File_Path">3.2.0.51</var1>
    #1.update MTable.set
    print('updateMTableStart .. [{}] '.format("-"))
    try:
        for file in os.listdir(sPath):
            #if file.startswith(sFileType):
                #print('GetIt startswith= [{}]'.format(file))
            if (file.find(sIniFile) != -1): 
                print('updateMTable sIniFile: {}, sIniSection: {}, file:{}, secction:{}'.format(sIniFile, sIniSection, file, sH14H16))
                bMicronSection = False
                sReadPath1 = os.path.join(sPath, file)

                rF = open(sReadPath1, 'r') 
        
                for line in rF.readlines():                          #依次读取每行  
                    line = line.strip()                             #去掉每行头尾空白  
                    if not len(line) or line.startswith('#'):       #判断是否是空行或注释行  
                        continue 
                    if(sH14H16.find("H14") != -1) or (sH14H16.find("H16") != -1):#[Hynix] section
                        if(line.find("[Micron]") != -1):#get [Micron] section, break;
                            break
                    elif(sH14H16.find("B0KB") != -1) or (sH14H16.find("B16A") != -1) :#[Micron] section
                        # print('B0KB, B16A, section:{}'.format(sH14H16))
                        if(line.find("Micron") == -1) and (bMicronSection == False): # not get [Micron] section, continue
                            continue
                        else:
                            # print('get [Micron] section:{}'.format(line))
                            bMicronSection = True # get [Micron] section, set true
                            
                    if  (line.find(sIniSection) != -1): #need to replace this line with new setting file 
                        sNewLine = sIniSection + sFileName
                        rF.close()
                        if (line != sNewLine):
                            replaceLine(sReadPath1, line, sNewLine)
                            print('updateMTable replaceLine ok path:{}\n old:{}\n new:{}'.format(sReadPath1, line, sNewLine))

                rF.close()
    except:
        showError("!!!except updateMTable", 7)

    print('updateMTable End {}..\n '.format("-"))    


def updateIni(sPath, sIniFile, sIniSection, sFileName, sH14H16):
    #<var1 Name="3S_HNX_14TLC_BNR" IniFile="H14_TLC_test.ini" IniSection="Firmware_Bin_File_Path">3.2.0.51</var1>
    #1.update ini
    print('updateIniStart .. [{}] '.format("-"))
    try:
        for file in os.listdir(sPath):
            #if file.startswith(sFileType):
                #print('GetIt startswith= [{}]'.format(file))
            if (file.find(sIniFile) != -1): 
                print('updateIni sIniFile: {}, sIniSection: {}, file:{}, secction:{}'.format(sIniFile, sIniSection, file, sH14H16))
                bMicronSection = False
                sReadPath1 = os.path.join(sPath, file)
                #print("updateIni path = ", sReadPath1)
                rF = open(sReadPath1, 'r') 
        
                for line in rF.readlines():                          #依次读取每行  
                    line = line.strip()                             #去掉每行头尾空白  
                    if not len(line) or line.startswith('#'):       #判断是否是空行或注释行  
                        continue 
                            
                    if  (line.find(sIniSection) != -1): #need to replace this line with new setting file 
                        sNewLine = sIniSection + sFileName

                        rF.close()
                        if (line != sNewLine):
                            replaceLine(sReadPath1, line, sNewLine)
                            print('updateIni replaceLine ok path:{}\n old:{}\n new:{}'.format(sReadPath1, line, sNewLine))

                rF.close()
    except:
        showError("!!!except updateIni End ..", 8)        

    print('updateIni End ..[{}]\n '.format("-"))    



def runReleaseNote(sXmlPath):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()   

    global sPC_NewMPUI_Path
    #global sToolVersion

    print('runReleaseNote[{}] start ..'.format('-'))
    
    for neighbor in root.iter('PATHObjects'):
        sPath1 = neighbor.find('S3800_SSD_MPUIPath').text
        sPath2 = neighbor.find('SDEPAP_SSD_MPUIPath').text
        sPath3 = neighbor.find('PCSourceCodePath').text
        
    # sPath1 = (os.path.abspath(os.path.join(sPath1, os.pardir)))
    # sPath2 = (os.path.abspath(os.path.join(sPath2, os.pardir)))
    sPath3 = (os.path.abspath(os.path.join(sPath3, os.pardir)))

    sTmp = ('Release_Note\SSD_MP_UI_Release_Note_{}.xls'.format(sPC_NewMPUI_Name))
    sPath4 = os.path.join(sPath3, sTmp)
    sPath3 = os.path.join(sPath3, 'Release_Note\SSD_MP_UI_Release_Note.xls')
    
    print('sPath1:{:>20}'.format(sPath1))
    print('sPath2:{:>20}'.format(sPath2))
    print('sPath3:{:>20}'.format(sPath3))
    print('sPath4:{:>20}'.format(sPath4))

    if os.path.exists(sPath3):
        if os.path.exists(sPath4):
            os.remove(sPath4)
            print('remove {} ok'.format(sPath4))   
        # if os.path.exists(sPath1):
        #     os.remove(sPath1)
        #     print('remove {} ok'.format(sPath1))
        # if os.path.exists(sPath2):     
        #     os.remove(sPath2)
        #     print('remove {} ok'.format(sPath2))

        #pc backup
        #copy to 3800
        #copy to DEPAP
        copyOneFile(sPath3, sPath4) 
        copyOneFile(sPath3, sPath1)        
        copyOneFile(sPath3, sPath2)   

    print('runReleaseNoteEnd ..[{}]\n'.format('-'))


def runVCVersion(sXmlPath):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()   

    global sPC_NewMPUI_Path
    global sToolVersion

    print('runVCVersion[{}] start ..'.format('-'))
    
    for neighbor in root.iter('PATHObjects'):
        sToolVersion = neighbor.find('ToolVersion').text

    sPath = os.path.join(sPC_NewMPUI_Path, 'src\SSDMP.rc')
    print(sPath)

    ##################################################
    # FILEVERSION 1,0,2017,103           
    #VALUE "FileVersion", "1, 0, 2017, 103\0"

    sV1 = " FILEVERSION 1,x,2017,xxx\n"
    sV2 = "            VALUE \"FileVersion\", \"1, x, 2017, xxx\\0\"\n"

    datetime.datetime.now()
    sMonth = time.strftime("%m") 
    iMonth = int(sMonth)
    sDate  = time.strftime("%d")

    sDateName = '{}{}'.format(sMonth, sDate)
    
    sV1 = sV1.replace('xxx', sDateName)
    sV1 = sV1.replace('x', sToolVersion)
    sV2 = sV2.replace("xxx", sDateName)
    sV2 = sV2.replace("x", sToolVersion)
    ##################################################
    

    rF = open(sPath, 'r') 
    for line in rF.readlines():                          #依次读取每行  
        if  (line.find('FILEVERSION') != -1): #need to replace this line with new setting file 
            rF.close()         
            replaceLine(sPath, line, sV1)            

        if  (line.find('FileVersion') != -1): #need to replace this line with new setting file 
            rF.close()        
            replaceLine(sPath, line, sV2)            
             
    rF.close()

    print('runVCVersion End ..[{}]\n '.format("-"))    

def runVERIFY_INI(sXmlPath):
    print('runVERIFY_INI[{}] start ..'.format('-'))

    tree = ET.parse(sXmlPath)
    root = tree.getroot()   

    global sPC_NewMPUI_Path
    sPath = os.path.join(sPC_NewMPUI_Path, "bin\Setting")

    print('sPath = {} ..'.format(sPath))

    for file in os.listdir(sPath):
        if (file.find(".ini") != -1): 
            # print('Got Ini file:{}'.format(file))

            sReadPath1 = os.path.join(sPath, file)
            print('Start Check Ini file:{}'.format(sReadPath1))
            
            rF = open(sReadPath1, 'r') 
    
            for line in rF.readlines():                          #依次读取每行  
                line = line.strip()                             #去掉每行头尾空白  
                if not len(line) or line.startswith('#'):       #判断是否是空行或注释行  
                    continue      

                #need to check path start with, Burner=.\Setting\
                if  (line.find("Burner=") != -1): 
                    if  (line.find("Burner=.\Setting") == -1): #need to check path start with, Burner=.\Setting\
                        # print('!!! Err Ini name:{}, Burner:{}'.format(file, line))
                        sMsg = '!!! Err Ini name:{}, Burner:{}'.format(file, line)
                        showError(sMsg, 9)
                #need to check Recv_Drv_Num_By_UI=1
                if  (line.find("Recv_Drv_Num_By_UI=") != -1): 
                    if  (line.find("=1") == -1): #need to check path start with, Burner=.\Setting\
                        # print('!!! Err Ini name:{}, Recv_Drv_Num_By_UI:{}'.format(file, line))            
                        sMsg = '!!! Err Ini name:{}, Recv_Drv_Num_By_UI:{}'.format(file, line)            
                        showError(sMsg, 10)

            rF.close()
    print('runVERIFY_INIEnd ..[{}]'.format('-'))


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
            iSize = os.path.getsize(filePath)
            tupleFileInfo = (relativefilePath, fileTimeInfo, iSize) #save file name , path into tuple
            listFileInfo.append(tupleFileInfo)  # Add it to the list.            
            # print('fileName = {}\n path1 = {},\n path2 = {} '.format(fileName, relativefilePath, fileTimeInfo))
    print('{:<10s}buildFileDateInfo  ..'.format('End'))
    return listFileInfo

def extraZip(sSrcFolder, sSrcFile):
    print('extraZip[{}] start ..'.format('-'))
    try:

        sSrcPath = os.path.join(sSrcFolder, sSrcFile) 
        if os.path.exists(sSrcPath):
            print('{}{}'.format(sSrcPath, ", exist ok"))

            # check destination folder, if exist, rmtree
            sDesFolder = os.path.splitext(sSrcFile)[0] #reduce Filename Extension
            sDesPath = os.path.join(sSrcFolder, sDesFolder) 
            print('sDesPath: {}'.format(sDesPath))
            if os.path.exists(sDesPath):
                print('{}{}'.format(sDesPath, ", exist prepare to rmtree"))                                    
                shutil.rmtree(sDesPath) 
                print('{}", rmtree ok"'.format(sDesPath))

            zf = zipfile.ZipFile(sSrcPath)
            print('{}{}'.format(sSrcPath, ", ready to Extract "))        
            zf.extractall(path=sSrcFolder, members=None, pwd=None)
            zf.close()
            print('{}{}'.format(sSrcPath, ", Extract done"))        

            # check extrat folder 
            if os.path.exists(sDesPath):
                print('check folder ok, {}'.format(sDesPath, ))                                    
            else:
                showError("!!!check folder fail, in extraZip", 2)
            
    except:
        showError("!!!except in extraZip", 1)

    print('extraZip[{}] end ..'.format('-'))

    return 0

def runCheckSourceCode(sXmlPath):   

    print('runCheckSourceCode[{}] start ..'.format('-'))

    try:
        tree = ET.parse(sXmlPath)
        root = tree.getroot()   

        for neighbor in root.iter('PATHObjects'):
            sPath1 = neighbor.find('pythonWorkingPath').text
            # get D:\3S_PC\ReleaseTool\MP_UI_V1.0\SourceCode
            sPath2 = os.path.abspath(os.path.join(sPath1, os.pardir))
            sPath2 = os.path.join(sPath2, "SourceCode") 
            sToolVersion = neighbor.find('ToolVersion').text
            iCurrentVer = int(sToolVersion)
            iPreVer = iCurrentVer -1

            sCurrentZipName = 'V1.{}'.format(iCurrentVer) 
            sPreZipName = 'V1.{}'.format(iPreVer) 



        # find last version zip
        for file in os.listdir(sPath2):
            # if start with "V1.33"(current )
            if file.startswith(sCurrentZipName) and file.endswith('.zip'):            
                print('get file: {}, path: {}'.format(file, sPath2))
                if (extraZip(sPath2, file) == 0):
                    sDesFolder = os.path.splitext(file)[0] #reduce Filename Extension
                    sSrcPathCurrent = os.path.join(sPath2, sDesFolder) 
                    listInfoCurrnetFile = buildFileDateInfo(sSrcPathCurrent)

            # if start with "V1.33"(Pre)
            if file.startswith(sPreZipName) and file.endswith('.zip'):            
                print('get file: {}, path: {}'.format(file, sPath2))
                if (extraZip(sPath2, file) == 0):
                    sDesFolder = os.path.splitext(file)[0] #reduce Filename Extension
                    sSrcPathPre = os.path.join(sPath2, sDesFolder) 
                    listInfoPreFile = buildFileDateInfo(sSrcPathPre)

                    # iPreFileInfoSize = len(listInfoPreFile)
        iCurrnetFileInfoSize = len(listInfoCurrnetFile)
        iPreFileInfoSize = len(listInfoPreFile)
        print('iCurrnetFileInfoSize = {} iPreFileInfoSize = {} \n'.format(iCurrnetFileInfoSize, iPreFileInfoSize))    

        # check new file(extra file)
        iIndex = 0
        
        for x, y, z in listInfoCurrnetFile:
            bNeedToShow = False
            bExistFile = 0
            for x1, y1, z1 in listInfoPreFile:
                if (x == x1 ):
                    bExistFile = 1
                    # check file date
                    sMsg1 = '-'
                    sMsg2 = '-'
                    if(y != y1):
                        bNeedToShow = True
                        sMsg1 = 'NewDate= {}({})'.format(y, y1)
                        # print('[{}]NewFileDate = {}, date = {},{}'.format(iIndex, x, y, y1))         
                    # check file size
                    if(z != z1):
                        bNeedToShow = True
                        sMsg2 = 'NewSize= {}'.format(z)
                        # print('[{}]NewSize = {:<50}, size = {},{}'.format(iIndex, x, z, z1))                             
                    if(bNeedToShow):
                        iIndex += 1
                        print('[{}]File = {:<50}{:<20}{:<70}'.format(iIndex, x, sMsg2, sMsg1))                             

            if (bExistFile == 0): # extra File, need remove
                print('[{}]NewFile = {:<50}'.format(iIndex, x))    
                iIndex += 1

    except:
        showError("!!!except in runCheckSourceCode", 3)

    print('\nrunCheckSourceCode[{}] End ..\n '.format('-'))
    return 0


def replaceLine(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with open(abs_path,'w') as new_file:  
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    close(fh)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)


def removeDiffFile(sPath, sFileType, sFileName):
    #print('removeDiffFileStart .. [{}] '.format("-"))
    for file in os.listdir(sPath):
        if file.startswith(sFileType):
            #print('GetIt startswith= [{}]'.format(file))
            if (file.find(sFileName) == -1): 
                sRmPath = os.path.join(sPath, file)
                print('ready to remove = name:[{}], path:[{}]'.format(file, sRmPath))
                os.remove(sRmPath)
    #print('removeDiffFile End ..[{}]\n '.format("-"))



def findFile(sPath, sFileName):
    print('findFile Start sPath = {}, name = {}'.format(sPath, sFileName))
    for file in os.listdir(sPath):
        if file.startswith(sFileName):
            print('GetIt = [{}] '.format(file))
            return 0
    print('findFile End ..[{}]\n '.format("-"))
    return -1

def runPause():
    print('runPause {} {}'.format("-", "-"))
    sYesNo = rawInputTest()
    if (sYesNo == 1):
        print('{}{}'.format(sYesNo, "-"))
    elif(sYesNo == 0):
        print("skip")
        sys.exit(0)
    print('EndPause {} {}'.format("-", "-"))        
    



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


def parseXML(sXmlPath):
    global g_ErrorCode
    xmlPath = r"D:\\3S_PC\\python\\3S_AUTO\\MP_UI.xml"

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
            if ( testName == 'CopyFromGit'):
                runCopyFromGit(xmlPath)                                                                 
            if ( testName == 'Bin2HexMPExe'):                
                B2HEX_MP(xmlPath)
            if ( testName == 'Bin2HexKEYDLL'):
                B2HEX_KEYPRO(xmlPath)     
            if ( testName == 'VC6AutoBuild'):
                runVC6AutoBuild(xmlPath)     
            if ( testName == 'UacBat'):
                runUacBat(xmlPath)                     
            if ( testName == 'HUATOOP_H14'):
                runHUATOOP(xmlPath, 'HUATOOP_H14')                                     
            if ( testName == 'HUATOOP_H16'):
                runHUATOOP(xmlPath, 'HUATOOP_H16')                                                     
            if ( testName == 'HUATOOP_H16_2LUN'):
                runHUATOOP(xmlPath, 'HUATOOP_H16_2LUN')   
            if ( testName == 'B0KB'):
                runHUATOOP(xmlPath, 'B0KB')   
            if ( testName == 'B16A'):
                runHUATOOP(xmlPath, 'B16A')   
            if ( testName == 'BiCS3'):
                runHUATOOP(xmlPath, 'BiCS3')     
            if ( testName == 'TSB'):
                runHUATOOP(xmlPath, 'TSB')                                
            if ( testName == 'VERIFY_INI'):
                runVERIFY_INI(xmlPath)                                  
                
            if ( testName == 'CopySSD_MP_tool_EV'):
                runCopySSD_MP_tool_EV(xmlPath)                                                     
            if ( testName == 'CopySSD_MP_UI'):
                runCopySSD_MP_UI(xmlPath)                                                                     
            if ( testName == 'CopyTo3800'):
                runCopyTo3800(xmlPath)
            if ( testName == 'CopyToGitbin'):
                runCopyToGitbin(xmlPath)                
            if ( testName == 'CompressFile'):
                runCompressFile(xmlPath)                
            if ( testName == 'VCVersion'):
                runVCVersion(xmlPath)                                
            if ( testName == 'ReleaseNote'):
                runReleaseNote(xmlPath)    
            if ( testName == 'CheckSourceCode'):        
                runCheckSourceCode(xmlPath)
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
        
    print("ErrorCode:{}".format(g_ErrorCode))
    print('\n-------------------excellent you are---------------------------------\n')

    return 0


if __name__ == "__main__":

    xmlPath = r"D:\\3S_PC\\python\\3S_AUTO\\MP_UI.xml"
    cmd = "D:\\3S_PC\sourceCode\SSD\VS2008\BIN2HEX\Release\BIN2HEX.exe D:\\3S_PC\\sourceCode\\SSD\\VS2008\\BIN2HEX\\Debug\\3S_SSD_MP.exe D:\\3S_PC\\sourceCode\\SSD\\VS2008\\BIN2HEX\\Release\\3S_SSD_MP.hex"

    sStartTime = datetime.datetime.now()
    print('StartTime:{} ..\n '.format(sStartTime))
    try:
        #ok
        #B2HEX_MP(xmlPath)
        #B2HEX_KEYPRO(xmlPath)

        parseXML(xmlPath)

        sEndTime = datetime.datetime.now()        
        print('EndTime:{}, Total:{} ..'.format(sEndTime, (sEndTime-sStartTime)))        

        #tree.write(data,"UTF-8")
    except:
        print('!!! exception happen in', xmlPath)


	
    sys.exit(0)