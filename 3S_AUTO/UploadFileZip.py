import zipfile
import os
import shutil
import glob
import datetime
import time
import sys

"""
Achive_Folder_To_ZIP: 壓縮資料夾，排除git檔，上傳至網芳
removeFolder:刪除特定資料夾
removeFile:刪除特定檔案
copyTo3800:將資料夾上傳至網芳
"""
 
def Achive_Folder_To_ZIP(sFilePath, dest = "", sSequenceNumber = "0"):
    """
    input : Folder path and name
    sSequenceNumber :
    output: using zipfile to ZIP folder
    """

    datetime.datetime.now()
    #sSequenceNumber = 15
    sDate = time.strftime("%Y.%m.%d")
    sRemoteFileName = '{}{}{}{}{}'.format('v1.0.', sDate,'_Temp', sSequenceNumber,'.zip')
    print(sRemoteFileName)

    if (dest == ""):
        zf = zipfile.ZipFile(sFilePath + '.ZIP', mode='w')
    else:
        dest = os.path.join(dest, sRemoteFileName) 
        print(dest)
        zf = zipfile.ZipFile(dest, mode='w')


    os.chdir(sFilePath)
    
    #print sFilePath
    for root, folders, files in os.walk(".\\"):
        for sfile in files:
            stmp = os.path.join(root, sfile) 

            if ( '.git' in folders ):
                folders.remove('.git') 
                print(stmp)   
            else:
                aFile = os.path.join(root, sfile)
                print ("zipFile = ", aFile)
                # ZIP_BZIP2
                #zf.write(aFile, compress_type=zipfile.ZIP_DEFLATED)
                zf.write(aFile, compress_type=zipfile.ZIP_BZIP2)

    zf.close()
 
def removeFolder(sPath):
    sDestinationPath = os.path.join(sPath,"src\debug")
    if (os.path.isdir(sDestinationPath)):
        print("remove folder = ", sDestinationPath)
        shutil.rmtree(sDestinationPath)

    sDestinationPath = os.path.join(sPath,"src\Release")
    if (os.path.isdir(sDestinationPath)):
        print("remove folder = ", sDestinationPath)
        shutil.rmtree(sDestinationPath)    
    
 

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
    #sSequenceNumber = 15
    sDate = time.strftime("%Y.%m%d")
    sRemoteFolderName = '{}{}{}{}'.format('v1.0.', sDate,'_Temp', sSequenceNumber)
    print("copyTo3800 path = ", sRemoteFolderName)
    
    det_file = os.path.join(det_file, sRemoteFolderName) 
    print(det_file)
    #sys.exit(0)
    if os.path.exists(det_file):
        shutil.rmtree(det_file)
        
    shutil.copytree(src_file, det_file)
    #shutil.copy2(src_file, det_file)



if __name__ == "__main__":
    sVersion = 16


    sCleanPath = "D:\\3S_PC\sourceCode\SSD\MP_UI\source_code\GIT_MP_UI\\v1.0\\v1.0.2016.918_Temp1"
    removeFolder(sCleanPath)
    removeFile("D:\\3S_PC\\sourceCode\\SSD\\MP_UI\\source_code\\GIT_MP_UI\\v1.0\\v1.0.2016.918_Temp1")

    
    sFileServer = r"\\fileserver\Dep_AP\Project\SSD\MP_UI\source_code\v1.0"
    sSourceFile = r"D:\\3S_PC\sourceCode\SSD\MP_UI\source_code\\GIT_MP_UI\v1.0\v1.0.2016.918_Temp1"
    Achive_Folder_To_ZIP(sSourceFile, sFileServer, sVersion)


    sRemotePath = r"\\fileserver\3800\SW\SSD_MP_UI_EV\v1.0"
    sSrcPath = r"D:\\3S_PC\sourceCode\SSD\MP_UI\source_code\GIT_MP_UI\v1.0\v1.0.2016.918_Temp1\bin"
    copyTo3800(sSrcPath, sRemotePath, sVersion)
 

    sys.exit(0)