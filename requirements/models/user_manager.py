from django.contrib.auth.models import User
from .user_association import UserAssociation
from .user_association import PERM_CREATE_STORY
from .user_association import PERM_EDIT_STORY
from .user_association import ROLE_OWNER
from functools import wraps
from django.http import HttpResponse
from django.dispatch.dispatcher import receiver
from django.conf import settings
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

# def createUser(request):

#     u = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
#     u.is_active = False
#     u.save()

#     return True


def getActiveUsers():
    return User.objects.filter(is_active=True)


def __hasRole(projectID, userID, roleName):
    assoc = __getAssoc(projectID, userID)
    if assoc.count() == 0:
        return False
    ua = assoc.first()
    return ua.get_permission(roleName)


def __getAssoc(projectID, userID):
    return UserAssociation.objects.filter(
        project__id=projectID, user__id=userID)


def isOwner(projectID, userID):
    assoc = __getAssoc(projectID, userID)
    if assoc.count() == 0:
        return False
    return ROLE_OWNER == assoc.first().role

# Decorator function that can be used to wrap a view method. The view method must take
# request and projectID as arguments. The decorator will redirect to
# a 401 screen if the user making a request does not have the passed in role on
# the project


def user_has_role(role):
    def _my_decorator(view_method):
        def _decorator(request, projectID, *args, **kwargs):
            if not __hasRole(projectID, request.user.id, role):
                return HttpResponse(
                    'You do not have permision to perform this function', status=401)
            return view_method(request, projectID, *args, **kwargs)
        return wraps(view_method)(_decorator)
    return _my_decorator

# Decorator function that can be used to wrap a view method. The view method must take
# request and projectID as arguments. The decorator will redirect to
# a 401 screen if the user making a request does not own the project


def user_owns_project():
    def _my_decorator(view_method):
        def _decorator(request, projectID, *args, **kwargs):
            if not isOwner(projectID, request.user.id):
                return HttpResponse(
                    'You do not have permision to perform this function', status=401)
            return view_method(request, projectID, *args, **kwargs)
        return wraps(view_method)(_decorator)
    return _my_decorator

# Decorator function that can be used to wrap a view method. The view method must take
# request and projectID as arguments. The decorator will redirect to
# a 401 screen if the user making a request does not have access to the project


def user_can_access_project():
    def _my_decorator(view_method):
        def _decorator(request, projectID, *args, **kwargs):
            if __getAssoc(projectID, request.user.id).count() == 0:
                return HttpResponse(
                    'You do not have permision to perform this function', status=401)
            return view_method(request, projectID, *args, **kwargs)
        return wraps(view_method)(_decorator)
    return _my_decorator


def canCreateStoryInProject(projectID, userID):
    return __hasRole(projectID, userID, PERM_CREATE_STORY)


def canEditStoryInProject(projectID, userID):
    return __hasRole(projectID, userID, PERM_EDIT_STORY)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
