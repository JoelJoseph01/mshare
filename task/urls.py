"""task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from mshare import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('signupuser/',views.signupuser,name='signupuser'),
    path('login/',views.login,name="loginuser"),
    path('logout/',views.logoutuser,name='logoutuser'),
    path('profile/',views.profile,name='profile'),
    path('add/',views.add,name='add'),
    path('obj/<int:pk>/', views.detail, name='detail'),
    path('items/',views.items,name='items'),
    path('search/',views.search,name='search'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('change_done/',views.change_done,name='change_done'),
    # """ path('data/<int:pk>', views.view, name='view'),
    # path('data/<int:pk>/delete',views.delete,name='delete')
    # """
    url(r'^profile/view/(?P<pk>\d+)/$',views.profile, name='profile_with_pk'), 
    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$',views.change_friends,name='change_friends'),
    url(r'^profile/others/$',views.others, name='others'),                                     
    url(r'^profile/friends/$',views.friends, name='friends'),

]

