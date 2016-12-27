import zipfile
import os
 
def Achive_Folder_To_ZIP(sFilePath, dest = ""):
    """
    input : Folder path and name
    output: using zipfile to ZIP folder
    """
    if (dest == ""):
        zf = zipfile.ZipFile(sFilePath + '.ZIP', mode='w')
    else:
        zf = zipfile.ZipFile(dest, mode='w')
 
    os.chdir(sFilePath)
    #print sFilePath
    for root, folders, files in os.walk(".\\"):
        for sfile in files:
            aFile = os.path.join(root, sfile)
            #print aFile
            zf.write(aFile)
    zf.close()
 
 
if __name__ == "__main__":
    #C:\Python34\XMLTest
    #Achive_Folder_To_ZIP(r"Z:\alarmchang\AutoUpdate", r"Z:\alarmchang\xyz.zip")
    Achive_Folder_To_ZIP(r"D:\3S_PC\python\XMLTest", r"D:\3S_PC\python\T.zip")