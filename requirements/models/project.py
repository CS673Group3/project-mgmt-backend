from django.db import models
from django.contrib.auth.models import User
from .base import ProjMgmtBase
#from .story import Story as story_model


class Project(ProjMgmtBase):
    # todo add stories

    owner = models.ForeignKey('auth.User', related_name='Project', null=True)

    users = models.ManyToManyField(User, through='UserAssociation')
    
    #def __id__(self):
        #return self.ID

    def __str__(self):
        return self.title
    
    def __repr__(self):
        return 'Project: %s' % self.title

    def description_as_list(self):
        return self.description.split('\n')
    
    #def save(self, *args, **kwargs):
        

    class Meta:
        permissions = (
            ("own_project", "Can own and create projects"),
        )

        app_label = 'requirements'
