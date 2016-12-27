import os
import glob

#for root, dirs, files in os.walk("./20160719/"):
    #print (root)
    #for f in files:
        #print (os.path.join(root, f))
        #file1 = os.path.join(root, f)
        #print (file1)
        #glob.glob(' *.text ')
        
        #if (file1)

#f1 = glob.glob(r'./20160719/*.log')
#f1 = glob.glob(r'./**/*.log')
for filename in glob.iglob('./**/*.log', recursive=True):
    #print(filename)
	try:
		with open(filename,  encoding = 'utf-8-sig') as f2:
		    for line in f2:
		        if "Result: PASS, Measured: getEquimpmentValue" in line:
		        	#print(line)
		        	print(filename)
		        	print(line)
		f2.close()
	except OSError as err:
	    print("OS error: {0}".format(err))
	except ValueError:
	    print("Could not convert data to an integer.")
	    print("line = ", sum_lines)
	except:
	    print("Unexpected error:", sys.exc_info()[0])
	    raise