# -*- coding: UTF-8 -*-
import json,sys
from mutils import getByValue,addSlot

dataFilePath="system.js"

if len(sys.argv)>1:
	dataFilePath=sys.argv[1]

data=json.loads(open(dataFilePath,"rb").read().decode("utf-8"))

baseSlots=[]
baseParams=[]

baseParams=[ i[1]+"&"+i[0] for i in getByValue(data,0,"program")[2]["params"]]

baseSlots=[i for i in getByValue(data,0,"program")[2]["contains"]]
baseSlots.remove("algorithm")

slots={}
slotsId={}

strategies={}
strategiesId={}

params={}
paramsId={}

## Collecting all slots,strategies and params
for i in data:
	if i[0] !="program" and i[0]!="algorithm":
		slots[i[0]]=i
		for j in i[2:]:
			strategies[i[0]+"&"+j["id"]]=j
			if "params" in j:
				for ij in j["params"]:
					params[ij[1]+"&"+ij[0]]=ij

i=getByValue(data,0,"program")[2]
if "params" in i:
	for j in i["params"]:
		params[j[1]+"&"+j[0]]=j

for i in getByValue(data,0,"algorithm")[2:]:
	if "params" in i:
		for j in i["params"]:
			params[j[1]+"&"+j[0]]=j

import os,django

projectPath=r"D:\MasterDissert\algdb"
sys.path.append(projectPath)
os.environ['DJANGO_SETTINGS_MODULE'] = 'algdb.settings'
django.setup()

import core.models as models

#get entities id
for i in slots:
	obj=None
	try:
		obj=models.Slot.objects.get(gen_id=i)
		obj.name=slots[i][1]
	except models.Slot.DoesNotExist:
		obj=models.Slot(name=slots[i][1],gen_id=slots[i][0])
	obj.save()
	slotsId[i]=obj.id

for i in params:
	pName,pType=i.split("&")
	obj=None
	try:
		obj=models.AlgParam.objects.get(gen_id=pName,type=models.TypeStrToTypeId(pType))
		obj.name=params[i][3]
	except models.AlgParam.DoesNotExist:
		obj=models.AlgParam(gen_id=pName,type=models.TypeStrToTypeId(pType),name=params[i][3])
	obj.save()
	paramsId[i]=obj.id

for i in strategies:
	slot,strategy=i.split("&")
	obj=None
	try:
		obj=models.Strategy.objects.get(gen_id=strategy,slot_id=slotsId[slot])
		obj.name=strategies[i]["title"];
		obj.desc=strategies[i]["details"].strip("/ ");
		obj.gen_id=strategy
		obj.slot=models.Slot.objects.get(id=slotsId[slot])
	except models.Strategy.DoesNotExist:
		obj=models.Strategy(name=strategies[i]["title"],gen_id=strategy,slot=models.Slot.objects.get(id=slotsId[slot]),desc=strategies[i]["details"].strip("/ "))
	obj.save()

	if "params" in strategies[i]:
		for j in strategies[i]["params"]:
			p=models.AlgParam.objects.get(id=paramsId[j[1]+"&"+j[0]])
			p.strategy=obj
			p.save()

	strategiesId[i]=obj.id

#create json data
sysdata=[slots,slotsId,strategies,strategiesId,params,paramsId]

for i in getByValue(data,0,"algorithm")[2:]:
	newAlg={}
	newAlg["baseparams"]=[ [paramsId[j],params[j][2]] for j in baseParams]
	if "params" in i:
		for j in i["params"]:
			newAlg["baseparams"].append( [paramsId[j[1]+"&"+j[0]],j[2]])
	
	newAlg["slots"]=[]
	for j in baseSlots:
		addSlot(newAlg,i["id"],True,j,sysdata)

	if("contains" in i):
		for j in i["contains"]:
			addSlot(newAlg,i["id"],True,j,sysdata)

	algObj=None;
	try:
		algObj=models.AlgConstructor.objects.get(gen_id=i["id"])
		algObj.name=i["title"]
		algObj.desc=i["details"].strip("/ ");
		algObj.data=json.dumps(newAlg)
	except models.AlgConstructor.DoesNotExist:
		algObj=models.AlgConstructor(name=i["title"],gen_id=i["id"],desc=i["details"].strip("/ "),data=json.dumps(newAlg))

	algObj.save()

	print('Alorithm constructor "'+i["id"]+'" added!')