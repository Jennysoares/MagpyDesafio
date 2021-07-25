from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError

from .models import Project,PackageRelease
from .serializers import ProjectSerializer
from drf_yasg.utils import swagger_auto_schema
import requests

class ProjectViewSet(viewsets.ModelViewSet):
    class Meta: model = Project, fields = ('name', 'packages')

    def get_serializer_class(self):
        return ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()
    
    def checkPackage(self, packages):
        request_extern = None
        validation = True
        final_packages = []

        for package in packages:
                version = False
                name_package = package['name']
                url = f'https://pypi.org/pypi/{name_package}'

                if 'version' in package.keys():
                    url = url + '/' + package['version']
                    version = True
                url = url + '/json'

                try:
                    request_extern = requests.get(url)
                    if request_extern.status_code == 200:
                        pac = package
                        if version == False:
                            json_package = request_extern.json()
                            pac =  {"name": name_package,"version": json_package['info']['version']} 

                        final_packages.append(pac)          
                    else:
                        validation = False
                except:
                    return Response({"error":"Can't connect with PyPI API"}, status=status.HTTP_400_BAD_REQUEST)

        return [validation, final_packages]


    def list(self, request):
        """ Retorna todos os projetos existentes"""
        serializer = ProjectSerializer(self.get_queryset(), many=True)
        if len(serializer.data) > 0:
            return Response(serializer.data)
        else:
            return Response({"message": "No projects registered"},status=status.HTTP_204_NO_CONTENT)

        
    def create(self, request):
        """ Insere um novo projeto"""
        validated_data = request.data
        serializer_class = ProjectSerializer(data=validated_data)
        
        if serializer_class.is_valid():
           
            validation, final_packages = self.checkPackage(validated_data['packages']) 
                
            if validation:
                pk_project = Project.objects.create(name=validated_data['name'])

                for package in final_packages:
                    PackageRelease.objects.create(name=package['name'], version=package['version'], project=pk_project)
                
                serializer = ProjectSerializer(pk_project)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            else:
                return Response({"error":"One or more packages doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST) 

    
    def update(self, request, pk=None):
        """ Atualiza um projeto existente """
        try:
            obj = Project.objects.get(name=pk)
            validation, final_packages = self.checkPackage(request.data['packages'])
            if validation: 
                PackageRelease.objects.filter(project=obj).delete()

                obj.name = request.data['name']
                obj.save()

                for package in final_packages:
                    PackageRelease.objects.create(name=package['name'], version=package['version'], project=obj)

                serializer = ProjectSerializer(obj)
                return Response(serializer.data, status=status.HTTP_200_OK)

            else:
                return Response({"error":"One or more packages doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
            
        except Project.DoesNotExist:
            return Response({"message":"Project does not exist"}, status=status.HTTP_404_NOT_FOUND)
        

    def retrieve(self, request, pk=None):
        """ Retorna um projeto específico"""
        try:
            obj = Project.objects.get(name=pk)
            serializer = ProjectSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({"message":"Project does not exist"}, status=status.HTTP_404_NOT_FOUND)


    def destroy(self, request, pk=None):
        """ Deleta um projeto existente"""
        try:
            obj = Project.objects.get(name=pk)
            obj.delete()
            return Response({"message":"Project has been deleted successfully"},status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({"message":"Project does not exist"}, status=status.HTTP_404_NOT_FOUND)