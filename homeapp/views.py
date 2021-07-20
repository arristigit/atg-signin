from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage # as fs
from django.contrib import messages
from django.contrib.auth.models import User
from homeapp.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def patient(request):
    if request.method == "POST" and request.FILES['pic']:
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')        
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')

        try:
            if not username.isalnum():
                messages.warning(request, "User name should only contain letters and numbers")
                return redirect('/patient')

            if User.objects.filter(username=username).first():
                messages.warning(request, 'Username is taken!')
                return redirect('/patient')
            
            if User.objects.filter(email=email).first():
                messages.warning(request, 'Email is taken!')
                return redirect('/patient')    
            
            if password != confirmpassword:
                messages.warning(request, 'The Confirm Password not matched with the Password!!')
                return redirect('/patient')

            user_obj = User(username=username, first_name=firstname, last_name=lastname, email=email)
            user_obj.set_password(password)
            user_obj.save()

            pic = request.FILES['pic']
            fs = FileSystemStorage()
            filename = fs.save(pic.name, pic) # Storing image in database with auto generated name:
            url = fs.url(filename)

            current_user = User.objects.filter(username=username).first()            
            patient_obj = Patient(user=current_user, pic=url, address=address, city=city, state=state, zip=zip)
            patient_obj.save()
            messages.warning(request, f'{firstname}, you have successfully sign up.')
            return redirect('/')

        except Exception as e:
            messages.warning(request, 'Sorry for incenvinence!')
            messages.info(request, f'An exception occured : {e}')
            return redirect('/patient')

        # print(firstname, lastname, pic, username,email,password,confirmpassword,address,city,state,zip)
    return render(request, 'homeapp/patient.html')

def doctor(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        pic = request.POST.get('pic')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')

        try:
            if not username.isalnum():
                messages.warning(request, "User name should only contain letters and numbers")
                return redirect('/doctor')

            if User.objects.filter(username=username).first():
                messages.warning(request, 'Username is taken!')
                return redirect('/doctor')
            
            if User.objects.filter(email=email).first():
                messages.warning(request, 'Email is taken!')
                return redirect('/doctor')    
            
            if password != confirmpassword:
                messages.warning(request, 'The Confirm Password not matched with the Password!!')
                return redirect('/doctor')

            user_obj = User(username=username, first_name=firstname, last_name=lastname, email=email)
            user_obj.set_password(password)
            user_obj.save()

            pic = request.FILES['pic']
            fs = FileSystemStorage()
            filename = fs.save(pic.name, pic) # Storing image in database with auto generated name:
            url = fs.url(filename)

            current_user = User.objects.filter(username=username).first()
            doctor_obj = Doctor(user=current_user, pic=url, address=address, city=city, state=state, zip=zip)
            doctor_obj.save()
            messages.warning(request, f'{firstname}, you have successfully sign up.')
            return redirect('/')

        except Exception as e:
            messages.warning(request, 'Sorry for incenvinence!')
            messages.info(request, f'An exception occured : {e}')
            return redirect('/doctor')

        # print(firstname, lastname, pic, username,email,password,confirmpassword,address,city,state,zip)
    return render(request, 'homeapp/doctor.html')

def login_user(request):
    if request.method == "POST":
        is_patient = request.POST.get('patient')
        is_doctor = request.POST.get('doctor')
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            if is_patient == 'patient':
            # print(is_patient, username, password)            
                user_obj = User.objects.filter(username=username).first()
                if user_obj is None:
                    messages.warning(request, 'User not found!')
                    return redirect('/')
                
                user = Patient.objects.filter(user=user_obj).first() 
                if user is None:
                    messages.warning(request, 'User not found!')
                    return redirect('/')          
                
                user = authenticate(username=username, password=password)
                if user is None:
                    messages.warning(request, 'Wrong password!')
                    return redirect('/')

                login(request, user)
                request.session['username'] = user.username
                request.session['type'] = is_patient
                messages.success(request, 'Your are succussfully logged in.')
                return redirect('/dashboard')
        
            if is_doctor == 'doctor':
                # print(is_doctor, username, password)
                user_obj = User.objects.filter(username=username).first()
                if user_obj is None:
                    messages.warning(request, 'User not found!')
                    return redirect('/')

                user = Doctor.objects.filter(user=user_obj).first()
                if user is None:
                    messages.warning(request, 'User not found!')
                    return redirect('/')  
                
                user = authenticate(username=username, password=password)
                if user is None:
                    messages.warning(request, 'Wrong password!')
                    return redirect('/')

                login(request, user)
                request.session['username'] = user.username
                request.session['type'] = is_doctor
                messages.success(request, 'Your are succussfully logged in.')
                return redirect('/dashboard')

        except Exception as e:
            messages.warning(request, 'Sorry for incenvinence!')
            messages.info(request, f'An exception occured : {e}')
            return redirect('/')

        #  = request.POST.get('')        
    return render(request, 'homeapp/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "Successfully logged out.")
    return redirect('/')    

# @login_required(login_url="/login/")
@login_required
def dashboard(request):
    try: 
        username = request.session['username']
        type = request.session['type']

        if type == 'patient':
            user = User.objects.filter(username=username).first()
            patient = Patient.objects.filter(user=user).first()

            print('patient: ',user.email, patient.city)
            context = {'user': user, 'type': patient}
            return render(request, 'homeapp/dashboard.html', context)
        
        if type == 'doctor':
            user = User.objects.filter(username=username).first()
            doctor = Doctor.objects.filter(user=user).first()

            print('doctor: ',user.email, doctor.city)
            context = {'user': user, 'type': doctor}
            return render(request, 'homeapp/dashboard.html', context)

    except Exception as e:
        messages.warning(request, 'Sorry for incenvinence!')
        messages.info(request, f'An exception occured : {e}')
        return redirect('/')
    
    return render(request, 'homeapp/dashboard.html')