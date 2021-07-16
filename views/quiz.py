from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseServerError
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.decorators import login_required
from db.models import Quiz, Question, UserProblemVerdict, TYPEDICT, MC_DELIMITOR

from django.core.paginator import Paginator
import os, json
from views.quizUtility import judge

ENTRIES_PER_PAGE = 25

# unit tests
from datetime import datetime

def nuke():
    #for testing purposes
    #dangerous
    UserProblemVerdict.objects.all().delete()
    Quiz.objects.all().delete()
    Question.objects.all().delete()

def unitTestingcapkek():

    if Question.objects.all().count() == 0:
        dummyQuestion = Question(questionHTML="Whats $9+10$")
        dummyQuestion.correctAnswer = "21"
        dummyQuestion.save()

        dummyQuestion2 = Question(questionHTML="Let $a,b$ be roots of the <b> equation </b> $x^2+3x+2=0$. Find $a+b$")
        dummyQuestion2.correctAnswer = "1" # the correct answer as 1 indexed position
        dummyQuestion2.answerType = "mc"
        dummyQuestion2.options = MC_DELIMITOR.join(['a. -3', 'b -5', 'c -2', 'd -1', 'e 3'])
        #dummyQuestion2.quiz_id = dummyQuizId
        dummyQuestion2.save()
        print(Question.objects.all().count(), "DEBUG unit testing")
        dummyQuiz = Quiz(date=datetime.now(), name="dummyQuiz",
        description="lets hope this bloody works", visible=True)
        dummyQuiz.save()
        dummyQuiz.questionList.add(Question.objects.all()[0])
        dummyQuiz.questionList.add(Question.objects.all()[1])

    #dummyQuiz = Quiz.objects.get(id = 1)
    #dummyQuiz.questionList.add(Question.objects.get(id=1))
    #dummyQuiz.questionList.add(Question.objects.get(id=2))
    #print(Quiz.objects.get(id=1).questionList)
    #print(Question.objects.get(id=1).question_set.all())
    #QTOFIX = Question.objects.get(id=2)
    #QTOFIX.options = MC_DELIMITOR.join(['-3', '-5', '-2', '-1', '3'])
    #QTOFIX.correctAnswer = "1" #
    #QTOFIX.save()


@login_required
def quizHome(request, page = 1):
    # if not registered login_required decorator
    # bonks the anonymous users back to home

    #get all quizes

    #debug
    #nuke()
    unitTestingcapkek()

    quizSet = Paginator(Quiz.objects.filter(visible=True).
    order_by('date'), ENTRIES_PER_PAGE)
    if page > quizSet.num_pages or page < 1:
        # automatic redirect
        page = 1

    ctx  = {"quizList" : quizSet.page(page),
    "pageNum" : page,
    "totalPages" : quizSet.num_pages}
    return render(request, "quizList.html",ctx)

#todo: refactor getQuiz
#todo: implement viewing done quiz

@login_required1
def getQuiz(request, quizId = 0):
    # if not registered the login_required bonks the users back Home
    # order by ID, temporary until we implement custom ordering
    questionSet = Quiz.objects.get(id = quizId).questionList.all().order_by('id')
    # First, add rendering ability
    # todo: answering and marking
    # todo: custom question ordering
    # todo: judge by post request to another site, rendering results and redirect
    # assume: the amount of questions doesn't need paginating
    # todo: scoring has not been implemented
    quizResult = UserProblemVerdict.objects.filter(user = request.user)\
    .filter(quiz_id = quizId)

    parsedQs = []
    qId = 1
    totalWeight= 0
    userScore = 0
    for question in questionSet:
        toRender = {}
        toRender['id'] = str(qId)
        toRender['questionHTML'] =question.questionHTML
        toRender['answerType'] = question.answerType
        if TYPEDICT[question.answerType] == 'multichoice':
            # option[0] is id of option, option[1] is HTML
            # +1 to 1 index
            optionList = question.options.split(MC_DELIMITOR)
            toRender['options'] = [[str(c+1), optionList[c]] for c in range(len(optionList))]
        else:
            pass # do nothing

        if len(quizResult) != 0:
            # quiz has already been attempted
            problemAttempt = quizResult.get(problem = question)
            toRender['studentOutput'] = problemAttempt.response
            toRender['judgeVerdict'] = problemAttempt.verdict
            print("DEBUG RESULT",problemAttempt.response,problemAttempt.verdict)
        toRender['weight'] = question.weight
        parsedQs.append(toRender)
        qId += 1
        totalWeight += question.weight
        userScore += judge.evalScore(problemAttempt.verdict) * question.weight
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
    # todo: store results
    # todo: hide submit button when request returned
    if request.method != "POST" or request.user.is_anonymous:
        # bonk goto home
        return redirect(request, "")

    answers = json.loads(request.body)
    print(answers)

    qId = int(answers['quizId'])
    questionSet = Quiz.objects.get(id = qId).questionList.all().order_by('id')
    numQs = len(questionSet)

    for i in range(1,numQs+1):
        # currently judging is just naive compare
        # lets hope blank mc and ia is fine
        result = UserProblemVerdict(user = request.user, quiz_id = qId,
        problem_id = questionSet[i-1].id, response = answers[str(i)],\
        verdict = judge.compareText(answers[str(i)], questionSet[i-1].correctAnswer))
        result.save()


    return HttpResponse(200)
