from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseServerError
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django import forms
from db.models import Quiz, UserProblemVerdict
from django.db.models import F, Sum
import os

TEST_MESSAGE = "$x^2+5x+6$ warrant officer mizuki send message <br> <b>tora tora tora</b>"
def home(request):
    ctx={'text':TEST_MESSAGE}
    return render(request, "home.html", ctx)

def globalLeaderboards(request):
    # F() turns a database field into a usable variable

    list_users = UserProblemVerdict.objects.filter(verdict = "CORRECT").\
            values("user__username").\
                annotate(total_score = Sum(F("problem__weight")*F("quiz__quizWeight"))).\
                    order_by("-total_score")
    
    return render(request, "globalLeaderboards.html", {"ctxUser":list_users})