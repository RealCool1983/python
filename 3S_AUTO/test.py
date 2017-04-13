import zipfile
import os
import shutil
import glob
import datetime
import time
import sys
from operator import itemgetter
from collections import Counter
"""
Achive_Folder_To_ZIP: 壓縮資料夾，排除git檔，上傳至網芳
removeFolder:刪除特定資料夾
removeFile:刪除特定檔案
copyTo3800:將資料夾上傳至網芳
copyRelease note:
"""


def runSortList():
    listL1 = [('abc', 121, "vv"),('bbc', 231, "v6"),('ccc', 148, "v2"), ('abc',221,"v1"),  ('ab5555555555555555555555c',221)]
    print(listL1)
    listL2 = sorted(listL1, key=itemgetter(0))
    # listL2 = sorted(listL1)
    # print(listL1)
    print('0',  sorted(listL1, key=itemgetter(0)))
    print('1',  sorted(listL1, key=itemgetter(1)))
    # print('2',  sorted(listL1, key=itemgetter(2)))    

    for item in listL1:
        try:
        # if (len(item)==3):
            print('item, {:2s} {:5d} {:10s}'.format(item[0], item[1], item[2]))
        except:
            print("except")

    print("runSortList done")

if __name__ == "__main__":

    runSortList()
    




    # print('0', listL2)
	
    sys.exit(0)