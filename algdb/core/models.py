from django.db import models

def TypeIdToTypeStr(typeId):
	data=["int","double","bool"]
	return data[typeId]

def TypeStrToTypeId(typeStr):
	data={"int":0,"double":1,"bool":2}
	return data[typeStr]

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
	class Meta:
		abstract=True

class AlgConstructor(TimeStamp):
	name=models.CharField(max_length=200)
	gen_id=models.CharField(max_length=100)
	data=models.CharField(max_length=3000)
	desc=models.CharField(max_length=500,blank=True)

class AlgParam(TimeStamp):
	name=models.CharField(max_length=200)
	desc=models.CharField(max_length=500,blank=True)
	gen_id=models.CharField(max_length=100,blank=True)
	type=models.PositiveSmallIntegerField()

class Slot(TimeStamp):
	name=models.CharField(max_length=200)
	gen_id=models.CharField(max_length=100,blank=True)
	desc=models.CharField(max_length=500,blank=True)

class Strategy(TimeStamp):
	name=models.CharField(max_length=200)
	slot=models.ForeignKey(Slot)
	desc=models.CharField(max_length=500,blank=True)
	gen_id=models.CharField(max_length=100,blank=True)

class AlgTemplate(TimeStamp):
	name=models.CharField(max_length=200)
	strategies=models.ManyToManyField(Strategy)
	params=models.ManyToManyField(AlgParam)
	constructor=models.ForeignKey(AlgConstructor,blank=True,null=True)
	desc=models.CharField(max_length=500,blank=True)

class Algorithm(TimeStamp):
	template=models.ForeignKey(AlgTemplate)

class AlgImplementation(TimeStamp):
	algorithm=models.ForeignKey(Algorithm)
	author=models.CharField(max_length=200)
	file=models.CharField(max_length=200)
	desc=models.CharField(max_length=500,blank=True)

class ParamOfAlg(TimeStamp,Value):
	algorithm=models.ForeignKey(Algorithm)
	param=models.ForeignKey(AlgParam)

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