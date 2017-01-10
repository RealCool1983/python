import zipfile
import os
import shutil
import glob
import datetime
import time
import sys
from subprocess import Popen

"""
Achive_Folder_To_ZIP: 壓縮資料夾，排除git檔，上傳至網芳
removeFolder:刪除特定資料夾
removeFile:刪除特定檔案
copyTo3800:將資料夾上傳至網芳
copyRelease note:
"""
 
def Achive_Folder_To_ZIP(sFilePath, dest = "", sSequenceNumber = "0"):
    """
    input : Folder path and name
    sSequenceNumber :
    output: using zipfile to ZIP folder
    """

    datetime.datetime.now()

    sMonth = time.strftime("%m") 
    iMonth = int(sMonth)
    sYear  = time.strftime("%Y")
    sDate  = time.strftime("%d")

    
    sRemoteFileName = '{}{}.{}{}{}{}{}'.format('v1.0.', sYear, iMonth, sDate ,'_Temp', sSequenceNumber,'.zip')
    #print(sRemoteFileName)

    #sDate = time.strftime("%Y.%m%d")
    #sRemoteFileName = '{}{}{}{}{}'.format('v1.0.', sDate,'_Temp', sSequenceNumber,'.zip')

    dest = os.path.join(dest, sRemoteFileName)         

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
    os.chdir(sFilePath)

    
    #print sFilePath
    for root, folders, files in os.walk(".\\"):
        for sfile in files:
            stmp = os.path.join(root, sfile) 

            if ( '.git' in folders ):
                folders.remove('.git') 
                print("Achive_Folder_To_ZIP remove ", stmp)
            if ( 'workingTMP' in folders ):
                folders.remove('workingTMP')                 
                print("Achive_Folder_To_ZIP remove ", stmp)
            else:
                aFile = os.path.join(root, sfile)
                #print ("zipFile = ", aFile)
                #zf.write(aFile, compress_type=zipfile.ZIP_DEFLATED)
                zf.write(aFile, compress_type=zipfile.ZIP_BZIP2)

    zf.close()
    print('{}{}'.format("Achive_Folder_To_ZIP done!  ", dest))

    

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

def copyTo3800(src_file, det_file, sSequenceNumber):
    datetime.datetime.now()

    sMonth = time.strftime("%m") 
    iMonth = int(sMonth)
    sYear  = time.strftime("%Y")
    sDate  = time.strftime("%d")

    sRemoteFolderName = '{}{}.{}{}{}{}'.format('v1.0.', sYear, iMonth, sDate ,'_Temp', sSequenceNumber)

    #sDate = time.strftime("%Y.%m%d")
    #sRemoteFolderName = '{}{}{}{}'.format('v1.0.', sDate,'_Temp', sSequenceNumber)
    #print("copyTo3800 path = ", sRemoteFolderName)
    
    det_file = os.path.join(det_file, sRemoteFolderName) 
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


    #if os.path.exists(det_file):
     #   shutil.rmtree(det_file)
        
    shutil.copytree(src_file, det_file)

    print('{}{}'.format("copyTo3800 done!  ", det_file))
    #shutil.copy2(src_file, det_file)

def copyReleaseNote(src_file, det_file):        
    shutil.copy2(src_file, det_file)
    print('{}{}'.format("copyReleaseNote done!  ", det_file))



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



if __name__ == "__main__":

    sVersion = 19
	#print('{}{}'.format("1.MTable.set ", "2.MP_H16_TLC_test.ini"))
    
	
    sCleanPath = "D:\\3S_PC\sourceCode\SSD\MP_UI\source_code\GIT_MP_UI\\default"
    removeFolder(sCleanPath)

    sCleanPath = "D:\\3S_PC\\sourceCode\\SSD\\MP_UI\\source_code\\GIT_MP_UI\\default"
    removeFile(sCleanPath)


    print("execute UAC !!!")
    sUACPath = r"D:\\3S_PC\sourceCode\SSD\MP_UI\source_code\GIT_MP_UI\\default\src\UAC"
    os.chdir(sUACPath)
    os.system("uac_path.bat")

    print('{}{}{}'.format("check done!  ", sUACPath, " SSDMP.exe modify date"))


    print("compress file ?")
    sYesNo = rawInputTest()
    if ( sYesNo == 1):
        sFileServer = r"\\fileserver\Dep_AP\Project\SSD\MP_UI\source_code\v1.0"
        sSourceFile = r"D:\\3S_PC\sourceCode\SSD\MP_UI\source_code\\GIT_MP_UI\default"
        Achive_Folder_To_ZIP(sSourceFile, sFileServer, sVersion)
    elif(sYesNo == 0):
        print("skip")
    else:        
        sys.exit(0)

    
    print("copy binary file to 3800 ?")
    sYesNo = rawInputTest()
    if ( sYesNo == 1):
        sRemotePath = r"\\fileserver\3800\SW\SSD_MP_UI_EV\v1.0"
        sSrcPath = r"D:\\3S_PC\sourceCode\SSD\MP_UI\source_code\GIT_MP_UI\default\bin"
        copyTo3800(sSrcPath, sRemotePath, sVersion)
    elif(sYesNo == 0):
        print("skip")
    else:        
        sys.exit(0)


    print("copyReleaseNote ?")
    sYesNo = rawInputTest()
    if ( sYesNo == 1):
        s3800RemotePath = r"\\fileserver\3800\SW\SSD_MP_UI_EV\SSD_MP_UI_Release_Note.xls"
        sDep_APRemotePath = r"\\fileserver\Dep_AP\Project\SSD\MP_UI\source_code\SSD_MP_UI_Release_Note.xls"
        sSrcPath = r"D:\\3S_PC\sourceCode\SSD\MP_UI\source_code\GIT_MP_UI\SSD_MP_UI_Release_Note.xls"
        copyReleaseNote(sSrcPath, s3800RemotePath)
        copyReleaseNote(sSrcPath, sDep_APRemotePath)
    elif(sYesNo == 0):
        print("skip")
    else:        
        sys.exit(0)

    
    print('\n\n {} \n {} \n'.format("remember \n 1.MTable.set", "2.MP_H16_TLC_test.ini"))
    #print("check D:\3S_PC\sourceCode\SSD\MP_UI\source_code\GIT_MP_UI\default\bin\SSDMP.exe date!!!")

	
    sys.exit(0)