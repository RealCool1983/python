import os
import glob
import datetime
import time
import sys

if __name__ == "__main__":

    sStartTime = datetime.datetime.now()
    print('.............. ParsingHead StartTime:{} ..............\n\n '.format(sStartTime))

    for filename in glob.iglob('D:\\3S_PC\\python\\3S_AUTO\\*.txt', recursive=True):
        
        try:
            #print(filename)
            if (filename.find("ParsingHead") != -1):
                #print(filename)
                #break
                #continue

                with open(filename,  encoding = 'utf-8-sig') as f2:

                                             
                    for line in f2:
                        for line1 in line.splitlines():
                            #print (line1)                        
                            line1 = line1.replace(";", "")
                            lineSplit = line1.split()

                            if (line1.find("typedef struct") != -1):
                                print('\n\n\n{}'.format(line1))
                                # print('\n\n\n................{},{},{}.........'.format(lineSplit[0], lineSplit[1], lineSplit[2]))
                                continue
                            if (line1.find("}") != -1):
                                continue
                            if (line1.find("#define") != -1):
                                continue                                
                                
                            if (len(lineSplit) > 1):
                                print('{},{}'.format(lineSplit[0], lineSplit[1]))
                f2.close()
            print("read ok, {}".format(filename))


        except OSError as err:
            print("OS error: {0}".format(err))
        except ValueError:
            print("Could not convert data to an integer.")
            print("line = ", sum_lines)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    sEndTime = datetime.datetime.now()        
    print('\n\n.............. ParsingHead EndTime:{}, Total:{} ....................'.format(sEndTime, (sEndTime-sStartTime)))        

    # printList()     
    sys.exit(0)

