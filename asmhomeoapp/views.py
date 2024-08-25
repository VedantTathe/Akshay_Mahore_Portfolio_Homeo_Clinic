from django.shortcuts import render, redirect
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest
import random
import string
from asmhomeoapp import models
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from pytz import timezone
import pytz
from rest_framework.decorators import api_view
from rest_framework.response import Response


@csrf_exempt
def index(request):
    obj = models.MyClinic()
    res = obj.getClinicStatus()
    
    # Get current UTC time
    utc_time = datetime.utcnow().replace(tzinfo=pytz.utc)

    # Convert UTC time to Indian Standard Time (IST)
    india_time = utc_time.astimezone(timezone('Asia/Kolkata'))

    # Extract hour and minute from IST
    current_hour = india_time.hour
    current_minute = india_time.minute

    # Print the IST time and its components
    print('India time:', india_time)
    print("Current Hour in IST:", current_hour)
    print("Current Minute in IST:", current_minute)


    # Check if the clinic status is 'NOTSET'
    if res['clinic_status'] == 'NOTSET':
        
        # Update clinic status based on the current hour
        if 10 <= current_hour < 13:
            res['clinic_status'] = 'OPEN'
            print('Status is OPEN\n\n')
        elif 13 <= current_hour < 18:
            res['clinic_status'] = 'CLOSED'
            print('Status is CLOSED\n\n')
        elif current_hour == 18 and current_minute > 30:
            res['clinic_status'] = 'OPEN'
            print('Status is OPEN\n\n')
        elif 19 <= current_hour < 21:
            res['clinic_status'] = 'OPEN'
            print('Status is OPEN\n\n')
        elif 21 == current_hour and current_minute < 30:
            res['clinic_status'] = 'OPEN'
            print('Status is OPEN\n\n')
        else:  # current_hour >= 21 or current_hour < 10
            res['clinic_status'] = 'CLOSED'
            print('Status is CLOSED\n\n')

        # res['time'] = now.time().strftime('%H:%M:%S')  # Format the time as a string

    elif res['clinic_status'] == 'CLOSED':
        date_updated_str = res.get('date_updated', '')
        print(f'Date updated string: {date_updated_str}')

        if date_updated_str:
            date_updated = datetime.strptime(date_updated_str, '%Y-%m-%d')

            # Get today's date
            today = datetime.now().date()
            
            today = today + timedelta(days=1)
            
            # Check if today's date is greater than date_updated
            if today > date_updated.date():
                print("Today's date is greater than the date updated.")
                res['status_changed'] = True

                if 10 <= current_hour < 14:
                    res['clinic_status'] = 'OPEN'
                    print('Status is OPEN\n\n')
                elif 14 <= current_hour < 19:
                    res['clinic_status'] = 'CLOSED'
                    print('Status is CLOSED\n\n')
                elif 19 <= current_hour < 21:
                    res['clinic_status'] = 'OPEN'
                    print('Status is OPEN\n\n')
                else:  # current_hour >= 21 or current_hour < 10
                    res['clinic_status'] = 'CLOSED'
                    print('Status is CLOSED\n\n')

                
                obj = models.MyClinic()
                obj.changeStatus('NOTSET')

                res['time'] = now.time().strftime('%H:%M:%S')  # Format the time as a string


            else:
                print("Today's date is not greater than the date updated.")
                res['status_changed'] = False

    print(res['notice'])

    return render(request, 'index.html', res)


@csrf_exempt
def loginpage(request):

    if 'user_role' in request.session:
        return redirect('/adminpage/')
    if request.method == 'POST':

        username = request.POST.get('uname')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            request.session['user_role'] = 'admin'
        
            # Passing session data to the template
            context = {
                'user_role': request.session['user_role'],
                'user_name': 'Akshay Mahore'
            }
            return render(request,'admin.html',context)
        else:
            return render(request, 'login.html', {'err': 'Invalid email or password'})

        
    else:
        return render(request, 'login.html')


@csrf_exempt
def adminpage(request):
    
    if 'user_role' not in request.session:
        return redirect('/')


    context = {
                'user_role': request.session['user_role'],
                'user_name': 'Akshay Mahore'
            }
    return render(request,'admin.html',context)


@csrf_exempt
def logoutpage(request):
    
    if 'user_role' in request.session:
        del request.session['user_role']

    return redirect('/')


@csrf_exempt
def forgotPassword(request):

    return render(request, 'login.html',{'message':'Check Your Mobile We have sent the password in your email'})



@csrf_exempt
def searchdata(request):
    query = request.GET.get('search', '')

    obj = models.MyClinic()
    data = obj.searchData(query)

    print(data)
    return JsonResponse(data, safe=False)



@csrf_exempt
def changestatus(request, stat=None):
    
    # query = request.GET.get('stat', None)

    obj = models.MyClinic()
    data = obj.changeStatus(stat)
    return render(request,'admin2.html',data)


@csrf_exempt
def updatenotice(request, stat=None):
    if request.method == 'POST':
        # Get the 'notice' field from the form
        notice = request.POST.get('notice')
        
        if notice is None or notice.strip() == '':
            return render(request, 'admin2.html', {'err':'Notice Content is empty... or missing'})
        
        # Process the notice here (e.g., update the database)
        print("Notice received:", notice)
        
        # Prepare the context data
        obj = models.MyClinic()
        data = obj.updateNotice(notice)
        
        # Render the response
        return render(request, 'admin2.html', data)
    
    # Handle GET or other methods if needed
    else:
        if stat:
            obj = models.MyClinic()
            data = obj.updateNotice(stat)

        return render(request, 'admin.html', data)





@csrf_exempt
def sendmessage(request):

    


    name = request.POST.get('uname')
    email = request.POST.get('email')
    msg = request.POST.get('msg')

    obj = models.MyClinic()
    data = obj.sendMessage(name,email,msg)
    return render(request,'index.html',data)


 
@csrf_exempt
def addpatient(request):
    name = request.POST.get('name')
    mobileno = request.POST.get('mobileno')
    regno = request.POST.get('regno')

    name=name.upper()

    regno=regno.upper()
    

    obj = models.MyClinic()
    data = obj.addPatient(name,mobileno,regno)
    return render(request, 'admin2.html',data)   




@csrf_exempt
def delpatient(request,regno):
    if regno == None:

        return render(request, 'admin.html',{'RegNo = None ...! Error'})   

    obj = models.MyClinic()
    data = obj.delPatient(regno)
    return render(request, 'admin.html',data)   

@csrf_exempt
def adminpage2(request):



    return render(request, 'admin2.html')





from bson.json_util import dumps


@api_view(['POST'])
def allusers_data(request):
    data=None
    if request.POST.get('code')=="secret-code":
        obj = models.MyClinic()
        data = obj.getAllData()
        data = dumps(data)
        return Response({'status':200,'payload':data,'message':'success'})
    return Response({'status':404,'payload':data,'message':'success'})