import glob
import os
from xml.etree import ElementTree

from tempfile import mkstemp
from shutil import move
from os import remove, close
#subprocess ,calling bat file
import subprocess
#data = "GT47B1A_MMI_BB_TestItem_RD.xml"

   xmlPath = "D:\03.Factory\02.T47\20150317_Tool_version\GT47B1A_MMI_BB_v1.000_20150209_del_speaker\MD5"
   print(xmlPath)
    if(xmlPath.find("MD5") != -1 ):
        xmlPath = os.path.dirname(xmlPath)
        xmlPath = os.path.join(xmlPath,'GenerateMD5File_Auto.bat')
        print('MD5 Path = ', xmlPath)
			
        try:
            p = subprocess.Popen(xmlPath, creationflags=subprocess.CREATE_NEW_CONSOLE)
            stdout, stderr = p.communicate()
            print ('PASS, path = ', xmlPath, p.returncode) # is 0 if success
            print ( p.returncode )
        except:
            print('!!! exception 02 happen in', xmlPath)
