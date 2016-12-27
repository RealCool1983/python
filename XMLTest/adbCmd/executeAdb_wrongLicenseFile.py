import os
import time
import subprocess

#cmd = 'adb shell ls'
#s = subprocess.check_output(cmd)
#print (s)

print ("Start : %s" % time.ctime())
time.sleep( 1 )
print ("End : %s" % time.ctime())

os.system("adb shell setprop persist.sys.factory.license.dec on")

cmd1 = "adb shell getprop  persist.sys.factory.license.dec"
x = subprocess.check_output(cmd1)
print("{0} = {1}".format(cmd1,x))


cmd1 = "adb push LICENSE.LIC /data"
x = subprocess.check_output(cmd1)
print("{0} = {1}".format(cmd1,x))

cmd1 = "adb shell write_license /data/LICENSE.LIC"
x = subprocess.check_output(cmd1)
print("{0} = {1}".format(cmd1,x))

cmd1 = "adb shell su -c reboot"
x = subprocess.check_output(cmd1)
print("{0} = {1}".format(cmd1,x))

#os.system("adb shell su -c reboot")