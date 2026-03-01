import random
from posts.forms import PostForm
from posts.models import Post
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.http import HttpResponse
import language_tool_python
import json
from difflib import get_close_matches
from django.contrib import auth
import pyrebase
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("firebase-sdk.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':''
})
ref=db.reference('/')

loginstat= False
email=""
definition=""
score=0
uid=""
loggedinuser={}
config = {'apiKey': "",
 'authDomain': "",
  'projectId': "",
    'databaseURL':"",
  'storageBucket': "",
 'messagingSenderId': "",
  'appId': ""
}
firebase=pyrebase.initialize_app(config)
db=firebase.database()
authe = firebase.auth()
# database=firebase.database()
# Create your views here.


user=""

tool = language_tool_python.LanguageTool('en-US')


def home(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def postlogin(request):
        global email
        global uid
        global loggedinuser
        global loginstat
        global user
        print('ok')
        email = request.POST.get('loginUser')
        pasw = request.POST.get('loginPassword')

        print(email, pasw)
        try:
            user = authe.sign_in_with_email_and_password(email, pasw)
            # print(user)
        except:
            print("not loggedin")
            message = "Invalid Credentials"
            return render(request, "login.html", {"messages": message})
        uid = user['localId']
        loginstat = True
        us=ref.child(uid)
        loggedinuser=dict(us.get())
        print('Successfully fetched user data:',uid)
        return render(request, "index.html")

#
def signup(request):
    return render(request, 'signup.html')



def postsignup(request):
        global uid

        print("postsignup")
        email = request.POST.get('loginUser')
        pasw = request.POST.get('loginPassword')
        repasw=request.POST.get('re_loginPassword')
        name = request.POST.get('disname')
        if pasw == repasw:
            try:
                global user
                user= authe.create_user_with_email_and_password(email, pasw)
            except:
                print("Reg failed")
                message = "User could not be created"
                return render(request, "signup.html", {"messages": message})

            user['displayName'] = name
            print(user)
            uid=user['localId']
            print(uid)
            data=ref.get()
            data[uid] = {'last score': 0,'highest score': 0, "name": name}
            ref.set(data)
        else:
            return render(request, "signup.html", {"messages": "Passwords do not match"})

        return render(request, "login.html")


def gram_error(request):
    text = str(request.POST.get('sentence'))

    print(text)

    # text = "what is ur name?"

    matches = tool.check(text)

    my_mistakes = []
    my_corrections = []
    start_positions = []
    end_positions = []
    for rules in matches:
        if len(rules.replacements) > 0:
            start_positions.append(rules.offset)
            end_positions.append(rules.errorLength + rules.offset)
            my_mistakes.append(text[rules.offset:rules.errorLength + rules.offset])
            my_corrections.append(rules.replacements[0])

    my_new_text = list(text)

    for m in range(len(start_positions)):
        for i in range(len(text)):
            my_new_text[start_positions[m]] = my_corrections[m]
            if (i > start_positions[m] and i < end_positions[m]):
                my_new_text[i] = ""

    my_new_text = "".join(my_new_text)
    return render(request, 'gram_error.html', {'corrected_sentence': my_new_text})


def dictionary(request):
    return render(request, 'dictionary.html')


def normal_dic(request):
    # if request.method == "POST":
    #     word = PostForm(request.POST)
    #     if word.is_valid():
    #         word.save()
    #         # return redirect("page2/normal_dic/")
    # else:
    #      word = PostForm()
    # word = request.POST.get('word', False)

    with open('data.json') as datafile:
        data = json.load(datafile)

    def findmeaning(w):
        wordlist = get_close_matches(w, data.keys(), 10, 0.7)
        if w in data.keys():
            return data[w]
        elif len(wordlist) > 0:
            return wordlist
        else:
            return "none"

    word = str(request.POST.get('word'))
    output = findmeaning(word)

    if output != "none":
        for item in output:
            Meaning = item
    else:
        print("Word not found")

    # print(word)

    return render(request, 'normal_dic.html', {'meaning': Meaning, "word": word})


def page2(request):
    global definition
    word=""
    def get_def_and_pop(word_list, word_dict):
        random_index = random.randrange(len(word_list))
        word = word_list.pop(random_index)
        definition = word_dict.get(word)
        return word, definition

    def get_word_and_definition(rawstring):
        word, definition1 = rawstring.split(",", 1)
        return word, definition1

    fh = open("Vocabulary_list.csv", "r")
    wd_list = fh.readlines()
    wd_list.pop(0)
    wd_set = set(wd_list)
    fh = open("Vocabulary_set.csv", "w")
    fh.writelines(wd_set)

    word_dict = dict()
    for rawstring in wd_set:
        word, definition = get_word_and_definition(rawstring)
        word_dict[word] = definition


    wd_list = list(word_dict)
    choice_list = []
    for x in range(4):
        word, definition = get_def_and_pop(wd_list, word_dict)
        choice_list.append(definition)
    random.shuffle(choice_list)
    choice1 = choice_list[0]
    choice2 = choice_list[1]
    choice3 = choice_list[2]
    choice4 = choice_list[3]

    return render(request, 'page2.html', {"choice1": choice1, "choice2": choice2, "choice3": choice3, "choice4": choice4, "word": word, "score":score,})


def postquiz(request):
    global definition
    global score
    global email
    global loggedinuser
    global loginstat
    choice=""

    # print(request.POST.get("choice2"))
    if request.POST.get("choice1"):
        print(request.POST.get("choice1"))
        choice = request.POST.get("choice1")
    elif request.POST.get("choice2"):
        print(request.POST.get("choice2"))
        choice = request.POST.get("choice2")
    elif request.POST.get("choice3"):
        print(request.POST.get("choice3"))
        choice = request.POST.get("choice3")
    elif request.POST.get("choice4"):
        print(request.POST.get("choice4"))
        choice = request.POST.get("choice4")
    print("choice=", type(choice), choice)
    print("definition=", type(definition), definition)
    if choice.strip() == definition.strip():
        score += 10
        print("correct")
    else:
        print("wrong")

    word = ""

    def get_def_and_pop(word_list, word_dict):
        random_index = random.randrange(len(word_list))
        word = word_list.pop(random_index)
        definition = word_dict.get(word)
        return word, definition

    def get_word_and_definition(rawstring):
        word, definition1 = rawstring.split(",", 1)
        return word, definition1

    fh = open("Vocabulary_list.csv", "r")
    wd_list = fh.readlines()
    wd_list.pop(0)
    wd_set = set(wd_list)
    fh = open("Vocabulary_set.csv", "w")
    fh.writelines(wd_set)

    word_dict = dict()
    for rawstring in wd_set:
        word, definition = get_word_and_definition(rawstring)
        word_dict[word] = definition

    wd_list = list(word_dict)
    choice_list = []
    for x in range(4):
        word, definition = get_def_and_pop(wd_list, word_dict)
        choice_list.append(definition)
    random.shuffle(choice_list)
    choice1 = choice_list[0]
    choice2 = choice_list[1]
    choice3 = choice_list[2]
    choice4 = choice_list[3]
    if loginstat:
        if request.POST.get("final"):
            finalscore=score
            # print('loggedinuser=',loggedinuser)
            lastscore=loggedinuser["last score"]
            loggedinuser["last score"]=score
            highscore = loggedinuser["highest score"]
            if score>highscore:
                loggedinuser["highest score"]=score
                highscore = loggedinuser["highest score"]
            score=0
            us = ref.child(uid)
            us.set(loggedinuser)
            return render(request, 'mark.html', {'score': finalscore,'last':lastscore,'high':highscore})
    else:
        return render(request,'login.html',{'messages':'Please log in first'})
    return render(request, 'page2.html',
                  {"choice1": choice1, "choice2": choice2, "choice3": choice3, "choice4": choice4, "word": word,
                   "score": score})


def gohome(request):
    return render(request, 'index.html')


def logout(request):
    score=0
    global uid
    global loggedinuser
    loggedinuser={}
    uid=""
    auth.logout(request)

    return render(request,'signup.html')


def reset(request):
    return render(request,"reset.html")

#
def postReset(request):
    email = request.POST.get('loginUser')
    print("Reset")
    try:
        print(email)
        authe.send_password_reset_email(email)
        print("try")
        message = "A email to reset password is succesfully sent"
        return render(request, "reset.html", {"msg": message})
    except:
        print("except")
        message = "Something went wrong, Please check the email you provided is registered or not"
        return render(request, "reset.html", {"msg": message})