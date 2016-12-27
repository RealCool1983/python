import os
import glob; glob.glob("*.xml")
fileName='*.txt'
if os.path.exists(fileName):
    print ("YES")
else :
    print ("NO")