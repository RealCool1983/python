import os
import time
import subprocess

#cmd = 'adb shell ls'
#s = subprocess.check_output(cmd)
#print (s)

print ("Start : %s" % time.ctime())
#time.sleep( 1 )
print ("End : %s" % time.ctime())

#os.system("adb shell setprop persist.sys.auto_freeze_status off")

#pw





#procId = subprocess.Popen('adb shell ls /storage/usbdisk1/', shell=False)
cmd1 = "adb shell ls /storage/usbdisk1/"

print("\n\r cmd  = {0} \n\r ".format(cmd1))
subprocess.call(cmd1, shell=True)

#rocId.communicate('ls /storage/usbdisk1/')