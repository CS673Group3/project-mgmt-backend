from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.contrib.auth.models import User
#import models
import django.contrib.auth
#import userManager
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required
#from forms import NewProjectForm, AddUserForm

#from forms import registrationForm
from django import forms

from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from requirements.models.project import Project
from requirements.models.serializers import projectSerializer
from requirements.models.serializers import userStorySerializer
from requirements.models.serializers import userSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from requirements.models import project_api
from requirements.models.story import Story as aStory
from rest_framework.authentication import SessionAuthentication,\
    BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from nt import link

## Django REST framework classes...
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all() 
    serializer_class = projectSerializer
    
class userStoryViewSet(viewsets.ModelViewSet):
    queryset = aStory.objects.all() 
    serializer_class = userStorySerializer
    
class currentUserViewSet(viewsets.ViewSet):
    #serializer_class = userStorySerializer
    
    def userInfo(self, request, userName=None):
        serializer_context = {
            'request': request,
        }

        if userName is None:
            queryset = User.objects.all()
        else:
            queryset = project_api.get_current_user_by_username(userName)
            
        serializer = userSerializer(queryset,context=serializer_context, many=True)
        return Response(serializer.data)
    
    def userProjects(self, request, userName, projectID=None):
        serializer_context = {
            'request': request,
        }
        if userName is not None:
            if projectID is None:   
                userID = project_api.get_user_id(userName)
                queryset = project_api.get_projects_for_user(userID)
            else:
                queryset = Project.objects.filter(id = projectID)
        #queryset = project_api.get_all_projects()
        serializer = projectSerializer(queryset,context=serializer_context, many=True)
        return Response(serializer.data)
        
    def userStories(self,request, userName, projectID):
        serializer_context = {
            'request': request,
        }
        
        if userName is not None and projectID is not None:
            project = project_api.get_project(projectID)
            queryset = project_api.get_stories_for_projects(project)
            serializer = userStorySerializer(queryset,context=serializer_context, many=True)
        return Response(serializer.data)
        
class ProjectList(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = projectSerializer
    
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.USER)
    
class ProjectDetail(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = projectSerializer
    
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content=JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
        
def project_list(request):
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = projectSerializer(projects, many=True)
        return JSONResponse(serializer.data)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = projectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.data, status=400)
   
def userStory_list(request):
        projectID = request.GET.get('projectid','')
        serializer_context = {
            'request': request,
        }
        if projectID == '':
            stories = aStory.objects.all()                               
            serializer = userStorySerializer(stories,context=serializer_context, many=True)
            return Response(serializer.data)
    
        project = project_api.get_project(projectID)    
        if request.method == 'GET':
            if projectID == None:
                stories = aStory.objects.all()                               
                serializer = userStorySerializer(stories,context=serializer_context, many=True)
                return JSONResponse(serializer.data)
            #stories = aStory.get_stories_for_project(project
            stories = aStory.objects.filter(project_id=project.id)                               
            serializer = userStorySerializer(stories,context=serializer_context, many=True)
            return JSONResponse(serializer.data)
        elif request.method == 'POST':
            data = JSONParser().parse(request)
            serializer = userStorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JSONResponse(serializer.data, status=201)
            return JSONResponse(serializer.data, status=400)

    
class ExampleView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    
    def __init__(self, data, **kwargs):
        content=JSONRenderer().render(data)
    
    def get(self, request, format=None):
        content = {
                   'user': request.user,
                   'auth': request.auth
            }
        return Response(content)