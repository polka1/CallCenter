"""borjomi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import logout, LoginView
from admin_panel.views import signup, index, profile, insert_data, check_data, i18n_javascript
from django.views.i18n import JavaScriptCatalog



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^signup/$', signup, name='signup'),
    url(r'^$', index, name='index'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^insert_data/$', insert_data, name='insert_data'),
    url(r'^check_data/$', check_data, name='check_data'),
    url(r'^admin/jsi18n', i18n_javascript),
    url('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'accounts/login/', LoginView.as_view()),
    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout')

    # url(r'^accounts/', include('django.contrib.auth.urls')),
]
