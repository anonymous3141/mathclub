from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseServerError
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from db.models import Quiz, Question, UserProblemVerdict
from db.models import TYPEDICT, MC_DELIMITOR, questionToJson, quizToJson
from django.core.paginator import Paginator
from django.http import QueryDict
from datetime import datetime
import json

ALLOWED_COMMANDS = ['saveQuestion', 'editQuestion', 'getQuestion',\
     'createQuiz', 'toggleQuiz', 'editQuiz', 'getQuiz', 'clearUserProblemInfo'] 

COMMAND_NOT_FOUND = "Server error: Command Not Found"
GENERIC_ERROR = "Server error: unknown error happened"
ARGUMENT_NOT_FOUND = "Server error: Argument not found"
DATABASE_ERROR = "Server error: Database error or invalid input"
INVALID_QUERY = "Server error: Invalid database query"
SUCCESS_MSG = "Operation successful"

# Post handlers
def saveOrEditQuestion(args, isEdit):
    #args is dictionary
    #validate input then save args
    #todo: support multichoice
    REQUIRED_ARGUMENTS = ['questionHTML', 'correctAnswer', 'weight',
    'answerType', 'options']
    newQuestion = Question()
    if isEdit:
        if args.get("id",ARGUMENT_NOT_FOUND) == ARGUMENT_NOT_FOUND:
            return HttpResponse(ARGUMENT_NOT_FOUND)
        else:
            try:
                newQuestion = Question.objects.get(id = int(args["id"]))
            except:
                return HttpResponse(DATABASE_ERROR)


    args['options'] = MC_DELIMITOR.join(args['options'])

    for arg in REQUIRED_ARGUMENTS:
        if args.get(arg,ARGUMENT_NOT_FOUND) == ARGUMENT_NOT_FOUND:
            return HttpResponse(ARGUMENT_NOT_FOUND)
        print("newQuestion.{} = args['{}']".format(arg,arg))
        exec("newQuestion.{} = args['{}']".format(arg,arg))

    newQuestion.save()
    return HttpResponse(SUCCESS_MSG)

def saveQuestion(args):
    return saveOrEditQuestion(args, False)

def editQuestion(args):
    return saveOrEditQuestion(args, True)

def createOrEditQuiz(args, edit = True):
    #try:
        REQUIRED_ARGUMENTS = ['name','description','quizResources', 'quizWeight']
        newQuiz = None 
        if edit:
            newQuiz = Quiz.objects.get(id = int(args['id']))
        else:
            newQuiz = Quiz()

        if edit == False:
            # set date of creation
            newQuiz.date = datetime.now()

        for arg in REQUIRED_ARGUMENTS:
            if args.get(arg,ARGUMENT_NOT_FOUND) == ARGUMENT_NOT_FOUND:
                return HttpResponse(ARGUMENT_NOT_FOUND)
            exec("newQuiz.{} = args['{}']".format(arg,arg))
        newQuiz.save()
        return HttpResponse(SUCCESS_MSG)
    #except:
    #    return HttpResponse(DATABASE_ERROR)    

def createQuiz(args):
    return createOrEditQuiz(args, False)

def editQuiz(args):
    return createOrEditQuiz(args, True)

def toggleQuiz(args):
    #try:
        questionId = int(args['questionId'])
        quizId = int(args['quizId'])
        quiz = Quiz.objects.get(id = quizId)
        if not Question.objects.filter(id = questionId).exists():
            pass
        elif quiz.questionList.filter(id=questionId).exists():
            quiz.questionList.remove(Question.objects.get(id = questionId))
        else:
            quiz.questionList.add(Question.objects.get(id = questionId))
        
        if args.get("toggleVisibility", "-1") != "-1":
            if quiz.visible:
                quiz.visible = False
            else:
                quiz.visible = True
        quiz.save()

        return HttpResponse(SUCCESS_MSG)    
    #except:
    #    return HttpResponse(DATABASE_ERROR)

def clearUserProblemInfo(args):
    #try:
        command = args['operationType']
        args['quizId'] = int(args['quizId'])
        if command == "DELETE_ALL":
            # dangerous!
            UserProblemVerdict.objects.all().delete()
        if command == "DELETE_QUIZ":
            # less dangerous!
            # deletes everything in queryset
            UserProblemVerdict.objects.filter(quiz__id = args['quizId']).delete()
        
        if command == "DELETE_USER_QUIZ":
            #mainly for testing
            UserProblemVerdict.objects.filter(quiz__id = args['quizId'],
            user__username = args['username']).delete()
        
        return HttpResponse(SUCCESS_MSG)    
    #except:
    #    return HttpResponse(DATABASE_ERROR)

#get handlers
def getQuestion(args):
    #input question id
    #output question json in string
    print("Get Question", args)
    question = None
    try:
        question = Question.objects.get(id = int(args["qId"]))
        return HttpResponse(json.dumps(questionToJson(question)))
    except:
        return HttpResponse(INVALID_QUERY)

def getQuiz(args):
    #input quiz id
    #output quiz json in string
    quiz = None
    try:
        quiz = Quiz.objects.get(id = int(args["qId"]))
        return HttpResponse(json.dumps(quizToJson(quiz)))
    except:
        return HttpResponse(INVALID_QUERY)

@login_required
def parseCommands(request):
    if not request.user.is_superuser:
        # bonk goto home
        return HttpResponseRedirect(reverse('quizHome'))

    saberCommand = None
    args = None
    if request.method == "POST":
        saberCommand = json.loads(request.body)['command']
        args = json.loads(request.body)['args']
    else:
        print("HIIIIII",request.GET)
        saberCommand = request.GET['command']
        args = request.GET
    # big brain: command name same as python command
    # for get requests it still works iff only strings and ints are passed
    # https://docs.djangoproject.com/en/3.2/ref/request-response/#django.http.QueryDict
    # shouldn't be security risk
    if saberCommand in ALLOWED_COMMANDS:
        print("YAY")
        return globals().get(saberCommand, -1)(args)
    else:
        return HttpResponse(COMMAND_NOT_FOUND)

    