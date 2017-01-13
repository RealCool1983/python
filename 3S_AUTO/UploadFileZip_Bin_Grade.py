import zipfile
import os
import shutil
import glob
import datetime
import time
import sys
from subprocess import Popen
from shutil import copyfile

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


    sRemoteFileName = '{}.{}.{}.{}{}{}'.format('1', sSequenceNumber, sYear, iMonth, sDate ,'.zip')
    sRemoteFolderName = '{}.{}.{}.{}{}'.format('1', sSequenceNumber, sYear, iMonth, sDate )

    dest = os.path.join(dest, sRemoteFileName)         
    #dest = os.path.join(dest, sRemoteFolderName)         
    #dest = os.path.join(dest, sRemoteFileName)         

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

   # sZipFolder = 
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
            elif ('ChangeList.txt' in files):              
                files.remove('ChangeList.txt')                 
                print("Achive_Folder_To_ZIP skikp ChangeList.txt", stmp)                                                                    
            else:
                aFile = os.path.join(root, sfile)
                sTmpPath = os.path.join(sRemoteFolderName, aFile)
                
                #zf.write(aFile, compress_type=zipfile.ZIP_DEFLATED)
                zf.write(aFile, sTmpPath, compress_type=zipfile.ZIP_BZIP2)

    zf.close()
    print('{}{}'.format("Achive_Folder_To_ZIP done!  ", dest))

    

def removeFolder(sPath):
    # sDestinationPath = os.path.join(sPath,"src\debug")
    # if (os.path.isdir(sDestinationPath)):
    #     print("remove folder = ", sDestinationPath)
    #     shutil.rmtree(sDestinationPath)

    # sDestinationPath = os.path.join(sPath,"src\Release")
    # if (os.path.isdir(sDestinationPath)):
    #     print("remove folder = ", sDestinationPath)
    #     shutil.rmtree(sDestinationPath)    

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

def copyTo3800(src_file, det_file, sSequenceNumber):
    datetime.datetime.now()
    sMonth = time.strftime("%m") 
    iMonth = int(sMonth)
    sYear  = time.strftime("%Y")
    sDate  = time.strftime("%d")


    sRemoteFolderName = '{}.{}.{}.{}{}'.format('BIN_GRADE_v1', sSequenceNumber, sYear, iMonth, sDate)
    #sRemoteFolderName = '{}.{}.{}.{}{}'.format('1', sSequenceNumber, sYear, iMonth, sDate )

    det_file = os.path.join(det_file, sRemoteFolderName) 
    #print(det_file)


    if os.path.exists(det_file):
        print('{}{}'.format(det_file, "   exist !! remove it ?"))
        sYesNo = rawInputTest()
        if (sYesNo == 1):
            shutil.rmtree(det_file)
            #os.remove(dest)
            print('{}{}'.format(det_file, ", rmtree ok"))
            time.sleep(5)
        elif(sYesNo == 0):
            print("skip")
            sys.exit(0)
    else:        
        print('{}{}'.format(det_file, "  do not exist"))
        #shutil.rmtree(det_file)
        
    shutil.copytree(src_file, det_file)

    print('{}{}'.format("copyTo3800 done!  ", det_file))
    #shutil.copy2(src_file, det_file)

def copyOneFile(src_file, det_file):        
    shutil.copy2(src_file, det_file)
    print('{}-[{}] to [{}]'.format("copyOneFile done! ",src_file, det_file))



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

    sVersion = 4
    sProgramimgPath = "D:\\3S_PC\sourceCode\SSD\MP_UI\VC6\BIN_GRADE_V1.0"
    sServerSourceCodePath = r"\\fileserver\Dep_AP\Project\SSD\tools"
    sServerBinaryPath = r"\\fileserver\3800\SW\tools"

    #prepare enviroment (sourcecode)
    sServerSourceCode = os.path.join(sServerSourceCodePath,"BIN_GRADE")
    if not (os.path.isdir(sServerSourceCode)):
        os.mkdir(sServerSourceCode)
        print('{}{}'.format("mkdir done!  ", sServerSourceCode))

    sServerSourceCode = os.path.join(sServerSourceCode,"SOURCE_CODE")
    if not (os.path.isdir(sServerSourceCode)):
        os.mkdir(sServerSourceCode)
        print('{}{}'.format("mkdir done!  ", sServerSourceCode))        

    #prepare enviroment (binary file)
    sServerBinary = os.path.join(sServerBinaryPath,"BIN_GRADE")
    if not (os.path.isdir(sServerBinary)):
        os.mkdir(sServerBinary)
        print('{}{}'.format("mkdir done!  ", sServerBinary))


    sSrcReleaseFile = os.path.join(sProgramimgPath,"src\Release\BIN_GRADE.exe")
    sDstBinFile = os.path.join(sProgramimgPath,"src\\UAC")
    copyOneFile(sSrcReleaseFile, sDstBinFile)


    print("execute UAC !!!")
    sUACPath = os.path.join(sProgramimgPath,"src\\UAC")
    os.chdir(sUACPath)
    os.system("uac_path.bat")
    print('{}{}{}'.format("check done!  ", sUACPath, " SSDMP.exe modify date"))

    sSrcReleaseFile = os.path.join(sProgramimgPath,"src\\UAC\BIN_GRADE.exe")
    sDstFile = os.path.join(sProgramimgPath,"src\\bin")
    copyOneFile(sSrcReleaseFile, sDstFile)


    


    sCleanPath = sProgramimgPath #os.path.join(sProgramimgPath,"src")
    removeFolder(sCleanPath)

    #sCleanPath = os.path.join(sProgramimgPath, "src") 
    removeFile(sCleanPath)
    


    print("compress file ?")
    sYesNo = rawInputTest()
    if ( sYesNo == 1):
        #sFileServer = r"\\fileserver\Dep_AP\Project\SSD\temp\BinGrade"
        #sProgramimgPath = r"D:\\3S_PC\sourceCode\SSD\MP_UI\source_code\GIT_MP_UI_BIN_GRADE\v1.0\v1.0.2016.918_Temp1"
        Achive_Folder_To_ZIP(sProgramimgPath, sServerSourceCode, sVersion)
    elif(sYesNo == 0):
        print("skip")
    else:        
        sys.exit(0)

    
    print("copy binary file to 3800 ?")
    sYesNo = rawInputTest()
    if ( sYesNo == 1):
        sSrcPath = os.path.join(sProgramimgPath,"src\\bin")
        copyTo3800(sSrcPath, sServerBinary, sVersion)
    elif(sYesNo == 0):
        print("skip")
    else:        
        sys.exit(0)


    print("copy change List ?")
    sYesNo = rawInputTest()
    if ( sYesNo == 1):
        s3800RemotePath = r"\\fileserver\3800\SW\SSD_MP_UI_EV\SSD_MP_UI_Release_Note.xls"
        sDep_APRemotePath = r"\\fileserver\Dep_AP\Project\SSD\MP_UI\source_code\SSD_MP_UI_Release_Note.xls"
        sSrcPath = os.path.join(sProgramimgPath,"ChangeList.txt")
        copyOneFile(sSrcPath, sServerSourceCode)
        #copyReleaseNote(sSrcPath, sDep_APRemotePath)
    elif(sYesNo == 0):
        print("skip")
    else:        
        sys.exit(0)

    print("\n\n")
    print("*** Excellent As You Are ***")
    print("\n")
    #print("check D:\3S_PC\sourceCode\SSD\MP_UI\source_code\GIT_MP_UI\v1.0\v1.0.2016.918_Temp1\bin\SSDMP.exe date!!!")

    sys.exit(0)