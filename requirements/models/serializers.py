'''
Created on Feb 24, 2016

@author: Josh
'''
from rest_framework import serializers
from .project import Project
from .story import Story
from django.contrib.auth.models import User
from django.db.models.query import QuerySet

class projectSerializer(serializers.HyperlinkedModelSerializer):
    
    ##projects = serializers.PrimaryKeyRelatedField(many=True, queryset=Project.objects.all())
    
    ##owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Project
        fields = ('title', 'description', 'owner', 'id', 'users')
        
class userStorySerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Story
        fields = ('title', 'description','owner', 'project')
        
class userSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        
