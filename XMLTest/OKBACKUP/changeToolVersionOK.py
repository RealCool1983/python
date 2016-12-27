#!/usr/bin/env python  
import os
import xml.etree.ElementTree as ET
from xml.etree import ElementTree

data = "GT47B1A_MMI_BB_TestItem_RD.xml"

tree = ElementTree.parse(data)   
bodys = tree.getiterator("ToolVersion")
bodys[0].text = "V2.000"
print ("ToolVersion = ", bodys[0].text) 
tree.write(data,"UTF-8")



