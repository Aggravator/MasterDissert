from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import View,ListView
from django.db.models import Count,Q
from django.core.urlresolvers import reverse
import json
import uuid
from . import models
from . import codegeneration as cg

programCodePath=r"D:/MasterDissert/algdb/core/static/code/"

def MainWindow(request):
	return render(request,'algorithms_menu.html')

def TaskMenu(request):
	return render(request,'tasks_menu.html')

def TemplateAlgoirthmView(request,algTemplId):
	tAlgObj=models.AlgTemplate.objects.get(pk=int(algTemplId))
	context={"alg":tAlgObj,"palgs":[]}
	for i in tAlgObj.algorithm_set.all():
		alg={"id":i.id,"desc":""}
		for j in i.paramofalg_set.order_by('param__name'):
			alg["desc"]=alg["desc"]+j.param.name+"="+str(models.getEntityValue(j))+";"
		context["palgs"].append(alg)
	return render(request,'templalg.html',context)

def AlgorithmView(request,algTemplId):
	alg=models.Algorithm.objects.get(pk=int(algTemplId))
	context={"alg":alg,"palgs":[]}
	for i in alg.paramofalg_set.all():
		param={"id":i.param.id,"name":i.param.name,"value":str(models.getEntityValue(i))}
		context["palgs"].append(param)
	return render(request,'algorithm.html',context)

class CreateTemplateAlgView(View):
    def get(self, request):
        return render(request, 'algtemplcreate.html')
    def post(self,request):
    	pass
    	#algC=models.AlgConstructor.objects.get(pk=genId)

def ImplementationView(request,implId):
	impl=models.AlgImplementation.objects.get(pk=int(implId))
	context={"alg_id":impl.algorithm.id,"alg_name":impl.algorithm.template.name,"impl":{"id":impl.id,"author":impl.author,"fileName":impl.fileName,"desc":impl.desc}}
	return render(request,'implementation.html',context)

def DownloadImplView(request,implId):
	impl=models.AlgImplementation.objects.get(pk=int(implId))
	code=open(programCodePath+impl.file).read()
	response = HttpResponse(content_type='application/force-download')
	response['Content-Disposition'] = 'attachment; filename='+impl.fileName
	response.write(code)
	return response

class AlgSearch(ListView):
	model=models.AlgTemplate
	template_name="algorithm_search.html"
	context_object_name="algs"
	paginate_by = 10
	def get_queryset(self):
		qs = super(AlgSearch, self).get_queryset()
		if("algname" in self.request.GET) and (self.request.GET["algname"]!=""):
			qs=qs.filter(name__icontains=self.request.GET["algname"])
		return qs
	def get_context_data(self, **kwargs):
		context = super(AlgSearch, self).get_context_data(**kwargs)
		context['get'] = self.request.GET
		return context

class GeneratorView(View):
    def get(self, request,genId):
        return render(request, 'generator.html', {"obj": get_object_or_404(models.AlgConstructor, pk=genId)})
    def post(self,request,genId):
    	algC=models.AlgConstructor.objects.get(pk=genId)
    	data=[]
    	slotsJs={}
    	paramsJs={}
    	slotsJs["program"]="defalut"
    	slotsJs["algorithm"]=algC.gen_id
    	strategies=[]
    	params={}
    	for i in request.POST:
    		if(i.startswith("slot")):
    			id=int(i.split("_")[1])
    			slotsJs[models.Slot.objects.get(pk=id).gen_id]=models.Strategy.objects.get(pk=int(request.POST[i])).gen_id
    			strategies.append(int(request.POST[i]))
    		elif(i.startswith("param")):
    			id=int(i.split("_")[1])
    			algParam=models.AlgParam.objects.get(pk=id)
    			paramsJs[algParam.gen_id]=request.POST[i]
    			params[id]=[models.stringToValue(request.POST[i],algParam.type),algParam.type]

    	tAlgs=models.AlgTemplate.objects.annotate(sCount=Count('strategies',distinct=True),pCount=Count('params',distinct=True)).filter(sCount=len(strategies),pCount=len(params))

    	for i in strategies:
    		tAlgs=tAlgs.filter(strategies=i)

    	for i in params.keys():
    		tAlgs=tAlgs.filter(params=i)

    	tAlg=None
    	if(tAlgs.count()>0):
    		tAlg=tAlgs[0]
    	else:
    		tAlg=models.AlgTemplate(name=algC.name,constructor=algC)
    		tAlg.save()
    		tAlg.strategies.add(*strategies)
    		tAlg.params.add(*list(params.keys()))

    	algs=models.Algorithm.objects.all()
    	for i in params.keys():
    		algs=algs.filter(paramofalg__param=i,**{"paramofalg__"+models.typeIdToFieldStr(params[i][1]):params[i][0]})

    	alg=None
    	if(algs.count()>0):
    		alg=algs[0]
    	else:
    		alg=models.Algorithm(template=tAlg)
    		alg.save()
    		for i in params.keys():
    			poa=models.ParamOfAlg(algorithm=alg,param=models.AlgParam.objects.get(id=i),**{models.typeIdToFieldStr(params[i][1]):params[i][0]})
    			poa.save()

    	data.append(slotsJs);
    	data.append(paramsJs);
    	programCode=cg.getCode(json.dumps(data))

    	implementations=models.AlgImplementation.objects.filter(algorithm=alg,author="Automatic")
    	impl=None
    	if(implementations.count()==0):
    		fileName=str(uuid.uuid1())+".cpp"
    		impl=models.AlgImplementation(algorithm=alg,author="Automatic",file=fileName,fileName="output.cpp")
    		impl.desc="Автоматически сгенерированный код"
    		impl.save()
    		file=open(programCodePath+fileName,"w")
    		file.write(programCode.decode("utf-8"))
    		file.close()
    	else:
    		impl=implementations[0]
    	
    	#response = HttpResponse(content_type='application/force-download')
    	#response['Content-Disposition'] = 'attachment; filename=output.cpp'
    	#response.write(programCode)
    	#response = HttpResponse(json.dumps({"id":impl.id}),content_type='application/json')
    	#return response;
    	return HttpResponseRedirect(reverse('impl', args=[impl.id])+"?download=1")