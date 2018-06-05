""" URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from django.conf.urls import url
from api_v1 import views

urlpatterns = {
    url(r'^company/$', views.company),
    url(r'^recruit/$', views.recruit),
    url(r'^delete_c/$', views.delete_c),
    url(r'^delete_j/$', views.delete_j),
    url(r'^add_company/$', views.add_company),
    url(r'^get_token/$', views.get_token),
    url(r'^company_info/$', views.company_info),
    url(r'^add_job/$', views.add_job),
}
