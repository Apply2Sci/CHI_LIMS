# -*- coding: utf-8 -*-
"""

Data Interface for Ray Ball at CUH Temple St by Karl De Ruyck <karlderuyck@pm.me>
Version 0.2 (alpha)

"""


# importing modules

import pandas as pd
import numpy as np
import os
import re
from datetime import datetime
from statistics import mean#, stdev
from click import confirm


# introduce scope

step = 1
print("\n",datetime.now().time(),"Step #%s: Program start." % step, sep = "\n")

print("\n~-~-~         Scripted Data Packer  v. 0.2         ~-~-~\n¦:         Intended for use by CHI, Temple St.        :¦\n¦:           For support contact the author:          :¦\n¦: https://www.linkedin.com/in/karl-de-ruyck-3138991/ :¦\n~-~                 ----------------                 ~-~\n\n")


# define functions

step+=1
print("\n",datetime.now().time(),"Step #%s: Initializing..." % step, sep = "\n")

def LIMS(inData,item):
    
    print("\n",datetime.now().time(),"Processing file #%s..." % item, sep = "\n")
    
    outData = inData.filter([1,2,4], axis = 1)
    outData = outData.rename({1:'ID',2:'Phe',4:'Tyr'}, axis = 1)
    
    outData[['Tyr %Dev','Phe %Dev','Tyr Mean','Phe Mean']] = np.nan
    for j in range(1,len(inData)):
        if j % 2 == 1:
            i = j-1
            outData.at[i,'Tyr Mean'] = int(round(mean([inData.iat[i,4],inData.iat[i+1,4]]),0))
            outData.at[i,'Phe Mean'] = int(round(mean([inData.iat[i,2],inData.iat[i+1,2]]),0))
            outData.at[i,'Tyr %Dev'] = int(round(100*([inData.iat[i,4]-inData.iat[i+1,4]]/outData.at[i,'Tyr Mean']),0))
            outData.at[i,'Phe %Dev'] = int(round(100*([inData.iat[i,2]-inData.iat[i+1,2]]/outData.at[i,'Phe Mean']),0))
    
    outData.to_csv(outfileList[item-1], index = False)
    
    print("\n",datetime.now().time(),"File #%s processed." % item, sep = "\n")

    return        
    

# map working directory

step+=1
print("\n",datetime.now().time(),"Step #%s: Identifying SOURCE directory." % step, sep = "\n")

while True:
    baseDirDate = input("Please type in the MET project date of the\ndirectory containing NeoLynx exported\ndatafiles to be processed.\n\nSuch datafiles must be named beginning\nwith eReport and having a .txt extension.\n\n(yymmdd): ")
    baseDir = "D:\\Metabolic Projects 20" + str(baseDirDate)[0:2] + "\\MET" + str(baseDirDate) + ".PRO"
    if os.path.isdir(baseDir):
        print("Thank you.")
        os.chdir(baseDir)
        print("\n",datetime.now().time(),"\nThe working directory is:\n", os.getcwd(), sep = "\n")
        break
    else:
        print("\n",datetime.now().time(),"\nERROR\n\nNo directory was found at this path:\n", baseDir, sep = "\n")
        continue


    
# search for input files

step+=1
print("\n",datetime.now().time(),"Step #%s: Searching directory." % step, sep = "\n")

infileList = []

for file in os.listdir(baseDir):
    if file.endswith('.txt') and file.startswith('eReport'):
        infileList.append(file)

if len(infileList) == 0:
    print(datetime.now().time(),"No valid input files found.\nThis program will end now.")
    raise SystemExit()

print('Found %s input files in directory:' % len(infileList), sep = '')
print("\n".join(infileList))


# confirm input files

step+=1
print("\n",datetime.now().time(),"Step #%s: File read check." % step, sep = "\n")

if confirm("\nPlease confirm ALL these input files will be converted to CSV:"):
    print("Thank you.")
else:
    print(datetime.now().time(),"\nThis program will end now.")
    exit()


# check for existing output files

step+=1
print("\n",datetime.now().time(),"Step #%s: Output file check." % step, sep = "\n")

outfileList = []
filedateList = []
for file in infileList:
    filedate = str(re.findall("\d{6}",file)[0])
    filedateList.append(filedate)
    filename = str("TEST PTDBS 220217E _ ") + filedate + (".csv")
    outfileList.append(filename)

newfileNames = []
oldfileNames = []
for file in outfileList:
    if os.path.exists(file):
        oldfileNames.append(file)
    else:
        newfileNames.append(file)

if len(oldfileNames) == 0:
    print("\n",datetime.now().time(),"\nNo existing output files found.\nContinuing...")
else:
    print("\n",datetime.now().time(),"\nThere are %s output files already in the directory.\n" % len(oldfileNames))
    print("\n".join(oldfileNames))

    if confirm("\nThese files will be OVERWRITTEN if the program proceeds, OK?"):
        print("Thank you, new data will be written to these files.")
    else:
        print(datetime.now().time(),"\nThis program will end now.")
        exit()


# call LIMS formatting function

step+=1
print("\n",datetime.now().time(),"Step #%s: Processing input files..." % step, sep = "\n")

for item in range(1,len(infileList)+1):
    inData = pd.read_csv(infileList[item-1], sep="\t", header=None)
    LIMS(inData,item)


step+=1
print("\n",datetime.now().time(),"Step #%s: All files processed locally." % step, sep = "\n")


# copy to LIMS directory

LIMSnet = "J:\\scriptoutput"
if os.path.isdir(LIMSnet):
    netPath = True
else:
    step+=1
    print("\n",datetime.now().time(),"Step #%s: Network path not found.\nThis program will end now." % step, sep = "\n")

while netPath:
    step+=1
    print("\n",datetime.now().time(),"Step #%s: The mapped network drive is J:\\scriptoutput" % step, sep = "\n")
    if confirm("\nDo you want to write output to LIMS?"):
        print("Thank you.")
        try:
            os.popen("copy *.csv j:\\scriptoutput")
        except:
            step+=1
            print("\n",datetime.now().time(),"Step #%s: Network transfer to LIMS has FAILED.\nPlease copy local files manually." % step, sep = "\n")
        else:
            step+=1
            print("\n",datetime.now().time(),"Step #%s: Write to LIMS was SUCCESSFUL!" % step, sep = "\n")

print(datetime.now().time(),"\nThis program will end now.")
exit()
