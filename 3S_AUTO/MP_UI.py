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

    print('runCompressFile[{}] End ..\n '.format(dest))


def runHUATOOP(sXmlPath, sH14H16):
    tree = ET.parse(sXmlPath)
    root = tree.getroot()   

    global sPC_NewMPUI_Path
    global sPCS3800_SSD_MPPath

    print('runHUATOOP[{}] start ..'.format(sH14H16))

    dict_Var = {'var1': '0', 'var2': '0', 'var3': '0', 'var4': '0', 'var5': '0'}

    sPC_NewMPUI_Setting_Path = os.path.join(sPC_NewMPUI_Path, "bin\Setting")

    if (sH14H16.find("14") != -1):
        sPCS3800_SSD_MP_SettingPath = os.path.join(sPCS3800_SSD_MPPath, "windows\HUATOOP\H14_TLC")
    elif (sH14H16.find("16") != -1) and (sH14H16.find("B16A") == -1):
        sPCS3800_SSD_MP_SettingPath = os.path.join(sPCS3800_SSD_MPPath, "windows\HUATOOP\H16_TLC")
    elif (sH14H16.find("B0KB") != -1):
        sPCS3800_SSD_MP_SettingPath = os.path.join(sPCS3800_SSD_MPPath, "windows\Micron_B0KB")        
    elif (sH14H16.find("B16A") != -1):
        sPCS3800_SSD_MP_SettingPath = os.path.join(sPCS3800_SSD_MPPath, "windows\Micron_B16A")     
    
    print(sPC_NewMPUI_Setting_Path)
    print(sPCS3800_SSD_MP_SettingPath)

    for neighbor in tree.iter('ProcessObject'):
        if ( neighbor.get('Name')  == sH14H16):
            for neighborChild in neighbor:
                dict_Var[neighborChild.tag] = neighborChild.text

                #------------from MP to MP_UI ------------------------------------#
                print('compare [{}] start ..'.format(neighborChild.text))

                #sBinName = neighborChild.get('Name') + "_" + neighborChild.text + ".bin"
                sBinName = neighborChild.get('Name') + neighborChild.text + ".bin"
                print ('get binName = ', sBinName )

                #return 0

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

                    #if (neighborChild.get('IniFile') == 'MTable.set'):
                    updateIni(sPC_NewMPUI_Setting_Path, neighborChild.get('IniFile') , neighborChild.get('IniSection'), sBinName, sH14H16 )
                #------------Compare MP_UI with MP, delete ------------------------------------#

                # ok
                # print ('neighborChild = ', neighborChild)
                # print ('tag = ', neighborChild.tag)
                # print ('text = ', neighborChild.text)
                # print ('attrib = ', neighborChild.attrib)
                #print ('get = ', neighborChild.get('Editable') )

            print('dict_Var', dict_Var)
        

    print('runHUATOOP[{}] End ..\n '.format(sH14H16))



def updateIni(sPath, sIniFile, sIniSection, sFileName, sH14H16):
    #<var1 Name="3S_HNX_14TLC_BNR" IniFile="H14_TLC_test.ini" IniSection="Firmware_Bin_File_Path">3.2.0.51</var1>
    #1.update MTable.set
    #2.update ini
    print('updateIni [{}] Start ..'.format("-"))

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
                if(sH14H16.find("14") != -1) or (sH14H16.find("16") != -1):#[Hynix] section
                    if(line.find("[Micron]") != -1):#get [Micron] section, break;
                        break
                 
                if(sH14H16.find("B0KB") != -1) or (sH14H16.find("B16KB") != -1) :#[Micron] section
                    if(line.find("[Micron]") == -1) and (bMicronSection == False): # not get [Micron] section, continue
                        continue
                    else:
                        #print('get [Micron] section:{}'.format(line))
                        bMicronSection = True # get [Micron] section, set true
                        
                if  (line.find(sIniSection) != -1): #need to replace this line with new setting file 
                    sNewLine = sIniSection + sFileName
                    # print("sReadPath1 =", sReadPath1 )
                    # print("oldLine = ", line)
                    # print("sNewLine = ", sNewLine)
                    rF.close()
                    if (line != sNewLine):
                        replaceLine(sReadPath1, line, sNewLine)
                        print('replaceLine ok path:{}\n old:{}\n new:{}'.format(sReadPath1, line, sNewLine))

            rF.close()

    print('updateIni [{}] End ..\n '.format("-"))    



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

    print('runReleaseNote[{}] End ..\n'.format('-'))


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

    print('runVCVersion [{}] End ..\n '.format("-"))    

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
                        print('Err!!! Ini name:{}, Burner:{}'.format(file, line))

                #need to check Recv_Drv_Num_By_UI=1
                if  (line.find("Recv_Drv_Num_By_UI=") != -1): 
                    if  (line.find("=1") == -1): #need to check path start with, Burner=.\Setting\
                        print('Err!!! Ini name:{}, Recv_Drv_Num_By_UI:{}'.format(file, line))            

            rF.close()
    print('runVERIFY_INI[{}] end ..'.format('-'))


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
    #print('removeDiffFile [{}] Start ..'.format("-"))
    for file in os.listdir(sPath):
        if file.startswith(sFileType):
            #print('GetIt startswith= [{}]'.format(file))
            if (file.find(sFileName) == -1): 
                sRmPath = os.path.join(sPath, file)
                print('ready to remove = name:[{}], path:[{}]'.format(file, sRmPath))
                os.remove(sRmPath)
    #print('removeDiffFile [{}] End ..\n '.format("-"))



def findFile(sPath, sFileName):
    print('findFile Start sPath = {}, name = {}'.format(sPath, sFileName))
    for file in os.listdir(sPath):
        if file.startswith(sFileName):
            print('GetIt = [{}] '.format(file))
            return 0
    print('findFile [{}] End ..\n '.format("-"))
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