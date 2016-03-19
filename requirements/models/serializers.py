'''
Created on Feb 24, 2016

@author: Josh
'''
from rest_framework import serializers
from .project import Project
from django.db.models.query import QuerySet

class projectSerializer(serializers.HyperlinkedModelSerializer):
    
    ##projects = serializers.PrimaryKeyRelatedField(many=True, queryset=Project.objects.all())
    
    ##owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Project
        fields = ('title', 'description', 'owner')