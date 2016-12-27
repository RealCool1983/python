import glob
import os
from xml.etree import ElementTree

from tempfile import mkstemp
from shutil import move
from os import remove, close
#subprocess ,calling bat file
import subprocess

def get_filepaths(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.


def replace(file_path, pattern, subst):
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

#replace(data, "ToolVersion", "Tool_Version")


# Run the above function and store its results in a variable.   
full_file_paths = get_filepaths("D:\\03.Factory\\04.F80\\20150715")

xmlPath = []
for eachPname in full_file_paths:
   #print(eachPname)
    if ((eachPname.find("TestItem.xml") != -1 ) or (eachPname.find("TestItem_RD.xml") != -1 )) :
    #if ((eachPname.find("OS_DL_TestItem") != -1 ) or (eachPname.find("Trigger_TestItem") != -1 )) :
            #data = "GT47B1A_MMI_BB_TestItem_RD.xml"
            xmlPath = eachPname
            #print(xmlPath)
            try:
                #replace(xmlPath, "ToolVersion", "TOOL_VERSION")
                #replace(xmlPath, "V1.002", "V1.000")
                #print( xmlPath , ' DONE')
                tree = ElementTree.parse(xmlPath)
                bodys = tree.getiterator("TOOL_VERSION")
                #replace tool version
                #(xmlPath, "ToolVersion", "Tool_Version")
                #modify too version
                #bodys[0].text = "V2.000"
                print (xmlPath, "TOOL_VERSION = ", bodys[0].text) 
                #tree.write(data,"UTF-8")
            except:
                print('!!! exception happen in', xmlPath)
'''		
        if (xmlPath.find("MD5") != -1 ):
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
'''


  
	   
