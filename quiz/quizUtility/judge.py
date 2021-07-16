from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseServerError
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.decorators import login_required
from db.models import Quiz, Question, TYPEDICT, MC_DELIMITOR

from django.core.paginator import Paginator
import os, json

ACCEPTED = "CORRECT"
WRONG_ANSWER = "INCORRECT"

# scorer
# return value in [0,1]. Problem score is val * weight
# partial marks are contained in verdict as percentage
def evalScore(verdict):
    if verdict == ACCEPTED:
        return 1
    elif verdict == WRONG_ANSWER:
        return 0

# whitediff comparison
def compareText(studentOutput, correctAnswer):
    print("judging", studentOutput, correctAnswer)
    if studentOutput.replace(" ", "").replace("\n","") ==\
    correctAnswer.replace(" ", "").replace("\n",""):
        return ACCEPTED
    else:
        return WRONG_ANSWER
