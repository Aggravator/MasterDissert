from . import models
from rest_framework import routers, serializers, viewsets

class AlgConstructorSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.AlgConstructor
		fields = ('id', 'gen_id', 'data', 'desc')

class AlgParamSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.AlgParam
		fields = ('id', 'gen_id', 'name', 'desc','type')

class SlotSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Slot
		fields = ('id', 'gen_id', 'name', 'desc')

class StrategySerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Strategy
		fields = ('id', 'gen_id', 'name', 'desc','slot')

class AlgTemplateSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.AlgTemplate
		fields = ('id', 'name', 'desc','constructor','strategies','params')

class AlgorithmSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Algorithm
		fields = ('id', 'template', 'desc','constructor','strategies','params')