from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden, HttpResponseServerError
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.decorators import login_required
from db.models import Quiz, Question, UserProblemVerdict, MC_DELIMITOR, questionToJson
from db.models import Profile
from django.urls import reverse
from django.core.paginator import Paginator
import os, json
from .quizUtility import judge

ENTRIES_PER_PAGE = 25

# unit tests
from datetime import datetime

@login_required
def quizHome(request, page = 1):
    # if not registered login_required decorator
    # bonks the anonymous users back to home

    #get all quizes
    quizSet = Paginator(Quiz.objects.filter(visible=True).
    order_by('date'), ENTRIES_PER_PAGE)
    ctx  = {"quizList" : quizSet.page(page),
    "pageNum" : page,
    "totalPages" : quizSet.num_pages}
    return render(request, "quizList.html",ctx)

def quizScore(quizId, user):

    quizResult = UserProblemVerdict.objects.filter(user = user)\
    .filter(quiz_id = quizId)
    score = 0

    for result in quizResult:
        score += judge.evalScore(result.verdict) *result.problem__weight
    return score

@login_required
def getQuiz(request, quizId = 0):
    # if not registered the login_required bonks the users back Home
    # order by ID, temporary until we implement custom ordering
    thisQuiz = Quiz.objects.get(id = quizId)

    if thisQuiz.visible == False:
        return HttpResponseRedirect(reverse('quizHome'))
    
    questionSet = thisQuiz.questionList.all().order_by('id')
    # todo: custom question ordering
    # assume: the amount of questions doesn't need paginating
    quizResult = UserProblemVerdict.objects.filter(user = request.user)\
    .filter(quiz_id = quizId)

    parsedQs = []
    totalWeight= 0
    userScore = 0
    for question in questionSet:
        toRender = questionToJson(question)
        if len(quizResult) != 0:
            # quiz has already been attempted
            toRender['studentOutput'] = ""
            toRender['judgeVerdict'] = 'INCORRECT'
            if quizResult.filter(problem = question).exists():
                problemAttempt = quizResult.get(problem = question)
                toRender['studentOutput'] = problemAttempt.response
                toRender['judgeVerdict'] = problemAttempt.verdict
                print("DEBUG RESULT",problemAttempt.response,problemAttempt.verdict)
                userScore += judge.evalScore(problemAttempt.verdict) * question.weight
        parsedQs.append(toRender)
        totalWeight += question.weight

    # print(parsedQs, Question.objects.all())
    ctx ={'quizId' : quizId,
    'qList' : parsedQs,
    'numQs' : len(parsedQs),
    'isDone' : (len(quizResult) > 0),
    'totalWeight': totalWeight,
    'userScore': userScore} #add quiz ID
    #print(ctx)
    return render(request, "quiztemplate.html", ctx)

@login_required
def gradeQuiz(request):
    # recieve ajax data from quiz
    if request.method != "POST" or request.user.is_anonymous:
        # bonk goto home
        return HttpResponseRedirect(reverse('quizHome'))

    answers = json.loads(request.body)
    print(answers)

    qId = int(answers['quizId'])
    questionSet = Quiz.objects.get(id = qId).questionList.all().order_by('id')

    if not Quiz.objects.get(id = qId).visible:
        # quiz is hidden, bonk
        return HttpResponse(200)

    quizScore = 0

    preExistingResult = UserProblemVerdict.objects.filter(user = request.user)\
    .filter(quiz_id = qId).exists()

    if preExistingResult:
        #bonk do nothing
        return HttpResponse(200)

    numQs = len(questionSet)

    for questionId, questionResponse in answers.items(): #python 3.x
        # currently judging is just naive compare
        # lets hope blank mc and ia is fine
        print(questionId, questionResponse)
        if not questionId.isdigit():
            #only consider positive integers
            continue
        result = UserProblemVerdict(user = request.user, quiz_id = qId,
        problem_id = int(questionId), response = questionResponse,\
        verdict = judge.compareText(questionResponse, questionSet.get(id=int(questionId)).correctAnswer))
        quizScore += judge.evalScore(result.verdict) * questionSet.get(id=int(questionId)).weight

        result.save()

    #screw user profiles I can do without them

    return HttpResponse(200)
