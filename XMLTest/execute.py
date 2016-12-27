import os
import time

print "Start : %s" % time.ctime()
time.sleep( 5 )
print "End : %s" % time.ctime()


os.system("adb shell su -c reboot")