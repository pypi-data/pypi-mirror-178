#!/usr/bin/env python3
import os
import subprocess
import sys

workdir = sys.argv[1]   # /nas/Project/KC2022-G1442/Upload
dest = sys.argv[2]      # /2022/1401-1500/KC2022-G1442/Data/
os.chdir(workdir)

files = subprocess.getoutput("find . " ).split()

def readlink(file):
    if os.path.islink(file):
        return readlink(os.readlink(file))
    else: return(file)
    
for file in files:
    if os.path.isdir(file):
        continue
    dir = file.split("/")[-2]
    remote_dest = dest
    if dir != ".":
        remote_dest = os.path.join(dest,dir)
    file = readlink(file)
    os.system("BaiduPCS-Go upload %s %s" %(file,remote_dest))
