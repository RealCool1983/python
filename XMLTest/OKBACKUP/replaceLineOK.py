#!/usr/bin/env python  
import os
import xml.etree.ElementTree as ET
from xml.etree import ElementTree

from tempfile import mkstemp
from shutil import move
from os import remove, close

data = "GT47B1A_MMI_BB_TestItem_RD.xml"

tree = ElementTree.parse(data)   
bodys = tree.getiterator("ToolVersion")
print ("ToolVersion = ", bodys[0].text) 


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

replace(data, "ToolVersion", "Tool_Version")	

