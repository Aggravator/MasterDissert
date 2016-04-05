
def getByValue(arr,key,value):
	for i in arr:
		if(i[key]==value): return i
	return None

def hasAlgStrategy(algObj,strategy,sysdata):#strategy is "slotId&strategyId"
	[slots,slotsId,strategies,strategiesId,params,paramsId]=sysdata
	strategyId=strategiesId[strategy]
	slotId=slotsId[strategy.split("&")[0]]
	res=getByValue(algObj["slots"],0,slotId)
	if res is not None:
		res=getByValue(res[2:],"id",strategyId)
		if res is not None: 
			return True

	return False

def addSlot(algObj,algName,isBase,slot,sysdata):
	[slots,slotsId,strategies,strategiesId,params,paramsId]=sysdata
	if getByValue(algObj["slots"],0,slotsId[slot]) is None:
		newSlot=[slotsId[slot],isBase]
		containSlots=[]
		for i in slots[slot][2:]:
			isActiveStrategy=True
			newStrategy={"id":strategiesId[slot+"&"+i["id"]]}
			if "depends" in i and i["depends"]:
				newStrategy["depends"]={}
				for j in i["depends"]:
					if j=="algorithm":
						if algName not in i["depends"][j]:
							isActiveStrategy=False
							break;
						else:
							continue;
					newDepend=[]
					for ij in i["depends"][j]:
						if hasAlgStrategy(algObj,j+"&"+ij,sysdata):
							newDepend.append(strategiesId[j+"&"+ij])
					if newDepend:
						newStrategy["depends"][slotsId[j]]=newDepend
					else:
						isActiveStrategy=False
						break;

			if isActiveStrategy:
				if ("depends" in newStrategy) and (not newStrategy["depends"]):
					newStrategy.pop("depends",None)
					
				if "contains" in i and i["contains"]:
					newStrategy["contains"]=[]
					for j in i["contains"]:
						containSlots.append(j)
						newStrategy["contains"].append(slotsId[j])

				if "params" in i and i["params"]:
					newStrategy["params"]=[]
					for j in i["params"]:
						newStrategy["params"].append([paramsId[j[1]+"&"+j[0]],j[2]])

				newSlot.append(newStrategy)

		algObj["slots"].append(newSlot)

		for i in containSlots:
			addSlot(algObj,algName,False,i,sysdata)
