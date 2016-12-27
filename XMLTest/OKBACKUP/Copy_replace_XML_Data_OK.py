#!/usr/bin/env python
import glob
import os
from xml.etree import ElementTree

from tempfile import mkstemp
from shutil import move
from os import remove, close
#subprocess ,calling bat file
import subprocess

import configparser
from configparser import SafeConfigParser
import shutil

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



# Run the above function and store its results in a variable.   
full_file_paths = get_filepaths("D:\\03.Factory\\01.Vivapro\\Apollo_V1.006_20161012\\offLineREhearsal\\")
UIMode_paths = "D:\\03.Factory\\01.Vivapro\\Apollo_V1.006_20161012\\offLineREhearsal\\UIConfig.xml"
print ("UIMode_paths = ", UIMode_paths) 
print ("= =start copy  = =") 
xmlPath = []
for eachPname in full_file_paths:
# read tool version
    if ((eachPname.find("UIConfig.xml") != -1 )) :
            xmlPath = eachPname
            try:
                shutil.copy(UIMode_paths, xmlPath)
                print("{:10}{:.15}   {:.150}".format('copy ok:',  UIMode_paths, xmlPath))


            # eg. src and dest are the same file
            except shutil.Error as e:
                print('Error: %s' % e)
            # eg. source or destination doesn't exist
            except IOError as e:
                print('Error: %s' % e.strerror)

print ("= = after copy  = =") 
xmlPath = []
for eachPname in full_file_paths:
# read tool version
    if ((eachPname.find("UIConfig.xml") != -1 )) :
            xmlPath = eachPname
            try:
                tree = ElementTree.parse(xmlPath)
                bodys = tree.getiterator("UIMode")
                print (xmlPath, "UIMode = ", bodys[0].text) 
            except:
                print('!!! exception happen in', xmlPath)


  
	   
    if (eachPname.find("TestItem_RD.xml") != -1 ) :
            xmlPath = eachPname
            try:
                tree = ElementTree.parse(xmlPath)   
                bodys = tree.getiterator("LogUpload")
                bodys[0].text = "FALSE"
                print ("LogUpload = ", bodys[0].text) 
                #tree.write(xmlPath,"UTF-8")

                #replace(data, "<LogUpload>TRUE</LogUpload>", "<LogUpload>FALSE</LogUpload>")    
                #replace(xmlPath, "TRUE", "FALSE")
                #print( xmlPath , ' DONE')
                tree = ElementTree.parse(xmlPath)
                bodys = tree.getiterator("LogUpload")
                print (xmlPath, "LogUpload = ", bodys[0].text) 
            except:
                print('!!! exception happen in', xmlPath)