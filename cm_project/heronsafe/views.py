from django.shortcuts import render
from .models import *
from .utils import predictDisease
# Create your views here.

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

def base(request):
    # student = Student.objects.get(student_id=pk_test)
    # assessments = student.assessment_set.all()
    # assessment_count = assessments.count()

    # context = {'student': student, 'assessments': assessments, 'assessment_count':assessment_count}
    context ={}
    return render(request, 'student/home.html', context)

def assessment(request):
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
    return render(request, 'student/assessment.html', results)
