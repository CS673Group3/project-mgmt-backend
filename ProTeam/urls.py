from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from requirements.views import users
from requirements.views import home
from requirements import req_urls
from rest_framework import routers, serializers, viewsets
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as rest_views
from rest_framework_jwt.views import obtain_jwt_token
from comm import views
from requirements.views import views as rqmt_views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'rooms', views.RoomViewSet)
router.register(r'messages', views.MessageViewSet)
router.register(r'messagesearch', views.MessageSearchSet)
router.register(r'messagedata', views.MessageDataViewSet)
router.register(r'roomuser', views.UserRoomViewSet)
router.register(r'roomuserdata', views.UserRoomDataViewSet)
router.register(r'projects', rqmt_views.ProjectViewSet)
#router.register(r'userstories', rqmt_views.userStoryViewSet )
#router.register(r'currentuser', rqmt.views.currentUserViewSet)

UserDetails = rqmt_views.currentUserViewSet.as_view({
    'get': 'userInfo'
})

UserProjects = rqmt_views.currentUserViewSet.as_view({
    'get': 'userProjects'
})

UserStories = rqmt_views.currentUserViewSet.as_view({
    'get': 'userStories'
}) 

urlpatterns = [
                        url(r'^signin', users.signin),
                        url(r'^signout', users.signout),
                        url(r'^signup', users.signup),
                        url(r'^req/', include(req_urls)),
                        url(r'^admin/',include(admin.site.urls)),
                        url(r'^$', home.home_page),
                        url(r'^communication/',include('comm.urls')),
                        url(r'^issue_tracker/',include('issue_tracker.urls')),
                        url(r'^admin/doc/',include('django.contrib.admindocs.urls')),
                        url(r'^api/', include(router.urls)),
                        
                        url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                        url(r'^get-token/', obtain_jwt_token),
                        url(r'^example/', rqmt_views.ExampleView),
                       # url(r'^admin/', include(admin.site.urls)),
                        #url('^api/userstories/(?P<projectID>\d+)/', rqmt_views.userStory_list),
                        url(r'^api/userstories$', rqmt_views.userStory_list),
                        url(r'^api/users/$',UserDetails),
                        url(r'^api/(?P<userName>\w+)/$',UserDetails,name = 'user-details'),
                        url(r'^api/(?P<userName>\w+)/projects/$',UserProjects,name = 'user-projects'),
                        url(r'^api/(?P<userName>\w+)/projects/(?P<projectID>\d+)/$',UserProjects,name = 'user-project-details'),
                        url(r'^api/(?P<userName>\w+)/projects/(?P<projectID>\d+)/userstories/$',UserStories,name = 'user-stories'),
                        url(r'^apisignup/', rqmt_views.signUp),
                      ]
