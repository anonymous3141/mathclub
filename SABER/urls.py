"""mathclub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import include, path
from django.conf.urls import url
from . import saberViews, saberCommands

urlpatterns = [
    path('', saberViews.saberHome, name="saberHome"),
    path('questionlist/<int:page>', saberViews.questionList, name="questionList"),
    path('quizlist/<int:page>', saberViews.quizList, name = "quizList"),
    path('questionsetting/<int:quizId>/<int:page>', saberViews.questionSetting, name = 'questionSetting'),
    path('quizleaderboards/<int:quizId>', saberViews.quizLeaderboards, name = "quizLeaderboards"),
    path('parse', saberCommands.parseCommands, name = "saberParser")
]

#These paths are depreciated:
    #path('questionCreator', saberViews.questionCreator, name="questionCreator"),
    #path('questionEditor/<int:editId>',saberViews.questionEditor,name="questionEditor"),