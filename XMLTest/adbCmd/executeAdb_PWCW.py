import os
import time
import subprocess

#cmd = 'adb shell ls'
#s = subprocess.check_output(cmd)
#print (s)

print ("Start : %s" % time.ctime())
time.sleep( 1 )
print ("End : %s" % time.ctime())

#os.system("adb shell setprop persist.sys.auto_freeze_status off")

#pw
cmd1 = "adb shell setprop persist.sys.auto_freeze_status off"
x = subprocess.check_output(cmd1)
print("{0} = {1}".format(cmd1,x))


cmd1 = "adb shell setprop Runtime.factory.Updatexml 2"
x = subprocess.check_output(cmd1)
print("{0} = {1}".format(cmd1,x))

cmd1 = "adb shell getprop  Runtime.factory.Updatexml"
x = subprocess.check_output(cmd1)
print("{0} = {1}".format(cmd1,x))

cmd1 = "adb  shell input tap 250 100"
x = subprocess.check_output(cmd1)
print("{0} = {1}".format(cmd1,x))

cmd1 = "adb shell setprop Runtime.factory.testmode 4"
x = subprocess.check_output(cmd1)
print("{0} = {1}".format(cmd1,x))


cmd1 = "adb shell getprop persist.sys.factory.modecheck"
x = subprocess.check_output(cmd1)
print("{0} = {1}".format(cmd1,x))

cmd1 = "adb shell getprop  Runtime.factory.testmode"
x = subprocess.check_output(cmd1)
print("{0} = {1}".format(cmd1,x))
#os.system("adb shell su -c reboot")


#cw 

cmd1 = "adb shell setprop persist.sys.auto_freeze_status off"
x = subprocess.check_output(cmd1)
print("{0} = {1}".format(cmd1,x))


cmd1 = "adb shell setprop Runtime.factory.Updatexml 2"
x = subprocess.check_output(cmd1)
print("{0} = {1}".format(cmd1,x))

cmd1 = "adb shell getprop  Runtime.factory.Updatexml"
x = subprocess.check_output(cmd1)
print("{0} = {1}".format(cmd1,x))

cmd1 = "adb  shell input tap 250 100"
x = subprocess.check_output(cmd1)
print("{0} = {1}".format(cmd1,x))

cmd1 = "adb shell setprop Runtime.factory.testmode 4"
x = subprocess.check_output(cmd1)
print("{0} = {1}".format(cmd1,x))


cmd1 = "adb shell getprop persist.sys.factory.modecheck"
x = subprocess.check_output(cmd1)
print("{0} = {1}".format(cmd1,x))

cmd1 = "adb shell getprop  Runtime.factory.testmode"
x = subprocess.check_output(cmd1)
print("{0} = {1}".format(cmd1,x))
#os.system("adb shell su -c reboot")
