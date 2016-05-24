from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from . import serializers
from . import models

class AlgConstructorList(APIView):
    def get(self, request, format=None):
        algConstructors = models.AlgConstructor.objects.all()
        if("ids" in request.GET):
            algConstructors=algConstructors.filter(id__in=request.GET["ids"].split(","))
        serializer = serializers.AlgConstructorSerializer(algConstructors, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.AlgConstructorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AlgConstructorDetail(APIView):
    def get_object(self, pk):
        try:
            return models.AlgConstructor.objects.get(pk=pk)
        except models.AlgConstructor.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        algConst = self.get_object(pk)
        serializer = serializers.AlgConstructorSerializer(algConst)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        algConst = self.get_object(pk)
        serializer = serializers.AlgConstructorSerializer(algConst, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        algConst = self.get_object(pk)
        algConst.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AlgParamList(APIView):
    def get(self, request, format=None):
        objects = models.AlgParam.objects.all()
        if("ids" in request.GET):
            objects=objects.filter(id__in=request.GET["ids"].split(","))
        if("strategies" in request.GET):
            objects=objects.filter(strategy__in=request.GET["strategies"].split(","))
        if("name" in request.GET):
            objects=objects.filter(name__contains=request.GET["name"])
        serializer = serializers.AlgParamSerializer(objects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.AlgParamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AlgParamDetail(APIView):
    def get_object(self, pk):
        try:
            return models.AlgParam.objects.get(pk=pk)
        except models.AlgParam.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = serializers.AlgParamSerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = serializers.AlgParamSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SlotList(APIView):
    def get(self, request, format=None):
        objects = models.Slot.objects.all()
        if("ids" in request.GET):
            objects=objects.filter(id__in=request.GET["ids"].split(","))
        serializer = serializers.SlotSerializer(objects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.SlotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SlotDetail(APIView):
    def get_object(self, pk):
        try:
            return models.Slot.objects.get(pk=pk)
        except models.Slot.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = serializers.SlotSerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = serializers.SlotSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StrategyList(APIView):
    def get(self, request, format=None):
        objects = models.Strategy.objects.all()
        if("ids" in request.GET):
            objects=objects.filter(id__in=request.GET["ids"].split(","))
        if("name" in request.GET):
            objects=objects.filter(name__contains=request.GET["name"])
        if("slots" in request.GET):
            objects=objects.filter(slot__in=request.GET["slots"].split(","))
        serializer = serializers.StrategySerializer(objects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.StrategySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StrategyDetail(APIView):
    def get_object(self, pk):
        try:
            return models.Strategy.objects.get(pk=pk)
        except models.Strategy.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = serializers.StrategySerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = serializers.StrategySerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)