from django.shortcuts import render, redirect
from .models import *
from .utils import predictDisease
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
import uuid
import datetime
# Create your views here.

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('base')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for' + user)

                return redirect('login')

        context = {'form':form}
        return render(request, 'register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('base')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_staff == False:
                    login(request, user)
                    return redirect('base')
            else:
                messages.info(request, 'Username OR password is incorrect')


    context={}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def home(request):
    assessments = Assessment.objects.all()
    students = Student.objects.all()
    total_students = students.count()
    total_assessments = assessments.count()
    context = {'assessments': assessments, 'students': students, 'total_students': total_students, 'total_assessments': total_assessments}

    return render(request, 'dashboard.html', context)

def student(request, pk_test):
    student = Student.objects.get(student_id=pk_test)
    assessments = student.assessment_set.all()
    assessment_count = assessments.count()

    context = {'student': student, 'assessments': assessments, 'assessment_count':assessment_count}
    return render(request, 'student.html', context)

@login_required(login_url='login')
def base(request, ):
    # user = request.user()
    # email = user.email
    student = Student.objects.get(user=request.user)
    assessments = student.assessment_set.all()
    assessment_count = assessments.count()

    context = {'student': student, 'assessments': assessments, 'assessment_count':assessment_count}
    # context ={}
    return render(request, 'student/home.html', context)

@login_required(login_url='login')
def assessment(request, pk_test):
    student = Student.objects.get(student_id=pk_test)
    fruits = []
    results = {}
    symptom = ""
    
    if request.method == 'POST':
        symptoms = request.POST.getlist('symptoms')
        # traverse in the string
        for elements in symptoms:
            symptom += elements
        symptom = symptom[:-1]
        
        results = predictDisease(symptom)
        
        # student = Student.objects.get(user=request.user)
        # email = student['email']

        # assessments = student.assessment_set.all()
        # assessments.symptoms = results['symptoms']
        # assessments.diagnosis = results['final_prediction']
        # assessments.date_created = datetime.datetime.now()
        # assessments.student = student.id
        # assessments.assessment_number = str(uuid.uuid4 ())[0:12]
        # id_user = student.id
        studentid = Student.objects.filter(student_id=pk_test)

        email_student = student.email
        a = Assessment.objects.create(
            student = student,
            assessment_number = str(uuid.uuid4 ())[0:12],
            date_created = datetime.datetime.now(),
            symptoms = results['symptoms'], 
            diagnosis = results['final_prediction']
        ).save()

    return render(request, 'student/assessment.html', results)
