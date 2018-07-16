"""mysite URL Configuration

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
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include, url
import analytics.views as AnalyticsViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dublinbus/', include('dublinbus.urls')),
    path('analytics/', AnalyticsViews.Analytics.as_view()),
    path('analytics_get_lines/', AnalyticsViews.Analytics.as_view(method='get_lines')),
    path('analytics_get_available_days/', AnalyticsViews.Analytics.as_view(method='get_available_days')),
    path('analytics_get_arrivaltime/', AnalyticsViews.Analytics.as_view(method='get_arrivaltime')),
    path('analytics_get_stoppointids/', AnalyticsViews.Analytics.as_view(method='get_stoppointids')),
]
