from django.db import models
import datetime

def TypeIdToTypeStr(typeId):
	data=["int","double","bool","string","date","time","datetime","file"]
	return data[typeId]

def TypeStrToTypeId(typeStr):
	data={"int":0,"double":1,"bool":2,"string":3,"date":4,"time":5,"datetime":6,"file":7}
	return data[typeStr]

def typeIdToFieldStr(typeId):
	data=["int_value","double_value","boolean_value","string_value","date_value","time_value","datetime_value","file_value"]
	return data[typeId]

def stringToValue(strValue,type):
	if type==0: return int(strValue)
	elif type==1: return float(strValue)
	elif type==2: return strValue in ['True','true', '1', 't', 'y', 'yes']
	elif type==3: return strValue
	elif type==4: return datetime.datetime.strptime(strValue,"%d.%m.%Y").date()
	elif type==5: return datetime.datetime.strptime(strValue,"%H:%M:%S").time()
	elif type==6: return datetime.datetime.strptime(strValue,"%d.%m.%Y %H:%M:%S").datetime()


class TimeStamp(models.Model):
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)
	class Meta:
		abstract=True

class Value(models.Model):
	int_value=models.IntegerField(blank=True,null=True)
	double_value=models.FloatField(blank=True,null=True)
	boolean_value=models.NullBooleanField(blank=True,null=True)
	string_value=models.CharField(max_length=200,blank=True)
	date_value=models.DateField(blank=True,null=True)
	time_value=models.TimeField(blank=True,null=True)
	datetime_value=models.DateTimeField(blank=True,null=True)
	file_value=models.CharField(max_length=400,blank=True)
	file_name=models.CharField(max_length=200,blank=True)
	class Meta:
		abstract=True

def getEntityValue(obj):
	if not (obj.int_value is None): return obj.int_value
	if not (obj.double_value is None): return obj.double_value
	if not (obj.boolean_value is None): return obj.boolean_value
	if not (obj.string_value is None): return obj.string_value
	if not (obj.date_value is None): return obj.date_value
	if not (obj.time_value is None): return obj.time_value
	if not (obj.datetime_value is None): return obj.datetime_value

class AlgConstructor(TimeStamp):
	name=models.CharField(max_length=200)
	gen_id=models.CharField(max_length=100)
	data=models.CharField(max_length=3000)
	desc=models.CharField(max_length=500,blank=True)

class Slot(TimeStamp):
	name=models.CharField(max_length=200)
	gen_id=models.CharField(max_length=100,blank=True)
	desc=models.CharField(max_length=500,blank=True)

class Strategy(TimeStamp):
	name=models.CharField(max_length=200)
	slot=models.ForeignKey(Slot)
	desc=models.CharField(max_length=500,blank=True)
	gen_id=models.CharField(max_length=100,blank=True)

class AlgParam(TimeStamp):
	name=models.CharField(max_length=200)
	desc=models.CharField(max_length=500,blank=True)
	gen_id=models.CharField(max_length=100,blank=True)
	strategy=models.ForeignKey(Strategy,blank=True,null=True)
	type=models.PositiveSmallIntegerField()

class AlgTemplate(TimeStamp):
	name=models.CharField(max_length=200)
	strategies=models.ManyToManyField(Strategy)
	params=models.ManyToManyField(AlgParam)
	constructor=models.ForeignKey(AlgConstructor,blank=True,null=True)
	desc=models.CharField(max_length=500,blank=True)

class Algorithm(TimeStamp):
	template=models.ForeignKey(AlgTemplate)

class ParamOfAlg(TimeStamp,Value):
	algorithm=models.ForeignKey(Algorithm)
	param=models.ForeignKey(AlgParam)

class AlgImplementation(TimeStamp):
	algorithm=models.ForeignKey(Algorithm)
	author=models.CharField(max_length=200)
	file=models.CharField(max_length=400)
	fileName=models.CharField(max_length=200)
	desc=models.CharField(max_length=500,blank=True)

class TaskParam(TimeStamp):
	name=models.CharField(max_length=200)
	desc=models.CharField(max_length=500,blank=True)
	type=models.PositiveSmallIntegerField()

class TaskTemplate(TimeStamp):
	name=models.CharField(max_length=200)
	params=models.ManyToManyField(TaskParam)
	desc=models.CharField(max_length=500,blank=True)

class Task(TimeStamp):
	template=models.ForeignKey(TaskTemplate)

class ParamOfTask(TimeStamp,Value):
	task=models.ForeignKey(Task)
	param=models.ForeignKey(TaskParam)

class Computer(TimeStamp):
	name=models.CharField(max_length=100)
	desc=models.CharField(max_length=500,blank=True)

class Launch(TimeStamp):
	task=models.ForeignKey(Task)
	alg_implementation=models.ForeignKey(AlgImplementation)
	computer=models.ForeignKey(Computer)
	time=models.FloatField()