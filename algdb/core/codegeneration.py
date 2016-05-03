import os
from . import models
ershSysPath=r"D:/algo_repo-selection_kaa/genetic_algorithm/"
def getCode(userJsData):
	path=os.getcwd()
	os.chdir(ershSysPath)
	f=open(ershSysPath+"user.js","w")
	f.write(userJsData)
	f.close()
	os.system("python "+ershSysPath+"gen.py")
	os.system("python "+ershSysPath+"apply.py")
	os.chdir(path)
	return open(ershSysPath+"output.cpp","rb").read()

def getBaseName(file):
	fname=re.split(r'[\\/]',file)[-1]
	basename=".".join(fname.split(".")[0:-1])
	if(basename==""):
		basename=fname
	return baseName