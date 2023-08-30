from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import requests
from . import models
import json
from datetime import datetime, time, date


# Create your views here.
@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')


@csrf_exempt
def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        # Check if the user exists 
        username = request.POST.get('username')
        # print(username)
        password = request.POST.get('password')

        try:
            user_login = models.Patient.objects.get(username=username)
            user_save = authenticate(request, username=username, password= password)
            print(request)
            print(user_login.password)
            print(user_save)

            if user_save is not None:
                login(request, user_save)
                return HttpResponseRedirect(reverse('index'))
            else:
                context = {'message': 'Invalid request'}
                # json_data = json.dumps(data)
                return render(request, "login.html", context)
        except models.Patient.DoesNotExist:
            context = {'message': 'Patient does not exist'}
            return render(request, 'login.html', context)


@csrf_exempt
def register_view(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        company_name = request.POST.get('company_name')
        company_designation = request.POST.get('company_designation')
        insurance = request.POST.get('insurance')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        email = request.POST.get('email')

        # Send data to manage_doctor app
        url = 'http://127.0.0.1:8000/doctors/create_data'
        data = {
            'username': username,
            'company_name': company_name,
            'company_designation': company_designation,
            'insurance': insurance
        }
        json_data = json.dumps(data)
        r = requests.post(url=url, data=json_data)

        # Check if password and confirm password match 
        if password != cpassword:
            data = {'message': 'Passwords do not match'}
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
        # # Check if Email is taken, else create the entry
        email_exists = models.Patient.objects.filter(email=email)
        if email_exists:
            data = {'message': 'Email already taken!'}
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')

        # # Check if username is taken, else create the entry 
        try:
            user_exists = models.Patient.objects.get(username=username)
            data = {'message': 'Username already taken!'}
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
        except models.Patient.DoesNotExist:
            user_create = models.Patient.objects.create_user(username=username, company_name=company_name,
                                                             company_designation=company_designation, password=password,
                                                             insurance=insurance, email=email
                                                             )
            user_create.save()
            data = {'message': 'Registered successfully!'}
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def validate_name(request):
    user_input = request.POST.get('username')
    try:
        user_exists = models.Patient.objects.get(username=user_input)
        data = {'r': 200}
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type='application/json')
    except models.Patient.DoesNotExist:
        data = {'r': 20}
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@csrf_exempt
def deactivate(request):
    user_active = request.user.username
    # Deleting corresponding entry in doctors app 
    url2 = 'http://127.0.0.1:8000/doctors/delete_data'
    data = {
        'username': user_active
    }
    json_data = json.dumps(data)
    r = requests.delete(url=url2, data=json_data)

    # Logging out and deleting the entry 
    logout(request)
    user_active_object = models.Patient.objects.get(username=user_active)
    user_active_object.delete()
    return HttpResponseRedirect(reverse('index'))


@csrf_exempt
def book_appointment(request):
    if request.method == 'GET':
        url = "http://127.0.0.1:8000/doctors/get_doctor"
        data = {}
        json_data = json.dumps(data)
        r = requests.get(url=url, data=json_data)
        response = r.json()
        context = {'response': response}

        return render(request, 'book_appointment.html', context)
    if request.method == 'POST':

        datetime_str = request.POST.get('datetime_str')

        if not datetime_str:
            data = {'message': 'Date and time cannot be empty'}
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')

        doc_name = request.POST.get('doc_name')

        if not doc_name:
            data = {'message': 'Doctor name required!'}
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')

        dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M")
        date_part = dt.date()
        time_part = dt.time()

        if time_part >= time(9, 0) and time_part <= time(17, 0):

            if date_part.weekday() >= 5:
                data = {'message': 'Appointments are not available on weekends'}
                json_data = json.dumps(data)
                return HttpResponse(json_data, content_type='application/json')


            elif date_part <= date.today():
                data = {'message': "Appointment date must be at least tomorrow"}
                json_data = json.dumps(data)
                return HttpResponse(json_data, content_type='application/json')

            data = {
                'DoctorName': doc_name,
                'PatientName': request.user.username,
                'DateOfAppointment': datetime_str
            }
            json_data = json.dumps(data)
            url = "http://127.0.0.1:8000/doctors/create_appointment"
            r = requests.post(url=url, data=json_data)
            response = r.json()

            # return HttpResponse(f'{response}')
            return HttpResponse(r, content_type='application/json')

        else:
            data = {'message': '"Time should be between 9 am and 5 pm"'}
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def test_route(request):
    datetime_str = request.POST.get('datetime')
    doc_name = request.POST.get('doc_name')
    data = {
        'DoctorName': doc_name,
        'PatientName': request.user.username,
        'DateOfAppointment': datetime_str
    }
    json_data = json.dumps(data)
    url = "http://127.0.0.1:8000/doctors/create_appointment"
    r = requests.post(url=url, data=json_data)
    response = r.json()
    return HttpResponse(f'success {response} Doc:{doc_name} {type(doc_name)}')

@csrf_exempt
def get_confirmed_appointments(request):
    patient_name = request.user.username 
    data = {'patient_name':patient_name}
    json_data = json.dumps(data)
    r = requests.get(url = 'http://127.0.0.1:8000/doctors/get_confirmed_appointments', data = json_data)
    all_confirmed = r.json()
    context = {'all_confirmed':all_confirmed}
    return render(request, 'confirmed1.html', context)

@csrf_exempt
def bill_show(request):
    patient_name = request.user.username
    data = {'patient_name':patient_name}
    json_data= json.dumps(data)
    r = requests.get(url = 'http://127.0.0.1:8000/doctors/get_bill', data = json_data)
    all_confirmed = r.json()
    print("Test",all_confirmed)
    context = {'all_confirmed':all_confirmed}
    return render(request, 'bills.html', context)



