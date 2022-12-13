"""settings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static


# def home(request):
#     if request.user.is_authenticated:
#         return redirect("home/")
#     return redirect("auth/login")


# urlpatterns = i18n_patterns(
urlpatterns = [
    path('', include('fixtureApp.urls')),
    path('pays/', include('competitionApp.urls')),
    path('predicition/', include('predictionApp.urls')),
    path('stats/', include('statsApp.urls')),
    # path('', home),
    # path('auth/', include('authApp.urls')),
    # path('core/', include('coreApp.urls')),
    # path('home/', include('fixtureApp.urls')),

    # path('boutique/', include('fixtureApp.urls_boutique')),
    # path('fabrique/', include('fixtureApp.urls_fabrique')),
    # path('manager/', include('fixtureApp.urls_manager')),

    # path('tresorerie/', include('comptabilityApp.urls')),

    # path('fiches/', include('ficheApp.urls')),
    # path('administration/', include('administrationApp.urls')),
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# handler404 = 'auth.views.handler404'
# handler400 = 'auth.views.handler400'
# handler500 = 'auth.views.handler500'