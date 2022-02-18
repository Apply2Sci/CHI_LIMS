# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


# importing modules

import openpyxl as xl
import pandas as pd
import os
from shutil import copyfile
from datetime import datetime
from openpyxl.styles import Alignment, Font
from statistics import mean, stdev
from click import confirm

# introduce scope

print(datetime.now().time(),"\n~-~-~       Scripted Data Packer V.0.1       ~-~-~\n¦:   Intended for use at CHI, Temple St.   :¦\n~-~              ----------------              ~-~\n\n")
baseDir = input("Please input SOURCE directory:\n(ENTER for default: c:\Users\Desktop)\n\n")


# search for input files

infileList = []

for files in os.walk(baseDir):
    for file in files:
        if file.endswith('.txt') and file.startswith('eReportOutput_'):
            infileList.append(file)

print('Found %s input files in directory:' % len(infileList), sep = '')
print("\n".join(infileList))

print('\n')
if confirm("\nPlease confirm ALL these input files will be converted to CSV."):
    continue
else:
    raise SystemExit()


print(datetime.now().time(),"\nOK! Run directory found at:", runPath.replace(baseDir, ''),"\nSearching for ClO3 & ClO4 raw data Excel files...")

