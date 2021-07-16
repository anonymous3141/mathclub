from django.db import models
from django.contrib.auth.models import User

# question type constant definitions
MULTICHOICE = 'mc'
INTEGERANSWER = 'ia' #lalalalalalalalala
QUESTION_TYPE_CHOICES = ((MULTICHOICE, 'multichoice'),
(INTEGERANSWER,'0 to 999 answer'))
TYPEDICT = {a:b for (a,b) in QUESTION_TYPE_CHOICES}
# world's dumbest hack to store all MC answers in 1 entry
# seperate the choices by an unlikely delimiter
# for fuck sakes don't make this an option pls it will break
MC_DELIMITOR = "URWAIFUSSHIT"

#Quiz stuff
# User Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    personal_message = models.CharField(max_length = 100)
    rating = models.IntegerField(default=500)
    # to determine if certain user has done a quiz,
    # see if a question from that quiz has been attempted
    # todo: solves, rating etc
    # todo: quiz leaderboards



class Question(models.Model):
    # to be rendered as html
    # I hope we dont have to delete stuff
    # can change question type support
    # for the time being use github as a source of static files
    # the correct answer is the answer for a int answer field
    # OR the 1 indexed position of the correct answer
    questionHTML = models.CharField(max_length=1500, default="")
    inUse = models.BooleanField(default=True)
    answerType = models.CharField(default='ia',max_length=2, choices= QUESTION_TYPE_CHOICES)
    options = models.CharField(default="", max_length = 500) # using dumb hack
    # conserve database lines which dont come cheap
    weight = models.IntegerField(default = 1) #problem score weight
    correctAnswer = models.CharField(max_length=20)

class Quiz(models.Model):
    # quiz id is primary key
    date = models.DateTimeField('date published')
    name = models.CharField(max_length = 50)
    description = models.CharField(max_length = 500) # I hope this is enough
    visible = models.BooleanField(default = False)
    readOnly = models.BooleanField(default = False)
    questionList = models.ManyToManyField(Question)
    quizResources = models.CharField(max_length = 250, default="") # pdfs etc
    quizWeight = models.IntegerField(default = 100)
    # max number of attempts? = 1
    # official?
    # time limits?
    # todo: questionOrder

class UserProblemVerdict(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Question, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE) #which quiz was this q done in
    response = models.CharField(max_length=100, default="") # what did user enter
    verdict = models.CharField(max_length = 20, default="") # score

def questionToJson(question):
    #question is Question class, not queryset
    #returns dict with everything stringed
    #standardised json form of question
    toRender = {}
    toRender['id'] = str(question.id)
    toRender['questionHTML'] =question.questionHTML
    toRender['answerType'] = question.answerType
    toRender['weight'] = str(question.weight)

    #as long as template doesn't use it its fine not security risk
    toRender['options'] = []
    toRender['correctAnswer'] = question.correctAnswer 
    if TYPEDICT[question.answerType] == 'multichoice':
            # option[0] is id of option, option[1] is HTML
            # +1 to 1 index
        toRender['options'] = question.options.split(MC_DELIMITOR)
    return toRender

def quizToJson(quiz):
    #quiz of quiz class
    #return dict with strings
    return (Quiz.objects.filter(id = quiz.id).values()[0])

