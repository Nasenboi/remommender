"""
URL configuration for remommender project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from ninja import NinjaAPI

from apps.recommendations.api import router as recommendations_router
from apps.session.api import router as session_router
from apps.test.api import router as test_router

api = NinjaAPI()
api.add_router("/recommend/", recommendations_router)
api.add_router("/session/", session_router)
api.add_router("/test/", test_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", api.urls),
]
