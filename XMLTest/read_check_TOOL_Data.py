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
# read tool version
    if ((eachPname.find("TestItem.xml") != -1 ) or (eachPname.find("TestItem_RD.xml") != -1 )) :
            xmlPath = eachPname
            try:
                tree = ElementTree.parse(xmlPath)
                bodys = tree.getiterator("TOOL_VERSION")
                print (xmlPath, "TOOL_VERSION = ", bodys[0].text) 
            except:
                print('!!! exception happen in', xmlPath)

#read RestestCount
    if ((eachPname.find("DBConfig.ini") != -1) and (eachPname.find("VMS") == -1) ) :
            xmlPath = eachPname
            try:
                parser = SafeConfigParser()
                parser.read(xmlPath)
                print (xmlPath,'RetestCount = ', parser.get('SETTING', 'RetestCount'))
            except:
                print('!!! exception happen in', xmlPath)
#read SQN
    if ((eachPname.find("config.ini") != -1) ) :
            xmlPath = eachPname
            try:
                parser = SafeConfigParser()
                parser.read(xmlPath)
                print (xmlPath,'SQN = ', parser.get('COMMON', 'SQN'))
            except:
                print('!!! exception happen in', xmlPath)




  
	   
