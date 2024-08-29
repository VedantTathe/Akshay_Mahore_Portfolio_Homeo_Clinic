from django.shortcuts import render, redirect
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest
import random
import string
from asmhomeoapp import mongodb as models
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
from django.conf import settings
from django.core.mail import send_mail



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

               
            else:
                print("Today's date is not greater than the date updated.")
                res['status_changed'] = False

    print(res)

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

    obj = models.MyClinic()
    data = obj.getClinicStatus()
    email = data['email']
    print(email,type(email))
    
    subject = 'Dear, Akshay Here is your username and password'
    message = 'Welcome, Your username is asmhomoeo786 and password is OMSai@786'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail( subject, message, email_from, recipient_list )

    return render(request, 'login.html',{'message':'Check Your Mobile We have sent the password in your email'})


@csrf_exempt
def searchdata(request):
    if 'user_role' not in request.session:
        return redirect('/')
    
    query = request.GET.get('search', '')

    obj = models.MyClinic()
    data = obj.searchData(query)

    print(data)
    return JsonResponse(data, safe=False)



@csrf_exempt
def changestatus(request, stat=None):
    if 'user_role' not in request.session:
        return redirect('/')

    # query = request.GET.get('stat', None)

    obj = models.MyClinic()
    data = obj.changeStatus(stat)
    res = obj.getClinicStatus()
    data.update(res)
    
    return render(request,'admin2.html',data)


@csrf_exempt
def updatenotice(request, stat=None):
    if 'user_role' not in request.session:
        return redirect('/')
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
        res = obj.getClinicStatus()
        data.update(res)
        
        # Render the response
        return render(request, 'admin2.html', data)
    
    # Handle GET or other methods if needed
    else:
        if stat:
            obj = models.MyClinic()
            data = obj.updateNotice(stat)
            res = obj.getClinicStatus()
            data.update(res)

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
    if 'user_role' not in request.session:
        return redirect('/')
    
    name = request.POST.get('name')
    mobileno = request.POST.get('mobileno')
    regno = request.POST.get('regno')

    name=name.upper()

    regno=regno.upper()
    

    obj = models.MyClinic()
    data = obj.addPatient(name,mobileno,regno)
    res = obj.getClinicStatus()
    data.update(res)
    return render(request, 'admin2.html',data)   




@csrf_exempt
def delpatient(request,regno):
    if 'user_role' not in request.session:
        return redirect('/')


    if regno == None:

        return render(request, 'admin.html',{'RegNo = None ...! Error'})   

    obj = models.MyClinic()
    data = obj.delPatient(regno)
    return render(request, 'admin.html',data)   

@csrf_exempt
def adminpage2(request):
    if 'user_role' not in request.session:
        return redirect('/')


    obj = models.MyClinic()
    data = obj.getClinicStatus()
    


    return render(request, 'admin2.html',data)


@csrf_exempt
def search_section(request):
    if 'user_role' not in request.session:
        return redirect('/')




    return render(request, 'search.html')


@csrf_exempt
def change_data(request):
    if 'user_role' not in request.session:
        return redirect('/')



    obj = models.MyClinic()
    data = obj.getClinicStatus()
    

    return render(request, 'change_data.html',data)


@csrf_exempt
def sendsms(request):
    if 'user_role' not in request.session:
        return redirect('/')


    return render(request, 'sendsms.html')


@csrf_exempt
def change_heroheading(request, stat=None):
    if 'user_role' not in request.session:
        return redirect('/')
    
    query = "NOTSET"
    if stat:
        query="NOTSET"
    else:
        query = request.POST.get('message')
        print(query)

    print(stat)
    

    obj = models.MyClinic()
    data = obj.changeHeroHeading(query)

    res = obj.getClinicStatus()

    data.update(res)
    

    return render(request,'change_data.html',data)


@csrf_exempt
def change_clinictimings(request, stat=None):
    if 'user_role' not in request.session:
        return redirect('/')
        
    query = "NOTSET"
    if stat:
        query="NOTSET"
    else:
        query = request.POST.get('message')
        print(query)

    print(stat)
    

    obj = models.MyClinic()
    data = obj.changeClinicTimings(query)
    res = obj.getClinicStatus()

    data.update(res)
    

    return render(request,'change_data.html',data)



@csrf_exempt
def change_aboutdata(request, stat=None):
    if 'user_role' not in request.session:
        return redirect('/')
    
    query = "NOTSET"
    if stat:
        query="NOTSET"
    else:
        query = request.POST.get('message')
        print(query)

    print(stat)
    

    obj = models.MyClinic()
    data = obj.changeAboutData(query)
    
    res = obj.getClinicStatus()
    data.update({ 'about_data': res['about_data']})
    res = obj.getClinicStatus()

    data.update(res)
    


    return render(request,'change_data.html',data)



@csrf_exempt
def change_contactdata(request):
    if 'user_role' not in request.session:
        return redirect('/')
    
    mobileno = request.POST.get('mobileno')
    email = request.POST.get('email')
    



    obj = models.MyClinic()
    data = obj.changeContactData(mobileno,email)
    return render(request,'change_data.html',data)


@csrf_exempt
def change_edudata(request,index):
    
    if 'user_role' not in request.session:
        return redirect('/')
    
    obj = models.MyClinic()


    cname = request.POST.get('cname')
    cyear = request.POST.get('cyear')
    cdesc = request.POST.get('cdesc')
    cdeg = request.POST.get('cdeg')
    

    res = obj.getClinicStatus()

    t1 = res['edu_data_name']
    t2 = res['edu_data_year']
    t3 = res['edu_data_desc']
    t4 = res['edu_data_degree']

    t1[index] = (cname)
    t2[index] = (cyear)
    t3[index] = (cdesc) 
    t4[index] = (cdeg)    

    data = obj.changeEduData(t1,t2,t3,t4)
    data.update(obj.getClinicStatus())
    return render(request,'change_data.html',data)


 
 
@csrf_exempt
def read_messages(request):   
    if 'user_role' not in request.session:
        return redirect('/')

    obj = models.MyClinic()
    data = obj.readMessages()

    mydic={}
    mydic['data'] = data

    return render(request,'read_messages.html',mydic)

 
@csrf_exempt
def delmsg(request, stat):
    if 'user_role' not in request.session:
        return redirect('/')

    obj = models.MyClinic()
    data = obj.delMsg(stat)

    t = obj.readMessages()
    data.update({'data':t})

    
    return render(request,'read_messages.html',data)











# from bson.json_util import dumps


# @api_view(['POST'])
# def allusers_data(request):
#     data=None
#     if request.POST.get('code')=="secret-code":
#         obj = models.MyClinic()
#         data = obj.getAllData()
#         data = dumps(data)
#         return Response({'status':200,'payload':data,'message':'success'})
#     return Response({'status':404,'payload':data,'message':'error'})
    