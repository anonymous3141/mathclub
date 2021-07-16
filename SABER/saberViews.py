from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseServerError
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from db.models import Quiz, Question, UserProblemVerdict
from db.models import User, questionToJson, quizToJson
from django.db.models import Sum
from django.core.paginator import Paginator
import json

def bonk():
    # user did something evil / stupid
    return HttpResponseRedirect(reverse('quizHome'))

@login_required
def questionCreator(request):
    if not request.user.is_superuser:
        return bonk()
    ctx={'edit': False,
         'target': None}
    return render(request, "SABER/questionCreator.html", ctx)

@login_required
def questionEditor(request, editId):
    if not request.user.is_superuser:
        return bonk()
    try:
        target = Question.objects.get(id = editId)
        target.questionHTML = target.questionHTML.replace('\\','\\\\') #stupid escape characters
        target.options = target.options.replace('\\','\\\\') #stupid escape characters
        print(target.questionHTML)
        ctx={'edit': True,
             'target': target}
        return render(request, "SABER/questionCreator.html", ctx)
    except:
        # question not found
        return bonk()


@login_required
def saberHome(request):
    if not request.user.is_superuser:
        return bonk()

    return render(request, "SABER/saberHome.html")

QUESTIONS_PER_PAGE = 20
QUIZ_PER_PAGE = 20

@login_required
def questionList(request, page = 1):
    if not request.user.is_superuser:
        return bonk()
    
    questionSet = Paginator(Question.objects.order_by("id"), QUESTIONS_PER_PAGE)
    #print([json.dumps(questionToJson(c)) for c in questionSet.page(page)])
    if page < 0 or page > questionSet.num_pages:
        return bonk()

    ctx  = {"questionList" : [json.dumps(questionToJson(c)) for c in questionSet.page(page)],
    "pageNum" : page,
    "totalPages" : questionSet.num_pages}
    return render(request, "SABER/questionList.html",ctx)

# todo: implement quiz HTML
def questionSetting(request, quizId, page = 1):
    # For each quiz choose questions
    if not request.user.is_superuser:
        return bonk()

    questionSet = Paginator(Question.objects.order_by("id"), QUESTIONS_PER_PAGE)
    if page < 0 or page > questionSet.num_pages:
        return bonk()

    if not Quiz.objects.filter(id = quizId).exists():
        return bonk()

    adjustedJson = []
    thisQuiz = Quiz.objects.get(id = quizId)
    for c in questionSet.page(page):
        questionJson = questionToJson(c) 
        questionJson['inUse'] = thisQuiz.questionList.filter(id = c.id).exists()
        adjustedJson.append(questionJson)
    ctx  = {"questionList" : adjustedJson,
    "pageNum" : page,
    "totalPages" : questionSet.num_pages,
    "quizId" : quizId,
    "quizName": Quiz.objects.get(id = quizId).name,
    "thisQuiz": thisQuiz
    }

    return render(request, "SABER/questionSetting.html", ctx)

def quizList(request, page = 1):
    # List quiz
    if not request.user.is_superuser:
        return bonk()

    quizSet = Paginator(Quiz.objects.order_by("id"), QUIZ_PER_PAGE)

    if page < 0 or page > quizSet.num_pages:
        return bonk()

    ctx  = {"quizList" : [quizToJson(c) for c in quizSet.page(page)],
            "pageNum" : page,
            "totalPages" : quizSet.num_pages
    }
    print(ctx)
    return render(request, "SABER/quizList.html", ctx)


def quizLeaderboards(request, quizId):
    if not request.user.is_superuser:
        return bonk()

    thisQuiz = Quiz.objects.get(id = quizId)
    # 0 - 1 scoring at the moment
    # user__username is the username property of the Foreign (one to many) key "user", fetching the username
    # .values makes a dict with only 1 entry, namely the username
    # .annotate adds a temporary attribute to the query set, in this case problem__count (autogens name)
    # Sum(problem_weight) sums problem weight
    # order_by does a sort. The - means sort descending not ascending
    users = UserProblemVerdict.objects.filter(verdict = "CORRECT", quiz=thisQuiz).\
            values("user__username").\
                annotate(Sum("problem__weight")).\
                    order_by("-problem__weight__sum")
    
    questionList = thisQuiz.questionList.order_by("id")
    ctxUser = []

    for user in users:
        username = user['user__username']
        relevantVerdicts = UserProblemVerdict.objects.\
            filter(quiz=thisQuiz, user__username = username).order_by("problem__id").\
                values("id", "verdict","problem__id")
        userVerdicts = []
        for i in range(questionList.count()):
            print(questionList[i].id, relevantVerdicts[i]["id"])
            if int(questionList[i].id) != int(relevantVerdicts[i]["problem__id"]):
                userVerdicts.append("INCORRECT")
            else:
                userVerdicts.append(relevantVerdicts[i]["verdict"])
        print(userVerdicts)
        ctxUser.append({"user": username, 
        "userVerdicts": userVerdicts, 
        "score": user['problem__weight__sum']})
    
    numCorrect = [UserProblemVerdict.objects.filter(verdict = "CORRECT", quiz=thisQuiz,
    problem=c).count() for c in questionList]
    ctx = {"ctxUser": ctxUser,
    "numCorrect": numCorrect,
    "numProblems": len(numCorrect),
    "thisQuiz": thisQuiz}

    return render(request, "SABER/quizLeaderboards.html", ctx)

    
    